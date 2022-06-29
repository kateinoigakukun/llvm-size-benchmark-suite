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
    name = "mibench_consumer",
    srcs = ["//benchmarks/mibench/consumer:all"],
    prefix = "benchmarks/mibench/consumer",
)

pkg_tar(
    name = "bitcode_tar",
    srcs = [
        ":linux",
        ":mibench_automotive",
        ":mibench_consumer",
    ],
)
