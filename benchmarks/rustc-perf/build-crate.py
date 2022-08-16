import subprocess
import sys
from tempfile import TemporaryDirectory
import argparse
import glob
import shutil
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", help="path to Cargo.toml to build")
    parser.add_argument("--output", help="output file")

    options = parser.parse_args()

    with TemporaryDirectory() as tmpdir:
        cargo_cmd = [os.path.join(os.getcwd(), os.environ["CARGO"]), "build", "--release",
                     "--tests", "--target-dir", tmpdir]
        cc = os.path.join(os.getcwd(), os.environ["CC"])
        cargo_home = os.path.join(tmpdir, ".cargo-home")

        cargo_env = {"CARGO_PROFILE_RELEASE_LTO": "true",
                     "CARGO_HOME": cargo_home,
                     "RUSTFLAGS": f"-C save-temps -C linker={cc} -C link-args=-fuse-ld=lld"}

        for var in ["RUSTC"]:
            if var in os.environ:
                cargo_env[var] = os.path.join(os.getcwd(), os.environ[var])

        cargo_proc = subprocess.Popen(
            cargo_cmd, env=cargo_env, cwd=os.path.dirname(options.package))
        cargo_proc.wait()
        if cargo_proc.returncode != 0:
            sys.exit(cargo_proc.returncode)

        bc = glob.glob("{}/release/deps/*.lto.input.bc".format(tmpdir))[0]
        shutil.copyfile(bc, options.output)


if __name__ == "__main__":
    main()
