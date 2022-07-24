load("//:bazel/bitcode.bzl", "bitcode_binary")
load("//:bazel/bitcode_testcase.bzl", "bitcode_testcase")

filegroup(
    name = "basicmath_base",
    srcs = [
        "@mibench_automotive//:basicmath/rad2deg.c",
        "@mibench_automotive//:basicmath/cubic.c",
        "@mibench_automotive//:basicmath/isqrt.c",
    ]
)
filegroup(
    name = "basicmath_hdrs",
    srcs = [
        "@mibench_automotive//:basicmath/pi.h",
        "@mibench_automotive//:basicmath/round.h",
        "@mibench_automotive//:basicmath/snipmath.h",
        "@mibench_automotive//:basicmath/sniptype.h",
    ]
)
bitcode_binary(
    name = "basicmath_small",
    srcs = ["@mibench_automotive//:basicmath/basicmath_small.c", ":basicmath_base"],
    hdrs = [":basicmath_hdrs"]
)
bitcode_binary(
    name = "basicmath_large",
    srcs = ["@mibench_automotive//:basicmath/basicmath_large.c", ":basicmath_base"],
    hdrs = [":basicmath_hdrs"]
)

bitcode_testcase(
    name = "basicmath_small_test",
    target = "basicmath_small.bc",
    visibility = ["//visibility:public"],
)

bitcode_testcase(
    name = "basicmath_large_test",
    target = "basicmath_large.bc",
    visibility = ["//visibility:public"],
)

filegroup(
    name = "all",
    srcs = [":basicmath_small", ":basicmath_large", ":basicmath_small_test", ":basicmath_large_test"],
    visibility = ["//visibility:public"],
)
