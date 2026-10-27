# -*- coding: utf-8 -*-
"""第 23 章插图：从图像重建动物。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle
import figstyle as fs


# ---------------- 图 23-1：一条简短的时间线 ----------------
def fig_timeline():
    fig, ax = fs.canvas(6.8, 3.4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    y = 0.50
    ax.plot([0.045, 0.965], [y, y], color=fs.INK, lw=1.2, zorder=2)
    ax.annotate("", xy=(0.975, y), xytext=(0.955, y),
                arrowprops=dict(arrowstyle="-|>", color=fs.INK, lw=1.2))

    items = [(2017, "SMAL", "四足形状空间", True, 1),
             (2018, "SMALR", "逐实例细化", False, 1),
             (2019, "SMALST", "像素直接回归", True, 1),
             (2020, "Dogs Out", "EM 闭环", False, 1),
             (2022, "BARC", "品种条件化", True, 1),
             (2023, "MagicPony", "学铰接先验", False, 1),
             (2023, "3D-Fauna", "3D 基准", True, 2),
             (2024, "AniMer", "渲染-比较", False, 1)]
    lo, hi = 2016.6, 2024.6
    seen = {}
    for i, (yr, name, sub, up, lvl) in enumerate(items):
        x = 0.05 + 0.92 * (yr - lo) / (hi - lo)
        seen[yr] = seen.get(yr, 0) + 1
        if seen[yr] > 1:
            x -= 0.010
        h = {1: 0.115, 2: 0.215}[lvl]
        ax.scatter([x], [y], s=34, color=fs.ACCENT, zorder=4, edgecolor="white", lw=0.8)
        ax.plot([x, x], [y, y + h if up else y - h], color=fs.FAINT, lw=0.8, zorder=1)
        yy = y + h if up else y - h
        sgn = 1 if up else -1
        va = "bottom" if up else "top"
        fs.label(ax, x, yy + sgn * 0.008, str(yr), fs=8.0, color=fs.ACCENT, va=va)
        fs.label(ax, x, yy + sgn * 0.070, name, fs=8.6, color=fs.INK, weight="bold", va=va)
        fs.label(ax, x, yy + sgn * 0.150, sub, fs=7.4, color=fs.MUTED, va=va)

    fs.label(ax, 0.045, 0.965, "监督信号从“手工关键点 + 轮廓”逐步退到“只要能渲染得像”",
             fs=9.2, color=fs.INK, ha="left", va="center")
    fs.label(ax, 0.045, 0.020, "越靠右，越少依赖人工标注；代价是更需要先验和更多算力",
             fs=8.4, color=fs.MUTED, ha="left", va="center")
    fs.save(fig, "ch23", "fig23-01")


def sil_dog(ax, cx, cy, w=0.16, h=0.055, color=fs.INK, alpha=1.0, z=2, leg=0.05):
    """极简四足剪影（示意图，不追求解剖精度）。"""
    ax.add_patch(Ellipse((cx, cy), w, h * 2, facecolor=color, alpha=alpha,
                         edgecolor="none", zorder=z))
    ax.add_patch(Ellipse((cx + w * 0.60, cy + h * 0.45), w * 0.34, h * 1.1,
                         angle=18, facecolor=color, alpha=alpha, edgecolor="none", zorder=z))
    for dx in (-w * 0.32, -w * 0.18, w * 0.22, w * 0.36):
        ax.add_patch(Polygon([(cx + dx - w * 0.022, cy - h * 0.35),
                              (cx + dx + w * 0.022, cy - h * 0.35),
                              (cx + dx + w * 0.015, cy - h * 0.35 - leg),
                              (cx + dx - w * 0.015, cy - h * 0.35 - leg)],
                             closed=True, facecolor=color, alpha=alpha,
                             edgecolor="none", zorder=z - 1))


# ---------------- 图 23-2：单图重建的回路 ----------------
def fig_pipeline():
    fig, ax = fs.canvas(6.8, 3.9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    fs.box(ax, 0.025, 0.560, 0.130, 0.240, "输入图像\n仅一个包围框", fc="white",
           ec=fs.INK, fs=8.4)
    fs.box(ax, 0.185, 0.560, 0.135, 0.240, "编码器\nResNet / ViT", fc="white",
           ec=fs.BLUE, fs=8.4)
    fs.arrow(ax, (0.158, 0.680), (0.182, 0.680), color=fs.FAINT)

    params = [("姿态 θ", 0.772, fs.PURPLE), ("形状 β", 0.674, fs.GREEN),
              ("相机 t, f", 0.576, fs.GOLD), ("纹理 T", 0.478, fs.ACCENT)]
    for t, y, c in params:
        fs.box(ax, 0.352, y, 0.140, 0.068, t, fc="white", ec=c, fs=8.6, lw=1.0)
        fs.arrow(ax, (0.322, 0.680), (0.350, y + 0.034), color=fs.FAINT, lw=0.9)

    fs.box(ax, 0.600, 0.460, 0.165, 0.380, "SMAL 网格\n+ 可微渲染", fc="white",
           ec=fs.INK, fs=8.4)
    for yy in (0.780, 0.508):
        fs.arrow(ax, (0.494, yy + 0.014), (0.597, yy + 0.020), color=fs.FAINT, lw=0.9)
    fs.arrow(ax, (0.494, 0.610), (0.597, 0.620), color=fs.FAINT, lw=0.9)
    fs.box(ax, 0.795, 0.460, 0.180, 0.380, "渲染结果\n轮廓 · 像素", fc="white",
           ec=fs.INK, fs=8.4)
    fs.arrow(ax, (0.767, 0.650), (0.792, 0.650), color=fs.FAINT)

    losses = [("轮廓 / 掩码", 0.020, fs.BLUE), ("关键点重投影", 0.260, fs.GREEN),
              ("光度（纹理与像素）", 0.500, fs.ACCENT), ("形状 / 姿态先验", 0.740, fs.PURPLE)]
    for t, x, c in losses:
        fs.box(ax, x, 0.130, 0.220, 0.085, t, fc="white", ec=c, fs=8.2, lw=1.0)
    fs.arrow(ax, (0.868, 0.455), (0.858, 0.218), color=fs.FAINT, lw=0.9)
    fs.arrow(ax, (0.090, 0.555), (0.300, 0.218), color=fs.FAINT, lw=0.9,
             ls=(0, (4, 2)), rad=0.10)
    fs.label(ax, 0.132, 0.335, "参考", fs=7.8, color=fs.MUTED)
    fs.label(ax, 0.878, 0.335, "梯度回传", fs=7.8, color=fs.MUTED, ha="left")
    fs.label(ax, 0.500, 0.045, "损失全部定义在 2D 图像上：不需要 3D 真值就能训练",
             fs=9.0, color=fs.INK)

    fs.label(ax, 0.500, 0.975, "回归 + 可微渲染：把“像不像”变成可求导的数",
             fs=9.6, color=fs.INK)
    fs.save(fig, "ch23", "fig23-02")


# ---------------- 图 23-3：三个评估量 ----------------
def fig_metrics():
    fig = plt.figure(figsize=(6.8, 2.9))
    ax1 = fig.add_axes([0.02, 0.09, 0.30, 0.68])
    ax2 = fig.add_axes([0.355, 0.09, 0.30, 0.68])
    ax3 = fig.add_axes([0.690, 0.09, 0.30, 0.68])
    for ax in (ax1, ax2, ax3):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # (a) PCK：预测点与标注点的距离 / 躯干长度
    ax1.plot([0.20, 0.85], [0.78, 0.86], color=fs.MUTED, lw=2.2, solid_capstyle="round")
    ax1.plot([0.20, 0.17], [0.78, 0.52], color=fs.MUTED, lw=2.2, solid_capstyle="round")
    ax1.scatter([0.55], [0.825], s=44, color=fs.GREEN, zorder=4, edgecolor="white", lw=0.8)
    ax1.scatter([0.61], [0.735], s=44, color=fs.ACCENT, zorder=4, edgecolor="white", lw=0.8)
    ax1.annotate("", xy=(0.605, 0.742), xytext=(0.555, 0.818),
                 arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=1.0))
    fs.label(ax1, 0.665, 0.800, "d", fs=9.5, color=fs.ACCENT)
    ax1.plot([0.16, 0.80], [0.40, 0.40], color=fs.MUTED, lw=0.8)
    fs.label(ax1, 0.480, 0.335, "躯干长度 s", fs=8.2, color=fs.MUTED)
    fs.label(ax1, 0.50, 0.185, "PCK：满足 d < τ·s 的关键点比例", fs=8.2, color=fs.INK)
    fs.label(ax1, 0.50, 0.075, "绿＝标注　橙＝预测", fs=7.8, color=fs.MUTED)
    ax1.set_title("(a) 关键点正确率", fontsize=9.2, color=fs.INK, pad=3)

    # (b) IoU：两个轮廓的交并比
    th = np.linspace(0, 2 * np.pi, 200)
    c1 = np.stack([0.44 + np.cos(th) * 0.26, 0.52 + np.sin(th) * 0.20], axis=1)
    c2 = np.stack([0.56 + np.cos(th) * 0.24, 0.50 + np.sin(th) * 0.19], axis=1)
    ax2.add_patch(Polygon(c1, closed=True, facecolor=fs.BLUE, alpha=0.18,
                          edgecolor=fs.BLUE, lw=1.2))
    ax2.add_patch(Polygon(c2, closed=True, facecolor=fs.ACCENT, alpha=0.18,
                          edgecolor=fs.ACCENT, lw=1.2))
    fs.label(ax2, 0.375, 0.545, "预测", fs=8.4, color=fs.BLUE)
    fs.label(ax2, 0.640, 0.450, "标注", fs=8.4, color=fs.ACCENT)
    fs.label(ax2, 0.50, 0.185, "IoU ＝ 交集 / 并集", fs=8.2, color=fs.INK)
    fs.label(ax2, 0.50, 0.075, "对漏掉的腿、尾巴特别敏感", fs=7.8, color=fs.MUTED)
    ax2.set_title("(b) 轮廓重叠", fontsize=9.2, color=fs.INK, pad=3)

    # (c) 尺度：同一只动物、不同深度
    sil_dog(ax3, 0.31, 0.66, w=0.34, h=0.078, leg=0.10, color="#C4CAD4")
    sil_dog(ax3, 0.75, 0.45, w=0.17, h=0.042, leg=0.060, color=fs.INK)
    fs.label(ax3, 0.31, 0.830, "远处：像素少", fs=7.8, color=fs.MUTED)
    fs.label(ax3, 0.59, 0.400, "近处", fs=7.8, color=fs.MUTED)
    fs.label(ax3, 0.50, 0.185, "像素尺寸 ∝ f / z，尺度与焦距耦合", fs=8.2, color=fs.INK)
    fs.label(ax3, 0.50, 0.075, "两者一起估，才可能得到米制尺寸", fs=7.8, color=fs.MUTED)
    ax3.set_title("(c) 尺度与相机", fontsize=9.2, color=fs.INK, pad=3)

    fig.text(0.02, 0.960, "三个量回答三个不同的问题：点准不准、轮廓像不像、尺寸对不对",
             fontsize=9.2, color=fs.ACCENT, weight="bold")
    fs.save(fig, "ch23", "fig23-03")


if __name__ == "__main__":
    fig_timeline()
    fig_pipeline()
    fig_metrics()


def fig_scale_ambiguity():
    """图 23-4：单目尺度歧义。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9))
    for ax in axes:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # 左：近小 vs 远大，投影完全相同
    ax = axes[0]
    fs.label(ax, 0.5, 0.95, "同一张图，两种真实尺寸", fs=9.4)
    cam = (0.06, 0.50)
    plane_x = 0.90
    ax.plot([plane_x, plane_x], [0.10, 0.90], color=fs.FAINT, lw=1.6)
    fs.label(ax, plane_x, 0.05, "成像平面", fs=7.8, color=fs.MUTED)
    fs.label(ax, cam[0], cam[1] - 0.09, "相机", fs=7.8, color=fs.MUTED)

    def bar(cx, h, color, tag):
        ax.plot([cx, cx], [0.50 - h / 2, 0.50 + h / 2], color=color, lw=4.0,
                solid_capstyle="round", zorder=4)
        for dy in (-h / 2, h / 2):
            ax.plot([cam[0], plane_x], [cam[1], 0.50 + dy * (plane_x - cam[0]) / (cx - cam[0])],
                    color=color, lw=0.9, alpha=0.55, ls=(0, (3, 2)))
        fs.label(ax, cx, 0.50 + h / 2 + 0.155, tag, fs=7.8, color=color)

    bar(0.38, 0.10, fs.BLUE, "小猫 · 近")
    bar(0.72, 0.184, fs.ACCENT, "大猫 · 远")
    fs.label(ax, 0.5, 0.16, "两条虚线在成像平面上重合：像素完全一致", fs=8.0, color=fs.MUTED)

    # 右：三种破局办法
    ax = axes[1]
    fs.label(ax, 0.5, 0.95, "把绝对尺度钉住的三种外部信息", fs=9.4)
    items = [("物种平均尺寸", "例如成年家猫肩高约 25 cm\n遇到幼崽、亚种会系统偏差", fs.BLUE),
             ("图内参照物", "栅栏、车道、旁边的人\n已知尺寸反推相机距离", fs.GREEN),
             ("多视图 / 相机移动", "三角化恢复绝对尺度\n与人体度量尺度同一原理", fs.PURPLE)]
    for (t, sub, c), y in zip(items, [0.63, 0.345, 0.06]):
        fs.box(ax, 0.04, y, 0.92, 0.25, "", fc="white", ec=c, lw=1.1)
        fs.label(ax, 0.08, y + 0.215, t, fs=8.6, color=c, ha="left", va="top")
        fs.label(ax, 0.08, y + 0.140, sub, fs=7.6, color=fs.MUTED, ha="left", va="top")
    fig.tight_layout()
    fs.save(fig, "ch23", "fig23-04")


if __name__ == "__main__":
    fig_scale_ambiguity()
