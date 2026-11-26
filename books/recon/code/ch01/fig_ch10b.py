# -*- coding: utf-8 -*-
"""第 1 章补充插图：尺度—深度歧义的几何（图 1-4）。

左：两种 (身高, 深度) 解释产生完全相同的图像——单帧无法区分。
右：把重投影误差画成身高假设的函数，谷底是一片平台；
    最优点由形状先验决定，而不是由图像决定。
"""
import sys
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = r"E:\Study\人体参数化技术\人体参数化技术学习\books\recon\images"

F_PX = 1000.0          # 焦距（像素）
H_PX = 425.0           # 人在图像里占的高度（像素）
K = H_PX / F_PX        # 身高 / 深度，恒定


def fig_scale_depth():
    fig = plt.figure(figsize=(6.9, 3.25))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.87, bottom=0.24)

    # ---------------- 左：两张一模一样的“图” ----------------
    ax = fig.add_axes([0.015, 0.13, 0.50, 0.72])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fs.label(ax, 0.5, 0.965, "两个假设，同一张像素阵列", fs=9.0)

    frames = [(0.04, fs.BLUE, "假设 A\n$h$=1.70 m，$Z$=4.0 m"),
              (0.56, fs.GREEN, "假设 B\n$h$=1.87 m，$Z$=4.4 m")]
    for x0, c, cap in frames:
        ax.add_patch(plt.Rectangle((x0, 0.34), 0.40, 0.54, facecolor="#F4F6FA",
                                   edgecolor=c, lw=1.1, zorder=1))
        fs.human(ax, cx=x0 + 0.20, cy=0.50, s=0.40, color=c, alpha=0.85, z=3, width=0.80)
        fs.label(ax, x0 + 0.20, 0.195, cap, fs=7.6, color=c)
    fs.label(ax, 0.50, 0.575, "≡", fs=15, color=fs.MUTED)

    fs.label(ax, 0.50, 0.045,
             "$h/Z$ 都是 0.425：像素差为 0，像素无法分辨",
             fs=7.6, color=fs.MUTED)

    # ---------------- 右：误差曲线 ----------------
    ax2 = fig.add_axes([0.615, 0.26, 0.365, 0.58])
    h = np.linspace(1.45, 2.10, 400)
    e_data = 0.02 + 0.05 * (h - 1.70) ** 2                 # 近乎平坦的谷（示意）
    e_prior = ((h - 1.70) / 0.085) ** 2
    e_prior = e_prior / e_prior.max()
    e_all = e_data + 0.45 * e_prior
    scale = e_all.max()
    for y, c, ls, lab in [(e_data / scale, fs.BLUE, "-", "重投影误差 $E_J$"),
                          (e_prior / e_prior.max(), fs.GREEN, "--", "形状先验 $E_\\beta$"),
                          (e_all / scale, fs.ACCENT, "-", "合计")]:
        ax2.plot(h, y, color=c, lw=1.4 if ls == "--" else 1.6, ls=ls, label=lab)
    ax2.axvline(1.70, color=fs.ACCENT, lw=0.8, ls=":")
    ax2.set_xlim(1.45, 2.10)
    ax2.set_ylim(0, 1.06)
    ax2.set_xlabel("身高假设 $h$（米）", fontsize=8.2)
    ax2.set_ylabel("能量（归一化）", fontsize=8.0)
    ax2.set_title("谷底由先验决定，不由图像决定", fontsize=8.8, pad=6)
    ax2.legend(loc="upper center", fontsize=7.0, ncol=1, handlelength=1.4,
               borderaxespad=0.2)
    ax2.set_xticks([1.5, 1.6, 1.7, 1.8, 1.9, 2.0])
    ax2.tick_params(labelsize=7.6)
    for sp in ("top", "right"):
        ax2.spines[sp].set_visible(False)
    ax2.annotate("$E_J$ 在整段上几乎不变", xy=(1.98, 0.10), xytext=(1.60, 0.55),
                 fontsize=7.2, color=fs.BLUE,
                 arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=0.7))

    fig.text(0.5, 0.035,
             "示意图：焦距 1000 像素、人物占 425 像素高时，只有先验或相机内参能挑出唯一解",
             fontsize=7.8, color=fs.MUTED, ha="center")
    fs.save(fig, "ch01", "fig01-04")


if __name__ == "__main__":
    fig_scale_depth()
