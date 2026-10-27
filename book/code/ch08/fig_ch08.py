# -*- coding: utf-8 -*-
"""第 8 章插图：SMPL 的组成与参数。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_pipeline():
    fig, ax = fs.canvas(6.9, 3.4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    # 顶部输入
    fs.box(ax, 0.02, 0.72, 0.20, 0.16, "模板 $\\bar{\\mathbf{T}}$\n6890 顶点", fc="#F9FAFB", ec=fs.MUTED, fs=8)
    fs.box(ax, 0.28, 0.72, 0.22, 0.16, "形状参数 $\\beta$\n10 维", fc="#EEF2FF", ec=fs.BLUE, fs=8.4)
    fs.box(ax, 0.56, 0.72, 0.22, 0.16, "姿态参数 $\\theta$\n24 关节 × 3", fc="#ECFDF5", ec=fs.GREEN, fs=8.2)
    fs.box(ax, 0.82, 0.72, 0.16, 0.16, "蒙皮权重\n$\\mathcal{W}$", fc="#FDF6EC", ec=fs.ACCENT, fs=8)

    fs.box(ax, 0.28, 0.44, 0.22, 0.16, "形状偏移\n$B_S(\\beta)$", fc="#EEF2FF", ec=fs.BLUE, fs=8.4)
    fs.box(ax, 0.56, 0.44, 0.22, 0.16, "姿势偏移\n$B_P(\\theta)$", fc="#ECFDF5", ec=fs.GREEN, fs=8.4)
    fs.box(ax, 0.82, 0.44, 0.16, 0.16, "关节回归\n$J(\\beta)$", fc="#FDF6EC", ec=fs.ACCENT, fs=8)

    fs.box(ax, 0.18, 0.16, 0.28, 0.16, "中间形状 $T_P$", fc="white", ec=fs.INK, fs=8.8)
    fs.box(ax, 0.54, 0.16, 0.26, 0.16, "LBS 蒙皮", fc="white", ec=fs.INK, fs=8.8)
    fs.box(ax, 0.84, 0.16, 0.14, 0.16, "网格 $M$", fc="#F5F3FF", ec=fs.PURPLE, fs=8.8)

    for p0, p1 in [((0.39, 0.72), (0.39, 0.60)), ((0.67, 0.72), (0.67, 0.60)),
                   ((0.90, 0.72), (0.90, 0.60)), ((0.39, 0.44), (0.34, 0.32)),
                   ((0.67, 0.44), (0.60, 0.32)), ((0.90, 0.44), (0.72, 0.32)),
                   ((0.46, 0.24), (0.54, 0.24)), ((0.80, 0.24), (0.84, 0.24))]:
        fs.arrow(ax, p0, p1, color=fs.FAINT, lw=1.0)
    fs.arrow(ax, (0.12, 0.72), (0.18, 0.32), color=fs.FAINT, lw=1.0, rad=-0.15)
    fs.label(ax, 0.5, 0.955, "SMPL 的前向计算：形状 + 姿势 → 顶点", fs=10)
    fs.label(ax, 0.5, 0.03, "$M(\\beta,\\theta)=W(T_P(\\beta,\\theta),J(\\beta),\\theta,\\mathcal{W})$",
             fs=10.5, color=fs.ACCENT)
    fs.save(fig, "ch08", "fig08-01")


def fig_joints():
    fig, ax = fs.canvas(6.9, 3.0)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    # 用图 5-1 的骨架但标注 SMPL 的关节
    J = {
        "pelvis": (0.50, 0.40), "spine1": (0.50, 0.48), "spine2": (0.50, 0.55),
        "spine3": (0.50, 0.62), "neck": (0.50, 0.70), "head": (0.50, 0.80),
        "l_clav": (0.44, 0.66), "l_sh": (0.40, 0.64), "l_el": (0.33, 0.53), "l_wr": (0.29, 0.42),
        "r_clav": (0.56, 0.66), "r_sh": (0.60, 0.64), "r_el": (0.67, 0.53), "r_wr": (0.71, 0.42),
        "l_hip": (0.45, 0.38), "l_kn": (0.43, 0.24), "l_an": (0.42, 0.10),
        "r_hip": (0.55, 0.38), "r_kn": (0.57, 0.24), "r_an": (0.58, 0.10),
        "l_foot": (0.42, 0.06), "r_foot": (0.58, 0.06),
    }
    bones = [("pelvis", "spine1"), ("spine1", "spine2"), ("spine2", "spine3"), ("spine3", "neck"),
             ("neck", "head"), ("spine3", "l_clav"), ("l_clav", "l_sh"), ("l_sh", "l_el"), ("l_el", "l_wr"),
             ("spine3", "r_clav"), ("r_clav", "r_sh"), ("r_sh", "r_el"), ("r_el", "r_wr"),
             ("pelvis", "l_hip"), ("l_hip", "l_kn"), ("l_kn", "l_an"), ("l_an", "l_foot"),
             ("pelvis", "r_hip"), ("r_hip", "r_kn"), ("r_kn", "r_an"), ("r_an", "r_foot")]
    for a, b in bones:
        ax.plot([J[a][0], J[b][0]], [J[a][1], J[b][1]], color="#CBD5E1", lw=6, solid_capstyle="round", zorder=1)
        ax.plot([J[a][0], J[b][0]], [J[a][1], J[b][1]], color=fs.BLUE, lw=1.6, zorder=2)
    for k, (x, y) in J.items():
        ax.add_patch(plt.Circle((x, y), 0.009, color=fs.ACCENT, zorder=4, ec="white", lw=0.8))
    fs.label(ax, 0.05, 0.94, "SMPL 的 24 个关节（图中省略左右对称的重复标注）", fs=9.6, ha="left")
    for k, dx, dy, txt in [("pelvis", 0.0, -0.06, "0 骨盆"), ("spine3", 0.03, 0.0, "3 胸"),
                           ("head", 0.03, 0.0, "15 头"), ("l_wr", -0.03, 0.0, "20 左腕"),
                           ("r_an", 0.03, 0.0, "17 右踝")]:
        x, y = J[k]
        fs.label(ax, x + dx, y + dy, txt, fs=7.8, color=fs.MUTED,
                 ha="left" if dx >= 0 else "right")
    fs.label(ax, 0.5, 0.02, "每个关节 3 个轴角 → 姿态参数共 $24\\times3=72$ 维", fs=8.4, color=fs.ACCENT)
    fs.save(fig, "ch08", "fig08-02")


def fig_grid():
    fig, ax = fs.canvas(6.9, 3.1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    widths = [0.82, 1.0, 1.18]
    poses = [{}, dict(l_arm=0.9, r_arm=0.4, l_leg=0.35), dict(l_arm=1.3, r_arm=1.1, l_leg=0.15, r_leg=0.45)]
    for i, w in enumerate(widths):
        for j, p in enumerate(poses):
            cx = 0.18 + j * 0.32
            cy = 0.73 - i * 0.27
            fs.human(ax, cx=cx, cy=cy, s=0.27, width=w, pose=p,
                     color=fs.ACCENT if i == 1 and j == 1 else "#C9A98F")
    fs.label(ax, 0.02, 0.38, "体型 $\\beta$", fs=9, color=fs.BLUE, rotation=90)
    fs.label(ax, 0.5, 0.96, "同一个模型，换 $\\beta$ 改变体型，换 $\\theta$ 改变姿势", fs=9.6)
    fs.label(ax, 0.52, 0.02, "中间是均值体型与静止姿势；周围是不同组合", fs=7.8, color=fs.MUTED)
    fs.save(fig, "ch08", "fig08-03")


if __name__ == "__main__":
    fig_pipeline()
    fig_joints()
    fig_grid()
