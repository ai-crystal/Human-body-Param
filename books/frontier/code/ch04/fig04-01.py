# -*- coding: utf-8 -*-
"""第 4 章 图 4-1：2020 年之后的四条线（时间只标到年）。"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = "E:/Study/人体参数化技术/人体参数化技术学习/books/frontier/images"


def fig_lanes():
    fig, ax = fs.canvas(7.0, 3.3)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    x0, x1 = 0.170, 0.975
    lo, hi = 2019, 2025

    def X(year):
        return x0 + (x1 - x0) * (year - lo) / (hi - lo)

    # 年份刻度
    for yr in range(lo, hi + 1):
        ax.plot([X(yr), X(yr)], [0.150, 0.885], color=fs.GRID, lw=0.7, zorder=0)
        fs.label(ax, X(yr), 0.112, str(yr), fs=7.6, color=fs.MUTED)

    lanes = [
        ("表示", 0.800, fs.BLUE,
         [(2020, "NeRF"), (2021.6, "HumanNeRF"), (2023, "3DGS")]),
        ("生成", 0.600, fs.ACCENT,
         [(2020, "DDPM"), (2022.5, "SDS 文生 3D"), (2024, "视频扩散")]),
        ("感知", 0.400, fs.TEAL,
         [(2021, "CLIP"), (2023, "SAM / DINOv2"), (2024.2, "深度大模型")]),
        ("参数", 0.200, fs.GREEN,
         [(2019, "SMPL-X"), (2023, "SMPLer-X"), (2025, "统一模型")]),
    ]

    for name, y, c, items in lanes:
        ax.plot([x0, x1], [y, y], color=c, lw=1.1, alpha=0.55, zorder=1)
        fs.label(ax, 0.150, y, name, fs=8.8, color=c, ha="right", weight="bold")
        for yr, txt in items:
            ax.scatter([X(yr)], [y], s=42, color=c, zorder=4, edgecolor="white", lw=0.9)
            fs.label(ax, X(yr), y + 0.058, txt, fs=7.4, color=c)

    fs.label(ax, 0.5, 0.975, "2020 年之后：表示、生成、感知、参数四条线并行推进", fs=9.6,
             color=fs.INK, weight="bold")
    fs.label(ax, 0.5, 0.030,
             "参数层十年未变，上面换了三代工具——这是“人体基础模型”能拼起来的原因",
             fs=7.8, color=fs.MUTED)
    fs.save(fig, "ch04", "fig04-01")


if __name__ == "__main__":
    fig_lanes()
