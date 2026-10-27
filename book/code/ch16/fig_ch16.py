# -*- coding: utf-8 -*-
"""第 16 章插图：FLAME。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Arc, Polygon
import figstyle as fs

W = 6.7


def fig_anatomy():
    """FLAME 的计算流程：模板 + 三类偏移 + 蒙皮。"""
    fig, ax = fs.canvas(W, 3.05)

    chain = ["模板 $\\bar T$\n5023 顶点",
             "$+$ 形状偏移\n$B_S(\\beta)$",
             "$+$ 表情偏移\n$B_E(\\psi)$",
             "$+$ 姿态矫正\n$B_P(\\theta)$",
             "蒙皮 $W$\n线性混合",
             "输出 $M$\n$N\\times 3$"]
    cols = [fs.INK, fs.BLUE, fs.PURPLE, fs.GOLD, fs.TEAL, fs.ACCENT]
    xs = fs.flow(ax, chain, y=0.70, h=0.19, fs=8.0, x0=0.02, x1=0.98, colors=cols)
    w = xs[0][1] - xs[0][0]

    ins = [("$\\beta$\n身份 300 维", 1, fs.BLUE),
           ("$\\psi$\n表情 100 维", 2, fs.PURPLE),
           ("$\\theta$\n姿态 15 维", 3, fs.GOLD)]
    for text, idx, col in ins:
        x = xs[idx][0]
        fs.box(ax, x, 0.875, w, 0.110, text, fc="white", ec=col, fs=8.0, lw=1.0)
        fs.arrow(ax, (x + w / 2, 0.872), (x + w / 2, 0.800), color=col, lw=1.1, ms=8)

    # 右：关节与蒙皮
    fs.arrow(ax, (xs[4][0] + w / 2, 0.598), (xs[4][0] + w / 2, 0.480), color=fs.TEAL, lw=1.1, ms=8)
    fs.box(ax, 0.575, 0.290, 0.395, 0.180,
           "关节 $J(\\beta)$：颈 · 下颌 · 左眼 · 右眼\n每个关节一个 $3\\times3$ 旋转，\n权重 $W$ 决定每个顶点听谁的话",
           fc="#ECFDF5", ec=fs.TEAL, fs=7.6, lw=0.9)

    # 左：两条容易忽略的细节
    fs.label(ax, 0.02, 0.500, "两处容易忽略的细节", fs=8.4, color=fs.INK,
             ha="left", weight="bold")
    fs.label(ax, 0.02, 0.455,
             "① 眼球顶点权重全给自己的眼球关节，是刚体；\n"
             "   所以无论怎么笑，眼球形状都不变。\n"
             "② 脖子顶点权重在颈与身体之间平滑过渡。\n"
             "   SMPL-X 正是从这里把 FLAME “缝”到身体上。",
             fs=7.6, color=fs.MUTED, ha="left", va="top")

    fig.text(0.5, 0.055,
             "三个参数各自只影响自己那一项；三项相加之后才交给蒙皮",
             ha="center", fontsize=8.6, color=fs.INK)
    fs.save(fig, "ch16", "fig16-01")


def fig_joints():
    HH = 3.30
    fig, ax = fs.canvas(W, HH)

    # ---- 左：头部示意与四个关节 ----
    cx, cy = 0.175, 0.60
    rx = 0.070
    ry = rx * W / HH
    ax.add_patch(Ellipse((cx, cy), 2 * rx, 2 * ry, facecolor="#F1F5F9",
                         edgecolor=fs.INK, lw=1.2, zorder=2))
    ax.add_patch(Polygon([[cx - 0.030, cy - 0.070 * W / HH],
                          [cx + 0.030, cy - 0.070 * W / HH],
                          [cx + 0.034, cy - 0.150 * W / HH],
                          [cx - 0.034, cy - 0.150 * W / HH]],
                         closed=True, facecolor="#E8EDF3", edgecolor=fs.INK, lw=1.0, zorder=2))
    ax.plot([cx - 0.078, cx + 0.078], [cy - 0.150 * W / HH] * 2, color=fs.INK, lw=1.2, zorder=2)

    ey = cy + 0.018 * W / HH
    for dx in (-0.026, 0.026):
        ax.add_patch(Circle((cx + dx, ey), 0.014, facecolor="white", edgecolor=fs.PURPLE,
                            lw=1.0, zorder=4))
        ax.add_patch(Circle((cx + dx, ey), 0.005, facecolor=fs.PURPLE, edgecolor="none", zorder=5))

    jn = (cx, cy - 0.130 * W / HH)
    jj = (cx, cy - 0.040 * W / HH)
    for p, lab, col in ((jn, "1", fs.TEAL), (jj, "2", fs.GOLD)):
        ax.add_patch(Circle(p, 0.012, facecolor=col, edgecolor="white", lw=0.9, zorder=6))
        ax.text(p[0], p[1] - 0.001, lab, fontsize=7.0, color="white", ha="center",
                va="center", zorder=7, weight="bold")

    # 下颌旋转弧

    # 引线标注
    notes = [(jn, "颈关节（3 维）", "点头 / 转头 / 歪头", fs.TEAL, 0.030),
             (jj, "下颌关节（3 维）", "张嘴为主，兼左右磨动", fs.GOLD, 0.060),
             ((cx + 0.026, ey), "两个眼球关节（各 3 维）", "只转眼睛，不动眼皮", fs.PURPLE, 0.100)]
    for (px, py), t1, t2, col, dy in notes:
        ax.plot([px + 0.045, 0.240], [py, py + dy], color=col, lw=0.7, zorder=5)
        fs.label(ax, 0.245, py + dy, t1, fs=8.0, color=col, ha="left")
        fs.label(ax, 0.245, py + dy - 0.048, t2, fs=7.4, color=fs.MUTED, ha="left")

    # ---- 右：运动链 ----
    ax.plot([0.545, 0.545], [0.06, 0.96], color=fs.GRID, lw=0.9)
    fs.label(ax, 0.765, 0.945, "运动链：谁是谁的子节点", fs=9.4, color=fs.INK, weight="bold")
    fs.box(ax, 0.675, 0.780, 0.18, 0.100, "全局旋转（3）", fc="white", ec=fs.MUTED, fs=8.0)
    fs.box(ax, 0.675, 0.585, 0.18, 0.100, "颈（3）", fc="white", ec=fs.TEAL, fs=8.0)
    fs.arrow(ax, (0.765, 0.778), (0.765, 0.688), color=fs.FAINT, lw=1.0, ms=7)
    for x0, lab, col in ((0.556, "下颌（3）", fs.GOLD), (0.708, "左眼（3）", fs.PURPLE),
                         (0.860, "右眼（3）", fs.PURPLE)):
        fs.box(ax, x0, 0.390, 0.112, 0.100, lab, fc="white", ec=col, fs=7.6)
        fs.arrow(ax, (0.765, 0.583), (x0 + 0.056, 0.492), color=fs.FAINT, lw=0.9, ms=6)
    fs.label(ax, 0.765, 0.320, "$\\theta\\in\\mathbb{R}^{3K+3}$，$K=4$，故 15 维",
             fs=8.0, color=fs.MUTED)
    fs.label(ax, 0.765, 0.170,
             "颈是头与身体的唯一接口：\n颈一动手臂以上全跟着走，\n这正是 BFM 没有的能力",
             fs=8.2, color=fs.INK)
    fs.label(ax, 0.765, 0.038, "（括号内为该关节的自由度）", fs=7.4, color=fs.FAINT)
    fs.save(fig, "ch16", "fig16-02")


def fig_genealogy():
    fig, ax = fs.canvas(W, 3.30)

    fs.box(ax, 0.040, 0.360, 0.205, 0.215,
           "FLAME 2017\n线性基 + 4 关节\n5023 顶点固定拓扑",
           fc="#ECFDF5", ec=fs.GREEN, fs=7.8, lw=1.3)

    targets = [
        (0.335, 0.760, "SMPL-X 2019", "作为脸部模块接入全身\n（10475 顶点 / 54 关节）", fs.TEAL),
        (0.335, 0.520, "DECA 2021", "加 UV 位移图，\n让皱纹随表情变化", fs.PINK),
        (0.335, 0.280, "NPHM 2023", "换掉线性基：\nSDF + 神经变形场", fs.PURPLE),
        (0.645, 0.760, "SMIRK 2023", "扩大数据规模，\n直接回归网格", fs.TEAL),
        (0.645, 0.520, "EMOCA 2022", "加情绪一致性损失，\n重建表情更像人", fs.PINK),
        (0.645, 0.280, "MonoNPHM 2024", "同一表示改为\n单目视频重建", fs.PURPLE),
    ]
    for x, y, title, sub, col in targets:
        fs.box(ax, x, y - 0.082, 0.255, 0.175, title + "\n" + sub,
               fc="white", ec=col, fs=7.3, lw=0.95)
    for y in (0.760, 0.520, 0.280):
        fs.arrow(ax, (0.248, 0.468), (0.329, y), color=fs.FAINT, lw=1.0,
                 rad=-0.20 if y > 0.5 else 0.20)
    fs.arrow(ax, (0.592, 0.760), (0.640, 0.760), color=fs.FAINT, lw=1.0)
    fs.arrow(ax, (0.592, 0.520), (0.640, 0.520), color=fs.FAINT, lw=1.0)
    fs.arrow(ax, (0.592, 0.280), (0.640, 0.280), color=fs.FAINT, lw=1.0)

    fs.label(ax, 0.5, 0.085,
             "两条路线：一条保留 FLAME 的“参数 + 拓扑”，只把细节和训练信号做得更足；另一条连表示本身也换掉",
             fs=8.3, color=fs.MUTED)
    fs.save(fig, "ch16", "fig16-03")


if __name__ == "__main__":
    fig_anatomy()
    fig_joints()
    fig_genealogy()
