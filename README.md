## LLVM Size Benchmark Suite

A suite of benchmarks for object size. This suite distributes the benchmark suites in LLVM bitcode format.

```console
$ bazel build //:bitcode_tar
```

`bazel-bin/bitcode_tar.tar` is a tarball of the LLVM bitcode size benchmark suite.
