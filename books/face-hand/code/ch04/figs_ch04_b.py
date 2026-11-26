# -*- coding: utf-8 -*-
"""第 4 章补充插图：同一段音频对应多个合理口型（一对多）。"""
import sys
import numpy as np

sys.path.insert(0, "E:/Study/人体参数化技术/人体参数化技术学习/books/code")
import figstyle as fs
from matplotlib.patches import Ellipse, Rectangle

fs.FIGDIR = "E:/Study/人体参数化技术/人体参数化技术学习/books/face-hand/images"


def mouth(ax, cx, cy, w, h, color=fs.INK, lw=1.4, teeth=True, z=3):
    """画一个张开的嘴：外唇 + 口腔 + 上排牙（牙齿用口腔形状裁剪）。"""
    ax.add_patch(Ellipse((cx, cy), w, h * 1.35, facecolor="#F3D9C8",
                         edgecolor=color, lw=lw, zorder=z))
    inner = Ellipse((cx, cy), w * 0.84, h * 0.95, facecolor="#7A3B37",
                    edgecolor="none", zorder=z + 1)
    ax.add_patch(inner)
    if teeth:
        r = Rectangle((cx - w * 0.45, cy + h * 0.14), w * 0.90, h * 0.32,
                      facecolor="#FDFDFB", edgecolor="none", zorder=z + 2)
        ax.add_patch(r)
        r.set_clip_path(inner)


def fig_one_to_many():
    fig, ax = fs.canvas(6.8, 3.7)
    fs.label(ax, 0.5, 0.955, "同一段音频，多种合理口型：平均解就是“僵尸脸”",
             fs=10.2, color=fs.INK, weight="bold")

    # 左：音频片段
    fs.box(ax, 0.028, 0.46, 0.19, 0.29,
           "音频片段\n“你好”的第一拍\n$t=0.12\\sim0.24$ s\n音素 /n/ → /i/",
           ec=fs.BLUE, fs=8.0)
    t = np.linspace(0, 1, 400)
    env = np.abs(np.sin(3.2 * np.pi * t)) * (0.45 + 0.55 * np.sin(np.pi * t))
    ax.plot(0.038 + 0.17 * t, 0.405 + 0.035 * env * np.sin(70 * np.pi * t),
            color=fs.BLUE, lw=0.55, zorder=4)
    ax.plot([0.038, 0.208], [0.405, 0.405], color=fs.FAINT, lw=0.6)

    # 右：同一拍的五个合理解释
    xs = [0.395, 0.520, 0.645, 0.770, 0.893]
    heights = [0.042, 0.070, 0.098, 0.126, 0.155]
    notes = ["几乎不张", "微开", "中等（平均解）", "偏大", "张大"]
    for i, (x, h, note) in enumerate(zip(xs, heights, notes)):
        c = fs.MUTED if i == 2 else fs.ACCENT
        mouth(ax, x, 0.645, 0.105, h, color=c, lw=1.7 if i == 2 else 1.3)
        fs.label(ax, x, 0.645 - h * 0.68 - 0.05, note, fs=7.2, color=c)

    fs.label(ax, 0.645, 0.855, "五个都“听得出来是这两个音”", fs=8.6, color=fs.ACCENT)

    fs.box(ax, 0.375, 0.185, 0.575, 0.135,
           "只学平均的结果：嘴形取中间那一档，开合幅度被削掉一半，\n"
           "看上去“嘴在动、脸不动”——僵尸脸就是这么来的",
           ec=fs.MUTED, fs=8.0, lw=0.9)

    fs.box(ax, 0.028, 0.055, 0.30, 0.135,
           "缺的信息：怎么说\n重音、语气、情绪",
           ec=fs.PURPLE, fs=7.8)

    fs.label(ax, 0.66, 0.048,
             "从音频到口型是多对一的逆问题，一次回归解不干净",
             fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch04", "fig04-04")


if __name__ == "__main__":
    fig_one_to_many()
