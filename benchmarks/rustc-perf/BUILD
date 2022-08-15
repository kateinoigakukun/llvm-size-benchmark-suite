load("utils.bzl", "cargo_test_bitcode_suite")

py_binary(
    name = "build-crate",
    srcs = ["build-crate.py"],
)

cargo_test_bitcode_suite(name = "helloworld", package = "@rustc_perf//:collector/benchmarks/helloworld/Cargo.toml")
cargo_test_bitcode_suite(name = "bitmaps-3.1.0", package = "@rustc_perf//:collector/benchmarks/bitmaps-3.1.0/Cargo.toml")
# cargo_test_bitcode(name = "cargo-0.60.0", package = "@rustc_perf//:collector/benchmarks/cargo-0.60.0/Cargo.toml")
cargo_test_bitcode_suite(name = "cranelift-codegen-0.82.1", package = "@rustc_perf//:collector/benchmarks/cranelift-codegen-0.82.1/Cargo.toml")
cargo_test_bitcode_suite(name = "html5ever-0.26.0", package = "@rustc_perf//:collector/benchmarks/html5ever-0.26.0/Cargo.toml")
# cargo_test_bitcode(name = "hyper-0.14.18", package = "@rustc_perf//:collector/benchmarks/hyper-0.14.18/Cargo.toml")
cargo_test_bitcode_suite(name = "image-0.24.1", package = "@rustc_perf//:collector/benchmarks/image-0.24.1/Cargo.toml")
cargo_test_bitcode_suite(name = "libc-0.2.124", package = "@rustc_perf//:collector/benchmarks/libc-0.2.124/Cargo.toml")
cargo_test_bitcode_suite(name = "regex-1.5.5", package = "@rustc_perf//:collector/benchmarks/regex-1.5.5/Cargo.toml")
cargo_test_bitcode_suite(name = "ripgrep-13.0.0", package = "@rustc_perf//:collector/benchmarks/ripgrep-13.0.0/Cargo.toml")
cargo_test_bitcode_suite(name = "unicode-normalization-0.1.19", package = "@rustc_perf//:collector/benchmarks/unicode-normalization-0.1.19/Cargo.toml")

filegroup(
    name = "all",
    srcs = [
      ":helloworld",
      ":bitmaps-3.1.0",
      ":cranelift-codegen-0.82.1",
      ":html5ever-0.26.0",
      ":image-0.24.1",
      ":libc-0.2.124",
      ":regex-1.5.5",
      ":ripgrep-13.0.0",
      ":unicode-normalization-0.1.19",
    ],
    visibility = ["//visibility:public"],
)
