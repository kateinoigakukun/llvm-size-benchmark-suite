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
        cmd = [options.opttool, "--filetype=obj", self.bitcode_path]
        if options.pass_plugin:
            cmd += ["--load", options.pass_plugin,
                    "--load-pass-plugin", options.pass_plugin]
        if options.Xopt:
            cmd += options.Xopt
        return cmd

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

    def run_case(self, case: BenchmarkCase, reporter: ConsoleReporter, options):
        cmd = case.plan(options)
        start = time.perf_counter()
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end = time.perf_counter()
        reporter.report(case, size=len(proc.stdout),
                        returncode=proc.returncode,
                        time=end - start, stderr=proc.stderr)
def make_reporter(options):
    if options.db_path:
        return SQLiteReporter(options)
    else:
        return ConsoleReporter(options)

def main():
    parser = argparse.ArgumentParser(description="""
Compare code sizes of differently optimized code from the same source code.""")
    parser.add_argument("--opttool", default="opt", help="Path to opt tool")
    parser.add_argument("--pass-plugin", help="Path to LLVM pass plugin")
    parser.add_argument("-Xopt", action='append', help="Extra arguments to pass to opt")
    parser.add_argument("--suite-path", required=True, help="Path to benchmark suite directory")
    parser.add_argument("--db-path", help="Path to SQLite database")

    options = parser.parse_args()
    cases = list(BenchmarkDriver.find_cases(options.suite_path))
    reporter = make_reporter(options)
    driver = BenchmarkDriver(cases)
    driver.run(options, reporter)

if __name__ == "__main__":
    main()
