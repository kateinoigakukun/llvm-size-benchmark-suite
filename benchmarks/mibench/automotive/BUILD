load("//:bazel/bitcode.bzl", "bitcode_binary")

bitcode_binary(name = "qsort_large", srcs = ["@mibench_automotive//:qsort/qsort_large.c"])
bitcode_binary(name = "qsort_small", srcs = ["@mibench_automotive//:qsort/qsort_small.c"])

filegroup(
    name = "all",
    srcs = [":qsort_large", ":qsort_small"],
    visibility = ["//visibility:public"],
)
