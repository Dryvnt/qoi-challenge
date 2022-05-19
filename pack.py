#!/usr/bin/env python3

from io import BytesIO
import os
import argparse
from itertools import chain
from glob import iglob
from zipfile import ZIP_DEFLATED, ZIP_LZMA, ZIP_STORED, ZipFile
from time import time
from datetime import timedelta

import qoi
import numpy as np
from PIL import Image, ImageCms

import os


def main():
    parser = argparse.ArgumentParser(description="Pack images for QOI challenge")
    parser.add_argument("output", type=argparse.FileType("w+b"))
    args = parser.parse_args()

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    os.chdir(script_dir)

    sRGB = ImageCms.createProfile("sRGB")

    def pack_image(archive: ZipFile, path: str):
        qoi_file_name = f"{os.path.splitext(path)[0]}.qoi"
        with Image.open(path) as img:
            print(f"{img.height}x{img.width} {img.mode}", end=" ")

            input_profile = sRGB

            # Required to confidently parse as sRGB
            assert img.mode in ["RGB", "RGBA"]
            if "icc_profile" in img.info:
                input_profile = ImageCms.ImageCmsProfile(
                    BytesIO(img.info.get("icc_profile"))
                )

            img_srgb = ImageCms.profileToProfile(img, input_profile, sRGB)

            qoi_data: bytes = qoi.encode(np.asarray(img_srgb))
            print(f"-> {qoi_file_name}", end=" ")

            with archive.open(qoi_file_name, "w") as qoi_file:
                qoi_file.write(qoi_data)

    with ZipFile(args.output, "w") as archive:
        for s in chain(iglob("images/*"), iglob("garbage/*")):
            print(s, end=" ")
            timer = time()

            extension = os.path.splitext(s)[1]
            if extension == ".qoi":
                with open(s, "rb") as qoi_file:
                    qoi_data = qoi_file.read()
                with archive.open(s, "w") as zip_file:
                    zip_file.write(qoi_data)
            else:
                pack_image(archive, s)

            print(f"{timedelta(seconds =time() - timer)}")


if __name__ == "__main__":
    main()
