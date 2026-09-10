#!/usr/bin/env python3
"""Composite the skill medallion onto the hachidori hummingbird and emit the
full s8sskills logo asset set (mark PNGs + favicons).

Run from the site root:  python3 tools/make_logo.py
Requires: Pillow, rsvg-convert on PATH.

The hummingbird master lives in the Hachidori brand repo, not here — this repo
only commits the generated results, so the site build never needs it. Point at
a checkout with HACHIDORI_BRAND, or keep one as a sibling of the s8sskills
workspace (the default below).
"""
import os
import subprocess
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, "assets", "brand")
STATIC = os.path.join(ROOT, "static")
BADGE_SVG = os.path.join(BRAND, "badge.svg")

# ROOT is .../Serverless/S8S-Skills/S8S-Skills-Workspace/site, so the sibling
# Hachidori checkout is four levels up.
DEFAULT_BRAND_HOME = os.path.normpath(
    os.path.join(ROOT, "..", "..", "..", "Hachidori", "brand")
)
BRAND_HOME = os.environ.get("HACHIDORI_BRAND", DEFAULT_BRAND_HOME)
BIRD = os.path.join(BRAND_HOME, "hachidori-logo-1.png")


def require_bird():
    """Fail loudly and usefully when the brand repo isn't where we expect."""
    if os.path.isfile(BIRD):
        return
    sys.exit(
        f"Hummingbird master not found: {BIRD}\n"
        "\n"
        "The master art lives in the Hachidori brand repo, not in this one.\n"
        "Clone it next to the s8sskills workspace, or set HACHIDORI_BRAND:\n"
        "\n"
        "    HACHIDORI_BRAND=/path/to/Hachidori/brand python3 tools/make_logo.py\n"
    )


def render_badge(size):
    out = os.path.join(BRAND, f"_badge_{size}.png")
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size), BADGE_SVG, "-o", out],
        check=True,
    )
    img = Image.open(out).convert("RGBA")
    os.remove(out)
    return img


def build_mark():
    """Square brand mark: hummingbird carrying the skill medallion."""
    bird = Image.open(BIRD).convert("RGBA")
    W, H = bird.size  # 4167 square
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(bird)

    badge_size = int(W * 0.42)
    badge = render_badge(badge_size)
    # lower-right quadrant, tucked into the empty space below the beak so it
    # reads as the hummingbird presenting the skill medallion
    bx = int(W * 0.57)
    by = int(H * 0.55)
    canvas.alpha_composite(badge, (bx, by))

    mark = canvas.crop(canvas.getbbox())
    mark.save(os.path.join(BRAND, "logo-mark.png"))
    return mark


def square_pad(img, pad_frac=0.06, bg=(0, 0, 0, 0)):
    w, h = img.size
    side = int(max(w, h) * (1 + pad_frac * 2))
    out = Image.new("RGBA", (side, side), bg)
    out.alpha_composite(img, ((side - w) // 2, (side - h) // 2))
    return out


def main():
    require_bird()
    os.makedirs(STATIC, exist_ok=True)

    # Full lockup (hummingbird + medallion) for in-page logo use.
    mark = build_mark()
    mark.save(os.path.join(STATIC, "logo.png"))

    # The medallion alone is bold and square, so it is the favicon / app icon
    # (the full lockup turns to mush below ~64px).
    icon = square_pad(render_badge(1024), pad_frac=0.04)
    for size in (512, 256, 192, 180, 64, 48, 32, 16):
        icon.resize((size, size), Image.LANCZOS).save(
            os.path.join(STATIC, f"icon-{size}.png")
        )
    icon.resize((180, 180), Image.LANCZOS).save(
        os.path.join(STATIC, "apple-touch-icon.png")
    )
    icon.resize((256, 256), Image.LANCZOS).save(
        os.path.join(STATIC, "favicon.ico"),
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )
    print("logo lockup:", mark.size, "-> static/logo.png + medallion icons")


if __name__ == "__main__":
    main()
