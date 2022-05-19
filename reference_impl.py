#!/usr/bin/env python3

import argparse
import sys
import hashlib
from zipfile import ZipFile
import numpy as np
import qoi


def main():
    parser = argparse.ArgumentParser(
        description="Reference QOI challenge implementation"
    )
    parser.add_argument(
        "input", nargs="?", type=argparse.FileType("rb"), default=sys.stdin.buffer
    )
    args = parser.parse_args()

    with ZipFile(args.input) as archive:
        for file_info in archive.filelist:
            archive_bytes = archive.read(file_info.filename)
            decoded_array: np.ndarray = qoi.decode(archive_bytes)

            print(
                file_info.filename,
                decoded_array.shape[1],
                decoded_array.shape[0],
                decoded_array.shape[2],
            )
            print(hashlib.sha512(decoded_array.tobytes()).hexdigest())


if __name__ == "__main__":
    main()
