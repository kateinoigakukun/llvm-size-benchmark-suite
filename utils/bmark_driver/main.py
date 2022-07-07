#!/usr/bin/env python3

import argparse
import os
import sqlite3
import subprocess
import time


class BenchmarkCase:
    def __init__(self, bitcode_path):
        self.bitcode_path = bitcode_path

    def plan(self, options):
        opt_cmd = [options.opttool, self.bitcode_path]
        if options.pass_plugin:
            opt_cmd += ["--load", options.pass_plugin,
                        "--load-pass-plugin", options.pass_plugin]
        if options.Xopt:
            opt_cmd += options.Xopt

        llc_cmd = [options.llctool, "-filetype=obj", "-", "-o", "-"]
        return [opt_cmd, llc_cmd]


class ConsoleReporter:
    def __init__(self, options):
        self.options = options

    def report(self, case, size, returncode, time, stderr):
        print("{} {} {} {}".format(case.bitcode_path, size, returncode, time))
        pass


class SQLiteReporter:
    def __init__(self, options):
        self.options = options
        self.db = sqlite3.connect(options.db_path)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS results (
                bitcode_path TEXT,
                size INTEGER,
                returncode INTEGER,
                time REAL,
                stderr TEXT
            )
        """)

    def report(self, case, size, returncode, time, stderr):
        self.db.execute("""
            INSERT INTO results (
                bitcode_path,
                size,
                returncode,
                time,
                stderr
            ) VALUES (?, ?, ?, ?, ?)
        """, (case.bitcode_path, size, returncode, time, stderr))
        self.db.commit()


class BenchmarkDriver:
    def __init__(self, cases):
        self.cases = cases

    @staticmethod
    def find_cases(suite_path):
        for root, _, files in os.walk(suite_path):
            for file in files:
                if file.endswith(".bc"):
                    yield BenchmarkCase(os.path.join(root, file))

    def run(self, options, reporter: ConsoleReporter):
        for case in self.cases:
            self.run_case(case, reporter, options)

    def format_command(self, cmd):
        return " ".join(map(lambda x: "'" + x + "'", cmd))

    def run_case(self, case: BenchmarkCase, reporter: ConsoleReporter, options):
        cmds = case.plan(options)
        start = time.perf_counter()
        if options.verbose:
            print(" | ".join(map(lambda cmd: self.format_command(cmd), cmds)))

        # create a pipeline through stdout/stdin
        procs = []
        last_proc = None
        for cmd in cmds:
            stdin = last_proc.stdout if last_proc else None
            last_proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=stdin)
            procs.append(last_proc)

        for proc in reversed(procs):
            proc.wait()

        last_proc = procs[-1]
        output = last_proc.stdout.read()
        end = time.perf_counter()
        reporter.report(case, size=len(output),
                        returncode=last_proc.returncode,
                        time=end - start, stderr=last_proc.stderr)


def make_reporter(options):
    if options.db_path:
        return SQLiteReporter(options)
    else:
        return ConsoleReporter(options)


def main():
    parser = argparse.ArgumentParser(description="""
Compare code sizes of differently optimized code from the same source code.""")
    parser.add_argument("--opttool", default="opt", help="Path to opt tool")
    parser.add_argument("--llctool", default="llc", help="Path to llc tool")
    parser.add_argument("--pass-plugin", help="Path to LLVM pass plugin")
    parser.add_argument("-Xopt", action='append',
                        help="Extra arguments to pass to opt")
    parser.add_argument("--suite-path", required=True,
                        help="Path to benchmark suite directory")
    parser.add_argument("--db-path", help="Path to SQLite database")
    parser.add_argument("--verbose", action='store_true',
                        help="Print extra information")

    options = parser.parse_args()
    cases = list(BenchmarkDriver.find_cases(options.suite_path))
    reporter = make_reporter(options)
    driver = BenchmarkDriver(cases)
    driver.run(options, reporter)


if __name__ == "__main__":
    main()
