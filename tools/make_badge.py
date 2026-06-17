#!/usr/bin/env python3
"""Generate the s8sskills "skill medallion" badge as a flat low-poly SVG.

The badge is a merit-rosette: a faceted sunburst ring around a cut-gem disc
with a four-point "skill spark" at the center. Palette is sampled from the
hachidori hummingbird so the badge and bird read as one brand.
"""
import math

# Palette sampled from hachidori-1.png
MAG = "#D848D8"
MAG_D = "#A92BB0"
IND = "#3C3CA8"
IND_D = "#2A2A86"
IND_L = "#5050C8"
CYAN = "#3CCCE4"
CYAN_L = "#9BE8F4"

CX = CY = 120.0
R_TIP = 116.0   # sunburst spike tip radius
R_BASE = 72.0   # sunburst spike base radius (tucks behind the gem)
N_SPIKES = 16

GEM_R = 82.0    # inner gem radius
GEM_FACETS = 12

SPARK_LONG = 46.0   # spark point length from center
SPARK_SHORT = 14.0  # spark waist


def pt(r, ang):
    return (CX + r * math.cos(ang), CY + r * math.sin(ang))


def poly(points, fill):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'  <polygon points="{pts}" fill="{fill}"/>'


def build():
    out = []
    out.append(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" '
        'width="240" height="240">'
    )

    # --- Sunburst ring: each spike split into two facets (light/dark) ---
    step = 2 * math.pi / N_SPIKES
    half = step * 0.5
    for i in range(N_SPIKES):
        theta = -math.pi / 2 + i * step  # start at top
        tip = pt(R_TIP, theta)
        base_l = pt(R_BASE, theta - half)
        base_r = pt(R_BASE, theta + half)
        base_mid = pt(R_BASE, theta)
        # alternate the dominant hue spike-to-spike
        if i % 2 == 0:
            light, dark = MAG, MAG_D
        else:
            light, dark = IND_L, IND_D
        out.append(poly([tip, base_l, base_mid], light))
        out.append(poly([tip, base_mid, base_r], dark))

    # --- Cut-gem disc: radial facets, alternating indigo shades ---
    gstep = 2 * math.pi / GEM_FACETS
    for i in range(GEM_FACETS):
        a0 = -math.pi / 2 + i * gstep
        a1 = a0 + gstep
        p0 = pt(GEM_R, a0)
        p1 = pt(GEM_R, a1)
        fill = IND if i % 2 == 0 else IND_D
        out.append(poly([(CX, CY), p0, p1], fill))
    # thin cyan rim
    out.append(
        f'  <circle cx="{CX}" cy="{CY}" r="{GEM_R:.2f}" fill="none" '
        f'stroke="{CYAN}" stroke-width="3"/>'
    )

    # --- Center skill spark: 4 long points + 4 short, faceted ---
    long_pts = []
    for k in range(4):
        a = -math.pi / 2 + k * (math.pi / 2)
        long_pts.append(pt(SPARK_LONG, a))
    waist = []
    for k in range(4):
        a = -math.pi / 2 + math.pi / 4 + k * (math.pi / 2)
        waist.append(pt(SPARK_SHORT, a))
    # build 8 alternating arm facets, light on one diagonal, cyan on other
    star = []
    for k in range(4):
        star.append(long_pts[k])
        star.append(waist[k])
    # left/right facet shading per arm for the origami look
    for k in range(4):
        tip = long_pts[k]
        w_prev = waist[(k - 1) % 4]
        w_next = waist[k]
        out.append(poly([(CX, CY), w_prev, tip], CYAN))
        out.append(poly([(CX, CY), tip, w_next], CYAN_L))
    # tiny white core highlight
    out.append(f'  <circle cx="{CX}" cy="{CY}" r="5.5" fill="#FFFFFF"/>')

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "assets/brand/badge.svg"
    with open(path, "w") as f:
        f.write(build())
    print("wrote", path)
