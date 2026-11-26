# -*- coding: utf-8 -*-
"""第 6 章插图：ASM 与 AAM 的搜索流程对照（图 6-7）。

上排是 ASM：证据来自每个关键点法线上的一维灰度剖面。
下排是 AAM：先把图像 warp 到平均形状，证据来自整块纹理的残差。
两排骨架相同（初始化 → 取证据 → 与统计模型比 → 解参数 → 判收敛），
差别在于"证据的维度"和"参数里有没有外观"。
"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

MATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fs.FIGDIR = os.path.join(MATH, "images")


def row(ax, y, labels, colors, x0=0.03, x1=0.97, h=0.125, gap=0.014,
        loop_label="未收敛：回到第 ② 步"):
    n = len(labels)
    w = (x1 - x0 - gap * (n - 1)) / n
    xs = []
    for i, (lab, c) in enumerate(zip(labels, colors)):
        x = x0 + i * (w + gap)
        fs.box(ax, x, y - h / 2, w, h, lab, fc="white", ec=c, fs=7.4, lw=1.15)
        xs.append((x, x + w))
        if i:
            fs.arrow(ax, (xs[i - 1][1] + 0.001, y), (x - 0.001, y), color=fs.FAINT, lw=1.0)
    # 回环：从最后一框底部绕回第二框（手动折线，位置可控）
    yl = y - h / 2 - 0.058
    xm = xs[-1][0] + w / 2
    xn = xs[1][0] + w / 2
    ax.plot([xm, xm, xn], [y - h / 2, yl, yl], color=fs.ACCENT, lw=1.0, zorder=2)
    fs.arrow(ax, (xn, yl), (xn, y - h / 2 - 0.004), color=fs.ACCENT, lw=1.0, z=3)
    fs.label(ax, (xn + xm) / 2, yl + 0.030, loop_label, fs=7.0, color=fs.ACCENT)
    return xs


def main():
    fig, ax = fs.canvas(7.0, 4.15)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    fs.label(ax, 0.5, 0.965,
             "同一套「证据 + 先验」的迭代，两处不同：证据多宽、参数里有没有外观",
             fs=8.8, color=fs.MUTED)

    # ---------------- ASM ----------------
    fs.label(ax, 0.03, 0.868,
             "ASM", fs=10.0, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 0.115, 0.868,
             "证据：每个点上一条 2k+1 长的灰度剖面　　先验：形状空间 P，系数裁剪到 $\\pm3\\sigma$",
             fs=7.8, color=fs.MUTED, ha="left")
    row(ax, 0.745,
        ["① 初始形状\n检测器给框", "② 沿法线采样\n$2k+1$ 个灰度",
         "③ 比平均剖面\n得建议点 $y$", "④ 投影回形状空间\n$b$ → 裁剪 → $x$",
         "⑤ 更新位姿\n$s,\\mathbf{R},\\mathbf{t}$"],
        [fs.MUTED, fs.BLUE, fs.BLUE, fs.ACCENT, fs.ACCENT])

    fs.label(ax, 0.5, 0.505,
             "证据从“每个点的一条灰度”扩到“整张脸的纹理”：判别力变强，参数翻倍，优化变难",
             fs=8.0, color=fs.INK)

    # ---------------- AAM ----------------
    fs.label(ax, 0.03, 0.432,
             "AAM", fs=10.0, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 0.115, 0.432,
             "证据：形状归一化后的整块纹理残差　　　先验：形状与外观的联合空间，两组系数同时裁剪",
             fs=7.8, color=fs.MUTED, ha="left")
    row(ax, 0.310,
        ["① 初始形状", "② warp 到\n平均形状", "③ 整块纹理\n与残差图",
         "④ 同解形状、外观\n与位姿", "⑤ 渲染比对\n$\\|\\mathbf{A}-\\mathbf{I}\\|^2$"],
        [fs.MUTED, fs.GREEN, fs.GREEN, fs.PURPLE, fs.PURPLE])

    fs.label(ax, 0.5, 0.072,
             "两排的第 ④ 步都是“投影”：ASM 投到形状空间，AAM 投到形状 × 外观的联合空间",
             fs=7.8, color=fs.MUTED)

    fs.save(fig, "ch06", "fig06-05")


if __name__ == "__main__":
    main()
