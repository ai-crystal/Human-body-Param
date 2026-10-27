# -*- coding: utf-8 -*-
"""第 2 章插图：向量、矩阵、最小二乘。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_vectors():
    fig, axs = plt.subplots(1, 3, figsize=(6.9, 2.5))
    for ax in axs:
        ax.set_xlim(-0.5, 3.6); ax.set_ylim(-0.5, 3.2)
        ax.set_aspect("equal"); fs.clean(ax, grid=True, spines=("left", "bottom"))
        ax.axhline(0, color=fs.MUTED, lw=0.8); ax.axvline(0, color=fs.MUTED, lw=0.8)
        ax.set_xticks([1, 2, 3]); ax.set_yticks([1, 2, 3])

    u = np.array([2.4, 1.0]); v = np.array([0.6, 2.2])
    ax = axs[0]
    ax.annotate("", xy=u, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=2))
    ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=2))
    fs.label(ax, u[0] + 0.1, u[1] - 0.15, r"$\mathbf{u}$", fs=12, color=fs.BLUE)
    fs.label(ax, v[0] + 0.12, v[1], r"$\mathbf{v}$", fs=12, color=fs.GREEN)
    ax.set_title("两个向量", fontsize=10)

    ax = axs[1]
    ax.set_xlim(-0.5, 5.2); ax.set_ylim(-0.5, 3.2)
    for k, c, a in [(1.5, fs.BLUE, 0.45), (2.0, fs.BLUE, 0.85)]:
        ax.annotate("", xy=k * u, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=2, alpha=a))
    fs.label(ax, 4.15, 1.65, r"$2\mathbf{u}$", fs=11, color=fs.BLUE)
    fs.label(ax, 2.85, 0.85, r"$1.5\mathbf{u}$", fs=10, color=fs.BLUE)
    ax.set_title("数乘：长度伸缩，方向不变", fontsize=9.5)

    ax = axs[2]
    s = u + v
    ax.annotate("", xy=u, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=1.6))
    ax.annotate("", xy=s, xytext=u, arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=1.6))
    ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=fs.GREEN,
                                                          lw=1.2, ls="--"))
    ax.annotate("", xy=s, xytext=v, arrowprops=dict(arrowstyle="-|>", color=fs.BLUE,
                                                    lw=1.2, ls="--"))
    ax.annotate("", xy=s, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=2.4))
    fs.label(ax, s[0] + 0.15, s[1] + 0.05, r"$\mathbf{u}+\mathbf{v}$", fs=11, color=fs.ACCENT)
    ax.set_title("加法：首尾相接", fontsize=10)

    fig.tight_layout()
    fs.save(fig, "ch02", "fig02-01")


def fig_matrix():
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 3.0))
    A = np.array([[1.5, 0.6], [0.3, 1.3]])
    for ax, M, title, c in [(axs[0], np.eye(2), "原坐标系", fs.MUTED),
                            (axs[1], A, "经过矩阵 A 之后", fs.ACCENT)]:
        ax.set_xlim(-0.4, 3.2); ax.set_ylim(-0.4, 3.2)
        ax.set_aspect("equal"); fs.clean(ax, spines=("left", "bottom"))
        ax.axhline(0, color=fs.MUTED, lw=0.7); ax.axvline(0, color=fs.MUTED, lw=0.7)
        for t in np.linspace(0, 2, 6):
            p0, p1 = np.array([t, 0]), np.array([t, 2])
            q0, q1 = M @ p0, M @ p1
            ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color="#D1D5DB", lw=0.6, zorder=1)
            p0, p1 = np.array([0, t]), np.array([2, t])
            q0, q1 = M @ p0, M @ p1
            ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color="#D1D5DB", lw=0.6, zorder=1)
        sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
        q = sq @ M.T
        ax.fill(q[:, 0], q[:, 1], color=c, alpha=0.16, zorder=2)
        ax.plot(q[:, 0], q[:, 1], color=c, lw=1.8, zorder=3)
        for i, lab in enumerate(["e1", "e2"]):
            e = M @ (np.eye(2)[i] * 1.8)
            ax.annotate("", xy=e, xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=fs.BLUE if i == 0 else fs.GREEN, lw=2))
            name = ("A" if title.startswith("经过") else "") + lab
            fs.label(ax, e[0] * 1.05, e[1] * 1.05 + 0.1, name, fs=9,
                     color=fs.BLUE if i == 0 else fs.GREEN)
        ax.set_title(title, fontsize=10)
    fig.tight_layout()
    fs.save(fig, "ch02", "fig02-02")


def fig_lsq():
    rng = np.random.default_rng(3)
    x = np.linspace(0, 5, 9)
    y = 1.2 + 0.75 * x + rng.normal(0, 0.45, size=x.size)
    A = np.stack([np.ones_like(x), x], 1)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = A @ coef

    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    fs.clean(ax, grid=True)
    for xi, yi, hi in zip(x, y, yhat):
        ax.plot([xi, xi], [yi, hi], color=fs.ACCENT, lw=1.0, alpha=0.85)
    ax.scatter(x, y, s=26, color=fs.BLUE, zorder=3, label="观测点")
    ax.plot(x, yhat, color=fs.ACCENT, lw=2, label="最小二乘直线")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.legend(loc="upper left")
    fs.label(ax, 3.4, 2.2, "残差 $y_i-\\hat{y}_i$", fs=9, color=fs.ACCENT, ha="left")
    ax.set_title("最小二乘：让红色竖线长度的平方和最小", fontsize=10)
    fs.save(fig, "ch02", "fig02-03")


if __name__ == "__main__":
    fig_vectors()
    fig_matrix()
    fig_lsq()
