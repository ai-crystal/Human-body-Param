# -*- coding: utf-8 -*-
"""入门册第 4 章图 4-3：六种现实麻烦，各自缺什么、靠什么补。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(BOOK), "code"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import figstyle as fs

FIGDIR = os.path.join(BOOK, "images")

ROWS = [
    ("遮挡", "信息真的不在\n被挡住的部位没有像素", "只能靠先验猜", fs.ACCENT),
    ("深度歧义", "信息在，但少了一维\n远近被压平了", "把相机一起估", fs.BLUE),
    ("尺度歧义", "放大倍数看不出来\n小人近处 = 大人远处", "找已知大小的参照物", fs.BLUE),
    ("数据偏差", "样本里没有这种人\n老人、孕妇、极胖", "补数据，改不了算法", fs.GREEN),
    ("多人", "信息都在\n但要先分清谁是谁", "先分实例，再逐人估", fs.PURPLE),
    ("衣服", "模型里没有衣服\n它是赤体的", "换更松的表示，或先估衣服", fs.PINK),
]


def fig_trouble():
    fig = plt.figure(figsize=(6.9, 4.0))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fs.label(ax, 0.04, 0.975, "六种麻烦，性质不同，药也不同",
             fs=9.8, color=fs.INK, ha="left", va="top")
    fs.label(ax, 0.04, 0.915, "先判断“缺的是哪一类信息”，再决定补什么；把网络做大解决不了其中任何一条",
             fs=8.0, color=fs.MUTED, ha="left", va="top")

    x_name, x_why, x_fix = 0.045, 0.175, 0.700
    fs.label(ax, x_name, 0.855, "麻烦", fs=7.6, color=fs.FAINT, ha="left")
    fs.label(ax, x_why, 0.855, "它到底缺什么", fs=7.6, color=fs.FAINT, ha="left")
    fs.label(ax, x_fix, 0.855, "只能靠什么补", fs=7.6, color=fs.FAINT, ha="left")

    h = 0.118
    y_top = 0.795
    for i, (name, why, fix, c) in enumerate(ROWS):
        y = y_top - (i + 1) * h
        if i % 2 == 0:
            ax.add_patch(Rectangle((0.035, y), 0.93, h, facecolor="#F7F7F8",
                                   edgecolor="none", zorder=1))
        ax.add_patch(Rectangle((0.035, y + 0.012), 0.006, h - 0.024, facecolor=c,
                               edgecolor="none", zorder=2))
        fs.label(ax, x_name, y + h / 2, name, fs=8.8, color=c, ha="left", weight="bold")
        fs.label(ax, x_why, y + h / 2, why, fs=7.9, color=fs.INK, ha="left", va="center")
        fs.label(ax, x_fix, y + h / 2, fix, fs=7.9, color=fs.MUTED, ha="left", va="center")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch04", "fig04-03")


if __name__ == "__main__":
    fig_trouble()
