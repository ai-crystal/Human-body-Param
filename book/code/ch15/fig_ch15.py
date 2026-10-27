# -*- coding: utf-8 -*-
"""第 15 章插图：3DMM 深入与 Basel Face Model。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
import figstyle as fs

W, H = 6.7, 4.15          # 画布（英寸）
KY = W / H                # 让 x/y 单位在屏幕上等长所需的 y 缩放


def _mini_face(ax, cx, cy, r=0.045, color=fs.INK, seed=0, arrows=False, alpha=1.0):
    """画一个“脸”的网格示意（椭圆网格 + 几个位移箭头）。"""
    pts = fs.mesh_disk(ax, cx=cx, cy=cy, rx=r, ry=r * KY, n=10,
                       color="#DDE3EA", ec=color, lw=0.45, z=3, alpha=alpha, seed=seed)
    if arrows:
        rng = np.random.default_rng(seed + 7)
        for k in range(6):
            th = 2 * np.pi * k / 6 + 0.3
            p0 = np.array([cx + 0.55 * r * np.cos(th), cy + 0.55 * r * KY * np.sin(th)])
            d = rng.normal(0, 0.006, 2) + np.array([0.02 * np.cos(th), 0.02 * KY * np.sin(th)])
            fs.arrow(ax, p0, p0 + d, color=fs.ACCENT, lw=1.0, ms=6)
    return pts


def fig_pipeline():
    fig, ax = fs.canvas(W, H)

    # ---------------- 上：分析-合成闭环 ----------------
    labels = ["输入图像\n$I$",
              "参数回归\n图像 → 参数",
              "3DMM 解码\n$S,\\ T$",
              "可微渲染\n$\\hat I=R(S,T,\\theta,c,l)$",
              "损失\n$\\|\\hat I-I\\|^2$"]
    cols = [fs.INK, fs.BLUE, fs.GREEN, fs.ACCENT, fs.PURPLE]
    fs.flow(ax, labels, y=0.86, h=0.155, fs=8.2, x0=0.02, x1=0.98, colors=cols)

    fs.box(ax, 0.40, 0.58, 0.34, 0.10,
           "$L=\\|\\hat I-I\\|^2+\\lambda\\|\\alpha\\|^2+\\lambda\\|\\psi\\|^2$",
           fc="#FFF7ED", ec=fs.ACCENT, fs=9.0, lw=1.1)
    fs.arrow(ax, (0.10, 0.782), (0.41, 0.682), color=fs.FAINT, lw=0.9, rad=-0.12)
    fs.arrow(ax, (0.90, 0.782), (0.73, 0.682), color=fs.FAINT, lw=0.9, rad=0.12)
    # 回传路径：损失框 → 左 → 上 → 参数回归框
    fs.arrow(ax, (0.40, 0.63), (0.205, 0.63), color=fs.ACCENT, lw=1.1, ls=(0, (4, 2)), ms=8)
    fs.arrow(ax, (0.205, 0.63), (0.212, 0.778), color=fs.ACCENT, lw=1.1, ls=(0, (4, 2)), ms=8)
    fs.label(ax, 0.232, 0.578, "梯度回传\n更新参数", fs=7.8, color=fs.ACCENT, ha="left")
    fs.label(ax, 0.50, 0.505, "分析-合成：先猜参数，再画出来，和照片比对，按误差修正猜测",
             fs=8.6, color=fs.MUTED)

    # ---------------- 下：均值 + 基向量 ----------------
    ax.plot([0.04, 0.96], [0.455, 0.455], color=fs.GRID, lw=0.9)
    fs.label(ax, 0.04, 0.418, "同一个式子的另一种读法：实例 = 平均脸 + 若干“位移场”的加权和",
             fs=8.8, color=fs.INK, ha="left")
    _mini_face(ax, 0.09, 0.225, seed=1)
    fs.label(ax, 0.09, 0.105, "$\\bar S$\n平均脸", fs=8.4)

    fs.label(ax, 0.185, 0.225, "$+$", fs=15, color=fs.MUTED)
    _mini_face(ax, 0.28, 0.225, seed=2, color=fs.BLUE, arrows=True)
    fs.label(ax, 0.28, 0.105, "$\\alpha_1 S_1+\\alpha_2 S_2$\n形状基", fs=8.4, color=fs.BLUE)

    fs.label(ax, 0.375, 0.225, "$+$", fs=15, color=fs.MUTED)
    _mini_face(ax, 0.47, 0.225, seed=3, color=fs.PURPLE, arrows=True)
    fs.label(ax, 0.47, 0.105, "$\\beta_1 B_1+\\beta_2 B_2$\n表情基", fs=8.4, color=fs.PURPLE)

    fs.label(ax, 0.565, 0.225, "$=$", fs=15, color=fs.MUTED)
    _mini_face(ax, 0.66, 0.225, seed=4, color=fs.INK, alpha=1.0)
    fs.label(ax, 0.66, 0.105, "$S$\n某个具体的人", fs=8.4)

    fs.box(ax, 0.775, 0.185, 0.195, 0.155,
           "$N$ 个顶点\n$\\Downarrow$ PCA\n几百个系数",
           fc="#F3F4F6", ec=fs.MUTED, fs=8.4, lw=0.9)
    fs.label(ax, 0.8725, 0.135, "压缩约 $10^4:1$", fs=8.0, color=fs.MUTED)

    fs.save(fig, "ch15", "fig15-02")


def fig_timeline():
    fig, ax = fs.canvas(W, 3.75)
    items = [
        (1999, "形变模型", "Blanz–Vetter\n200 张激光扫描\n光流建立对应", fs.ACCENT),
        (2005, "多线性模型", "Vlasic\n身份 $\\times$ 表情\n$\\times$ 视位", fs.GOLD),
        (2009, "BFM 公开", "Paysan\n形状 / 纹理\n两个 PCA", fs.BLUE),
        (2016, "实时重演", "Face2Face\n稠密光度跟踪\n模型参数传递", fs.TEAL),
        (2017, "FLAME", "4D 扫描训练\n含颈与眼球\n5023 顶点", fs.GREEN),
        (2019, "深度拟合", "GANFIT、MoFA\n可微渲染\n端到端回归", fs.PURPLE),
        (2021, "可动画细节", "DECA\nUV 位移图\n皱纹随表情变", fs.PINK),
        (2023, "神经参数化", "NPHM、3DGS 头像\nSDF / 高斯\n脱离固定拓扑", fs.INK),
    ]
    y = 0.5
    n = len(items)
    xs = np.linspace(0.055, 0.945, n)
    ax.plot([0.02, 0.98], [y, y], color=fs.FAINT, lw=1.4, zorder=1)
    for i, ((yr, name, sub, col), x) in enumerate(zip(items, xs)):
        above = (i % 2 == 0)
        yy = y + 0.115 if above else y - 0.115
        va = "bottom" if above else "top"
        ax.plot([x, x], [y, yy], color=fs.FAINT, lw=0.8, zorder=1)
        ax.scatter([x], [y], s=26, color=col, zorder=3, edgecolor="white", linewidth=0.9)
        fs.label(ax, x, yy + (0.015 if above else -0.015), str(yr), fs=9.4, color=col,
                 weight="bold", va=va)
        fs.label(ax, x, yy + (0.062 if above else -0.062), name, fs=8.8, color=fs.INK, va=va)
        fs.label(ax, x, yy + (0.148 if above else -0.148), sub, fs=7.6, color=fs.MUTED, va=va)
    fs.label(ax, 0.5, 0.965, "人脸参数化：二十五年的一条主线", fs=10.2, color=fs.INK, weight="bold")
    fs.label(ax, 0.5, 0.022, "（横轴按事件等间距排列，不严格对应时间比例）", fs=7.6, color=fs.FAINT)
    fs.save(fig, "ch15", "fig15-01")


def fig_linear_vs_bilinear():
    fig, ax = fs.canvas(W, 3.05)

    # 左：矩阵 / 线性 PCA
    fs.label(ax, 0.245, 0.93, "线性模型：一个方向轴", fs=9.6, color=fs.INK, weight="bold")
    # 数据矩阵
    for i in range(5):
        for j in range(3):
            ax.add_patch(plt.Rectangle((0.075 + j * 0.030, 0.60 + i * 0.030), 0.026, 0.026,
                                       facecolor="#E8EDF3", edgecolor=fs.MUTED, lw=0.4, zorder=2))
    fs.label(ax, 0.105, 0.55, "样本 $\\times$ 顶点", fs=7.6, color=fs.MUTED)
    fs.arrow(ax, (0.235, 0.675), (0.30, 0.675), color=fs.MUTED, lw=1.0)
    fs.label(ax, 0.268, 0.715, "PCA", fs=8.0, color=fs.MUTED)
    for j in range(3):
        ax.add_patch(plt.Rectangle((0.315 + j * 0.030, 0.60), 0.026, 0.15,
                                   facecolor="#FDE8D7", edgecolor=fs.ACCENT, lw=0.6, zorder=2))
    fs.label(ax, 0.36, 0.55, "基向量 $S_i$", fs=7.6, color=fs.ACCENT)
    fs.label(ax, 0.245, 0.30,
             "$S=\\bar S+\\sum_i \\alpha_i S_i$\n每个 $\\alpha_i$ 只管一条“变化方向”，\n形状与表情混在同一条轴上",
             fs=8.2)

    # 分隔
    ax.plot([0.50, 0.50], [0.08, 0.93], color=fs.GRID, lw=0.9)

    # 右：张量 / 双线性
    fs.label(ax, 0.755, 0.93, "双线性模型：两个方向轴", fs=9.6, color=fs.INK, weight="bold")
    for k in range(3):
        off = 0.026 * k
        ax.add_patch(Polygon([[0.545 + off, 0.60 + off], [0.665 + off, 0.60 + off],
                              [0.665 + off, 0.775 + off], [0.545 + off, 0.775 + off]],
                             closed=True, facecolor="#EEF0FD", edgecolor=fs.PURPLE,
                             lw=0.6, alpha=0.75, zorder=2 + k))
    fs.label(ax, 0.66, 0.545, "顶点 $\\times$ 身份 $\\times$ 表情", fs=7.6, color=fs.PURPLE)
    fs.arrow(ax, (0.735, 0.685), (0.79, 0.685), color=fs.MUTED, lw=1.0)
    fs.label(ax, 0.766, 0.645, "Tucker", fs=7.4, color=fs.MUTED)
    ax.add_patch(plt.Rectangle((0.80, 0.635), 0.055, 0.10, facecolor="#EFE7FD",
                               edgecolor=fs.PURPLE, lw=0.7, zorder=2))
    fs.label(ax, 0.8275, 0.685, "核心\n$C_r$", fs=7.4, color=fs.PURPLE)
    ax.add_patch(plt.Rectangle((0.875, 0.635), 0.026, 0.10, facecolor="#DDE7FD",
                               edgecolor=fs.BLUE, lw=0.7, zorder=2))
    fs.label(ax, 0.888, 0.60, "$w_{id}$", fs=7.4, color=fs.BLUE)
    ax.add_patch(plt.Rectangle((0.915, 0.635), 0.026, 0.10, facecolor="#DCF2E6",
                               edgecolor=fs.GREEN, lw=0.7, zorder=2))
    fs.label(ax, 0.928, 0.60, "$w_{exp}$", fs=7.4, color=fs.GREEN)
    fs.label(ax, 0.755, 0.30,
             "$V=C_r\\times_{id} w_{id}\\times_{exp} w_{exp}$\n身份与表情各自一条轴，可以单独调；\n但要求每个人有相同的“表情清单”",
             fs=8.2)

    fs.label(ax, 0.5, 0.075,
             "代价：双线性把表情离散成若干张现成脸，捕捉不到连续说话、皱眉这类过渡",
             fs=8.4, color=fs.MUTED)
    fs.save(fig, "ch15", "fig15-03")


if __name__ == "__main__":
    fig_pipeline()
    fig_timeline()
    fig_linear_vs_bilinear()
