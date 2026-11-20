# -*- coding: utf-8 -*-
"""入门册第 8 章插图：从零到看见一个人（四步）。"""
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

STEPS = [
    ("① 装环境", "Python + 一个\n模型库", "别从零实现\n先跑通别人的", fs.ACCENT),
    ("② 载入模型", "模板、形状基、\n权重、关节树", "注意许可\n与文件版本", fs.BLUE),
    ("③ 前向一次", "给一组参数\n算出顶点", "先只改一个\n参数看变化", fs.GREEN),
    ("④ 看与导出", "渲染一张图\n或写 obj/fbx", "单位、朝向、\n关节顺序", fs.PURPLE),
]


def main():
    fig = plt.figure(figsize=(6.9, 2.9))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    w, h = 0.205, 0.42
    y = 0.28
    xs = [0.035, 0.275, 0.515, 0.755]
    for (head, mid, tip, col), x in zip(STEPS, xs):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.006,rounding_size=0.014",
                                    ec=col, fc="#FFFFFF", lw=1.1, zorder=2))
        ax.text(x + w / 2, y + h * 0.87, head, ha="center", va="center",
                fontsize=9.0, color=col, zorder=3)
        ax.text(x + w / 2, y + h * 0.60, mid, ha="center", va="center",
                fontsize=7.4, color=fs.INK, zorder=3, linespacing=1.6)
        ax.text(x + w / 2, y + h * 0.19, tip, ha="center", va="center",
                fontsize=6.6, color=fs.MUTED, zorder=3, linespacing=1.7)
        if x != xs[-1]:
            ax.add_patch(FancyArrowPatch((x + w + 0.004, y + h / 2),
                                         (x + w + 0.030, y + h / 2),
                                         arrowstyle="-|>", mutation_scale=10,
                                         color=fs.FAINT, lw=1.0, zorder=1))

    ax.text(0.035, 0.90, "从零到看见一个人：四步", fontsize=9.6, color=fs.INK, va="top")
    ax.text(0.035, 0.815, "每一步都有现成工具，先把链路跑通，再回头补原理",
            fontsize=7.8, color=fs.MUTED, va="top")
    ax.text(0.035, 0.12, "第一张图出来之后，再决定往哪个方向深入：几何、拟合、渲染，还是生成。",
            fontsize=7.6, color=fs.FAINT, va="top")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch08", "fig08-01")


if __name__ == "__main__":
    main()
