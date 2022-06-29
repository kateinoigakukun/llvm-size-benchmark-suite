load("//:bazel/bitcode.bzl", "bitcode_binary")

bitcode_binary(
    name = "libjpeg",
    srcs = [
        "@mibench_consumer//:jpeg/jpeg-6a/cjpeg.c",
        "@mibench_consumer//:jpeg/jpeg-6a/cdjpeg.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdbmp.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdcolmap.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdgif.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdppm.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdrle.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdswitch.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdtarga.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrbmp.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrgif.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrppm.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrrle.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrtarga.c",
    ],
    hdrs = [
        "@mibench_consumer//:jpeg/jpeg-6a/jconfig.h",
        "@mibench_consumer//:jpeg/jpeg-6a/jerror.h",
        "@mibench_consumer//:jpeg/jpeg-6a/jinclude.h",
        "@mibench_consumer//:jpeg/jpeg-6a/jmorecfg.h",
        "@mibench_consumer//:jpeg/jpeg-6a/jpeglib.h",
        "@mibench_consumer//:jpeg/jpeg-6a/jversion.h",
        "@mibench_consumer//:jpeg/jpeg-6a/cdjpeg.h",
        "@mibench_consumer//:jpeg/jpeg-6a/cderror.h",
    ],
)

filegroup(
    name = "all",
    srcs = [":libjpeg"],
    visibility = ["//visibility:public"],
)
