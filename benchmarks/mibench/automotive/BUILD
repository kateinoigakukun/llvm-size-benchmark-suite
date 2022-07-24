load("//:bazel/bitcode.bzl", "bitcode_binary")

bitcode_binary(name = "qsort_large", srcs = ["@mibench_automotive//:qsort/qsort_large.c"])
bitcode_binary(name = "qsort_small", srcs = ["@mibench_automotive//:qsort/qsort_small.c"])

bitcode_binary(
    name = "susan",
    srcs = ["@mibench_automotive//:susan/susan.c"]
)

filegroup(
    name = "all",
    srcs = [":qsort_large", ":qsort_small", ":susan"],
    visibility = ["//visibility:public"],
)
