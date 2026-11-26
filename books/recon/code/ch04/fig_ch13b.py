# -*- coding: utf-8 -*-
"""第 4 章补充插图：体渲染与光栅化的成本（图 4-3）。

左：体渲染沿射线逐点查询，1080p 一帧上亿次网络调用。
右：几种表示的单帧渲染耗时量级（示意，1080p）。
"""
import sys
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = r"E:\Study\人体参数化技术\人体参数化技术学习\books\recon\images"


def fig_cost():
    fig = plt.figure(figsize=(6.9, 3.1))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.26)

    # ---------------- 左：体渲染的采样 ----------------
    ax = fig.add_axes([0.015, 0.10, 0.44, 0.76])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fs.label(ax, 0.5, 0.975, "体渲染：沿射线逐点查询", fs=8.8)

    ax.add_patch(plt.Rectangle((0.04, 0.22), 0.10, 0.58, facecolor="#EEF2FF",
                               edgecolor=fs.BLUE, lw=0.9, zorder=1))
    fs.label(ax, 0.09, 0.15, "图像平面", fs=7.2, color=fs.BLUE)
    ax.add_patch(plt.Circle((0.015, 0.51), 0.012, facecolor=fs.INK, zorder=3))

    fs.human(ax, cx=0.62, cy=0.50, s=0.52, color="#D8DEE9", alpha=0.85, z=2, width=1.0)
    p0 = np.array([0.05, 0.51]); p1 = np.array([0.92, 0.46])
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=fs.ACCENT, lw=1.0, zorder=4)
    ts = np.linspace(0.30, 0.80, 11)
    pts = p0[None, :] + (p1 - p0)[None, :] * ts[:, None]
    ax.scatter(pts[:, 0], pts[:, 1], s=11, color=fs.ACCENT, zorder=5)
    fs.label(ax, 0.63, 0.30, "每条射线 64–128 个采样点，\n每个点一次网络前向", fs=7.2,
             color=fs.ACCENT)
    fs.label(ax, 0.50, 0.045,
             "1080p 约 200 万像素 × 96 次 ≈ 2 亿次调用", fs=7.6, color=fs.MUTED)

    # ---------------- 右：单帧耗时量级 ----------------
    ax2 = fig.add_axes([0.585, 0.28, 0.395, 0.52])
    names = ["网格 + LBS", "3DGS 光栅化", "神经渲染（体渲染）"]
    vals = [2, 8, 500]
    cols = [fs.GREEN, fs.ACCENT, fs.PURPLE]
    y = np.arange(len(names))[::-1]
    ax2.barh(y, vals, height=0.52, color=cols, alpha=0.85)
    ax2.set_yticks(y); ax2.set_yticklabels(names, fontsize=7.8)
    ax2.set_xscale("log")
    ax2.set_xlim(1, 2000)
    ax2.set_xlabel("单帧渲染耗时（毫秒，1080p，示意）", fontsize=7.8)
    for yy, v in zip(y, vals):
        ax2.text(v * 1.25, yy, "%d ms" % v, va="center", fontsize=7.6, color=fs.INK)
    ax2.tick_params(labelsize=7.2)
    for sp in ("top", "right"):
        ax2.spines[sp].set_visible(False)
    ax2.set_title("数量级差别：两个数量级", fontsize=8.8, pad=6)


    fig.text(0.5, 0.035, "注：耗时为量级示意，随分辨率、模型大小、硬件变化两个数量级",
             fontsize=7.2, color=fs.MUTED, ha="center")
    fs.save(fig, "ch04", "fig04-03")


if __name__ == "__main__":
    fig_cost()
