# -*- coding: utf-8 -*-
"""第 6 章插图：ASM 一轮迭代的三步（图 6-4）。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import figstyle as fs


def contour(cx, cy, rx, ry, n=40):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], axis=1)


def draw_face(ax, cx, cy, rx, ry, color, ls="-", lw=1.4, alpha=1.0, n=60):
    pts = contour(cx, cy, rx, ry, n)
    ax.plot(np.r_[pts[:, 0], pts[0, 0]], np.r_[pts[:, 1], pts[0, 1]],
            color=color, ls=ls, lw=lw, alpha=alpha)


def fig_asm():
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.9))

    # ---------- ① 初始化 ----------
    ax = axes[0]
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    draw_face(ax, 0.52, 0.50, 0.30, 0.36, "#D1D5DB", lw=2.6)       # 图像里的真实轮廓
    draw_face(ax, 0.46, 0.47, 0.23, 0.29, fs.BLUE, ls="--", lw=1.5)  # 均值形状（初始）
    fs.label(ax, 0.52, 0.90, "① 从均值形状出发", fs=9.2, color=fs.INK)
    fs.label(ax, 0.52, 0.05, "灰：图像轮廓　蓝：初始形状", fs=7.6, color=fs.MUTED)

    # ---------- ② 沿法线搜索 ----------
    ax = axes[1]
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    draw_face(ax, 0.52, 0.50, 0.30, 0.36, "#D1D5DB", lw=2.6)
    mean = contour(0.46, 0.47, 0.23, 0.29, 40)
    draw_face(ax, 0.46, 0.47, 0.23, 0.29, fs.BLUE, ls="--", lw=1.2)
    for i in range(0, 40, 5):
        p = mean[i]
        nrm = np.array([(p[0] - 0.46) / 0.23 ** 2, (p[1] - 0.47) / 0.29 ** 2])
        nrm /= np.linalg.norm(nrm)
        a, b = p - 0.05 * nrm, p + 0.075 * nrm
        ax.plot([a[0], b[0]], [a[1], b[1]], color=fs.FAINT, lw=0.9)
        ax.scatter([p[0]], [p[1]], s=12, color=fs.BLUE, zorder=5)
        q = p + 0.062 * nrm
        fs.arrow(ax, p, q, color=fs.ACCENT, lw=1.0, ms=6)
        ax.scatter([q[0]], [q[1]], s=12, color=fs.ACCENT, zorder=5)
    fs.label(ax, 0.52, 0.90, "② 沿法线找边缘", fs=9.2, color=fs.INK)
    fs.label(ax, 0.52, 0.05, "橙点 = 灰度剖面最像训练样本的位置", fs=7.6, color=fs.MUTED)

    # ---------- ③ 投影回形状空间 ----------
    ax = axes[2]
    ax.set_xlim(-2.05, 3.25); ax.set_ylim(-1.75, 2.05); ax.axis("off")
    ax.set_aspect("equal")

    ax.add_patch(Ellipse((0, 0), 3.0, 2.0, fill=False, ec=fs.GREEN, lw=1.4, ls="--"))
    ax.add_patch(Ellipse((0, 0), 1.55, 1.03, fill=False, ec="#D1D5DB", lw=0.8, ls=":"))
    ax.text(-1.42, 0.0, r"$\pm3\sigma$ 边界", fontsize=8.0, color=fs.GREEN,
            ha="center", va="bottom", bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    ax.axhline(0, color=fs.FAINT, lw=0.8)
    ax.text(3.18, 0.10, "$b_1$", fontsize=8.4, color=fs.MUTED, ha="right")

    cur = np.array([0.35, 0.18])
    sug = np.array([1.95, 1.15])
    t = 1.0 / np.sqrt((sug[0] / 1.5) ** 2 + (sug[1] / 1.0) ** 2)
    proj = sug * t

    ax.scatter(*cur, s=26, color=fs.BLUE, zorder=6)
    ax.text(cur[0] - 0.05, cur[1] - 0.20, r"当前 $\mathbf{b}$", fontsize=7.8, color=fs.BLUE,
            ha="center", va="top")
    ax.scatter(*sug, s=26, color=fs.ACCENT, zorder=6)
    ax.text(sug[0] + 0.05, sug[1] + 0.10, r"建议 $\mathbf{b}$（越界）", fontsize=7.8,
            color=fs.ACCENT, ha="left", va="bottom")
    fs.arrow(ax, cur, sug, color=fs.ACCENT, lw=1.0, ls=(0, (3, 2)))
    fs.arrow(ax, sug, proj, color=fs.GREEN, lw=1.2)
    ax.scatter(*proj, s=32, color=fs.GREEN, zorder=7)
    ax.text(proj[0] - 0.10, proj[1] + 0.10, "裁剪后", fontsize=7.8, color=fs.GREEN,
            ha="right", va="bottom")

    fs.label(ax, 0.05, 1.86, "③ 投影回形状空间", fs=9.2, color=fs.INK, ha="left")

    fig.tight_layout(pad=0.4, w_pad=0.6)
    fs.save(fig, "ch06", "fig06-04")


if __name__ == "__main__":
    fig_asm()
