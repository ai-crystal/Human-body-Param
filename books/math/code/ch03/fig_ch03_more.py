# -*- coding: utf-8 -*-
"""第 3 章补充插图：四道坐标变换（图 3-3）与两种旋转插值（图 3-2）。"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

MATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fs.FIGDIR = os.path.join(MATH, "images")


def fig_slerp():
    """图 3-2：SLERP 与“线性插值再归一化”的差别。"""
    th = np.deg2rad(120.0)
    u0 = np.array([1.0, 0.0])
    u1 = np.array([np.cos(th), np.sin(th)])
    ts = np.linspace(0, 1, 9)

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.2), gridspec_kw=dict(width_ratios=[1, 1.15], wspace=0.28))

    # 左：单位圆上的两条路径
    ax = axs[0]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.08, 1.22)
    ax.set_ylim(-1.16, 1.22)
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, ec=fs.GRID, lw=1.0))
    sl = np.array([np.cos(ts * th), np.sin(ts * th)]).T
    nl = (1 - ts)[:, None] * u0 + ts[:, None] * u1
    nl = nl / np.linalg.norm(nl, axis=1, keepdims=True)

    ax.plot(sl[:, 0], sl[:, 1], color=fs.GREEN, lw=1.6, alpha=0.9, label="SLERP：走圆弧")
    ax.plot(nl[:, 0], nl[:, 1], color=fs.BLUE, lw=1.2, ls="--", alpha=0.9,
            label="线性插值：走弦")
    ax.scatter(sl[:, 0], sl[:, 1], s=26, color=fs.GREEN, zorder=5, label="等间隔采样")
    ax.scatter(nl[:, 0], nl[:, 1], s=24, color=fs.BLUE, marker="s", zorder=5)
    fs.label(ax, 0.84, -0.24, "$q_0$", fs=11, color=fs.INK)
    fs.label(ax, -0.56, 0.94, "$q_1$", fs=11, color=fs.INK)
    ax.legend(loc="lower center", fontsize=8.2, handlelength=1.6, ncol=1,
              borderaxespad=0.2)
    ax.set_title("两种插值走的路", fontsize=10)

    # 右：转角随 t 的变化
    ax = axs[1]
    fs.clean(ax, grid=True)
    ang_sl = ts * th
    ang_nl = np.arctan2(nl[:, 1], nl[:, 0])
    ax.plot(ts, np.rad2deg(ang_sl), color=fs.GREEN, lw=2, label="SLERP：匀速")
    ax.plot(ts, np.rad2deg(ang_nl), color=fs.BLUE, lw=1.8, ls="--", label="线性插值：先快后慢")
    ax.set_xlabel("插值参数 $t$")
    ax.set_ylabel("转角（度）")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 130)
    ax.legend(loc="lower right", fontsize=8.5)
    ax.set_title("转角是否匀速", fontsize=10)

    fs.save(fig, "ch03", "fig03-02")


def fig_pipeline():
    """图 3-3：局部 → 世界 → 相机 → 像素。"""
    fig, ax = fs.canvas(7.0, 3.1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = [0.008, 0.263, 0.518, 0.773]
    w = 0.196
    heads = ("关节局部坐标", "世界坐标", "相机坐标", "像素坐标")
    vals = ("(0.5, 0, 0)", "(−1, 0.5, 0)", "(0.1, −0.2, 3.0)", "(346.7, 186.7)")
    cols = [fs.PURPLE, fs.BLUE, fs.GREEN, fs.ACCENT]
    for i, x in enumerate(xs):
        fs.box(ax, x, 0.56, w, 0.18, heads[i], fc="white", ec=cols[i], fs=9, lw=1.3)
        fs.box(ax, x, 0.22, w, 0.15, vals[i], fc=fs.LIGHT, ec=fs.GRID, fs=8.4)

    for i in range(3):
        x0 = xs[i] + w + 0.004
        x1 = xs[i + 1] - 0.004
        fs.arrow(ax, (x0, 0.65), (x1, 0.65), color=fs.MUTED, lw=1.3, ms=7)
        fs.arrow(ax, (x0, 0.295), (x1, 0.295), color=fs.FAINT, lw=1.0, ls=":", ms=6)

    ops = [r"乘 $\mathbf{L}_k$", r"乘 $[\mathbf{R}|\mathbf{t}]$", r"乘 $\mathbf{K}$，除 $Z$"]
    for i, op in enumerate(ops):
        xm = (xs[i] + w + xs[i + 1]) / 2
        fs.label(ax, xm, 0.83, op, fs=8.2, color=fs.INK)

    fs.label(ax, 0.008, 0.94, "每一步都是一个矩阵乘法", fs=9, color=fs.MUTED, ha="left")
    fs.label(ax, 0.008, 0.45, "同一个点在各坐标系里的值", fs=9, color=fs.MUTED, ha="left")
    fs.label(ax, 0.5, 0.07, "只有最后一步要除以深度 $Z$", fs=9, color=fs.ACCENT)
    fs.save(fig, "ch03", "fig03-03")


if __name__ == "__main__":
    fig_slerp()
    fig_pipeline()
