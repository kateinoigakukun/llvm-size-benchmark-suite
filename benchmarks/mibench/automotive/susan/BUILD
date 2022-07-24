load("//:bazel/bitcode.bzl", "bitcode_binary")
load("//:bazel/bitcode_test.bzl", "bitcode_testsuite", "bitcode_testcase")

bitcode_binary(
    name = "susan",
    srcs = ["@mibench_automotive//:susan/susan.c"]
)

bitcode_testcase(name = "susan_small_test_s", args = ["input_small.pgm", "/dev/null", "-s"])
bitcode_testcase(name = "susan_small_test_e", args = ["input_small.pgm", "/dev/null", "-e"])
bitcode_testcase(name = "susan_small_test_c", args = ["input_small.pgm", "/dev/null", "-c"])
bitcode_testsuite(
    name = "susan_small_test",
    target = "susan.bc",
    cases = [":susan_small_test_s", ":susan_small_test_e", ":susan_small_test_c"],
    ldflags = ["-lm"],
)

bitcode_testcase(name = "susan_large_test_s", args = ["input_large.pgm", "/dev/null", "-s"])
bitcode_testcase(name = "susan_large_test_e", args = ["input_large.pgm", "/dev/null", "-e"])
bitcode_testcase(name = "susan_large_test_c", args = ["input_large.pgm", "/dev/null", "-c"])
bitcode_testsuite(
    name = "susan_large_test",
    target = "susan.bc",
    cases = [":susan_large_test_s", ":susan_large_test_e", ":susan_large_test_c"],
    ldflags = ["-lm"],
)

filegroup(
    name = "all",
    srcs = [
        ":susan",
        ":susan_small_test",
        ":susan_large_test",
        "@mibench_automotive//:susan/input_small.pgm",
        "@mibench_automotive//:susan/input_large.pgm",
    ],
    visibility = ["//visibility:public"],
)
