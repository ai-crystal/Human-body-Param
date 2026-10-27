# -*- coding: utf-8 -*-
"""第 9 章插图：SMPL 家族。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_timeline():
    fig, ax = fs.canvas(6.9, 2.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    items = [(2015, "SMPL\n身体"), (2017, "SMPL+H\n+ 手"), (2019, "SMPL-X\n+ 脸"),
             (2020, "STAR\n稀疏关节"), (2020, "GHUM\n连续尺度")]
    fs.timeline(ax, items, y=0.50)
    fs.save(fig, "ch09", "fig09-01")


def fig_smplx():
    fig, ax = fs.canvas(6.9, 3.1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fs.box(ax, 0.06, 0.42, 0.26, 0.30, "身体\n$\\beta\\in\\mathbb{R}^{10}$\n$\\theta_{body}$", fc="#EEF2FF", ec=fs.BLUE, fs=8.4)
    fs.box(ax, 0.37, 0.42, 0.26, 0.30, "手\n每手 15 关节\n$\\theta_{hand}$", fc="#ECFDF5", ec=fs.GREEN, fs=8.4)
    fs.box(ax, 0.68, 0.42, 0.26, 0.30, "脸\n$\\psi\\in\\mathbb{R}^{10}$\n下颌 / 眼球", fc="#FDF6EC", ec=fs.ACCENT, fs=8.4)
    fs.arrow(ax, (0.32, 0.57), (0.37, 0.57), color=fs.FAINT)
    fs.arrow(ax, (0.63, 0.57), (0.68, 0.57), color=fs.FAINT)
    fs.box(ax, 0.25, 0.10, 0.50, 0.16, "统一网格：10475 顶点 / 54 关节", fc="white", ec=fs.PURPLE, fs=9)
    for x in [0.19, 0.50, 0.81]:
        fs.arrow(ax, (x, 0.42), (0.50, 0.26), color=fs.FAINT, rad=0.0)
    fs.label(ax, 0.5, 0.92, "SMPL-X：身体、手、脸共享一套 LBS 与网格", fs=9.8)
    fs.label(ax, 0.5, 0.03, "代价：参数更多、拟合更难、手脸数据更稀缺", fs=8, color=fs.MUTED)
    fs.save(fig, "ch09", "fig09-02")


def fig_param_ledger():
    """图 9-3：54 个关节与 119 个参数的对账。"""
    fig, ax = fs.canvas(6.9, 3.3)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fs.label(ax, 0.5, 0.945, "上排：关节（每个用轴角占 3 维）　下排：模型文件里真正存的参数",
             fs=9.0)

    # 上排：关节构成
    fs.box(ax, 0.035, 0.58, 0.26, 0.22, "身体关节 21（含根）\n×3 = 63 维",
           fc="#EEF2FF", ec=fs.BLUE, fs=8.6)
    fs.box(ax, 0.315, 0.58, 0.25, 0.22, "面部关节 3\n下颌 + 双眼，×3 = 9 维",
           fc="#FDF6EC", ec=fs.ACCENT, fs=8.4)
    fs.box(ax, 0.585, 0.58, 0.37, 0.22, "手指关节 30（每手 15）\n×3 = 90 维",
           fc="#ECFDF5", ec=fs.GREEN, fs=8.6)

    # 下排：参数构成
    fs.box(ax, 0.035, 0.22, 0.26, 0.22, "身体姿态 75 维\n63 + 9 + 全局旋转 3",
           fc="white", ec=fs.BLUE, fs=8.4)
    fs.box(ax, 0.315, 0.22, 0.22, 0.22, "手指 PCA 24 维\n90 → 24（每手 12）",
           fc="white", ec=fs.PURPLE, fs=8.4)
    fs.box(ax, 0.565, 0.22, 0.18, 0.22, "形状\n10 维", fc="white", ec=fs.GOLD, fs=8.6)
    fs.box(ax, 0.775, 0.22, 0.18, 0.22, "表情\n10 维", fc="white", ec=fs.GOLD, fs=8.6)

    # 合并与压缩
    fs.arrow(ax, (0.14, 0.58), (0.14, 0.445), color=fs.BLUE, lw=1.0)
    fs.arrow(ax, (0.40, 0.58), (0.23, 0.447), color=fs.ACCENT, lw=1.0, rad=0.18, z=6)
    fs.arrow(ax, (0.70, 0.575), (0.445, 0.448), color=fs.GREEN, lw=1.0, rad=-0.12, z=6)

    fs.label(ax, 0.5, 0.085,
             "手指的 90 维被 MANO 的 PCA 压成 24 维；形状与表情直接乘主成分加到模板上，不经过关节",
             fs=8.2, color=fs.MUTED)
    fs.label(ax, 0.5, 0.015, "合计 75 + 24 + 10 + 10 = 119 维", fs=8.8, color=fs.INK)
    fs.save(fig, "ch09", "fig09-03")


if __name__ == "__main__":
    fig_timeline()
    fig_smplx()
    fig_param_ledger()
