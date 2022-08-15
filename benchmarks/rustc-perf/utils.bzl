load("//:bazel/bitcode_test.bzl", "bitcode_testsuite", "bitcode_testcase")

CARGO_TEST_BITCODE_ATTRS = {
    "package": attr.label(allow_single_file=True),
    "_all_files": attr.label(
        allow_files = True,
        default = Label("@rustc_perf//:all"),
    ),
    "_build_crate": attr.label(
        default = Label("//benchmarks/rustc-perf:build-crate"),
        executable = True,
        cfg = "host",
    ),
    "_cc_toolchain": attr.label(
        default = Label("@bazel_tools//tools/cpp:current_cc_toolchain"),
        providers = [cc_common.CcToolchainInfo],
        cfg = "host",
    ),
    "_rust_toolchain": attr.label(
        default = Label("@rules_rust//rust/toolchain:current_rust_toolchain"),
    ),
    "_bin_ext": attr.string(default = ".bc"),
}


def _cargo_test_bitcode(ctx):
    cc_toolchain = ctx.attr._cc_toolchain[cc_common.CcToolchainInfo]
    rust_toolchain = ctx.attr._rust_toolchain[platform_common.ToolchainInfo]
    output = ctx.actions.declare_file(ctx.label.name)
    args = ctx.actions.args()
    args.add_all(["--output", output])
    args.add_all(["--package", ctx.file.package.path])

    ctx.actions.run(
        inputs = depset(
          direct = ctx.attr._all_files.files.to_list(),
          transitive = [cc_toolchain.all_files, rust_toolchain.all_files],
        ),
        outputs = [output],
        executable = ctx.executable._build_crate,
        arguments = [args],
        env = {
            "CC": cc_toolchain.compiler_executable,
            "LD": cc_toolchain.ld_executable,
            "RUSTC": rust_toolchain.rustc.path,
        },
    )

    return [
        DefaultInfo(files = depset([output])),
        OutputGroupInfo(
            bitcode = depset([output]),
        ),
    ]

cargo_test_bitcode = rule(
    implementation = _cargo_test_bitcode,
    attrs = CARGO_TEST_BITCODE_ATTRS,
    toolchains = [
      "@bazel_tools//tools/cpp:toolchain_type",
      "@rules_rust//rust:toolchain_type",
    ],
)

def cargo_test_bitcode_suite(name, package):
    cargo_test_bitcode(name = name + ".bc", package = package)
    bitcode_testcase(name = name + "_args", args = [])
    bitcode_testsuite(
        name = name + "_test",
        target = name + ".bc",
        cases = [name + "_args"],
        visibility = ["//visibility:public"],
    )
    native.filegroup(name = name, srcs = [name + "_test", name + ".bc"])
