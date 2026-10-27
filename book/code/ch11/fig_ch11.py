# -*- coding: utf-8 -*-
"""第 11 章插图：视频、世界坐标与多人。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch
import figstyle as fs


def fig_video():
    fig, ax = fs.canvas(6.9, 2.7)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fs.box(ax, 0.02, 0.38, 0.13, 0.26, "视频帧", fc="white", ec=fs.MUTED, fs=8)
    fs.box(ax, 0.18, 0.38, 0.17, 0.26, "逐帧特征\nCNN / ViT", fc="#EEF2FF", ec=fs.BLUE, fs=8)
    fs.box(ax, 0.38, 0.38, 0.18, 0.26, "时序融合\nGRU / Transformer", fc="#ECFDF5", ec=fs.GREEN, fs=8)
    fs.box(ax, 0.59, 0.38, 0.17, 0.26, "SMPL 序列\n$\\beta,\\theta_t$", fc="#FDF6EC", ec=fs.ACCENT, fs=8)
    fs.box(ax, 0.79, 0.38, 0.18, 0.26, "世界坐标\n轨迹 + 接触", fc="#F5F3FF", ec=fs.PURPLE, fs=8)
    for x in [0.15, 0.35, 0.56, 0.76]:
        fs.arrow(ax, (x, 0.51), (x + 0.03, 0.51), color=fs.FAINT)
    fs.label(ax, 0.5, 0.80, "视频人体重建：单帧不够，要靠时间上的连续性", fs=9.6)
    fs.label(ax, 0.5, 0.17, "关键约束：同一段视频里，人的身份 $\\beta$ 不变，相机可以动，重力方向不变",
             fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch11", "fig11-01")


def fig_frames():
    fig, ax = fs.canvas(6.9, 3.2)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ox, oy = 0.28, 0.30
    ax.annotate("", xy=(0.94, oy), xytext=(ox, oy),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0))
    ax.annotate("", xy=(ox, 0.90), xytext=(ox, oy),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0))
    fs.label(ax, 0.90, oy - 0.06, "世界 X", fs=8.4, color=fs.MUTED)
    fs.label(ax, ox - 0.03, 0.86, "世界 Y", fs=8.4, color=fs.MUTED, ha="right")
    # 轨迹（贴地）
    t = np.linspace(0, 1, 60)
    ax.plot(0.34 + 0.52 * t, oy + 0.006 * np.sin(6 * t), color=fs.GREEN, lw=1.2, ls="--")
    fs.label(ax, 0.44, oy + 0.05, "根关节轨迹", fs=7.8, color=fs.GREEN)
    # 相机
    cam = np.array([0.41, 0.60])
    ax.add_patch(Circle(cam, 0.022, color=fs.INK, zorder=5))
    ax.annotate("", xy=(0.70, 0.72), xytext=cam,
                arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=1.3))
    fs.label(ax, cam[0] - 0.02, cam[1] + 0.05, "相机", fs=8.4, color=fs.BLUE, ha="right")
    fs.label(ax, 0.71, 0.74, "光轴", fs=8, color=fs.BLUE, ha="left")
    # 人（站在地面上）
    fs.human(ax, cx=0.72, cy=0.415, s=0.26, color=fs.ACCENT, width=0.95)
    fs.label(ax, 0.72, 0.21, "人：局部骨架 + 全局朝向", fs=8.2, color=fs.ACCENT)
    fs.label(ax, 0.52, 0.95, "三个坐标系：图像、相机、世界", fs=9.6)
    fs.label(ax, 0.5, 0.04, "把逐帧的相机坐标结果变换到统一世界坐标，才能得到“走了多远”",
             fs=8, color=fs.MUTED)
    fs.save(fig, "ch11", "fig11-02")




def fig_camera_contact():
    """相机位姿 -> 世界坐标；脚接触定住尺度（配合 11.8 节）。"""
    fig, ax = fs.canvas(6.9, 3.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    AR = fig.get_size_inches()[1] / fig.get_size_inches()[0]   # y/x 单位长度比

    def dot(xy, r, fc, ec="white", lw=0.8, z=6):
        ax.add_patch(Ellipse(xy, 2 * r * AR, 2 * r, facecolor=fc, edgecolor=ec,
                             lw=lw, zorder=z))

    def ring(xy, r, ec, fc="white", lw=1.2, z=8):
        ax.add_patch(Ellipse(xy, 2 * r * AR, 2 * r, facecolor=fc, edgecolor=ec,
                             lw=lw, zorder=z))

    fs.label(ax, 0.5, 0.962, "相机在动：先估相机位姿，再把每帧的人搬进世界坐标", fs=9.6)

    # ---------- 左：两个坐标系 ----------
    O = np.array([0.090, 0.400])
    C = np.array([0.140, 0.760])
    P = np.array([0.400, 0.590])
    fs.arrow(ax, O, O + np.array([0.150, 0]), color=fs.MUTED, lw=1.1)
    fs.arrow(ax, O, O + np.array([0, 0.210]), color=fs.MUTED, lw=1.1)
    fs.label(ax, O[0] + 0.157, O[1] - 0.024, "X", fs=8.4, color=fs.MUTED, ha="left")
    fs.label(ax, O[0] - 0.020, O[1] + 0.216, "Y", fs=8.4, color=fs.MUTED, ha="right")
    fs.label(ax, 0.045, 0.335, "世界坐标系 $W$", fs=8.4, color=fs.MUTED, ha="left")

    # 相机
    dot(C, 0.017, fc=fs.BLUE, ec="white", lw=0.8, z=6)
    fs.label(ax, C[0] + 0.030, C[1] + 0.030, "相机（第 $t$ 帧）", fs=8.4,
             color=fs.BLUE, ha="left")

    # 两条向量
    fs.arrow(ax, C, P, color=fs.BLUE, lw=1.6, rad=0.03)
    fs.label(ax, 0.300, 0.585, r"$\mathbf{X}^{c}_t$：相机坐标", fs=8.6, color=fs.BLUE)
    ax.annotate("", xy=P, xytext=O,
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0,
                                ls=(0, (3, 2)), shrinkA=2, shrinkB=3))
    fs.label(ax, 0.330, 0.462, r"$\mathbf{X}^{w}_t$：世界坐标", fs=8.4, color=fs.MUTED, ha="left")
    dot(P, 0.013, fc=fs.ACCENT, ec="white", lw=0.8, z=7)
    fs.label(ax, P[0] + 0.014, P[1] + 0.042, "人体根节点", fs=8.2,
             color=fs.ACCENT, ha="left")

    # 变换式
    fs.label(ax, 0.265, 0.205,
             r"$\mathbf{X}^{w}_t=\mathbf{R}_t^{\top}\mathbf{X}^{c}_t+\mathbf{t}_t$",
             fs=10.0)
    fs.label(ax, 0.265, 0.125,
             r"$\mathbf{R}_t$（3×3）把世界方向转到相机，$\mathbf{t}_t$（3 维）是光心位置",
             fs=7.9, color=fs.MUTED)

    # ---------- 右：脚接触 ----------
    gy = 0.340
    ax.plot([0.545, 0.978], [gy, gy], color=fs.FAINT, lw=1.4, zorder=1)
    for gx in np.arange(0.560, 0.978, 0.030):
        ax.plot([gx, gx], [gy, gy - 0.008], color="#D1D5DB", lw=0.7, zorder=1)
    fs.label(ax, 0.946, gy + 0.026, "地面", fs=8.0, color=fs.MUTED, ha="right")

    s_fig = 0.32
    hip_y = gy + 0.435 * s_fig
    fs.human(ax, cx=0.622, cy=hip_y, s=s_fig, color="#CBD5E1", z=3)
    fs.label(ax, 0.622, hip_y + 0.235, "第 $t$ 帧", fs=8.4, color=fs.FAINT)
    fs.human(ax, cx=0.812, cy=hip_y, s=s_fig, color=fs.ACCENT, z=4)
    fs.label(ax, 0.812, hip_y + 0.235, "第 $t{+}1$ 帧", fs=8.4, color=fs.ACCENT)

    ring((0.640, gy + 0.012), 0.010, fs.GREEN)
    dot((0.768, gy + 0.012), 0.009, fc=fs.GOLD, ec="white", lw=0.8, z=8)
    ax.annotate("", xy=(0.756, gy + 0.055), xytext=(0.652, gy + 0.055),
                arrowprops=dict(arrowstyle="<->", color=fs.GOLD, lw=1.0))
    fs.label(ax, 0.703, gy + 0.082, r"$\Delta$", fs=9.0, color=fs.GOLD)
    fs.label(ax, 0.640, gy - 0.038, "接触点", fs=8.0, color=fs.GREEN)
    fs.label(ax, 0.772, gy - 0.038, "预测的脚", fs=8.0, color=fs.GOLD)

    # 页脚
    fs.label(ax, 0.5, 0.045,
             "同一段视频里脚踩地时脚在世界中不动：这条约束既修漂移，也定住单目的尺度",
             fs=8.4, color=fs.MUTED)
    fs.save(fig, "ch11", "fig11-03")


if __name__ == "__main__":
    fig_video()
    fig_frames()
    fig_camera_contact()
