# -*- coding: utf-8 -*-
"""第 13 章插图：着装人体与神经表示。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_spectrum():
    fig, ax = fs.canvas(6.9, 3.0)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    xs = [0.02 + i * 0.196 for i in range(5)]
    names = ["参数化网格\nSMPL", "加位移\nCAPE/ARCH", "隐式表面\nPIFu/SNARF", "神经辐射场\nHumanNeRF", "3D 高斯\nSplatting"]
    cols = [fs.BLUE, fs.GREEN, fs.PURPLE, fs.GOLD, fs.ACCENT]
    for i, (x, n, c) in enumerate(zip(xs, names, cols)):
        fs.box(ax, x, 0.40, 0.175, 0.26, n, fc="white", ec=c, fs=8.2)
        if i:
            fs.arrow(ax, (x - 0.02, 0.53), (x, 0.53), color=fs.FAINT)
    ax.annotate("", xy=(0.98, 0.28), xytext=(0.02, 0.28),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0))
    fs.label(ax, 0.5, 0.20, "可控性 / 可驱动性  ←——→  真实感 / 细节", fs=8.4, color=fs.MUTED)
    fs.label(ax, 0.5, 0.86, "人体表示的光谱：从“可动的骨架”到“照片级的外观”", fs=9.6)
    fs.label(ax, 0.13, 0.74, "优点：实时、可编辑", fs=7.8, color=fs.BLUE, ha="center")
    fs.label(ax, 0.85, 0.74, "优点：细节、真实感", fs=7.8, color=fs.ACCENT, ha="center")
    fs.label(ax, 0.5, 0.06, "实际系统常常混合：用 SMPL 驱动，用神经场/高斯补细节", fs=8, color=fs.MUTED)
    fs.save(fig, "ch13", "fig13-01")


def fig_pipeline():
    fig, ax = fs.canvas(6.9, 2.4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fs.flow(ax, ["多视角/\n视频", "SMPL 拟合\n(姿态+体型)", "残差/位移\n学习", "纹理与光照\n分离", "可驱动\nAvatar"],
            y=0.52, h=0.30, fs=8.2, colors=[fs.MUTED, fs.BLUE, fs.GREEN, fs.GOLD, fs.ACCENT])
    fs.label(ax, 0.5, 0.12, "关键：把“人”与“衣服/头发/光照”分开，才能换装、换姿势、换视角",
             fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch13", "fig13-02")


if __name__ == "__main__":
    fig_spectrum()
    fig_pipeline()
