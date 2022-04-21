# A linker wrapper that also links input bitcode files with llvm-link.

import os
import subprocess
import sys
import logging
from tempfile import TemporaryDirectory


class Toolchain:
    def __init__(self, llvm_link, llvm_ar, lld):
        self.llvm_link = llvm_link
        self.llvm_ar = llvm_ar
        self.lld = lld


class BitcodeLinkerWrapper:
    def __init__(self, args: list, toolchain: Toolchain):
        args = args.copy()
        self.toolchain = toolchain

        self.args = args
        self.output = None
        self.objects = []
        self.archives = []

        while len(args) > 0:
            arg = args.pop(0)
            if arg == "-o":
                self.output = args.pop(0)
            elif arg.endswith(".o"):
                self.objects.append(arg)
            elif arg.endswith(".a"):
                self.archives.append(arg)

    def should_link(self) -> bool:
        if self.output is None:
            return False
        if len(self.objects) == 0 and len(self.archives) == 0:
            return False
        return True

    def is_thin_archive(self, path) -> list:
        thin_magic = bytes([0x21, 0x3c, 0x74, 0x68, 0x69, 0x6e, 0x3e])
        with open(path, "rb") as f:
            return f.read(len(thin_magic)) == thin_magic

    def is_raw_bitcode(self, path):
        magic = bytes([0x42, 0x43, 0xc0, 0xde])
        with open(path, "rb") as f:
            return f.read(len(magic)) == magic

    def expand_thin_archive(self, path) -> list:
        output = subprocess.check_output([self.toolchain.llvm_ar, "t", path])
        return output.splitlines()

    def expand_archive(self, path, dir) -> list:
        if self.is_thin_archive(path):
            return self.expand_thin_archive(path)
        raise Exception(f"Regular archive format is not supported: {path}")

    def run(self, tmpdir):
        assert(self.should_link())
        args = [self.toolchain.llvm_link, "-o", self.output + ".bc"]
        inputs = []

        for object in self.objects:
            if self.is_raw_bitcode(object):
                inputs.append(object)

        for archive in self.archives:
            objs = self.expand_archive(archive, tmpdir)
            for obj in objs:
                if self.is_raw_bitcode(obj):
                    inputs.append(obj)
                else:
                    logging.warning(
                        f"Skipping non-bitcode object in archive: {obj}")
        if len(inputs) == 0:
            return None
        return subprocess.Popen(args + inputs)

def main():
    llvm_link = os.environ.get("LLVM_LINK_WRAPPER_LLVM_LINK_PATH", "llvm-link")
    llvm_ar = os.environ.get("LLVM_LINK_WRAPPER_LLVM_AR_PATH", "llvm-ar")
    lld = os.environ.get("LLVM_LINK_WRAPPER_LLD_LD_PATH", "ld.lld")
    toolchain = Toolchain(llvm_link, llvm_ar, lld)
    args = sys.argv[1:]
    bitcode_ld = BitcodeLinkerWrapper(args, toolchain)

    processes = []
    processes.append(subprocess.Popen([lld, *args]))

    with TemporaryDirectory() as tmpdir:
        if bitcode_ld.should_link():
            process = bitcode_ld.run(tmpdir)
            if process:
                processes.append(process)

        for process in processes:
            if process is not None:
                process.wait()


if __name__ == "__main__":
    main()
