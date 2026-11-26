# -*- coding: utf-8 -*-
"""入门册第 3 章图 3-4：三种补救路线的取舍。"""
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
    ("① 姿势修正位移", fs.BLUE,
     "在蒙皮结果上再叠一层\n随姿势变化的位移",
     "捏细和鼓包被补回来，\n管线不用改，代价最小",
     "要多学一组方向；\n极端姿势仍会露馅"),
    ("② 对偶四元数", fs.GREEN,
     "不混矩阵，改混\n只表示旋转的四元数",
     "结果一定是刚体变换，\n扭转的细颈基本消失",
     "算得更贵；带缩放就用\n不了，引擎支持也不齐"),
    ("③ 辅助关节", fs.PURPLE,
     "在肩、腋下插几根\n虚拟骨头，拆大角度",
     "每个关节只担小角度，\n收缩立刻轻很多",
     "骨架变复杂，动画师\n要多调几根骨头"),
]


def fig_fix():
    fig = plt.figure(figsize=(6.9, 3.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fs.label(ax, 0.04, 0.965, "三条补救路线：各有各的药效，也各有各的代价",
             fs=9.8, color=fs.INK, ha="left", va="top")
    fs.label(ax, 0.04, 0.900, "病根只有一个：两个刚体变换做平均，平均完就不再是刚体",
             fs=8.2, color=fs.MUTED, ha="left", va="top")

    w = 0.285
    x0, gap = 0.04, 0.0375
    y0, h = 0.075, 0.695
    labels = ["怎么做", "换来什么", "付出什么"]
    body_y = [0.525, 0.335, 0.155]
    for i, (title, c, how, gain, cost) in enumerate(CARDS):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, y0), w, h,
                                    boxstyle="round,pad=0.006,rounding_size=0.02",
                                    ec=c, fc="#FFFFFF", lw=1.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y0 + h - 0.085), w, 0.085,
                                    boxstyle="round,pad=0.006,rounding_size=0.02",
                                    ec=c, fc=c, lw=1.2, alpha=0.13, zorder=3))
        fs.label(ax, x + 0.024, y0 + h - 0.045, title, fs=9.2, color=c,
                 ha="left", va="center", weight="bold")
        for k, (lab, txt) in enumerate(zip(labels, (how, gain, cost))):
            ly = body_y[k]
            fs.label(ax, x + 0.024, ly + 0.075, lab, fs=7.3, color=fs.FAINT,
                     ha="left", va="center")
            fs.label(ax, x + 0.024, ly - 0.015, txt, fs=7.9,
                     color=fs.INK if k < 2 else fs.MUTED, ha="left", va="center")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch03", "fig03-04")


if __name__ == "__main__":
    fig_fix()
