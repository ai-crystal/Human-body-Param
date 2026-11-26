# -*- coding: utf-8 -*-
"""第 3 章（人体册）插图：SMPL 家族的规模与解耦

fig03-04  各代模型的顶点数与关节数（对数刻度），以及“顶点×关节”的成本
fig03-05  骨架与形状耦合（SMPL 系）vs 解耦（ATLAS / MHR）
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = os.path.join(BOOK, "images")

MODELS = [
    # 名称, 顶点, 关节, 颜色
    ("MANO", 778, 16, fs.MUTED),
    ("SMPL", 6890, 24, fs.BLUE),
    ("SMPL+H", 8446, 54, fs.TEAL),
    ("SMPL-X", 10475, 54, fs.GREEN),
    ("STAR", 6890, 24, fs.PURPLE),
    ("MHR（最高 LOD）", 73639, 127, fs.GOLD),
    ("ATLAS", 115000, 77, fs.ACCENT),
]


def fig_scale():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.2))
    names = [m[0] for m in MODELS]
    y = np.arange(len(MODELS))[::-1]

    ax = axes[0]
    vals = [m[1] for m in MODELS]
    ax.barh(y, vals, color=[m[3] for m in MODELS], height=0.6, alpha=0.85)
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8.6)
    for yy, v in zip(y, vals):
        ax.text(v * 1.08, yy, f"{v:,}", va="center", fontsize=8, color=fs.INK)
    ax.set_xlim(4e2, 4e5)
    ax.set_xlabel("网格顶点数（对数刻度）", fontsize=9)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    ax.set_title("① 网格规模差了两个数量级", fontsize=9.8, pad=5)

    ax = axes[1]
    vals = [m[2] for m in MODELS]
    ax.barh(y, vals, color=[m[3] for m in MODELS], height=0.6, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels([])
    for yy, v in zip(y, vals):
        ax.text(v + 2, yy, f"{v}", va="center", fontsize=8, color=fs.INK)
    ax.set_xlim(0, 150)
    ax.set_xlabel("关节数", fontsize=9)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    ax.set_title("② 关节数的增长更平缓", fontsize=9.8, pad=5)
    fig.tight_layout(pad=0.4, w_pad=1.2)
    fs.save(fig, "ch03", "fig03-04")


def fig_decouple():
    fig, ax = fs.canvas(7.4, 3.9)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    fs.label(ax, 0.25, 0.955, "① 耦合：形状一动，骨架跟着动", fs=9.8, color=fs.ACCENT, weight="bold")
    fs.box(ax, 0.03, 0.79, 0.16, 0.11, "肩宽参数\n（β 里的某一维）", fc="#FEF2F2", ec=fs.ACCENT, fs=7.8)
    fs.box(ax, 0.235, 0.79, 0.15, 0.11, "顶点位移\n（表面变窄）", fc="white", ec=fs.ACCENT, fs=7.8)
    fs.box(ax, 0.41, 0.79, 0.16, 0.11, "关节回归 J\n（顶点加权）", fc="white", ec=fs.ACCENT, fs=7.8)
    fs.box(ax, 0.60, 0.79, 0.15, 0.11, "肩关节\n跟着内移", fc="#FEF2F2", ec=fs.ACCENT, fs=7.8)
    for x0, x1 in ((0.19, 0.235), (0.385, 0.41), (0.57, 0.60)):
        fs.arrow(ax, (x0, 0.845), (x1, 0.845), color=fs.ACCENT, lw=1.0)
    fs.box(ax, 0.16, 0.575, 0.50, 0.13,
           "调窄肩，上臂起点、胸廓、体重都会跟着变\n所以“只改肩宽”这件事做不到",
           fc="#FFF1F2", ec=fs.ACCENT, fs=7.4)
    fs.arrow(ax, (0.675, 0.785), (0.60, 0.705), color=fs.PINK, lw=1.0, rad=0.2)

    fs.label(ax, 0.25, 0.50, "② 解耦：表面和骨架各有一套参数", fs=9.8, color=fs.TEAL, weight="bold")
    fs.box(ax, 0.03, 0.33, 0.19, 0.11, "表面参数\n$\\beta_s,\\beta_f$", fc="#ECFEFF", ec=fs.TEAL, fs=7.8)
    fs.box(ax, 0.27, 0.33, 0.17, 0.11, "表面形变基\n（只改肉）", fc="white", ec=fs.TEAL, fs=7.8)
    fs.box(ax, 0.49, 0.33, 0.16, 0.11, "网格顶点", fc="white", ec=fs.TEAL, fs=7.8)
    fs.box(ax, 0.03, 0.15, 0.19, 0.11, "骨架参数\n$\\beta_k$", fc="#F0FDF4", ec=fs.GREEN, fs=7.8)
    fs.box(ax, 0.27, 0.15, 0.17, 0.11, "骨架基\n（只改骨长/位置）", fc="white", ec=fs.GREEN, fs=7.8)
    fs.box(ax, 0.49, 0.15, 0.16, 0.11, "关节位置", fc="white", ec=fs.GREEN, fs=7.8)
    for x0, x1 in ((0.22, 0.27), (0.44, 0.49)):
        fs.arrow(ax, (x0, 0.385), (x1, 0.385), color=fs.TEAL, lw=1.0)
        fs.arrow(ax, (x0, 0.205), (x1, 0.205), color=fs.GREEN, lw=1.0)
    fs.box(ax, 0.69, 0.20, 0.28, 0.19,
           "两条路互不干扰\n改肩宽只动骨架\n改体重只动表面",
           fc="#F0FDFA", ec=fs.TEAL, fs=7.6)
    fs.label(ax, 0.83, 0.135, "代价：参数、网格分辨率、\n部署成本都上去", fs=7.3, color=fs.MUTED)
    fs.arrow(ax, (0.665, 0.385), (0.69, 0.34), color=fs.FAINT, lw=1.0)
    fs.arrow(ax, (0.665, 0.205), (0.69, 0.24), color=fs.FAINT, lw=1.0)
    fs.save(fig, "ch03", "fig03-05")


if __name__ == "__main__":
    fig_scale()
    fig_decouple()
