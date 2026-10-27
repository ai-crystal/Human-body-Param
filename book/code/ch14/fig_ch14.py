# -*- coding: utf-8 -*-
"""第 14 章插图：动作先验与生成。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_pipeline():
    fig, ax = fs.canvas(6.9, 2.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fs.flow(ax, ["文本/音频\n条件", "扩散/自回归\n生成 $\\theta_{1:T}$", "SMPL 序列\n+ 根轨迹", "物理/接触\n后处理", "渲染/驱动"],
            y=0.52, h=0.30, fs=8, colors=[fs.MUTED, fs.BLUE, fs.ACCENT, fs.GREEN, fs.PURPLE])
    fs.label(ax, 0.5, 0.12, "生成的是“参数序列”而不是像素：天然带骨架、可重定向、可编辑",
             fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch14", "fig14-02")


def fig_timeline():
    fig, ax = fs.canvas(6.9, 2.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    items = [(2019, "VPoser\n姿态先验", ""), (2021, "HuMoR\n运动先验", ""),
             (2022, "MDM / MotionDiffuse\n文本生成动作", ""),
             (2023, "Physics / 接触\n可控生成", "")]
    fs.timeline(ax, items, y=0.50)
    fs.save(fig, "ch14", "fig14-01")


if __name__ == "__main__":
    fig_pipeline()
    fig_timeline()
