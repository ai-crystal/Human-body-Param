# -*- coding: utf-8 -*-
"""第 5 章插图：骨架、LBS 与蒙皮伪影。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyArrowPatch
import figstyle as fs


def fig_skeleton():
    fig, ax = fs.canvas(6.6, 3.3)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    # 关节坐标（2D 示意）
    J = {
        "pelvis": (0.50, 0.42),
        "spine": (0.50, 0.52),
        "chest": (0.50, 0.62),
        "neck": (0.50, 0.72),
        "head": (0.50, 0.82),
        "l_shoulder": (0.41, 0.70), "l_elbow": (0.34, 0.58), "l_wrist": (0.30, 0.46),
        "r_shoulder": (0.59, 0.70), "r_elbow": (0.66, 0.58), "r_wrist": (0.70, 0.46),
        "l_hip": (0.45, 0.40), "l_knee": (0.43, 0.26), "l_ankle": (0.42, 0.12),
        "r_hip": (0.55, 0.40), "r_knee": (0.57, 0.26), "r_ankle": (0.58, 0.12),
    }
    bones = [("pelvis", "spine"), ("spine", "chest"), ("chest", "neck"), ("neck", "head"),
             ("chest", "l_shoulder"), ("l_shoulder", "l_elbow"), ("l_elbow", "l_wrist"),
             ("chest", "r_shoulder"), ("r_shoulder", "r_elbow"), ("r_elbow", "r_wrist"),
             ("pelvis", "l_hip"), ("l_hip", "l_knee"), ("l_knee", "l_ankle"),
             ("pelvis", "r_hip"), ("r_hip", "r_knee"), ("r_knee", "r_ankle")]
    for a, b in bones:
        ax.plot([J[a][0], J[b][0]], [J[a][1], J[b][1]], color="#CBD5E1", lw=7, solid_capstyle="round", zorder=1)
        ax.plot([J[a][0], J[b][0]], [J[a][1], J[b][1]], color=fs.BLUE, lw=2.0, zorder=2)
    for k, (x, y) in J.items():
        ax.add_patch(Circle((x, y), 0.012, color=fs.ACCENT, zorder=4, ec="white", lw=1))
    for k in ["pelvis", "chest", "head", "l_wrist", "r_wrist", "l_ankle", "r_ankle", "l_elbow"]:
        x, y = J[k]
        fs.label(ax, x + (0.02 if x > 0.5 else -0.02), y + 0.028,
                 {"pelvis": "根关节 (pelvis)", "chest": "胸", "head": "头",
                  "l_wrist": "腕", "r_wrist": "腕", "l_ankle": "踝", "r_ankle": "踝",
                  "l_elbow": "肘"}[k], fs=8, ha="left" if x > 0.5 else "right", color=fs.MUTED)
    fs.label(ax, 0.02, 0.95, "关节树：每个关节只有一个父节点，变换沿树向下传递", fs=9.5, ha="left")
    fs.label(ax, 0.02, 0.04, "橙色 = 关节（变换的支点）；蓝色 = 骨骼（两个关节之间的刚体段）", fs=8.2, ha="left", color=fs.MUTED)
    fs.save(fig, "ch05", "fig05-01")


def fig_lbs():
    fig, axs = plt.subplots(1, 2, figsize=(6.9, 3.0))
    for ax in axs:
        ax.set_xlim(-0.15, 1.35); ax.set_ylim(-0.15, 1.25)
        ax.set_aspect("equal"); ax.axis("off")

    def bones(ax, ang):
        J = np.array([0.55, 0.30])
        R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        elbow = J
        wrist = J + R @ np.array([0.55, 0.0])
        ax.plot([0.05, elbow[0]], [0.30, elbow[1]], color=fs.BLUE, lw=9,
                solid_capstyle="round", alpha=0.32, zorder=2)
        ax.plot([elbow[0], wrist[0]], [elbow[1], wrist[1]], color=fs.GREEN, lw=9,
                solid_capstyle="round", alpha=0.32, zorder=2)
        ax.add_patch(Circle(elbow, 0.032, color=fs.MUTED, zorder=5))
        return J, R

    # 左：静止
    J, R = bones(axs[0], 0.0)
    v = J + np.array([0.36, 0.07])
    axs[0].scatter([v[0]], [v[1]], s=55, color=fs.ACCENT, zorder=7)
    fs.label(axs[0], v[0] + 0.03, v[1] + 0.07, r"顶点 $\mathbf{v}$", fs=8.8, color=fs.ACCENT, ha="left")
    fs.label(axs[0], 0.05, 0.09, "权重：上臂 0.3，前臂 0.7", fs=8, color=fs.MUTED, ha="left")
    axs[0].set_title("静止姿势（rest pose）", fontsize=9.4)

    # 右：弯曲 90°，比较三种位置
    ang = np.deg2rad(90)
    J, R = bones(axs[1], ang)
    v1 = v
    v2 = J + R @ (v - J)
    vb = 0.3 * v1 + 0.7 * v2
    axs[1].scatter([v1[0]], [v1[1]], s=40, color=fs.BLUE, zorder=7)
    axs[1].scatter([v2[0]], [v2[1]], s=40, color=fs.GREEN, zorder=7)
    axs[1].scatter([vb[0]], [vb[1]], s=55, color=fs.ACCENT, zorder=8)
    axs[1].plot([v1[0], v2[0]], [v1[1], v2[1]], color=fs.MUTED, lw=1.0, ls="--", zorder=4)
    fs.label(axs[1], v1[0] - 0.03, v1[1] + 0.05, "只随上臂", fs=7.8, color=fs.BLUE, ha="right")
    fs.label(axs[1], v2[0] - 0.03, v2[1], "只随前臂", fs=7.8, color=fs.GREEN, ha="right")
    fs.label(axs[1], vb[0] + 0.03, vb[1] - 0.08, "线性混合", fs=8.2, color=fs.ACCENT, ha="left")
    axs[1].set_title("关节弯曲 90°", fontsize=9.4)
    fs.label(axs[1], 0.05, 0.07, "混合点落在两点连线上 → 肢体变短", fs=7.8, color=fs.MUTED, ha="left")
    fig.tight_layout()
    fs.save(fig, "ch05", "fig05-02")


def fig_artifact():
    """权重沿肢体的平滑过渡（颜色 = 前臂权重）。"""
    fig, ax = plt.subplots(figsize=(6.6, 2.6))
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.40, 0.35); ax.axis("off")
    n = 60
    for i in range(n):
        t = i / (n - 1)
        x = 0.05 + 0.9 * t
        # 0→0.45 上臂，0.45→1 前臂
        w = 1 / (1 + np.exp(-(t - 0.45) * 18))
        r = 0.055 * (1 - 0.25 * abs(t - 0.5))
        c = (0.12 + 0.75 * w, 0.25 + 0.15 * (1 - w), 0.65 * (1 - w) + 0.12)
        ax.add_patch(Circle((x, 0), r, color=c, zorder=2, lw=0))
    ax.add_patch(Circle((0.05 + 0.9 * 0.45, 0), 0.012, color="white", zorder=4, ec=fs.MUTED))
    fs.label(ax, 0.05, -0.22, "肩：前臂权重 = 0", fs=8.2, color=fs.BLUE, ha="left")
    fs.label(ax, 0.50, 0.20, "肘：权重平滑过渡", fs=8.4, color=fs.MUTED)
    fs.label(ax, 1.00, -0.22, "腕：前臂权重 = 1", fs=8.2, color=fs.GREEN, ha="right")
    ax.annotate("", xy=(0.95, 0.12), xytext=(0.10, 0.12),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=0.9))
    fs.label(ax, 0.52, 0.145, "权重从 0 连续过渡到 1", fs=8, color=fs.MUTED)
    fs.label(ax, 0.5, -0.35, "如果权重是硬切换（0 或 1），关节处会撕裂；平滑权重让皮肤自然弯折",
             fs=8.2, color=fs.INK)
    fs.save(fig, "ch05", "fig05-03")


if __name__ == "__main__":
    fig_skeleton()
    fig_lbs()
    fig_artifact()
