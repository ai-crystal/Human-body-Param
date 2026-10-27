# -*- coding: utf-8 -*-
"""第 27 章插图：四次范式转移。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_paradigm():
    fig, ax = fs.canvas(6.9, 3.2)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    stages = [
        ("1995–2005\n统计形状", "ASM · AAM\n3DMM · SCAPE", fs.BLUE),
        ("2005–2015\n参数化 + 蒙皮", "SMPL · FAUST\n形状/姿态分离", fs.GREEN),
        ("2016–2020\n学习回归", "SMPLify · HMR\nSPIN · DECA", fs.ACCENT),
        ("2021– 至今\n神经与生成", "NeRF · 3DGS\n扩散 · 基础模型", fs.PURPLE),
    ]
    w = 0.215
    for i, (title, body, c) in enumerate(stages):
        x = 0.02 + i * 0.245
        fs.box(ax, x, 0.42, w, 0.34, "", fc="white", ec=c, lw=1.5)
        fs.label(ax, x + w / 2, 0.66, title, fs=8.6, color=c, weight="bold")
        fs.label(ax, x + w / 2, 0.50, body, fs=8.0, color=fs.INK)
        if i:
            fs.arrow(ax, (x - 0.028, 0.59), (x - 0.002, 0.59), color=fs.FAINT, lw=1.1)
    fs.label(ax, 0.5, 0.88, "四次范式转移：从“手工统计”到“可学习的先验”", fs=9.8)
    fs.label(ax, 0.5, 0.18, "每一次转移都不是推翻前一次，而是把前一次变成新系统的“表示层”",
             fs=8.4, color=fs.MUTED)
    fs.label(ax, 0.5, 0.08, "今天的模型仍然在用 PCA、LBS、最小二乘——只是外面包了一层神经网络",
             fs=8.0, color=fs.MUTED)
    fs.save(fig, "ch27", "fig27-01")


if __name__ == "__main__":
    fig_paradigm()
