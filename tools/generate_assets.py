"""
Draws the two bundled images that are pure geometry, and strips metadata from
every PNG in assets/.

- backgrounds/disks.png: 90 wall disks on five concentric rings (ring k holds
  6k disks), the same layout as the original project's "Disks" map.
- gradients/grayscale.png: a linear ramp, black at the top, white at the bottom.

The originals were made with a personal-use-only student license (it says so
in their metadata), so these are regenerated here from the geometry alone.

Run it before tools/embed_assets.py:

    python tools/generate_assets.py
    python tools/embed_assets.py
"""
import math
import struct
import zlib
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# Chunks that carry text, dates or EXIF. Nothing the image needs to render.
METADATA_CHUNKS = {b"tEXt", b"zTXt", b"iTXt", b"eXIf", b"tIME"}


def chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def write_png(path, width, height, color_type, rows):
    """rows: one bytes object per scanline, without the filter byte."""
    raw = b"".join(b"\x00" + row for row in rows)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(png)


def disks(size=2048, spacing=169, radius=25, rings=5):
    """Black disks (alpha = wall) on transparent ground, edges antialiased."""
    alpha = bytearray(size * size)
    centre = size / 2
    samples = 4  # 4x4 supersampling for the edge pixels
    for k in range(1, rings + 1):
        count = 6 * k
        for n in range(count):
            angle = 2 * math.pi * n / count
            cx = centre + k * spacing * math.cos(angle)
            cy = centre + k * spacing * math.sin(angle)
            for y in range(int(cy - radius - 1), int(cy + radius + 2)):
                for x in range(int(cx - radius - 1), int(cx + radius + 2)):
                    hits = 0
                    for sy in range(samples):
                        for sx in range(samples):
                            dx = x + (sx + 0.5) / samples - cx
                            dy = y + (sy + 0.5) / samples - cy
                            if dx * dx + dy * dy <= radius * radius:
                                hits += 1
                    if hits:
                        i = y * size + x
                        alpha[i] = max(alpha[i], round(255 * hits / samples ** 2))
    rows = []
    for y in range(size):
        row = bytearray(size * 4)
        row[3::4] = alpha[y * size:(y + 1) * size]
        rows.append(bytes(row))
    write_png(ASSETS / "backgrounds" / "disks.png", size, size, 6, rows)


def grayscale(width=10, height=2048):
    rows = []
    for y in range(height):
        v = round(255 * y / (height - 1))
        rows.append(bytes([v, v, v]) * width)
    write_png(ASSETS / "gradients" / "grayscale.png", width, height, 2, rows)


def strip_metadata(path):
    data = path.read_bytes()
    out = bytearray(data[:8])
    i = 8
    while i < len(data):
        (length,) = struct.unpack(">I", data[i:i + 4])
        kind = data[i + 4:i + 8]
        end = i + 12 + length
        if kind not in METADATA_CHUNKS:
            out += data[i:end]
        i = end
    if len(out) != len(data):
        path.write_bytes(bytes(out))
        print(f"stripped metadata: {path.relative_to(ASSETS)}")


def main():
    disks()
    grayscale()
    for path in sorted(ASSETS.rglob("*.png")):
        strip_metadata(path)
    print("done")


if __name__ == "__main__":
    main()
