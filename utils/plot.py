#!/usr/bin/env python3

import argparse
import os
from glob import glob
import numpy as np
import yaml
from yaml import CLoader as Loader


class Passed(yaml.YAMLObject):
    yaml_loader = Loader
    yaml_tag = "!Passed"

    def __init__(self, Name, Args):
        self.Name = Name
        self.Args = Args

    def is_n_merge(self, n):
        if not self.Name == "Merge":
            return False
        funcs = 0
        for arg in self.Args:
            if "Function" in arg:
                funcs += 1
        return funcs == n


class Missed(yaml.YAMLObject):
    yaml_loader = Loader
    yaml_tag = "!Missed"

    def __init__(self, Name):
        self.Name = Name


class BenchmarkResult:

    def __init__(self, path, options):
        self.path = path
        self.data = {}
        obj_filename = "obj.strip.o"
        objects = glob(os.path.join(
            path, "**", obj_filename), recursive=True)

        def display_case_name(case_name):
            if case_name == "helloworld":
                return "rustc-perf-helloworld"
            if "-" in case_name:
                return "rustc-perf-" + case_name[:case_name.rfind("-")]
            return "mibench-" + case_name
        for obj_path in objects:
            key = os.path.dirname(obj_path)[len(path):]
            if key.startswith("/"):
                key = key[1:]
            if key.endswith("_test"):
                key = key[:-5]

            key = display_case_name(key)
            value = None
            if options.target == "objsize":
                value = os.path.getsize(obj_path)
            elif options.target == "mergecount" or options.target == "mergecount3":
                remark_path = os.path.join(
                    os.path.dirname(obj_path), "remarks.yaml")
                remarks = yaml.load_all(open(remark_path), Loader=Loader)
                value = 0
                for remark in remarks:
                    if isinstance(remark, Passed) and remark.Name == "Merge":
                        if options.target == "mergecount":
                            value += 1
                        elif options.target == "mergecount3" and remark.is_n_merge(3):
                            value += 1
            self.data[key] = value

    def case_names(self):
        return sorted(self.data.keys())

    def name(self):
        return os.path.basename(self.path)


class Plotter:

    def __init__(self, options):
        self.options = options

    def plot_value(self, result, case_name, baseline):
        v = result.data[case_name]
        if baseline:
            v = 100 * (1 - v / baseline.data[case_name])
        return v

    def plot(self, results, baseline, ax):
        fontsize = self.options.fontsize
        x_labels = set(results[0].case_names())
        for result in results[1:]:
            x_labels = x_labels.union(result.case_names())

        if self.options.exclude_failures:
            for result in results:
                x_labels = x_labels.intersection(result.case_names())

        if self.options.exclude_zeros:
            for result in results:
                for case_name in result.case_names():
                    if self.plot_value(result, case_name, baseline) == 0 \
                            and case_name in x_labels:
                        x_labels.remove(case_name)

        x_labels = sorted(x_labels)

        bar_width = 0.4
        x = np.arange(len(x_labels))
        values_by_variant = []

        for idx, result in enumerate(results):
            xs = x + idx * bar_width - (len(results) - 1) * bar_width/2
            values = []
            bar_labels = []
            for case_name in x_labels:
                if case_name in result.data:
                    v = self.plot_value(result, case_name, baseline)
                    values.append(v)
                    if baseline:
                        bar_labels.append("{v:.3f}".format(v=v))
                    else:
                        bar_labels.append("{v}".format(v=v))
                else:
                    values.append(0)
                    bar_labels.append("failure")

            print(f"{result.name()}: {sum(values)/len(values)}")
            rect = ax.barh(xs, values,
                           bar_width, label=result.name())
            ax.bar_label(rect, padding=3, labels=bar_labels, fontsize=fontsize)
            values_by_variant.append(values)

        hans, labs = ax.get_legend_handles_labels()
        ax.legend(handles=hans[::-1], labels=labs[::-1], fontsize=fontsize)

        ax.axvline(0, color="black", linewidth=0.5)
        if self.options.baseline:
            ax.set_title(
                "Object size reduction rate compared to baseline", fontsize=fontsize + 6)
            ax.set_xlabel("Reduction rate in size (%)", fontsize=fontsize)
            stats_text = ""
            for idx, result in enumerate(results):
                values = values_by_variant[idx]
                stats_text += "mean ({name}): {mean:.3f}%\n".format(name=result.name(), mean=np.mean(values))
            ax.text(0.98, 0.8, stats_text, ha="right",
                    transform=ax.transAxes, fontsize=fontsize + 2)
        elif self.options.target == "mergecount":
            ax.set_title("Number of merge", fontsize=fontsize + 6)
            ax.set_xlabel("Count", fontsize=fontsize)
        elif self.options.target == "mergecount3":
            ax.set_title("Number of 3 merge", fontsize=fontsize + 6)
            ax.set_xlabel("Count", fontsize=fontsize)
        else:
            ax.set_title("Object size comparison", fontsize=fontsize + 6)
            ax.set_xlabel("Object size (bytes)", fontsize=fontsize)
        ax.set_yticks(x, x_labels, fontsize=fontsize)


def main():
    parser = argparse.ArgumentParser(
        description="Plot the results of the benchmark")
    parser.add_argument("results", type=str, nargs="+")
    parser.add_argument("-o", "--output", type=str, default="plot.png")
    parser.add_argument("--baseline", type=str)
    parser.add_argument("--exclude-failures", action="store_true")
    parser.add_argument("--exclude-zeros", action="store_true")
    parser.add_argument("--fontsize", type=int, default=12)
    parser.add_argument("--target", type=str, default="objsize")

    options = parser.parse_args()
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(15, 10))
    plotter = Plotter(options)
    results = [BenchmarkResult(path, options) for path in options.results]
    baseline = BenchmarkResult(
        options.baseline, options) if options.baseline else None
    plotter.plot(results, baseline, ax)
    fig.tight_layout()
    plt.savefig(options.output)


if __name__ == "__main__":
    main()
