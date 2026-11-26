# -*- coding: utf-8 -*-
"""第 7 章新插图：三种耦合方式（先估手再估物 / 联合优化 / 生成式先验）。"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import figstyle as fs

fs.FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "images")


def _panel(fig, rect, title, color, note):
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.5, 0.985, title, fontsize=8.4, ha="center", va="top", weight="bold",
            color=color)
    ax.text(0.5, 0.015, note, fontsize=6.9, color=fs.MUTED, ha="center", va="bottom")
    return ax


def fig07_03():
    fig = plt.figure(figsize=(6.8, 3.5))
    fig.text(0.02, 0.985, "手与物体的三种耦合方式", fontsize=9.8, weight="bold")

    # ---------------- ① 先估手，再估物 -------------------------
    ax = _panel(fig, [0.015, 0.06, 0.31, 0.86], "① 先估手，再估物", fs.BLUE,
                "误差不互补：两处各错一点")
    fs.box(ax, 0.20, 0.80, 0.60, 0.11, "单目图像", ec=fs.INK, fs=7.2)
    fs.box(ax, 0.02, 0.60, 0.45, 0.12, "手部网络", ec=fs.BLUE, fs=7.2)
    fs.box(ax, 0.53, 0.60, 0.45, 0.12, "物体位姿", ec=fs.BLUE, fs=7.2)
    fs.arrow(ax, (0.36, 0.795), (0.24, 0.725), color=fs.FAINT)
    fs.arrow(ax, (0.64, 0.795), (0.76, 0.725), color=fs.FAINT)
    fs.box(ax, 0.06, 0.36, 0.88, 0.12, "后处理：尺度 / 接触 / 支撑", ec=fs.MUTED, fs=7.0)
    fs.arrow(ax, (0.245, 0.595), (0.30, 0.485), color=fs.FAINT)
    fs.arrow(ax, (0.755, 0.595), (0.70, 0.485), color=fs.FAINT)
    fs.box(ax, 0.22, 0.14, 0.56, 0.11, "手 + 物体位姿", ec=fs.INK, fs=7.2)
    fs.arrow(ax, (0.50, 0.355), (0.50, 0.255), color=fs.FAINT)

    # ---------------- ② 联合优化 -------------------------------
    ax = _panel(fig, [0.345, 0.06, 0.31, 0.86], "② 联合优化", fs.ACCENT,
                "误差能互补，代价是迭代")
    fs.box(ax, 0.20, 0.80, 0.60, 0.11, "单目图像", ec=fs.INK, fs=7.2)
    fs.box(ax, 0.14, 0.62, 0.72, 0.11, "初值：手 + 物", ec=fs.MUTED, fs=7.2)
    fs.arrow(ax, (0.50, 0.795), (0.50, 0.735), color=fs.FAINT)
    for i, lab in enumerate(["重投影", "接触", "穿透"]):
        fs.box(ax, 0.03 + i * 0.33, 0.40, 0.29, 0.13, lab, ec=fs.ACCENT, fs=7.0)
        if i:
            fs.arrow(ax, (0.03 + i * 0.33 - 0.035, 0.465),
                     (0.03 + i * 0.33 - 0.004, 0.465), color=fs.ACCENT, style="<|-|>",
                     lw=0.9, ms=6)
    fs.arrow(ax, (0.50, 0.615), (0.50, 0.535), color=fs.FAINT)
    # 迭代回路
    ax.plot([0.955, 0.985, 0.985, 0.015, 0.015, 0.045], [0.465, 0.465, 0.305, 0.305, 0.465, 0.465],
            color=fs.ACCENT, lw=0.9, ls=(0, (2.5, 2)), zorder=2)
    fs.label(ax, 0.50, 0.355, "迭代 T 轮", fs=6.8, color=fs.ACCENT)
    fs.box(ax, 0.22, 0.085, 0.56, 0.11, "手 + 物体位姿", ec=fs.INK, fs=7.2)
    ax.annotate("", xy=(0.50, 0.20), xytext=(0.50, 0.30),
                arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=1.0))

    # ---------------- ③ 生成式先验 -----------------------------
    ax = _panel(fig, [0.675, 0.06, 0.31, 0.86], "③ 生成式先验", fs.GREEN,
                "覆盖广，真实度取决于仿真器")
    fs.box(ax, 0.06, 0.80, 0.88, 0.11, "物体库 + 仿真抓取", ec=fs.GREEN, fs=7.0)
    fs.box(ax, 0.06, 0.63, 0.88, 0.11, "合成图像 + 标注", ec=fs.GREEN, fs=7.0)
    fs.box(ax, 0.06, 0.46, 0.88, 0.11, "训练（权重里带先验）", ec=fs.GREEN, fs=7.0)
    fs.box(ax, 0.06, 0.26, 0.42, 0.11, "单目图像", ec=fs.INK, fs=7.0)
    fs.box(ax, 0.54, 0.26, 0.40, 0.11, "一次前向", ec=fs.GREEN, fs=7.0)
    fs.arrow(ax, (0.50, 0.795), (0.50, 0.745), color=fs.FAINT)
    fs.arrow(ax, (0.50, 0.625), (0.50, 0.575), color=fs.FAINT)
    fs.arrow(ax, (0.50, 0.455), (0.74, 0.375), color=fs.FAINT)
    fs.arrow(ax, (0.48, 0.315), (0.535, 0.315), color=fs.FAINT)
    fs.box(ax, 0.22, 0.09, 0.56, 0.10, "手 + 物体位姿", ec=fs.INK, fs=7.2)
    fs.arrow(ax, (0.74, 0.255), (0.60, 0.195), color=fs.FAINT)

    fs.save(fig, "ch07", "fig07-03", dpi=230)


if __name__ == "__main__":
    fig07_03()
