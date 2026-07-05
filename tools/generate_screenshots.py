from __future__ import annotations

import struct
import zlib
from pathlib import Path


def _chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_png(path: Path, width: int, height: int, accent: tuple[int, int, int]) -> None:
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            if 24 < x < width - 24 and 24 < y < height - 24:
                base = (246, 248, 250)
            else:
                base = (36, 41, 47)
            if 70 < x < width - 70 and 80 < y < 125:
                base = accent
            if 70 < x < width - 70 and 155 < y < 175:
                base = (210, 215, 222)
            if 70 < x < width - 220 and 210 < y < 235:
                base = (121, 184, 255)
