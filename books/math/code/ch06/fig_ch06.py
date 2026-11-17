# -*- coding: utf-8 -*-
"""第 6 章插图：对应、ASM 形状空间、3DMM 流程。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import figstyle as fs


def face_outline(cx=0.5, cy=0.5, w=0.26, h=0.34, jaw=1.0, n=18, rot=0.0):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # 上圆下尖的轮廓
    x = np.cos(t) * w
    y = np.sin(t) * h
    y = np.where(y < 0, y * jaw, y)
    x = x * (1 + 0.06 * np.sin(3 * t))
    R = np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
    P = np.stack([x, y], 1) @ R.T
    return P + np.array([cx, cy])


def fig_correspondence():
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.8))
    for ax in axs:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_aspect("equal")
    A = face_outline(0.5, 0.5, 0.24, 0.32, 1.0)
    B = face_outline(0.5, 0.5, 0.20, 0.30, 1.25, rot=0.05)
    for ax, P, title in [(axs[0], A, "扫描 A"), (axs[1], B, "扫描 B")]:
        ax.add_patch(Polygon(P, closed=True, fill=True, fc="#FDF6EC", ec=fs.ACCENT, lw=1.2))
        ax.scatter(P[:, 0], P[:, 1], s=18, color=fs.BLUE, zorder=5)
        for i in [0, 4, 9, 13]:
            ax.text(P[i, 0] + 0.02, P[i, 1] + 0.02, str(i), fontsize=7, color=fs.MUTED)
        ax.set_title(title, fontsize=9.5)
    # 对应连线
    for i in range(len(A)):
        axs[1].plot([A[i, 0] - 0.5 + 0.5, B[i, 0]], [A[i, 1], B[i, 1]],
                    color="#D1D5DB", lw=0.4, ls=":")
    fig.tight_layout()
    fs.save(fig, "ch06", "fig06-01")


def fig_shape_space():
    fig, ax = fs.canvas(6.9, 2.7)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    labels = ["$-2\\sigma$", "$-1\\sigma$", "均值", "$+1\\sigma$", "$+2\\sigma$"]
    for i, (lab, w, jaw) in enumerate(zip(labels, [0.070, 0.078, 0.086, 0.094, 0.102],
                                          [1.35, 1.18, 1.0, 0.86, 0.74])):
        cx = 0.13 + i * 0.185
        P = face_outline(cx, 0.52, w, 0.17, jaw)
        ax.add_patch(Circle((cx - w * 0.42, 0.60), 0.008, color=fs.INK, zorder=6))
        ax.add_patch(Circle((cx + w * 0.42, 0.60), 0.008, color=fs.INK, zorder=6))
        ax.plot([cx - w * 0.3, cx + w * 0.3], [0.445, 0.445], color=fs.INK, lw=1.0)
        ax.add_patch(Polygon(P, closed=True, fill=True,
                             fc=fs.ACCENT if i == 2 else "#E8D5C4",
                             ec=fs.ACCENT if i == 2 else "#C9A98F", lw=1.0))
        ax.scatter(P[:, 0], P[:, 1], s=3, color="white", zorder=5, alpha=0.9)
        fs.label(ax, cx, 0.13, lab, fs=9, color=fs.MUTED)
    fs.label(ax, 0.5, 0.92, "第一主成分：脸型宽窄与下巴尖圆", fs=9.6)
    fs.label(ax, 0.5, 0.04, "每个主成分都是所有关键点的一次协同位移", fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch06", "fig06-02")


def fig_pipeline():
    fig, ax = fs.canvas(6.9, 2.4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    labs = ["三维扫描\n(点云/网格)", "对应\n(配准到模板)", "展平成向量\n$N\\times3$", "PCA\n得到基 $\\mathbf{B}$", "新形状\n$\\mu+\\mathbf{B}\\beta$"]
    cols = [fs.BLUE, fs.GREEN, fs.MUTED, fs.ACCENT, fs.PURPLE]
    fs.flow(ax, labs, y=0.52, h=0.30, fs=8.2, colors=cols)
    fs.label(ax, 0.5, 0.12, "关键：所有扫描必须顶点一一对应，否则“相减”没有意义", fs=8.4, color=fs.MUTED)
    fs.save(fig, "ch06", "fig06-03")


if __name__ == "__main__":
    fig_correspondence()
    fig_shape_space()
    fig_pipeline()
