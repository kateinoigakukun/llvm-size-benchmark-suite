load("//:bazel/bitcode.bzl", "bitcode_binary")
load("//:bazel/bitcode_test.bzl", "bitcode_testsuite", "bitcode_testcase")

bitcode_binary(name = "qsort_large", srcs = ["@mibench_automotive//:qsort/qsort_large.c"])
bitcode_binary(name = "qsort_small", srcs = ["@mibench_automotive//:qsort/qsort_small.c"])

bitcode_testcase(name = "qsort_large_testcase", args = ["input_large.dat", "/dev/null"])
bitcode_testcase(name = "qsort_small_testcase", args = ["input_small.dat", "/dev/null"])
bitcode_testsuite(
    name = "qsort_large_test",
    target = "qsort_large.bc",
    cases = [":qsort_large_testcase"],
    ldflags = ["-lm"],
)
bitcode_testsuite(
    name = "qsort_small_test",
    target = "qsort_small.bc",
    cases = [":qsort_small_testcase"],
    ldflags = ["-lm"],
)

filegroup(
    name = "all",
    srcs = [
        ":qsort_large",
        ":qsort_small",
        ":qsort_large_test",
        ":qsort_small_test",
        "@mibench_automotive//:qsort/input_small.dat",
        "@mibench_automotive//:qsort/input_large.dat",
    ],
    visibility = ["//visibility:public"],
)
