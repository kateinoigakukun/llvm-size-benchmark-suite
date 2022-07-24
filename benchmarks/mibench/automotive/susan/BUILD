load("//:bazel/bitcode.bzl", "bitcode_binary")
load("//:bazel/bitcode_testcase.bzl", "bitcode_testcase")

bitcode_binary(
    name = "susan",
    srcs = ["@mibench_automotive//:susan/susan.c"]
)

bitcode_testcase(
    name = "susan_small_test_s",
    target = "susan.bc",
    args = ["input_small.pgm", "/dev/null", "-s"],
    ldflags = ["-lm"],
    visibility = ["//visibility:public"],
)

bitcode_testcase(
    name = "susan_small_test_e",
    target = "susan.bc",
    args = ["input_small.pgm", "/dev/null", "-e"],
    ldflags = ["-lm"],
    visibility = ["//visibility:public"],
)

bitcode_testcase(
    name = "susan_small_test_c",
    target = "susan.bc",
    args = ["input_small.pgm", "/dev/null", "-c"],
    ldflags = ["-lm"],
    visibility = ["//visibility:public"],
)

bitcode_testcase(
    name = "susan_large_test_s",
    target = "susan.bc",
    args = ["input_large.pgm", "/dev/null", "-s"],
    ldflags = ["-lm"],
    visibility = ["//visibility:public"],
)

bitcode_testcase(
    name = "susan_large_test_e",
    target = "susan.bc",
    args = ["input_large.pgm", "/dev/null", "-e"],
    ldflags = ["-lm"],
    visibility = ["//visibility:public"],
)

bitcode_testcase(
    name = "susan_large_test_c",
    target = "susan.bc",
    args = ["input_large.pgm", "/dev/null", "-c"],
    ldflags = ["-lm"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "all",
    srcs = [
        ":susan",
        ":susan_small_test_s",
        ":susan_small_test_e",
        ":susan_small_test_c",
        ":susan_large_test_s",
        ":susan_large_test_e",
        ":susan_large_test_c",
        "@mibench_automotive//:susan/input_small.pgm",
        "@mibench_automotive//:susan/input_large.pgm",
    ],
    visibility = ["//visibility:public"],
)
