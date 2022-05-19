#!/usr/bin/env python3

from PIL import Image
import numpy as np
import struct
import os
import qoi
import io

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
os.chdir(script_dir)
os.makedirs("images/garbage", exist_ok=True)

for i in range(0, 10):
    filename = f"images/garbage/random-{i}.png"
    print(filename)

    pixels = np.random.randint(low=0, high=255, size=(1000, 1000, 4)).astype(np.uint8)
    img = Image.fromarray(pixels, mode="RGBA")
    img.save(filename, compress_level=0)

for i in range(0, 10):
    filename = f"images/garbage/bit-mangle-{i}.qoi"
    print(filename)

    pixels = np.random.randint(low=0, high=255, size=(4000 * 1000)).astype(np.uint8)
    qoi_garbage = io.BytesIO()
    header = struct.pack(">4sIIBB", b"qoif", 4000, 4000, 3, 0)
    qoi_garbage.write(header)
    qoi_garbage.write(pixels.tobytes())

    decoded_garbage = qoi.decode(qoi_garbage.getvalue())
    with open(filename, "wb+") as f:
        encoded_garbage = qoi.encode(decoded_garbage)
        f.write(encoded_garbage)
