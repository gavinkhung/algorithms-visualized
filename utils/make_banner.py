#!/usr/bin/env python3
"""Render the site banner: an array sorted on the left, still shuffled on the right.

    python3 utils/make_banner.py

Writes ``book/banner.png`` at 2400 x 400. The site crops it to the screen
width and shows its top, so the bars are kept short and low-contrast.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from algoviz.draw import IDLE  # noqa: E402

WIDTH, HEIGHT, DPI = 2400, 400, 100
BARS = 96
BACKGROUND = "#f8fafc"
SORTED = "#94a3b8"
COMPARED = ("#3b82f6", "#ec4899")


def main():
    rng = random.Random(161)
    values = [rng.uniform(0.15, 0.9) for _ in range(BARS)]
    split = BARS // 2
    values[:split] = sorted(values[:split])
    colors = [SORTED] * split + [IDLE] * (BARS - split)
    colors[split - 1], colors[split + 2] = COMPARED

    fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_facecolor(BACKGROUND)
    ax.bar(range(BARS), values, width=0.62, color=colors, alpha=0.55)
    ax.set_xlim(-1, BARS)
    ax.set_ylim(0, 1)
    ax.axis("off")

    out = ROOT / "book" / "banner.png"
    fig.savefig(out, dpi=DPI, facecolor=BACKGROUND)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
