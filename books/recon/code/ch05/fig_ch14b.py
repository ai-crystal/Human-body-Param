# -*- coding: utf-8 -*-
"""第 5 章补充插图：把“可信 vs 多样”的权衡量化（图 5-3）。

横轴是引导强度 w（或物理约束权重）。三条曲线同向不同步：
对齐度上升并饱和，多样性下降，物理错误率下降。
"""
import sys
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = r"E:\Study\人体参数化技术\人体参数化技术学习\books\recon\images"


def fig_tradeoff():
    fig, ax = plt.subplots(figsize=(6.9, 3.1))
    fig.subplots_adjust(left=0.085, right=0.965, top=0.84, bottom=0.28)

    w = np.linspace(1, 10, 200)
    align = 0.42 + 0.50 * (1 - np.exp(-(w - 1) / 2.2))          # 文本对齐：先升后饱和
    divers = 1.00 - 0.11 * (w - 1)                             # 多样性：线性下降
    physical = 0.62 * np.exp(-(w - 1) / 3.0) + 0.06            # 物理错误率：下降

    ax.plot(w, align, color=fs.BLUE, lw=1.8, label="文本对齐度 ↑ 越好")
    ax.plot(w, divers, color=fs.ACCENT, lw=1.8, label="内部多样性 ↑ 越好")
    ax.plot(w, physical, color=fs.GREEN, lw=1.8, label="物理错误率 ↓ 越好")

    ax.axvspan(3.2, 5.5, color=fs.GOLD, alpha=0.10, zorder=0)
    ax.text(4.35, 1.03, "典型可选区间", fontsize=7.6, color=fs.GOLD, ha="center")

    ax.set_xlim(1, 10); ax.set_ylim(0, 1.10)
    ax.set_xlabel("引导强度 $w$（或物理约束权重）", fontsize=8.6)
    ax.set_ylabel("归一化指标（示意）", fontsize=8.6)
    ax.set_title("一个旋钮，三条曲线：调参就是在这三条线之间选点", fontsize=9.2, pad=8)
    ax.legend(fontsize=7.6, loc="center right", ncol=1)
    ax.tick_params(labelsize=7.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.annotate("$w$ 过大：动作僵硬、过饱和", xy=(8.6, align.max() + 0.02),
                xytext=(6.0, 0.34), fontsize=7.4, color=fs.MUTED,
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=0.7))

    fig.text(0.5, 0.07,
             "示意曲线：真实数值取决于模型与数据集，但三条线的方向在多篇工作里一致",
             fontsize=7.8, color=fs.MUTED, ha="center")
    fs.save(fig, "ch05", "fig05-03")


if __name__ == "__main__":
    fig_tradeoff()
