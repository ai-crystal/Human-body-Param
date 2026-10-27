# -*- coding: utf-8 -*-
"""第 25 章插图：生成模型与基础模型。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import figstyle as fs


def fig_diffusion():
    fig, ax = fs.canvas(6.9, 2.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    rng = np.random.default_rng(3)
    n = 7
    for i in range(n):
        x = 0.08 + i * 0.13
        k = i if i < 4 else 6 - i          # 0,1,2,3,2,1,0
        sd = 0.012 + 0.016 * k
        pts = rng.normal(0, sd, (40, 2)) + np.array([x, 0.55])
        col = fs.BLUE if i <= 3 else fs.ACCENT
        ax.scatter(pts[:, 0], pts[:, 1], s=4, color=col, alpha=0.55, linewidths=0)
        fs.label(ax, x, 0.30, f"$t={i}$" if i <= 3 else f"$t={6-i}$", fs=7.5, color=col)
    fs.arrow(ax, (0.02, 0.22), (0.46, 0.22), color=fs.MUTED)
    fs.label(ax, 0.24, 0.14, "前向：逐步加噪", fs=8.2, color=fs.BLUE)
    fs.arrow(ax, (0.54, 0.22), (0.98, 0.22), color=fs.MUTED)
    fs.label(ax, 0.76, 0.14, "反向：学习去噪", fs=8.2, color=fs.ACCENT)
    fs.label(ax, 0.5, 0.93, "扩散模型：把“生成”变成“逐步去噪”", fs=9.8)
    fs.label(ax, 0.5, 0.04, "条件（文本/图像/骨架）在每一步注入，控制去噪方向", fs=8, color=fs.MUTED)
    fs.save(fig, "ch25", "fig25-01")


def fig_timeline():
    fig, ax = fs.canvas(6.9, 2.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    items = [(2020, "NeRF / PIFu\n神经表示", ""), (2022, "HumanNeRF\n4D 重建", ""),
             (2022, "DreamFusion\nSDS 文生 3D", ""), (2023, "3DGS\n实时渲染", ""),
             (2024, "SMPLer-X / Multi-HMR\n基础模型化", "")]
    fs.timeline(ax, items, y=0.50, fs=7.8)
    fs.save(fig, "ch25", "fig25-02")


def fig_stack():
    fig, ax = fs.canvas(6.9, 3.0)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    layers = [("应用层：数字人 / 游戏 / 影视 / 医疗", 0.74, fs.PURPLE),
              ("生成层：扩散 / 3DGS / 神经场", 0.56, fs.ACCENT),
              ("参数层：SMPL-X / FLAME / MANO / SMAL", 0.38, fs.GREEN),
              ("感知层：ViT / SAM / 深度 / 光流", 0.20, fs.BLUE)]
    for txt, y, c in layers:
        fs.box(ax, 0.08, y, 0.84, 0.13, txt, fc="white", ec=c, fs=9)
    for y in [0.33, 0.51, 0.69]:
        fs.arrow(ax, (0.5, y + 0.005), (0.5, y + 0.06), color=fs.FAINT, lw=1.1)
    fs.label(ax, 0.5, 0.95, "现代人体系统的四层栈", fs=9.8)
    fs.label(ax, 0.5, 0.06, "越往下越通用，越往上越贴近应用；参数层是“共同语言”", fs=8, color=fs.MUTED)
    fs.save(fig, "ch25", "fig25-03")


if __name__ == "__main__":
    fig_diffusion()
    fig_timeline()
    fig_stack()
