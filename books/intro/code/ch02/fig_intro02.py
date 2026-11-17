# -*- coding: utf-8 -*-
"""入门册第 2 章插图：参数空间的直觉（平均人 + 主成分滑块）。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))               # books/<册>
sys.path.insert(0, os.path.join(os.path.dirname(BOOK), "code"))      # books/code（共用 figstyle）
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figstyle as fs

FIGDIR = os.path.join(BOOK, "images")


def ellipse_cloud(n=60, seed=7):
    """二维点云：沿 p1 方向拉长，沿 p2 方向很薄。"""
    rng = np.random.default_rng(seed)
    t = rng.normal(0, 1, n)
    s = rng.normal(0, 0.28, n)
    th = np.deg2rad(28)
    p1 = np.array([np.cos(th), np.sin(th)])
    p2 = np.array([-np.sin(th), np.cos(th)])
    pts = np.outer(t, p1) + np.outer(s, p2)
    return pts, p1, p2


def fig_space():
    """图 2-1：高维点云其实躺在一张薄片上。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.1))
    pts, p1, p2 = ellipse_cloud()

    ax = axes[0]
    fs.clean(ax, grid=True)
    ax.scatter(pts[:, 0], pts[:, 1], s=9, color=fs.BLUE, alpha=0.55, lw=0)
    ax.set_title("① 一堆拉长的点云", fontsize=9.4, pad=4)
    ax.set_xlabel("$x_1$", fontsize=9)
    ax.set_ylabel("$x_2$", fontsize=9)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7.8)

    ax = axes[1]
    fs.clean(ax, grid=True)
    ax.scatter(pts[:, 0], pts[:, 1], s=9, color="#C9D3DF", alpha=0.85, lw=0)
    lo, hi = -2.2, 2.2
    for k in (lo, hi):
        ax.plot([k * p1[0]], [k * p1[1]], marker="", color=fs.ACCENT, lw=0)
    ax.plot([lo * p1[0], hi * p1[0]], [lo * p1[1], hi * p1[1]],
            color=fs.ACCENT, lw=1.1, ls="--", alpha=0.8)
    ax.annotate("", xy=1.55 * p1, xytext=np.zeros(2),
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.8))
    ax.annotate("", xy=0.55 * p2, xytext=np.zeros(2),
                arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=1.5))
    ax.text(1.62 * p1[0] + 0.02, 1.62 * p1[1] + 0.13, "$\\mathbf{p}_1$",
            color=fs.ACCENT, fontsize=9.6, ha="center")
    ax.text(0.62 * p2[0] + 0.09, 0.62 * p2[1], "$\\mathbf{p}_2$",
            color=fs.GREEN, fontsize=9.6, ha="left", va="center")
    ax.set_title("② 换到 $\\mathbf{p}_1,\\mathbf{p}_2$ 看：几乎只剩一个方向",
                 fontsize=9.4, pad=4)
    ax.set_xlabel("$x_1$", fontsize=9)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7.8)

    fig.tight_layout(pad=0.5, w_pad=1.2)
    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch02", "fig02-01")


def fig_sliders():
    """图 2-2：平均人 + 三个滑块 = 一个人。"""
    fig = plt.figure(figsize=(6.9, 2.9))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0.03, 0.14), 0.17, 0.60,
                                boxstyle="round,pad=0.008,rounding_size=0.02",
                                ec=fs.INK, fc="#F6F4EF", lw=1.0))
    ax.text(0.115, 0.66, "平均人", ha="center", fontsize=9.2, color=fs.INK)
    ax.text(0.115, 0.57, "$\\bar{\\mathbf{T}}$", ha="center", fontsize=11.5, color=fs.INK)
    ax.text(0.115, 0.36, "20670 个数", ha="center", fontsize=7.6, color=fs.MUTED)
    ax.text(0.115, 0.24, "固定不动", ha="center", fontsize=7.2, color=fs.FAINT)

    rows = [("$\\beta_1$", "高矮 / 胖瘦", 0.66, fs.ACCENT, 0.40),
            ("$\\beta_2$", "肩宽", 0.44, fs.BLUE, 0.335),
            ("$\\beta_3$", "腿身比", 0.22, fs.GREEN, 0.455)]
    for sym, name, y, c, pos in rows:
        ax.text(0.245, y, sym, fontsize=10.2, color=c, ha="left", va="center")
        ax.text(0.295, y, name, fontsize=8.0, color=fs.MUTED, ha="left", va="center")
        ax.plot([0.245, 0.505], [y - 0.075, y - 0.075], color="#D1D5DB", lw=3.0,
                solid_capstyle="round", zorder=1)
        ax.plot([0.245, pos], [y - 0.075, y - 0.075], color=c, lw=3.0,
                solid_capstyle="round", zorder=2)
        ax.plot([pos], [y - 0.075], marker="o", ms=7.0, color="white", mec=c,
                mew=1.8, zorder=3)

    ax.text(0.555, 0.44, "=", fontsize=17, color=fs.INK, ha="center", va="center")

    ax.add_patch(FancyBboxPatch((0.605, 0.14), 0.22, 0.60,
                                boxstyle="round,pad=0.008,rounding_size=0.02",
                                ec=fs.ACCENT, fc="#FDF6EE", lw=1.2))
    ax.text(0.715, 0.66, "具体的人", ha="center", fontsize=9.2, color=fs.ACCENT)
    ax.text(0.715, 0.53, "$\\bar{\\mathbf{T}}+\\sum_n \\beta_n \\mathbf{S}_n$",
            ha="center", fontsize=9.8, color=fs.INK)
    ax.text(0.715, 0.36, "体型由 10 个数决定", ha="center", fontsize=7.6, color=fs.MUTED)
    ax.text(0.715, 0.24, "再给 72 个姿态数\n就摆出任意姿势", ha="center",
            fontsize=7.2, color=fs.FAINT, va="center")

    ax.text(0.03, 0.95, "一个平均形状，加上少数几个方向上的刻度",
            fontsize=9.4, color=fs.INK, va="top")
    ax.text(0.03, 0.865, "刻度就是参数，也就是界面上能拖动的那几根滑块",
            fontsize=8.2, color=fs.MUTED, va="top")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch02", "fig02-02")


if __name__ == "__main__":
    fig_space()
    fig_sliders()
