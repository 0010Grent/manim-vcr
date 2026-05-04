#!/usr/bin/env python3
"""Generate showcase assets: architecture diagram and SVG character gallery."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.image as mpimg
from PIL import Image
import cairosvg
import io

SHOWCASE_DIR = Path(__file__).parent.parent / "showcase"
CHARACTER_DIR = Path(__file__).parent.parent / "character"
SHOWCASE_DIR.mkdir(exist_ok=True)


def make_architecture_png():
    fig, ax = plt.subplots(figsize=(14, 6), facecolor="#0a0e27")
    ax.set_facecolor("#0a0e27")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis("off")

    box_style = dict(boxstyle="round,pad=0.4", linewidth=1.5)

    boxes = [
        (1.2, 4.5, "content/\nscript.yml", "#4fc3f7", 2.0, 0.9),
        (1.2, 2.8, "content/\ncharacter.yml", "#4fc3f7", 2.0, 0.9),
        (1.2, 1.1, "config/\nvideo.yml", "#ffd54f", 2.0, 0.9),
        (4.5, 4.5, "TTS Generate\nedge-tts", "#ce93d8", 2.0, 0.9),
        (4.5, 2.8, "SVG Generate\nsvgwrite", "#ce93d8", 2.0, 0.9),
        (7.8, 3.6, "Manim Render\nscenes/vcr.py", "#ff8a65", 2.2, 1.0),
        (11.0, 3.6, "AV Merge\nFFmpeg", "#66bb6a", 2.0, 0.9),
    ]

    for (x, y, label, color, w, h) in boxes:
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                               boxstyle="round,pad=0.15",
                               facecolor=color + "33", edgecolor=color,
                               linewidth=1.5, transform=ax.transData)
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center",
                fontsize=9, color="white", fontfamily="monospace",
                fontweight="bold")

    arrows = [
        (2.2, 4.5, 3.5, 4.5),
        (2.2, 2.8, 3.5, 2.8),
        (5.5, 4.5, 6.9, 4.0),
        (5.5, 2.8, 6.9, 3.6),
        (1.2, 1.1, 6.9, 3.2),
        (8.9, 3.6, 10.0, 3.6),
    ]
    for (x1, y1, x2, y2) in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#888888", lw=1.5))

    ax.text(7, 0.4, "output/VCR_Final.mp4", ha="center", va="center",
            fontsize=10, color="#ffd54f", fontfamily="monospace", fontweight="bold")
    ax.annotate("", xy=(7, 0.7), xytext=(12.0, 3.1),
                arrowprops=dict(arrowstyle="->", color="#ffd54f", lw=1.5, linestyle="dashed"))

    ax.text(7, 5.7, "Manim VCR - Pipeline Architecture",
            ha="center", va="center", fontsize=13, color="white",
            fontfamily="sans-serif", fontweight="bold")

    out = SHOWCASE_DIR / "architecture.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="#0a0e27")
    plt.close()
    print(f"  architecture.png saved ({out.stat().st_size // 1024}KB)")


def make_character_gallery():
    svg_files = [
        CHARACTER_DIR / "fu_yao_front.svg",
        CHARACTER_DIR / "fu_yao_thinking.svg",
        CHARACTER_DIR / "fu_yao_confident.svg",
        CHARACTER_DIR / "fu_yao_side_right.svg",
        CHARACTER_DIR / "fu_yao_side_left.svg",
    ]
    labels = ["Front\n(Smile)", "Thinking", "Confident", "Side Right", "Side Left"]

    fig, axes = plt.subplots(1, 5, figsize=(15, 5), facecolor="#0a0e27")
    fig.suptitle("SVG Character — Expression Gallery", color="white", fontsize=14, fontweight="bold")

    for ax, svg_path, label in zip(axes, svg_files, labels):
        ax.set_facecolor("#0a0e27")
        ax.axis("off")
        if svg_path.exists():
            png_data = cairosvg.svg2png(url=str(svg_path), output_width=400, output_height=500)
            img = Image.open(io.BytesIO(png_data))
            ax.imshow(img)
        ax.set_title(label, color="#4fc3f7", fontsize=9, fontfamily="monospace")

    plt.tight_layout()
    out = SHOWCASE_DIR / "character_gallery.png"
    plt.savefig(out, dpi=120, bbox_inches="tight", facecolor="#0a0e27")
    plt.close()
    print(f"  character_gallery.png saved ({out.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    print("Generating showcase assets...")
    make_architecture_png()
    make_character_gallery()
    print("Done.")
