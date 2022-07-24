load("//:bazel/bitcode.bzl", "bitcode_binary")
load("//:bazel/bitcode_test.bzl", "bitcode_testsuite", "bitcode_testcase")

LIBSOURCES = [
    "@mibench_consumer//:jpeg/jpeg-6a/jcapimin.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcapistd.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jccoefct.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jccolor.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcdctmgr.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jchuff.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcinit.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcmainct.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcmarker.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcmaster.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcomapi.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcparam.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcphuff.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcprepct.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jcsample.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdapimin.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdapistd.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdatadst.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdatasrc.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdcoefct.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdcolor.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jddctmgr.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdhuff.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdinput.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdmainct.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdmarker.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdmaster.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdmerge.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdphuff.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdpostct.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jdsample.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jerror.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jfdctflt.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jfdctfst.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jfdctint.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jidctflt.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jidctfst.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jidctint.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jidctred.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jmemmgr.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jmemnobs.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jquant1.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jquant2.c",
    "@mibench_consumer//:jpeg/jpeg-6a/jutils.c",
]

LIBHEADERS = [
    "@mibench_consumer//:jpeg/jpeg-6a/cderror.h",
    "@mibench_consumer//:jpeg/jpeg-6a/cdjpeg.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jchuff.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jconfig.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jdct.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jdhuff.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jerror.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jinclude.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jmemsys.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jmorecfg.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jpegint.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jpeglib.h",
    "@mibench_consumer//:jpeg/jpeg-6a/jversion.h",
]

bitcode_binary(
    name = "cjpeg",
    srcs = LIBSOURCES + [
        "@mibench_consumer//:jpeg/jpeg-6a/cjpeg.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdppm.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdgif.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdtarga.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdrle.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdbmp.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdswitch.c",
        "@mibench_consumer//:jpeg/jpeg-6a/cdjpeg.c",
    ],
    hdrs = LIBHEADERS,
    copts = ["-Wno-shift-negative-value"],
)

bitcode_binary(
    name = "djpeg",
    srcs = LIBSOURCES + [
        "@mibench_consumer//:jpeg/jpeg-6a/djpeg.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrppm.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrgif.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrtarga.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrrle.c",
        "@mibench_consumer//:jpeg/jpeg-6a/wrbmp.c",
        "@mibench_consumer//:jpeg/jpeg-6a/rdcolmap.c",
        "@mibench_consumer//:jpeg/jpeg-6a/cdjpeg.c",
    ],
    hdrs = LIBHEADERS,
    copts = ["-Wno-shift-negative-value"],
)

bitcode_testcase(
    name = "cjpeg_small_test",
    args = ["-dct", "int", "-progressive", "-opt", "-outfile", "/dev/null", "input_small.ppm"]
)
bitcode_testcase(
    name = "cjpeg_large_test",
    args = ["-dct", "int", "-progressive", "-opt", "-outfile", "/dev/null", "input_large.ppm"]
)
bitcode_testcase(
    name = "djpeg_small_test",
    args = ["-dct", "int", "-ppm", "-outfile", "/dev/null", "input_small.jpg"]
)
bitcode_testcase(
    name = "djpeg_large_test",
    args = ["-dct", "int", "-ppm", "-outfile", "/dev/null", "input_large.jpg"]
)
bitcode_testsuite(
    name = "cjpeg_test",
    target = "cjpeg.bc",
    cases = [":cjpeg_small_test", ":cjpeg_large_test"],
    ldflags = ["-lm"],
)
bitcode_testsuite(
    name = "djpeg_test",
    target = "djpeg.bc",
    cases = [":djpeg_small_test", ":djpeg_large_test"],
    ldflags = ["-lm"],
)

filegroup(
    name = "all",
    srcs = [
        ":cjpeg", ":djpeg",
        ":cjpeg_test", ":djpeg_test",
        "@mibench_consumer//:jpeg/input_small.ppm",
        "@mibench_consumer//:jpeg/input_large.ppm",
        "@mibench_consumer//:jpeg/input_small.jpg",
        "@mibench_consumer//:jpeg/input_large.jpg",
    ],
    visibility = ["//visibility:public"],
)
