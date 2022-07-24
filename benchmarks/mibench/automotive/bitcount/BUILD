load("//:bazel/bitcode.bzl", "bitcode_binary")
load("//:bazel/bitcode_testcase.bzl", "bitcode_testcase")

bitcode_binary(
    name = "bitcount",
    srcs = [
        "@mibench_automotive//:bitcount/bitcnt_1.c",
        "@mibench_automotive//:bitcount/bitcnt_2.c",
        "@mibench_automotive//:bitcount/bitcnt_3.c",
        "@mibench_automotive//:bitcount/bitcnt_4.c",
        "@mibench_automotive//:bitcount/bitcnts.c",
        "@mibench_automotive//:bitcount/bitfiles.c",
        "@mibench_automotive//:bitcount/bitstrng.c",
        "@mibench_automotive//:bitcount/bstr_i.c",
    ],
    hdrs = [
        "@mibench_automotive//:bitcount/bitops.h",
        "@mibench_automotive//:bitcount/runme_large.sh",
        "@mibench_automotive//:bitcount/conio.h",
        "@mibench_automotive//:bitcount/runme_small.sh",
        "@mibench_automotive//:bitcount/extkword.h",
        "@mibench_automotive//:bitcount/sniptype.h",
    ]
)

bitcode_testcase(
    name = "bitcount_small_test",
    target = "bitcount.bc",
    args = ["75000"],
    visibility = ["//visibility:public"],
)

bitcode_testcase(
    name = "bitcount_large_test",
    target = "bitcount.bc",
    args = ["1125000"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "all",
    srcs = [":bitcount", ":bitcount_small_test", "bitcount_large_test"],
    visibility = ["//visibility:public"],
)
