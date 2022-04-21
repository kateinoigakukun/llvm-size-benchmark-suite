
load("//:bazel/bitcode.bzl", "bitcode_binary")

bitcode_binary(name = "qsort_large", srcs = ["@mibench_automotive//:qsort/qsort_large.c"])
bitcode_binary(name = "qsort_small", srcs = ["@mibench_automotive//:qsort/qsort_small.c"])

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

filegroup(
    name = "all",
    srcs = [":qsort_large", ":qsort_small", ":basicmath_small", ":basicmath_large"],
    visibility = ["//visibility:public"],
)
