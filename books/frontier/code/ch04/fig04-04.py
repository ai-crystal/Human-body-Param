# -*- coding: utf-8 -*-
"""第 4 章 图 4-4：生成式人体的五类典型失败（示意）。"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle
import figstyle as fs

fs.FIGDIR = "E:/Study/人体参数化技术/人体参数化技术学习/books/frontier/images"


def panel_frame(ax, cx, title, color):
    ax.plot([cx - 0.082, cx + 0.082], [0.815, 0.815], color=color, lw=1.0, alpha=0.6)
    fs.label(ax, cx, 0.900, title, fs=8.6, color=color, weight="bold")


def head_with_nose(ax, cx, cy, s, color, flip=1):
    ax.add_patch(Ellipse((cx, cy), 0.115 * s, 0.150 * s, facecolor=color, alpha=0.85,
                         edgecolor="none", zorder=3))
    pts = [(cx + flip * 0.055 * s, cy + 0.010 * s),
           (cx + flip * 0.105 * s, cy - 0.005 * s),
           (cx + flip * 0.055 * s, cy - 0.030 * s)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, alpha=0.85,
                         edgecolor="none", zorder=3))


def fig_failures():
    fig, ax = fs.canvas(7.0, 3.2)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    xs = [0.105, 0.305, 0.505, 0.705, 0.905]
    titles = ["多面（Janus）", "露洞", "时序抖动", "过饱和", "语义漂移"]
    colors = [fs.ACCENT, fs.BLUE, fs.PURPLE, fs.PINK, fs.TEAL]
    causes = ["2D 分数在 3D 上\n不自洽",
              "高斯密度不随\n形变自适应",
              "每帧独立优化，\n无时序约束",
              "引导强度 $s$\n过大",
              "条件注入太弱，\n或被纹理吸收"]

    for cx, t, c in zip(xs, titles, colors):
        panel_frame(ax, cx, t, c)

    # (a) 多面：两个头，鼻子朝相反方向
    cx = xs[0]
    head_with_nose(ax, cx - 0.018, 0.620, 1.0, "#E8B4A0", flip=-1)
    head_with_nose(ax, cx + 0.018, 0.610, 1.0, "#E8B4A0", flip=1)
    fs.label(ax, cx, 0.470, "两个视角都“像正面”", fs=6.8, color=fs.MUTED)

    # (b) 露洞：躯干拉伸后出现空隙
    cx = xs[1]
    ax.add_patch(Polygon([(cx - 0.075, 0.560), (cx - 0.045, 0.700), (cx + 0.045, 0.700),
                          (cx + 0.075, 0.560), (cx + 0.010, 0.560), (cx, 0.620),
                          (cx - 0.010, 0.560)],
                         closed=True, facecolor="#C7D2FE", edgecolor=fs.BLUE, lw=0.8,
                         zorder=3))
    ax.add_patch(Polygon([(cx - 0.010, 0.575), (cx + 0.048, 0.575), (cx + 0.030, 0.665),
                          (cx + 0.002, 0.640)],
                         closed=True, facecolor="white", edgecolor=fs.BLUE, lw=0.8,
                         ls=(0, (2, 1.5)), zorder=4))
    fs.label(ax, cx, 0.470, "弯曲时露出背景", fs=6.8, color=fs.MUTED)

    # (c) 抖动：平滑曲线与抖动折线
    cx = xs[2]
    tt = np.linspace(-1, 1, 60)
    ax.plot(cx + tt * 0.070, 0.640 + 0.030 * np.sin(tt * 1.6), color=fs.FAINT, lw=1.0,
            ls=(0, (3, 2)), zorder=2)
    tk = np.linspace(-1, 1, 7)
    ax.plot(cx + tk * 0.070, 0.640 + 0.030 * np.sin(tk * 1.6) + 0.022 * np.cos(tk * 5.0),
            color=fs.PURPLE, lw=1.2, marker="o", ms=3.0, zorder=3)
    fs.label(ax, cx, 0.470, "逐帧对、连续看抽搠", fs=6.8, color=fs.MUTED)

    # (d) 过饱和：高饱和色块 + 环
    cx = xs[3]
    ax.add_patch(Circle((cx, 0.640), 0.062, facecolor="#F97316", edgecolor="none",
                        alpha=0.95, zorder=3))
    for r, a in ((0.040, 0.55), (0.024, 0.40)):
        ax.add_patch(Circle((cx, 0.640), r, facecolor="white", edgecolor="none",
                            alpha=a, zorder=4))
    fs.label(ax, cx, 0.470, "颜色越出真实分布", fs=6.8, color=fs.MUTED)

    # (e) 语义漂移：条件说红裙，生成为灰衣
    cx = xs[4]
    fs.human(ax, cx=cx, cy=0.640, s=0.255, pose=dict(l_arm=0.2, r_arm=0.15),
             color="#9CA3AF", z=3)
    fs.box(ax, cx - 0.052, 0.762, 0.070, 0.040, "", fc="#FFFFFF", ec=fs.PINK, lw=0.8)
    fs.label(ax, cx - 0.017, 0.782, "红裙", fs=6.6, color=fs.PINK)
    fs.label(ax, cx, 0.470, "生成成灰衣", fs=6.8, color=fs.MUTED)

    for cx, t in zip(xs, causes):
        fs.label(ax, cx, 0.310, t, fs=6.9, color=fs.INK)

    fs.label(ax, 0.5, 0.975, "五类失败：单张定妆图里大多看不出来", fs=9.6, color=fs.INK,
             weight="bold")
    fs.label(ax, 0.5, 0.130, "检查办法：环视渲染、极端姿态、连续帧", fs=7.8, color=fs.MUTED)
    fs.label(ax, 0.5, 0.060, "前两类是几何问题，中间两类是优化与超参，最后一类是条件注入",
             fs=7.4, color=fs.MUTED)
    fs.save(fig, "ch04", "fig04-04")


if __name__ == "__main__":
    fig_failures()
