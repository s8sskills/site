#!/usr/bin/env python3
"""Render the 1200x630 social card, embedding the logo mark as a data URI so
rsvg-convert reliably rasterizes it. Run from site root after make_logo.py."""
import base64
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = os.path.join(ROOT, "tools", "og.svg")
MARK = os.path.join(ROOT, "assets", "brand", "logo-mark.png")
OUT = os.path.join(ROOT, "static", "og-image.png")

with open(MARK, "rb") as f:
    data = base64.b64encode(f.read()).decode("ascii")
uri = "data:image/png;base64," + data

with open(SVG) as f:
    svg = f.read()

# swap whatever href is present for the embedded data URI
import re
svg = re.sub(r'xlink:href="[^"]*"', f'xlink:href="{uri}"', svg, count=1)

tmp = os.path.join(ROOT, "tools", "_og_embedded.svg")
with open(tmp, "w") as f:
    f.write(svg)

subprocess.run(
    ["rsvg-convert", "-w", "1200", "-h", "630", tmp, "-o", OUT], check=True
)
os.remove(tmp)
print("wrote", OUT)
