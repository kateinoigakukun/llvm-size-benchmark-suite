py_binary(
    name = "llvm-link-wrapper",
    srcs = ["llvm-link-wrapper.py"],
)

genrule(
    name = "vmlinux",
    srcs = ["@linux_kernel_src//:all", "@linux_kernel_src//:Makefile", "config"],
    cmd = """
    cp "$(location config)" "$(RULEDIR)/.config"
    export LLVM_LINK_WRAPPER_LLD_LD_PATH="$$PWD/$(LD)"
    export LLVM_LINK_WRAPPER_LLVM_AR_PATH="$$PWD/$(AR)"
    export LLVM_LINK_WRAPPER_LLVM_LINK_PATH="$$PWD/$$(dirname $$(dirname $(LD)))_llvm/bin/llvm-link"
    make vmlinux \
        -j $$(nproc) -f "$(location @linux_kernel_src//:Makefile)" O="$(RULEDIR)" \
        LLVM=1 LLVM_IAS=1 \
        CC="$$PWD/$(CC)" LD="$$PWD/$(locations :llvm-link-wrapper)"
    """,
    outs = ["vmlinux.o.bc"],
    tools = [":llvm-link-wrapper"],
    toolchains = ["@bazel_tools//tools/cpp:current_cc_toolchain"],
    visibility = ["//visibility:public"],
)
