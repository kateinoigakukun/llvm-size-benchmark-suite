#!/usr/bin/env python3

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time


class BenchmarkCase:
    def __init__(self, manifest_path):
        with open(manifest_path) as f:
            self.manifest = json.load(f)
        manifest_base = os.path.dirname(manifest_path)
        self.bitcode_path = os.path.join(manifest_base, self.manifest["target"])

    def plan(self, options):
        obj = tempfile.NamedTemporaryFile(
            delete=False, prefix=self.manifest["name"], suffix=".o")
        obj.close()
        opt_cmd = [options.opttool, self.bitcode_path]
        if options.pass_plugin:
            opt_cmd += ["--load", options.pass_plugin,
                        "--load-pass-plugin", options.pass_plugin]
        if options.Xopt:
            opt_cmd += options.Xopt

        llc_cmd = [options.llctool, "-filetype=obj", "-", "-o", "-"]
        tee_cmd = ["tee", obj.name]
        return {
            "pipelines": [[opt_cmd, llc_cmd, tee_cmd]],
            "outputs": {
                "object": obj.name,
            }
        }

    def plan_test(self, options):
        plan = self.plan(options)
        exe = tempfile.NamedTemporaryFile(
            delete=False, prefix=self.manifest["name"], suffix=".out")
        exe.close()
        link_cmd = [options.ldtool, plan["outputs"]["object"],
                    "-o", exe.name] + self.manifest["ldflags"]
        test_cmd = [exe.name] + self.manifest["args"]
        plan["pipelines"].append([link_cmd])
        plan["pipelines"].append([test_cmd])
        return plan


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
                if file.endswith(".manifest.json"):
                    yield BenchmarkCase(os.path.join(root, file))

    def run(self, options, reporter: ConsoleReporter):
        for case in self.cases:
            self.run_case(case, reporter, options)

    def format_command(self, cmd):
        return " ".join(map(lambda x: "'" + x + "'", cmd))

    def run_pipeline(self, pipeline: list, options):
        if options.verbose:
            print(" | ".join(map(lambda cmd: self.format_command(cmd), pipeline)))

        # create a pipeline through stdout/stdin
        procs = []
        last_proc = None
        for cmd in pipeline:
            stdin = last_proc.stdout if last_proc else None
            last_proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=stdin)
            procs.append(last_proc)

        for proc in procs[:-1]:
            proc.wait()

        last_proc = procs[-1]
        return last_proc

    def run_case(self, case: BenchmarkCase, reporter: ConsoleReporter, options):
        plan = case.plan_test(options) if options.test else case.plan(options)
        pipelines = plan["pipelines"]
        start = time.perf_counter()
        for pipeline in pipelines:
            last_proc = self.run_pipeline(pipeline, options)
            output = last_proc.stdout.read()
            last_proc.wait()
            if not last_proc.returncode == 0:
                print("{} FAILED".format(case.manifest["name"]))
                print(last_proc.stderr.read().decode('utf-8'), file=sys.stderr)
                sys.exit(last_proc.returncode)
        end = time.perf_counter()
        reporter.report(case, size=len(output),
                        returncode=last_proc.returncode,
                        time=end - start, stderr=last_proc.stderr)


def make_reporter(options):
    if options.db_path:
        return SQLiteReporter(options)
    else:
        return ConsoleReporter(options)


def expand_response_file(args):
    out = []
    for arg in args:
        if arg.startswith("@"):
            with open(arg[1:]) as f:
                out.extend(f.read().splitlines())
        else:
            out.append(arg)
    return out


def main():
    parser = argparse.ArgumentParser(description="""
Compare code sizes of differently optimized code from the same source code.""")
    parser.add_argument("--opttool", default="opt", help="Path to opt tool")
    parser.add_argument("--llctool", default="llc", help="Path to llc tool")
    parser.add_argument("--ldtool", default="ld.lld", help="Path to ld tool")
    parser.add_argument("--pass-plugin", help="Path to LLVM pass plugin")
    parser.add_argument("-Xopt", action='append',
                        help="Extra arguments to pass to opt")
    parser.add_argument("--suite-path", required=True,
                        help="Path to benchmark suite directory")
    parser.add_argument("--db-path", help="Path to SQLite database")
    parser.add_argument("--verbose", action='store_true',
                        help="Print extra information")
    parser.add_argument("--test", action='store_true', help="Perform test run")

    args = expand_response_file(sys.argv[1:])
    options = parser.parse_args(args)
    cases = list(BenchmarkDriver.find_cases(options.suite_path))
    reporter = make_reporter(options)
    driver = BenchmarkDriver(cases)
    driver.run(options, reporter)


if __name__ == "__main__":
    main()
