# -*- coding: utf-8 -*-
"""入门册第 5 章插图：六册的依赖关系。"""
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


def node(ax, x, y, w, h, title, sub, fc="#FFFFFF", ec=fs.INK, tc=fs.INK, tfs=9.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.006,rounding_size=0.014",
                                ec=ec, fc=fc, lw=1.1, zorder=2))
    ax.text(x + w / 2, y + h * 0.70, title, ha="center", va="center",
            fontsize=tfs, color=tc, zorder=3)
    ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center",
            fontsize=7.0, color=fs.MUTED, zorder=3, linespacing=1.6)


def arrow(ax, p, q, color=fs.MUTED, lw=1.1, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11,
                                 color=color, lw=lw, linestyle=ls,
                                 connectionstyle="arc3,rad=%s" % rad, zorder=1,
                                 shrinkA=1.5, shrinkB=1.5))


def main():
    fig = plt.figure(figsize=(6.9, 3.3))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    W, H = 0.205, 0.155
    x0 = 0.045
    # 左列：入门 -> 数学 -> 人体
    node(ax, x0, 0.700, W, H, "入门册", "概念与全局地图",
         fc="#FDF6EE", ec=fs.ACCENT, tc=fs.ACCENT, tfs=9.6)
    node(ax, x0, 0.390, W, H, "数学册", "向量 · PCA · 旋转\n蒙皮 · 优化",
         fc="#F3F6FD", ec=fs.BLUE, tc=fs.BLUE, tfs=9.6)
    node(ax, x0, 0.080, W, H, "人体册", "SCAPE · SMPL\nSMPL 家族",
         fc="#F1F8F4", ec=fs.GREEN, tc=fs.GREEN, tfs=9.6)

    # 右列：三个专业方向
    W3 = 0.175
    xs = [0.375, 0.575, 0.775]
    items = [("重建册", "单图 · 视频\n评估 · 动作", fs.PURPLE),
             ("脸手册", "3DMM · FLAME\nMANO · 交互", fs.GOLD),
             ("前沿册", "SMAL · 扩散\n基础模型", fs.PINK)]
    for (t, s, c), x in zip(items, xs):
        node(ax, x, 0.080, W3, H, t, s, fc="#FAF7F2", ec=c, tc=c, tfs=9.2)

    # 纵向依赖：入门 -> 数学 -> 人体
    cx = x0 + W / 2
    arrow(ax, (cx, 0.700), (cx, 0.548))
    arrow(ax, (cx, 0.390), (cx, 0.238))
    # 人体 -> 三个方向
    for x in xs:
        arrow(ax, (x0 + W, 0.141), (x - 0.004, 0.141), color=fs.FAINT, lw=1.0)
    # 数学 -> 三个方向（虚线捷径）
    for x in xs:
        arrow(ax, (x0 + W, 0.435), (x, 0.237), color="#D8DEE7", lw=0.9,
              rad=-0.14, ls=(0, (3, 2.6)))

    ax.text(0.775, 0.012, "虚线表示可以直接跳过去，缺的知识再回补",
            fontsize=7.2, color=fs.FAINT, ha="right")
    ax.text(0.045, 0.985, "六册的分工与依赖", fontsize=9.8, color=fs.INK, va="top")
    ax.text(0.045, 0.925, "实线是建议顺序，虚线是可选的捷径",
            fontsize=8.0, color=fs.MUTED, va="top")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch05", "fig05-01")


if __name__ == "__main__":
    main()
