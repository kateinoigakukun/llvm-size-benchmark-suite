load("//:bazel/bitcode.bzl", "bitcode_binary")
load("//:bazel/bitcode_test.bzl", "bitcode_testsuite", "bitcode_testcase")

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

bitcode_testcase(name = "bitcount_small_test_case", args = ["75000"])
bitcode_testcase(name = "bitcount_large_test_case", args = ["1125000"])
bitcode_testsuite(
    name = "bitcount_test",
    target = "bitcount.bc",
    cases = [":bitcount_small_test_case", ":bitcount_large_test_case"],
)

filegroup(
    name = "all",
    srcs = [":bitcount", ":bitcount_test"],
    visibility = ["//visibility:public"],
)
