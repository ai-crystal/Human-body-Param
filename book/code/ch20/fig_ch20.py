# -*- coding: utf-8 -*-
"""第 20 章插图：四种重建范式、时间线、FreiHAND 上的公开结果。"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import figstyle as fs


def _panel(fig, rect, title, sub, boxes, color, loop=False):
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.02, 0.93, title, fontsize=8.8, color=color, weight="bold", ha="left")
    ax.text(0.02, 0.80, sub, fontsize=7.2, color=fs.MUTED, ha="left")

    n = len(boxes)
    w = (0.96 - 0.035 * (n - 1)) / n
    for i, txt in enumerate(boxes):
        x = 0.02 + i * (w + 0.035)
        fs.box(ax, x, 0.26, w, 0.24, txt, ec=color, fs=7.0)
        if i:
            fs.arrow(ax, (x - 0.032, 0.38), (x - 0.004, 0.38), color=fs.FAINT, lw=0.9)
    if loop:
        x0 = 0.02 + (n - 1) * (w + 0.035) + w / 2
        x1 = 0.02 + (n - 2) * (w + 0.035) + w / 2
        ax.plot([x0, x0, x1], [0.25, 0.10, 0.10], color=fs.ACCENT, lw=1.0,
                linestyle=(0, (2.5, 2)), zorder=2)
        ax.annotate("", xy=(x1, 0.255), xytext=(x1, 0.11),
                    arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.0,
                                    linestyle=(0, (2.5, 2))))
        ax.text((x0 + x1) / 2, 0.005, "迭代直到收敛", fontsize=7.0, color=fs.ACCENT, ha="center")
    return ax


def fig20_01():
    fig = plt.figure(figsize=(6.6, 3.0))
    fig.text(0.02, 0.965, "四种范式：监督信号与计算路径的差别", fontsize=9.8, weight="bold")

    _panel(fig, [0.01, 0.54, 0.48, 0.40], "① 优化式拟合（2010–2016）",
           "把参数当未知数，反复渲染比对",
           ["深度图", "渲染手模型", "算残差", "更新参数"], fs.GOLD, loop=True)
    _panel(fig, [0.51, 0.54, 0.48, 0.40], "② 参数回归（2019）",
           "一次前向出参数，解码器固定可微",
           ["RGB 图", "CNN 编码器", "β / θ / π", "MANO 网格"], fs.BLUE)
    _panel(fig, [0.01, 0.04, 0.48, 0.40], "③ 顶点 / 热图回归（2020–2021）",
           "绕开参数，直接回归几何",
           ["RGB 图", "特征图", "lixel 热图", "顶点坐标"], fs.GREEN)
    _panel(fig, [0.51, 0.04, 0.48, 0.40], "④ Transformer（2021–2023）",
           "图像块与顶点 token 一起做注意力",
           ["RGB 图", "ViT 图块", "token 注意力", "β / θ / π"], fs.PURPLE)

    fs.save(fig, "ch20", "fig20-01")


def fig20_02():
    fig, ax = fs.canvas(6.6, 4.2, xlim=(0, 1), ylim=(0, 1))
    fs.label(ax, 0.04, 0.955, "单手重建的时间线：两个转折点", fs=9.8, ha="left", weight="bold")

    items = [
        (2016, "优化式拟合", "深度图 / 多视角；粒子群等在参数空间里搜索", False),
        (2017, "MANO", "手部统计模型；从此有了可微、低维的手模型", False),
        (2019, "端到端回归", "Boukhayma 等；固定可微解码器 + 二维/三维弱监督", True),
        (2020, "lixel 热图", "I2L-MeshNet；逐顶点一维热图，绕开参数回归", True),
        (2020, "全身一体化", "FrankMocap；回归模块 + 整合模块，手与身体一起出", True),
        (2021, "图网络 + 注意力", "Mesh Graphormer、PyMAF；局部卷积 + 全局对齐反馈", True),
        (2023, "规模化", "HaMeR；270 万训练样本 + ViT，赢在野外泛化", True),
    ]
    x_line = 0.135
    ax.plot([x_line, x_line], [0.055, 0.885], color=fs.GRID, lw=1.4, zorder=1)

    step = 0.118
    for i, (yr, name, desc, stop) in enumerate(items):
        y = 0.860 - i * step
        c = fs.ACCENT if stop else fs.MUTED
        ax.scatter([x_line], [y], s=34, color=c, zorder=4, edgecolor="white", linewidth=1.0)
        fs.label(ax, x_line - 0.022, y, str(yr), fs=8.2, color=c, ha="right", weight="bold")
        fs.box(ax, 0.165, y - 0.042, 0.815, 0.084, "", fc="#FFFFFF", ec=fs.GRID, lw=0.8, z=2)
        fs.label(ax, 0.180, y + 0.017, name, fs=8.4, color=c if stop else fs.INK,
                 ha="left", weight="bold")
        fs.label(ax, 0.180, y - 0.020, desc, fs=7.2, color=fs.MUTED, ha="left")

    fs.label(ax, 0.04, 0.020,
             "灰色：同一时期的旁支与铺垫；橙色：本章重点讨论的工作",
             fs=7.2, color=fs.MUTED, ha="left")

    fs.save(fig, "ch20", "fig20-02")


def fig20_03():
    # 数值取自 HaMeR 论文 Table 1（FreiHAND，PA-MPJPE，毫米，越小越好）
    data = [("MobRecon (2021)", 5.7),
            ("Mesh Graphormer (2021)", 5.9),
            ("HaMeR (2023)", 6.0),
            ("METRO (2021)", 6.5),
            ("I2L-MeshNet (2020)", 7.4),
            ("Pose2Mesh (2020)", 7.7)]

    fig, ax = fs.new(6.6, 3.0)
    x0 = 5.2
    for i, (name, v) in enumerate(data):
        c = fs.ACCENT if name.startswith("HaMeR") else "#B6C2D1"
        ax.plot([x0, v], [i, i], color=c, lw=1.6, zorder=2, solid_capstyle="round")
        ax.scatter([v], [i], s=70, color=c, zorder=3, edgecolor="white", linewidth=1.2)
        ax.text(v + 0.10, i, f"{v:.1f}", va="center", fontsize=8.6,
                color=fs.INK, zorder=4)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([d[0] for d in data], fontsize=8.4)
    ax.set_xlim(x0, 8.6)
    ax.set_ylim(-0.7, len(data) - 0.3)
    ax.set_xticks([5.5, 6.0, 6.5, 7.0, 7.5, 8.0])
    ax.set_xlabel("PA-MPJPE（毫米，越小越好）", fontsize=8.8)
    ax.set_title("FreiHAND 测试集：2021 年之后基本不再下降", fontsize=9.4, loc="left", pad=8)
    fs.clean(ax, grid=False, spines=("bottom",))
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", labelsize=7.8)

    ax.annotate("2021 年的最好成绩 5.7", xy=(5.7, 0), xytext=(6.25, -0.45),
                fontsize=7.2, color=fs.MUTED,
                arrowprops=dict(arrowstyle="-", color=fs.FAINT, lw=0.8))
    ax.annotate("HaMeR 误差略高，\n但野外泛化强得多", xy=(6.0, 2), xytext=(6.55, 2.05),
                fontsize=7.2, color=fs.ACCENT,
                arrowprops=dict(arrowstyle="-", color=fs.FAINT, lw=0.8))

    fs.save(fig, "ch20", "fig20-03")


if __name__ == "__main__":
    fig20_01()
    fig20_02()
    fig20_03()
