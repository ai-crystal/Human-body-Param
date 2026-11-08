# -*- coding: utf-8 -*-
"""第 5 章：绕关节旋转 = 旋转 + 平移（图 5-5）。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import figstyle as fs


def rot90(p):
    return np.array([-p[1], p[0]])


def fig_rot_trans():
    C = np.array([0.55, 0.30])      # 关节（肘）在静止姿势下的位置
    P = np.array([0.91, 0.37])      # 顶点
    Q = C + rot90(P - C)            # 绕关节转 90°
    R = rot90(P)                    # 只绕世界原点转 90°
    T = Q - R                       # 差额就是平移项 (I-R)c

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.1))
    for ax in axes:
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(-0.80, 1.18); ax.set_ylim(-0.28, 1.20)
        ax.plot([-0.65, 1.10], [0, 0], color="#E7E9EC", lw=0.8, zorder=0)
        ax.plot([0, 0], [-0.20, 1.12], color="#E7E9EC", lw=0.8, zorder=0)

    box = dict(facecolor="white", edgecolor="none", pad=1.2)

    # ---------- 左：绕关节旋转 ----------
    ax = axes[0]
    ax.set_title("① 绕关节 c 转 90°", fontsize=9.2, pad=6, color=fs.INK)
    ax.scatter(*C, s=28, color=fs.BLUE, zorder=6)
    ax.text(C[0] + 0.04, C[1] - 0.13, "关节 c", fontsize=8.2, color=fs.BLUE, va="top")
    ax.plot([C[0], P[0]], [C[1], P[1]], color=fs.FAINT, lw=1.0, ls=":", zorder=2)
    ax.plot([C[0], Q[0]], [C[1], Q[1]], color=fs.FAINT, lw=1.0, ls=":", zorder=2)
    r = np.linalg.norm(P - C)
    ax.add_patch(Arc(C, 2 * r, 2 * r, theta1=0, theta2=90, color=fs.ACCENT, lw=1.3, zorder=3))
    ax.scatter(*P, s=26, color=fs.INK, zorder=6)
    ax.text(P[0] + 0.05, P[1] - 0.02, "p", fontsize=10, va="top")
    ax.scatter(*Q, s=26, color=fs.ACCENT, zorder=6)
    ax.text(Q[0] - 0.14, Q[1] + 0.02, "p′", fontsize=10, color=fs.ACCENT, ha="right", va="bottom")
    ax.text(0.22, -0.26, "在关节自己看来，顶点只是转了一下", fontsize=7.6, color=fs.MUTED)

    # ---------- 右：拆成“绕原点转 + 平移” ----------
    ax = axes[1]
    ax.set_title("② 同一变换 = 绕原点转 + 平移", fontsize=9.2, pad=6, color=fs.INK)
    ax.scatter([0], [0], s=22, color=fs.MUTED, zorder=6)
    ax.text(-0.05, -0.03, "O", fontsize=8.6, color=fs.MUTED, ha="right", va="top")
    ax.scatter(*P, s=26, color=fs.INK, zorder=6)
    ax.text(P[0] + 0.04, P[1] - 0.03, "p", fontsize=10, va="top")
    ax.scatter(*R, s=26, color=fs.BLUE, zorder=6)
    ax.text(R[0] - 0.04, R[1] - 0.06, "先绕原点转 90°", fontsize=7.8, color=fs.BLUE,
            ha="right", va="top", bbox=box)
    # 从 p 到 R 的弧（示意旋转路径）
    fs.arrow(ax, P, R, color="#B6BBC2", lw=0.9, ls=(0, (2, 2)), rad=-0.35, ms=7)
    # 平移箭头
    fs.arrow(ax, R, Q, color=fs.ACCENT, lw=1.7, ms=9)
    ax.scatter(*Q, s=26, color=fs.ACCENT, zorder=6)
    ax.text(Q[0] + 0.05, Q[1] - 0.03, "p′", fontsize=10, color=fs.ACCENT, va="top")
    mid = (R + Q) / 2
    ax.text(mid[0] - 0.02, mid[1] + 0.16, "平移  t = (I − R)c", fontsize=7.8,
            color=fs.ACCENT, ha="center", va="bottom", bbox=box)
    ax.text(0.22, -0.26, "以世界原点为参照，平移项就露出来了", fontsize=7.6, color=fs.MUTED)

    fig.tight_layout(pad=0.4, w_pad=0.8)
    fs.save(fig, "ch05", "fig05-05")


if __name__ == "__main__":
    fig_rot_trans()
