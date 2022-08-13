#!/usr/bin/env python3

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
import multiprocessing


class BenchmarkCase:
    def __init__(self, manifest_path):
        with open(manifest_path) as f:
            self.manifest = json.load(f)
        self.manifest_base = os.path.dirname(manifest_path)
        self.bitcode_path = os.path.join(
            self.manifest_base, self.manifest["target"])
        self.name = self.manifest["name"]

    def plan(self, options):
        output_path = os.path.abspath(
            os.path.join(options.output_dir, self.name))

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        bc_path = os.path.join(output_path, "obj.bc")
        remarks_path = os.path.join(output_path, "remarks.yaml")
        obj_path = os.path.join(output_path, "obj.o")
        obj_strip_path = os.path.join(output_path, "obj.strip.o")

        opt_cmd = [options.opttool, self.bitcode_path, "-o",
                   bc_path, "--pass-remarks-output", remarks_path]
        if options.pass_plugin:
            opt_cmd += ["--load", options.pass_plugin,
                        "--load-pass-plugin", options.pass_plugin]
        if options.Xopt:
            opt_cmd += options.Xopt

        llc_cmd = [options.llctool, "-filetype=obj", bc_path, "-o", obj_path]
        strip_cmd = ["strip", obj_path, "-o", obj_strip_path]

        pipelines = [[opt_cmd], [llc_cmd]]

        cat_cmd = ["cat", obj_path]
        if not options.test:
            pipelines.append([strip_cmd])
            cat_cmd = ["cat", obj_strip_path]
        pipelines.append([cat_cmd])

        return {
            "pipelines": pipelines,
            "outputs": {
                "object": obj_path,
            },
        }

    def plan_test(self, build_outputs, options):
        exe = tempfile.NamedTemporaryFile(
            delete=False, prefix=self.name, suffix=".out")
        exe.close()
        link_cmd = [options.ldtool, build_outputs["object"],
                    "-o", exe.name] + self.manifest["ldflags"]
        test_cmds = []
        for test in self.manifest["cases"]:
            test_cmd = [exe.name] + test["args"]
            test_cmds.append([test_cmd])
        return {
            "pipelines": [[link_cmd]] + test_cmds,
            "cwd": self.manifest_base,
        }


class BenchmarkResult:
    def __init__(self, case, size, returncode, time, stderr):
        self.case = case
        self.size = size
        self.returncode = returncode
        self.time = time
        self.stderr = stderr

    def __iter__(self):
        return iter((self.case, self.size, self.returncode, self.time, self.stderr))


class NopReporter:
    def report(self, result):
        pass

    def flush(self):
        pass


class ConsoleReporter(NopReporter):
    def __init__(self, options):
        self.options = options

    def report(self, result):
        case, size, returncode, time, stderr = result
        print("{} {} {} {}".format(case.bitcode_path, size, returncode, time))


class MarkdownReporter(NopReporter):
    def __init__(self, options):
        self.options = options
        self.rows_by_name = dict()

    def report(self, result):
        case, size, returncode, time, stderr = result
        status = "Passed" if returncode == 0 else "Failed"
        self.rows_by_name[case.name] = f"| `{case.bitcode_path}` | {size} | {status} | {time} |"

    def flush(self):
        print("| Name | Size (byte) | Status | Time (sec) |")
        print("|:----:|:-----------:|:------:|:----------:|")
        for key in self.rows_by_name.keys():
            print(self.rows_by_name[key])


class SQLiteReporter(NopReporter):
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

    def report(self, result):
        case, size, returncode, time, stderr = result
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


class WorkContext:
    def __init__(self, driver, reporter, options):
        self.driver = driver
        self.reporter = reporter
        self.options = options

    def work(self, case):
        return self.driver.run_case(case, self.reporter, self.options)


