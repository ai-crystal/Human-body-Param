# -*- coding: utf-8 -*-
"""第 1 章插图。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib.tri as mtri
import figstyle as fs

rng = np.random.default_rng(7)


# ---------------- 图 1-1 从像素到参数 ----------------
def mask(x, y):
    """一个站姿人形的解析“遮罩”，用于像素/点云示意。"""
    m = np.zeros_like(x, dtype=bool)
    m |= (x - 0.5) ** 2 + (y - 0.86) ** 2 < 0.055 ** 2          # 头
    m |= (np.abs(x - 0.5) < 0.085) & (y > 0.55) & (y < 0.79)     # 躯干
    m |= (np.abs(x - 0.5) < 0.055) & (y > 0.47) & (y < 0.58)     # 髋
    for s in (-1, 1):
        m |= (np.abs(x - (0.5 + s * 0.11)) < 0.028) & (y > 0.6) & (y < 0.78)  # 上臂
        m |= (np.abs(x - (0.5 + s * 0.14)) < 0.024) & (y > 0.44) & (y < 0.62) # 前臂
        m |= (np.abs(x - (0.5 + s * 0.04)) < 0.038) & (y > 0.25) & (y < 0.5)  # 大腿
        m |= (np.abs(x - (0.5 + s * 0.05)) < 0.03) & (y > 0.06) & (y < 0.28)  # 小腿
        m |= (np.abs(x - (0.5 + s * 0.06)) < 0.045) & (y > 0.03) & (y < 0.08) # 脚
    return m


def fig_representations():
    fig, axs = plt.subplots(1, 4, figsize=(6.9, 2.5))
    titles = ["① 像素", "② 点云", "③ 网格", "④ 参数"]
    for ax, t in zip(axs, titles):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        ax.set_title(t, fontsize=9.5, color=fs.INK, pad=4)

    # 像素
    n = 26
    gx, gy = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, n))
    m = mask(gx, gy)
    img = np.where(m, 0.25 + 0.55 * gx, 1.0)
    axs[0].imshow(img, cmap="Greys", origin="lower", extent=[0, 1, 0, 1], vmin=0, vmax=1)
    for i in range(n + 1):
        axs[0].axvline(i / n, color="white", lw=0.25, alpha=0.5)
        axs[0].axhline(i / n, color="white", lw=0.25, alpha=0.5)
    fs.label(axs[0], 0.5, -0.1, "$256\\times256$ 个数", fs=7.8, color=fs.MUTED)

    # 点云
    pts = rng.random((900, 2))
    keep = mask(pts[:, 0], pts[:, 1])
    pts = pts[keep]
    axs[1].scatter(pts[:, 0], pts[:, 1], s=3.2, color=fs.BLUE, alpha=0.75, linewidths=0)
    fs.label(axs[1], 0.5, -0.1, "$N$ 个三维点", fs=7.8, color=fs.MUTED)

    # 网格
    tri = mtri.Triangulation(pts[:, 0], pts[:, 1])
    axs[2].triplot(tri, color=fs.GREEN, lw=0.3, alpha=0.8)
    axs[2].scatter(pts[:, 0], pts[:, 1], s=1.2, color=fs.GREEN, alpha=0.9)
    fs.label(axs[2], 0.5, -0.1, "$N$ 个顶点 + 面片", fs=7.8, color=fs.MUTED)

    # 参数
    fs.human(axs[3], cx=0.38, cy=0.5, s=0.72, color="#D8C3AE", alpha=1.0)
    for i in range(6):
        y = 0.82 - i * 0.11
        axs[3].plot([0.62, 0.95], [y, y], color="#E5E7EB", lw=2.2, solid_capstyle="round")
        v = [0.25, 0.55, 0.4, 0.7, 0.3, 0.6][i]
        axs[3].plot([0.62, 0.62 + 0.33 * v], [y, y], color=fs.ACCENT, lw=2.2, solid_capstyle="round")
    fs.label(axs[3], 0.78, 0.06, "$\\beta_1,\\ldots,\\beta_{10}$", fs=8, color=fs.ACCENT)
    fs.label(axs[3], 0.5, -0.1, "10 个数就能重建", fs=7.8, color=fs.MUTED)

    fig.subplots_adjust(wspace=0.18, bottom=0.2, top=0.88)
    fs.save(fig, "ch01", "fig01-01")


# ---------------- 图 1-2 技术版图 ----------------
def fig_map():
    fig, ax = fs.canvas(6.9, 4.0)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    cols = [
        (0.02, "人体 Body", ["SCAPE 2005", "SMPL 2015", "SMPL-X 2019", "STAR / GHUM", "HMR / 4D-Humans"], fs.BLUE),
        (0.265, "人脸 Face", ["3DMM 1999", "BFM 2009", "FLAME 2017", "DECA / EMOCA", "3DGS 头像"], fs.ACCENT),
        (0.51, "人手 Hand", ["MANO 2017", "FrankMocap 2020", "HaMeR 2023", "MANUS 2024"], fs.GREEN),
        (0.755, "动物 Animal", ["SMAL 2017", "BARC 2022", "MagicPony 2023", "AniMer 2024"], fs.PURPLE),
    ]
    for x, title, items, c in cols:
        fs.box(ax, x, 0.845, 0.225, 0.085, title, fc="white", ec=c, fs=10, weight="bold")
        ax.plot([x + 0.015, x + 0.015], [0.84, 0.30], color=c, lw=1.6, alpha=0.35, zorder=1)
        for i, it in enumerate(items):
            y = 0.75 - i * 0.088
            ax.add_patch(Circle((x + 0.028, y), 0.008, color=c, zorder=4))
            fs.label(ax, x + 0.048, y, it, fs=8.3, ha="left", color=fs.INK)
        fs.arrow(ax, (x + 0.112, 0.29), (x + 0.112, 0.225), color=c, lw=0.9, ls="--")
    fs.box(ax, 0.06, 0.10, 0.88, 0.115,
           "共同地基：统计形状模型（PCA）· 关节层次 · 线性混合蒙皮 · 可微渲染",
           fc="#FDF6EC", ec=fs.ACCENT, fs=9.2)
    fs.label(ax, 0.5, 0.045, "四条主线解决的是同一个问题：用少量参数，控制一个高维的三维形状",
             fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-02")


# ---------------- 图 1-3 阅读路线 ----------------
def fig_route():
    fig, ax = fs.canvas(6.9, 2.9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    NL = chr(10)
    def two(a, b):
        return a + NL + b
    rows = [
        ("零基础通读", [two("第 1–6 章", "数学与形变"), two("第 7–14 章", "人体"),
                        two("第 15–24 章", "脸 / 手 / 动物"), two("第 25–27 章", "前沿与实战")], fs.ACCENT),
        ("只想做人体", [two("第 1–6 章", "重点第 3、5 章"), two("第 7–14 章", "人体全流程"),
                        two("第 26 章", "动手实践")], fs.BLUE),
        ("只想做人脸", [two("第 2–3、6 章", "PCA 与 3DMM"), two("第 15–18 章", "人脸"),
                        two("第 26 章", "动手实践")], fs.GREEN),
    ]
    for r, (name, chips, c) in enumerate(rows):
        y = 0.80 - r * 0.30
        fs.label(ax, 0.02, y, name, fs=9.2, ha="left", color=c, weight="bold")
        x = 0.20
        gap = 0.035
        w = (0.985 - x - gap * (len(chips) - 1)) / len(chips)
        for i, ch in enumerate(chips):
            fs.box(ax, x, y - 0.075, w, 0.15, ch, fc="white", ec=c, fs=7.9, lw=1.0)
            if i:
                fs.arrow(ax, (x - 0.035, y), (x - 0.004, y), color=c, lw=0.9)
            x += w + gap
    fs.label(ax, 0.5, 0.045, "章节之间有依赖，但第 26 章的代码可以随时插入练习",
             fs=8, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-03")


if __name__ == "__main__":
    fig_representations()
    fig_map()
    fig_route()
