# -*- coding: utf-8 -*-
"""入门册第 1 章插图：三条阅读路线（按六册重新画）。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(BOOK), "code"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import figstyle as fs

FIGDIR = os.path.join(BOOK, "images")


def chip(ax, x, y, w, h, head, sub, ec, fc="#FFFFFF"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.004,rounding_size=0.012",
                                ec=ec, fc=fc, lw=1.0, zorder=2))
    ax.text(x + w / 2, y + h * 0.63, head, ha="center", va="center",
            fontsize=8.2, color=ec, zorder=3)
    ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center",
            fontsize=6.8, color=fs.MUTED, zorder=3)


def arrow(ax, p, q, color=fs.FAINT):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9,
                                 color=color, lw=1.0, zorder=1,
                                 shrinkA=1.0, shrinkB=1.0))


ROUTES = [
    ("零基础通读", fs.ACCENT,
     [("入门册", "概念地图"), ("数学册", "全部公式"), ("人体册", "SMPL 公式"),
      ("重建册", "从图像到人"), ("前沿册", "动物与前沿")]),
    ("只想做人体", fs.BLUE,
     [("入门册", "概念"), ("数学册", "PCA 与蒙皮"), ("人体册", "SMPL 公式"),
      ("重建册", "拟合与评估")]),
    ("只做人脸或手", fs.GREEN,
     [("入门册", "概念"), ("数学册", "PCA 与蒙皮"), ("人体册", "公式写法"),
      ("脸手册", "3DMM / MANO")]),
]


def main():
    fig = plt.figure(figsize=(6.9, 3.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    x0, w, gap = 0.150, 0.128, 0.026
    h = 0.115
    ys = [0.70, 0.42, 0.14]
    for (label, col, chips), y in zip(ROUTES, ys):
        ax.text(0.012, y + h * 0.45, label, fontsize=8.2, color=col, va="center")
        for i, (head, sub) in enumerate(chips):
            x = x0 + i * (w + gap)
            chip(ax, x, y, w, h, head, sub, col)
            if i:
                arrow(ax, (x - gap + 0.004, y + h / 2), (x - 0.004, y + h / 2))

    ax.text(0.015, 0.955, "三条路线", fontsize=9.6, color=fs.INK, va="top")
    ax.text(0.015, 0.885, "每册都能单独读，给的是最小前置；缺的知识按指路回补",
            fontsize=7.6, color=fs.MUTED, va="top")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch01", "fig01-04")


if __name__ == "__main__":
    main()
