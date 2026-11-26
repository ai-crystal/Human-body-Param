# -*- coding: utf-8 -*-
"""入门册第 1 章图 1-2：四种表示各自擅长什么、改起来难在哪（四张卡片）。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(BOOK), "code"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figstyle as fs

FIGDIR = os.path.join(BOOK, "images")

CARDS = [
    ("像素", fs.GOLD,
     "能看：剪影、抠图、找关节",
     "改不动：想让人长高，不知道动哪个格子"),
    ("点云", fs.BLUE,
     "能量：测围度、存档案、前后比对",
     "改不动：没有面，不能贴图，也不能动"),
    ("网格", fs.GREEN,
     "能画能动：游戏影视的公共格式",
     "改得慢：换个体型要手工拖几千个顶点"),
    ("参数", fs.ACCENT,
     "改得快：十几个数就换一个体型",
     "看不细：毛孔、衣褶、极端个体都表达不了"),
]


def fig_ground():
    fig = plt.figure(figsize=(6.9, 3.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fs.label(ax, 0.04, 0.955, "四种表示各有主场：没有更好的，只有更合适的",
             fs=9.8, color=fs.INK, ha="left", va="top")
    fs.label(ax, 0.04, 0.885, "每张卡片写两件事：它最擅长干什么，以及想改的时候卡在哪",
             fs=8.1, color=fs.MUTED, ha="left", va="top")

    w, h = 0.445, 0.285
    xs = [0.04, 0.515]
    ys = [0.535, 0.135]
    for i, (name, c, good, bad) in enumerate(CARDS):
        x = xs[i % 2]
        y = ys[i // 2]
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.006,rounding_size=0.018",
                                    ec=c, fc="#FFFFFF", lw=1.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y + h - 0.075), w, 0.075,
                                    boxstyle="round,pad=0.006,rounding_size=0.018",
                                    ec=c, fc=c, lw=1.2, alpha=0.13, zorder=3))
        fs.label(ax, x + 0.028, y + h - 0.038, name, fs=10.4, color=c,
                 ha="left", va="center", weight="bold")
        fs.label(ax, x + 0.028, y + 0.128, good, fs=8.3, color=fs.INK,
                 ha="left", va="center")
        fs.label(ax, x + 0.028, y + 0.048, bad, fs=8.3, color=fs.MUTED,
                 ha="left", va="center")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch01", "fig01-02")


if __name__ == "__main__":
    fig_ground()
