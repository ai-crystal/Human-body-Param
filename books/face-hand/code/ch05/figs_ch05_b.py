# -*- coding: utf-8 -*-
"""第 5 章补充插图：16 关节 × 3 参数 = 48，与解剖上真正可动的自由度。"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, "E:/Study/人体参数化技术/人体参数化技术学习/books/code")
import figstyle as fs

fs.FIGDIR = "E:/Study/人体参数化技术/人体参数化技术学习/books/face-hand/images"

# 每行：关节名，以及三个轴角分量在解剖上是否有意义（2 = 主要自由度，1 = 有限，0 = 几乎不用）
ROWS = [
    ("0  腕", [2, 2, 1]),
    ("1  食指 MCP", [2, 1, 1]), ("2  食指 PIP", [2, 0, 0]), ("3  食指 DIP", [2, 0, 0]),
    ("4  中指 MCP", [2, 1, 1]), ("5  中指 PIP", [2, 0, 0]), ("6  中指 DIP", [2, 0, 0]),
    ("7  小指 MCP", [2, 1, 1]), ("8  小指 PIP", [2, 0, 0]), ("9  小指 DIP", [2, 0, 0]),
    ("10 无名指 MCP", [2, 1, 1]), ("11 无名指 PIP", [2, 0, 0]), ("12 无名指 DIP", [2, 0, 0]),
    ("13 拇指 CMC", [1, 2, 1]), ("14 拇指 MCP", [2, 1, 0]), ("15 拇指 IP", [2, 0, 0]),
]

COL = {2: "#DCF2E6", 1: "#FDF0D5", 0: "#EFEFEF"}
EDG = {2: fs.GREEN, 1: fs.GOLD, 0: "#D1D5DB"}


def fig_joint_params():
    fig, ax = fs.canvas(6.6, 5.0)
    fs.label(ax, 0.5, 0.972, "48 个姿态参数，解剖上真正有意义的不到三十个",
             fs=10.2, color=fs.INK, weight="bold")
    fs.label(ax, 0.5, 0.930, "每行一个关节，三列对应轴角向量的三个分量（示意划分）",
             fs=8.2, color=fs.MUTED)

    x0, y0 = 0.325, 0.115
    cw, ch = 0.115, 0.0455
    heads = ["屈伸\nflex", "外展/内收\nabduct", "扭转\ntwist"]
    for j, h in enumerate(heads):
        fs.label(ax, x0 + cw * (j + 0.5), y0 + ch * 16 + 0.032, h, fs=7.6, color=fs.INK)

    for i, (name, vals) in enumerate(ROWS):
        y = y0 + ch * (15 - i)
        fs.label(ax, x0 - 0.015, y + ch / 2, name, fs=7.6, color=fs.INK, ha="right")
        for j, v in enumerate(vals):
            ax.add_patch(Rectangle((x0 + cw * j + 0.003, y + 0.003), cw - 0.006, ch - 0.006,
                                   facecolor=COL[v], edgecolor=EDG[v], lw=0.7, zorder=2))

    # 右侧统计
    n2 = sum(v.count(2) for _, v in ROWS)
    n1 = sum(v.count(1) for _, v in ROWS)
    fs.box(ax, 0.700, 0.560, 0.275, 0.180,
           "绿：主要自由度  %d\n黄：有限转动      %d\n灰：几乎不动      %d"
           % (n2, n1, 48 - n2 - n1), ec=fs.FAINT, fs=8.0, lw=0.8)
    fs.box(ax, 0.700, 0.320, 0.275, 0.190,
           "MANO 用 48 个数\n粗算的自由度约 21 个\n→ 过参数化两倍多",
           ec=fs.ACCENT, fs=8.2)
    fs.label(ax, 0.700, 0.265,
             "补救：姿态 PCA 压到 6 维，\n再加较强的正则", fs=7.8, color=fs.MUTED, ha="left")

    fs.label(ax, 0.06, 0.045,
             "灰色的组合在解剖上不可能出现，但优化时仍会被尝试；\n"
             "这就是 MANO 必须依赖先验与正则的原因。",
             fs=7.8, color=fs.MUTED, ha="left")
    fs.save(fig, "ch05", "fig05-02")


if __name__ == "__main__":
    fig_joint_params()
