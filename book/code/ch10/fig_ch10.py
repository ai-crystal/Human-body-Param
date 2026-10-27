# -*- coding: utf-8 -*-
"""第 10 章插图：单图人体重建的两条路线。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_two_routes():
    fig, ax = fs.canvas(6.9, 3.4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    fs.label(ax, 0.02, 0.90, "A. 优化法（analysis-by-synthesis）", fs=9.4, ha="left", color=fs.BLUE)
    fs.box(ax, 0.02, 0.66, 0.13, 0.14, "图像", fc="white", ec=fs.MUTED, fs=8)
    fs.box(ax, 0.19, 0.66, 0.16, 0.14, "2D 关键点\n/ 轮廓", fc="#EEF2FF", ec=fs.BLUE, fs=8)
    fs.box(ax, 0.39, 0.66, 0.18, 0.14, "优化\n$\\beta,\\theta$", fc="#FDF6EC", ec=fs.ACCENT, fs=8.2)
    fs.box(ax, 0.61, 0.66, 0.15, 0.14, "SMPL\n渲染", fc="#ECFDF5", ec=fs.GREEN, fs=8)
    fs.box(ax, 0.80, 0.66, 0.16, 0.14, "重投影误差", fc="white", ec=fs.INK, fs=8)
    for x in [0.15, 0.35, 0.57, 0.76]:
        fs.arrow(ax, (x, 0.73), (x + 0.035, 0.73), color=fs.FAINT)
    fs.arrow(ax, (0.88, 0.66), (0.48, 0.66), color=fs.ACCENT, lw=1.2, rad=0.25)
    fs.label(ax, 0.70, 0.53, "闭环：误差反传，迭代更新参数", fs=7.8, color=fs.ACCENT)

    fs.label(ax, 0.02, 0.42, "B. 回归法（discriminative）", fs=9.4, ha="left", color=fs.GREEN)
    fs.box(ax, 0.02, 0.16, 0.13, 0.16, "图像", fc="white", ec=fs.MUTED, fs=8)
    fs.box(ax, 0.19, 0.16, 0.22, 0.16, "CNN / Transformer\n特征", fc="#ECFDF5", ec=fs.GREEN, fs=8)
    fs.box(ax, 0.45, 0.16, 0.22, 0.16, "直接回归\n$\\beta,\\theta,\\pi$", fc="#FDF6EC", ec=fs.ACCENT, fs=8)
    fs.box(ax, 0.71, 0.16, 0.16, 0.16, "SMPL\n网格", fc="#EEF2FF", ec=fs.BLUE, fs=8)
    for x in [0.15, 0.41, 0.67]:
        fs.arrow(ax, (x, 0.24), (x + 0.035, 0.24), color=fs.FAINT)
    fs.label(ax, 0.88, 0.24, "一次前向\n实时", fs=7.6, color=fs.GREEN, ha="center")

    fs.label(ax, 0.5, 0.02, "实际系统常把两者结合：回归给初值，优化做精修（SPIN 的思路）",
             fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch10", "fig10-01")


def fig_energy():
    fig, ax = fs.canvas(6.9, 2.8)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fs.box(ax, 0.02, 0.38, 0.17, 0.30, "总目标\n$E(\\beta,\\theta)$", fc="#FDF6EC", ec=fs.ACCENT, fs=9)
    terms = [("2D 关键点\n重投影", fs.BLUE), ("轮廓\nsilhouette", fs.GREEN),
             ("姿态先验\n关节角限位", fs.PURPLE), ("形状先验\n$\\|\\beta\\|^2$", fs.GOLD)]
    for i, (t, c) in enumerate(terms):
        y = 0.86 - i * 0.19
        fs.box(ax, 0.34, y - 0.075, 0.22, 0.15, t, fc="white", ec=c, fs=8)
        fs.arrow(ax, (0.19, 0.53), (0.34, y), color=c, lw=0.9, rad=0.12)
        fs.label(ax, 0.60, y, f"$\\lambda_{i+1}$", fs=8.4, color=c, ha="left")
    fs.label(ax, 0.78, 0.53, "每一项都有\n一个权重 $\\lambda$\n需要调", fs=8.4, color=fs.MUTED, ha="center")
    fs.label(ax, 0.5, 0.03, "优化法的成败，一半在模型，一半在损失函数与权重", fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch10", "fig10-02")


def fig_ambiguity():
    """图 10-3：尺度-深度歧义与“平均人”"""
    fig = plt.figure(figsize=(6.9, 3.1))

    # 左：同一张图里的两种 3D 解释
    axL = fig.add_axes([0.005, 0.04, 0.46, 0.86])
    axL.set_xlim(0, 1); axL.set_ylim(0, 1); axL.axis("off")
    fs.label(axL, 0.5, 0.95, "同一张图，两种 3D 解释", fs=9.2)
    axL.add_patch(plt.Rectangle((0.08, 0.16), 0.84, 0.62, fill=False,
                                ec=fs.FAINT, lw=0.9, ls=(0, (4, 3)), zorder=1))
    fs.human(axL, cx=0.30, cy=0.50, s=0.50, width=1.55, color=fs.BLUE, alpha=0.45, z=3)
    fs.human(axL, cx=0.70, cy=0.50, s=0.50, width=0.62, color=fs.GREEN, alpha=0.55, z=4)
    fs.label(axL, 0.5, 0.845, "图像里的 2D 轮廓", fs=8.4, color=fs.MUTED)
    fs.label(axL, 0.5, 0.545, "≈", fs=13, color=fs.MUTED)
    fs.label(axL, 0.30, 0.105, "体型宽 + 离得近", fs=8.4, color=fs.BLUE)
    fs.label(axL, 0.70, 0.105, "体型瘦 + 离得远", fs=8.4, color=fs.GREEN)

    # 右：参数空间里的两个峰与均值
    axR = fig.add_axes([0.565, 0.24, 0.40, 0.52])
    x = np.linspace(0, 1, 400)
    g = lambda mu, sd: np.exp(-(x - mu) ** 2 / (2 * sd ** 2))
    d1, d2 = g(0.30, 0.075), g(0.70, 0.075)
    axR.fill_between(x, 0, d1, color=fs.BLUE, alpha=0.18)
    axR.fill_between(x, 0, d2, color=fs.GREEN, alpha=0.18)
    axR.plot(x, d1, color=fs.BLUE, lw=1.3)
    axR.plot(x, d2, color=fs.GREEN, lw=1.3)
    axR.axvline(0.5, color=fs.ACCENT, lw=1.2, ls="--")
    axR.set_xlim(0, 1); axR.set_ylim(0, 1.12)
    axR.set_xticks([]); axR.set_yticks([])
    for sp in ("top", "right"):
        axR.spines[sp].set_visible(False)
    axR.spines["left"].set_color(fs.FAINT); axR.spines["bottom"].set_color(fs.FAINT)
    axR.set_xlabel("体型参数（某一维，示意）", fontsize=8.6)
    axR.set_ylabel("概率密度", fontsize=8.6)
    axR.set_title("训练用平方误差 → 输出取中间值", fontsize=9.0, color=fs.INK)
    axR.text(0.30, 1.02, "解释 A", ha="center", fontsize=8.4, color=fs.BLUE)
    axR.text(0.70, 1.02, "解释 B", ha="center", fontsize=8.4, color=fs.GREEN)
    axR.text(0.535, 0.62, "平方误差的解\n= 条件均值", ha="left", va="center",
             fontsize=8.4, color=fs.ACCENT, linespacing=1.5)
    fs.label(fig, 0.5, 0.015, "两个峰都解释得通，均值却可能谁都不像", fs=8.4,
             color=fs.MUTED)
    fs.save(fig, "ch10", "fig10-03")


if __name__ == "__main__":
    fig_two_routes()
    fig_energy()
    fig_ambiguity()
