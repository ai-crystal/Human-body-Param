# -*- coding: utf-8 -*-
"""第 1 章 图 1-5：SMAL 的三类失败与检查方法。"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = r"E:\Study\人体参数化技术\人体参数化技术学习\books\frontier\images"


def fig_failure_map():
    fig, ax = fs.canvas(7.0, 3.5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    fs.label(ax, 0.5, 0.955, "三类失败、三种成因、三种一分钟检查", fs=10.0,
             color=fs.INK, weight="bold")

    cols = [(0.165, 0.255, "看到的症状", fs.BLUE),
            (0.445, 0.255, "成因", fs.GOLD),
            (0.720, 0.265, "一分钟检查", fs.GREEN)]
    for x, w, t, c in cols:
        fs.label(ax, x + w / 2, 0.868, t, fs=8.8, color=c, weight="bold")

    rows = [
        ("对应\n坏了", fs.BLUE,
         "换一个个体，同一个 $\\beta$ 维\n改动的位置全变",
         "配准把左右腿、内外侧\n弄混了",
         "把形状基单独渲染成位移场，\n看它是否只改一小块"),
        ("驱动\n坏了", fs.ACCENT,
         "参数还在合法范围，网格\n仍然自交、腿部翻面",
         "形状空间没有先验，\n$\\beta$ 跑到训练分布外",
         "扫一维 $\\beta$，从 $-3\\sigma$ 到\n$+3\\sigma$ 逐格渲染对比"),
        ("反推\n坏了", fs.PURPLE,
         "拟合出的 $\\boldsymbol{\\theta}$ 与目视\n姿态明显不符",
         "监督太弱；尺度与相机\n没有解耦",
         "重建结果投影回原图，\n遮住一半看另一半"),
    ]

    ys = [0.615, 0.345, 0.075]
    h = 0.215
    for (tag, tc, sym, cause, check), y in zip(rows, ys):
        fs.box(ax, 0.020, y, 0.120, h, tag, fc="#FFFFFF", ec=tc, fs=8.2, tc=tc, lw=1.2)
        for (x, w, _, c), txt in zip(cols, (sym, cause, check)):
            fs.box(ax, x, y, w, h, txt, fc="#FFFFFF", ec="#D1D5DB", fs=7.5, lw=0.9)
        fs.arrow(ax, (0.142, y + h / 2), (0.162, y + h / 2), color=fs.FAINT, lw=0.9)
        fs.arrow(ax, (0.421, y + h / 2), (0.442, y + h / 2), color=fs.FAINT, lw=0.9)
        fs.arrow(ax, (0.701, y + h / 2), (0.717, y + h / 2), color=fs.FAINT, lw=0.9)

    fs.label(ax, 0.5, 0.020, "三类经常同时出现，但根因不同：先判断落在哪一行，再谈加数据还是加先验",
             fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-05")


if __name__ == "__main__":
    fig_failure_map()