class BenchmarkDriver:
    def __init__(self, cases):
        self.cases = cases

    @staticmethod
    def find_cases(suite_path):
        if suite_path.endswith(".manifest.json"):
            yield BenchmarkCase(suite_path)
            return

        for root, _, files in os.walk(suite_path):
            for file in files:
                if file.endswith(".manifest.json"):
                    yield BenchmarkCase(os.path.join(root, file))

    def run(self, options, reporter):
        def handle_result(result):
            reporter.report(result)
            if options.test and result.returncode != 0:
                sys.exit(result.returncode)

        if options.paralell:
            with multiprocessing.Pool() as pool:
                context = WorkContext(self, reporter, options)
                for result in pool.map(context.work, self.cases):
                    handle_result(result)
        else:
            for case in self.cases:
                result = self.run_case(case, reporter, options)
                handle_result(result)

    def format_command(self, cmd):
        return " ".join(map(lambda x: "'" + x + "'", cmd))

    def run_pipeline(self, pipeline: list, cwd, options):
        if options.verbose:
            print("(", end="")
            if cwd is not None:
                print(f"cd {cwd}; ", end="")
            print(" | ".join(map(lambda cmd: self.format_command(cmd), pipeline)), end="")
            print(")")

        # create a pipeline through stdout/stdin
        procs = []
        last_proc = None
        for cmd in pipeline:
            stdin = last_proc.stdout if last_proc else None
            last_proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=stdin, cwd=cwd)
            procs.append(last_proc)

        for proc in procs[:-1]:
            proc.wait()

        last_proc = procs[-1]
        return last_proc

    def run_case(self, case: BenchmarkCase, reporter, options):
        build_plan = case.plan(options)
        start = time.perf_counter()
        for pipeline in build_plan["pipelines"]:
            last_proc = self.run_pipeline(pipeline, None, options)
            output = last_proc.stdout.read()
            last_proc.wait()
            if last_proc.returncode != 0:
                break
        end = time.perf_counter()
        result = BenchmarkResult(case=case, size=len(output),
                                 returncode=last_proc.returncode,
                                 time=end - start, stderr=last_proc.stderr.read())
        if options.test and result.returncode == 0:
            return self.run_testcase(case, build_plan["outputs"], options)
        return result

    def run_testcase(self, case: BenchmarkCase, build_outputs, options):
        print(f"Testing {case.bitcode_path}")
        test_plan = case.plan_test(build_outputs, options)
        start = time.perf_counter()
        for pipeline in test_plan["pipelines"]:
            last_proc = self.run_pipeline(
                pipeline, test_plan.get("cwd", None), options)
            last_proc.stdout.read()
            last_proc.wait()
            if not last_proc.returncode == 0:
                print("{} FAILED".format(case.manifest["name"]))
                print(last_proc.stderr.read().decode('utf-8'), file=sys.stderr)
                break
        end = time.perf_counter()
        return BenchmarkResult(case=case, size=None,
                               returncode=last_proc.returncode,
                               time=end - start, stderr=last_proc.stderr.read())


def make_reporter(options):
    if options.reporter == "console":
        return ConsoleReporter(options)
    elif options.reporter == "sqlite":
        return SQLiteReporter(options)
    elif options.reporter == "markdown":
        return MarkdownReporter(options)

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
    parser.add_argument("--reporter", default=None,
                        help="Reporter to show results")
    parser.add_argument("--db-path", help="Path to SQLite database")
    parser.add_argument("--verbose", action='store_true',
                        help="Print extra information")
    parser.add_argument("--test", action='store_true', help="Perform test run")
    parser.add_argument("--paralell", action='store_true',
                        help="Perform commands in paralell")
    parser.add_argument("--output-dir", default="./benchmarks-out",
                        help="Path to a directory where results will be output")

    args = expand_response_file(sys.argv[1:])
    options = parser.parse_args(args)
    cases = list(BenchmarkDriver.find_cases(options.suite_path))
    if not os.path.exists(options.output_dir):
        os.makedirs(options.output_dir)
    reporter = make_reporter(options)
    driver = BenchmarkDriver(cases)
    driver.run(options, reporter)
    reporter.flush()


if __name__ == "__main__":
    main()
