import argparse
import subprocess
from pathlib import Path
import sys
from time import perf_counter


def main():
    parser = argparse.ArgumentParser(description="Timer tool for QOI challenge")
    parser.add_argument("executable_cmd", type=str)
    parser.add_argument("input", type=argparse.FileType("rb"))

    args = parser.parse_args()

    start = perf_counter()
    subprocess.run(
        args.executable_cmd.split(" "),
        stdin=args.input,
        stdout=subprocess.DEVNULL,
        stderr=sys.stderr,
        check=True,
    )
    stop = perf_counter()
    elapsed = stop - start
    print(elapsed)


if __name__ == "__main__":
    main()
