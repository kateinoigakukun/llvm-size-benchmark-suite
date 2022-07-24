load("//:bazel/bitcode.bzl", "bitcode_binary")

bitcode_binary(name = "qsort_large", srcs = ["@mibench_automotive//:qsort/qsort_large.c"])
bitcode_binary(name = "qsort_small", srcs = ["@mibench_automotive//:qsort/qsort_small.c"])


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

bitcode_binary(
    name = "susan",
    srcs = ["@mibench_automotive//:susan/susan.c"]
)

filegroup(
    name = "all",
    srcs = [":qsort_large", ":qsort_small", ":bitcount", ":susan"],
    visibility = ["//visibility:public"],
)
