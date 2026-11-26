# -*- coding: utf-8 -*-
"""第 1 章补充插图：三点最小二乘（图 1-4）与线性组合生成形状（图 1-5）。"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

MATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fs.FIGDIR = os.path.join(MATH, "images")


def fig_lsq3():
    """图 1-4：三点拟合直线，标出每条残差的大小。"""
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.0, 4.0])
    A = np.column_stack([np.ones_like(x), x])
    (a, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    yh = a + b * x
    print(f"a={a:.4f} b={b:.4f} RSS={np.sum((y - yh) ** 2):.4f}")

    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    fs.clean(ax, grid=True)

    xs = np.linspace(-0.25, 2.25, 50)
    ax.plot(xs, a + b * xs, color=fs.ACCENT, lw=2, zorder=2,
            label=f"最小二乘直线 $y={a:.3f}+{b:.2f}x$")

    for xi, yi, hi in zip(x, y, yh):
        ax.plot([xi, xi], [yi, hi], color=fs.ACCENT, lw=1.0, ls="--", alpha=0.8, zorder=1)

    ax.scatter(x, y, s=46, color=fs.BLUE, zorder=4, label="观测点")
    ax.scatter(x, yh, s=30, marker="x", color=fs.ACCENT, zorder=5, label="拟合值")

    # 残差标注
    off = {0: (0.46, -0.44), 1: (0.22, -0.50), 2: (0.02, -0.80)}
    for i, (xi, yi, hi) in enumerate(zip(x, y, yh)):
        dx, dy = off[i]
        ax.annotate(f"$r_{i + 1}={yi - hi:+.3f}$", xy=(xi, (yi + hi) / 2),
                    xytext=(xi + dx, (yi + hi) / 2 + dy), fontsize=9, color=fs.ACCENT,
                    arrowprops=dict(arrowstyle="-", color=fs.FAINT, lw=0.7,
                                    shrinkA=2, shrinkB=2))

    ax.text(0.03, 0.96, "残差平方和\n$0.0278+0.1111+0.0278=0.1667$",
            transform=ax.transAxes, ha="left", va="top", fontsize=9, color=fs.INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=fs.GRID, lw=0.8))

    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_xlim(-0.42, 2.30)
    ax.set_ylim(0.4, 4.45)
    ax.legend(loc="lower right", fontsize=8.5, ncol=1)
    ax.set_title("三个点、一条直线：无解，但可以最小化平方和", fontsize=10.5)
    fs.save(fig, "ch01", "fig01-04")


def fig_blend():
    """图 1-5：平均形状 + β × 一个方向。左：方向；右：三个系数下的结果。"""
    S0 = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 1.0]])
    d = np.array([[-0.1, 0.0], [0.1, 0.0], [0.0, 0.15]])
    K = 2.5  # 箭头视觉放大倍数

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.3))
    for ax in axs:
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.34, 1.34)
        ax.set_ylim(-0.30, 1.50)

    # 左：均值 + 方向箭头
    ax = axs[0]
    tri0 = np.vstack([S0, S0[:1]])
    ax.plot(tri0[:, 0], tri0[:, 1], color=fs.INK, lw=1.8, alpha=0.65)
    ax.scatter(S0[:, 0], S0[:, 1], s=40, color=fs.INK, zorder=5)
    for i in range(3):
        tip = S0[i] + K * d[i]
        fs.arrow(ax, tuple(S0[i]), tuple(tip), color=fs.ACCENT, lw=1.6)
    pos = [(-0.10, -0.14), (1.10, -0.14), (0.50, 1.10)]
    for i, (px, py) in enumerate(pos):
        fs.label(ax, px, py, f"顶点 {i + 1}", fs=8.6, color=fs.MUTED)
    fs.label(ax, 0.50, -0.24, "橙色箭头＝方向 d（放大 2.5 倍）", fs=8.8, color=fs.ACCENT)
    ax.set_title("平均形状与一个形变方向", fontsize=10)

    # 右：三个 β 的结果
    ax = axs[1]
    for beta, c, lab in [(-1.0, fs.BLUE, "β = −1"), (0.0, fs.INK, "β = 0"),
                         (1.0, fs.ACCENT, "β = +1")]:
        S = S0 + beta * d
        tri = np.vstack([S, S[:1]])
        ax.plot(tri[:, 0], tri[:, 1], color=c, lw=1.9, alpha=0.92, label=lab)
        ax.scatter(S[:, 0], S[:, 1], s=24, color=c, zorder=5)
    ax.legend(loc="upper right", fontsize=8.8, bbox_to_anchor=(1.02, 1.02))
    ax.set_title("同一个方向、三个系数", fontsize=10)

    fs.save(fig, "ch01", "fig01-05")


if __name__ == "__main__":
    fig_lsq3()
    fig_blend()
