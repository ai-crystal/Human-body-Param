# -*- coding: utf-8 -*-
"""第 7 章插图：SCAPE 的形状/姿态分解。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_pipeline():
    fig, ax = fs.canvas(6.9, 2.5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fs.box(ax, 0.02, 0.40, 0.16, 0.28, "模板网格\n(统一拓扑)", fc="#F9FAFB", ec=fs.MUTED, fs=8.2)
    fs.box(ax, 0.23, 0.40, 0.17, 0.28, "形状变形\n$\\mathbf{D}_S(\\beta)$", fc="#EEF2FF", ec=fs.BLUE, fs=8.2)
    fs.box(ax, 0.45, 0.40, 0.17, 0.28, "姿态变形\n$\\mathbf{D}_P(\\theta)$", fc="#ECFDF5", ec=fs.GREEN, fs=8.2)
    fs.box(ax, 0.67, 0.40, 0.15, 0.28, "拼接\n$Q\\mathbf{s}+\\mathbf{d}$", fc="#FDF6EC", ec=fs.ACCENT, fs=8.0)
    fs.box(ax, 0.86, 0.40, 0.12, 0.28, "人体\n实例", fc="white", ec=fs.PURPLE, fs=8.4)
    for x in [0.18, 0.40, 0.62, 0.82]:
        fs.arrow(ax, (x, 0.54), (x + 0.045, 0.54), color=fs.FAINT)
    fs.label(ax, 0.50, 0.85, "SCAPE：把“体型”与“姿势”拆成两套变形", fs=10)
    fs.label(ax, 0.315, 0.30, "每个人一套\n低维系数", fs=7.6, color=fs.BLUE)
    fs.label(ax, 0.535, 0.30, "每个三角形\n随关节角变化", fs=7.6, color=fs.GREEN)
    fs.label(ax, 0.5, 0.10, "关键区别：形状变形作用在顶点上，姿态变形作用在三角形的局部坐标系上",
             fs=8, color=fs.MUTED)
    fs.save(fig, "ch07", "fig07-01")


def fig_factorization():
    fig, ax = fs.canvas(6.9, 3.2)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    # 2x2
    titles = ["同一个人，不同姿势", "不同的人，同一姿势", "不同的人，不同姿势"]
    poses = [dict(l_arm=0.9, r_arm=0.2, l_leg=0.3), {}, dict(l_arm=1.1, r_arm=0.5, l_leg=0.4)]
    for i in range(3):
        cx = 0.20 + i * 0.30
        fs.human(ax, cx=cx, cy=0.55, s=0.62, pose=poses[i], width=1.0 - 0.12 * (i == 1),
                 color=[fs.BLUE, fs.ACCENT, fs.GREEN][i])
        fs.label(ax, cx, 0.20, titles[i], fs=8.4, color=fs.MUTED)
    fs.label(ax, 0.5, 0.90, "SCAPE 的分解假设：体型参数与姿势参数可以独立变化", fs=9.8)
    fs.label(ax, 0.5, 0.06, "这个假设让“换个人做同一个动作”变成两次参数替换", fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch07", "fig07-02")


def fig_timeline():
    fig, ax = fs.canvas(6.9, 2.4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    items = [(2003, "Allen 等\n人体形状空间", ""), (2005, "SCAPE\n形状/姿态分解", ""),
             (2009, "Hasler 等\n姿态+体型统计", ""), (2014, "FAUST\n对应基准", ""),
             (2015, "SMPL\n实时 LBS 模型", "")]
    fs.timeline(ax, items, y=0.52)
    ax.set_ylim(0, 1)
    fs.save(fig, "ch07", "fig07-03")


if __name__ == "__main__":
    fig_pipeline()
    fig_factorization()
    fig_timeline()
