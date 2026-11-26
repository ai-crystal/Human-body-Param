# -*- coding: utf-8 -*-
"""第 5 章补充插图：三级骨架链的数值例子（图 5-7）。"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

MATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fs.FIGDIR = os.path.join(MATH, "images")


def rot2(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s], [s, c]])


def chain(ts, te):
    """骨盆(0,0) → 肩(0,0.30) → 肘 → 腕。ts 是肩的转角，te 是肘的转角。"""
    pelvis = np.zeros(2)
    Rs = rot2(ts)
    shoulder = pelvis + np.array([0.0, 0.30])
    elbow = shoulder + Rs @ np.array([0.28, 0.0])
    wrist = elbow + Rs @ rot2(te) @ np.array([0.26, 0.0])
    return np.array([pelvis, shoulder, elbow, wrist])


def draw(ax, P, color, lw, ls="-", alpha=1.0, z=3):
    for i in range(3):
        ax.plot([P[i, 0], P[i + 1, 0]], [P[i, 1], P[i + 1, 1]], color=color, lw=lw,
                ls=ls, alpha=alpha, solid_capstyle="round", zorder=z)
    ax.scatter(P[:, 0], P[:, 1], s=34, color=color, alpha=alpha, zorder=z + 1,
               edgecolor="white", linewidth=0.8)


def fig_fk():
    cases = [(0.0, 0.0, fs.MUTED, "静止姿势", "(0.84, 0.30)"),
             (np.pi / 2, 0.0, fs.ACCENT, "肩转 90°，肘不转", "(0, 0.84)"),
             (np.pi / 2, -np.pi / 2, fs.GREEN, "肩转 90°，肘转 −90°", "(0.26, 0.58)")]
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.9))
    names = ["骨盆", "肩", "肘", "腕"]
    for ax, (ts, te, c, title, wr) in zip(axs, cases):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.16, 1.00)
        ax.set_ylim(-0.16, 1.00)
        P = chain(ts, te)
        draw(ax, P, c, 3.2, z=3)
        for i, (x, y) in enumerate(P):
            if i == 3:
                dx, dy, ha = 0.06, -0.05, "left"
            else:
                dx, dy, ha = -0.06, (-0.09 if i == 2 else -0.02), "right"
            fs.label(ax, x + dx, y + dy, names[i], fs=8.4, color=fs.INK, ha=ha)
        fs.label(ax, 0.62, 0.02, "腕 " + wr, fs=8.2, color=c)
        ax.set_title(title, fontsize=9)

    fig.suptitle("同一棵树、三组局部旋转：差异只出现在关节下游", fontsize=10, y=1.02)
    fs.save(fig, "ch05", "fig05-02")


if __name__ == "__main__":
    fig_fk()
