load("@rules_pkg//pkg:mappings.bzl", "pkg_files")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")

pkg_files(
    name = "linux",
    srcs = ["//benchmarks/linux:vmlinux"],
    prefix = "benchmarks/linux",
)

pkg_files(
    name = "mibench_automotive",
    srcs = ["//benchmarks/mibench/automotive:all"],
    prefix = "benchmarks/mibench/automotive",
)

pkg_files(
    name = "mibench_automotive_basicmath",
    srcs = ["//benchmarks/mibench/automotive/basicmath:all"],
    prefix = "benchmarks/mibench/automotive/basicmath",
)

pkg_files(
    name = "mibench_automotive_bitcount",
    srcs = ["//benchmarks/mibench/automotive/bitcount:all"],
    prefix = "benchmarks/mibench/automotive/bitcount",
)

pkg_files(
    name = "mibench_consumer",
    srcs = ["//benchmarks/mibench/consumer:all"],
    prefix = "benchmarks/mibench/consumer",
)

pkg_tar(
    name = "bitcode_tar",
    srcs = [
        ":linux",
        ":mibench_automotive",
        ":mibench_automotive_basicmath",
        ":mibench_consumer",
    ],
)
