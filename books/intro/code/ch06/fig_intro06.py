# -*- coding: utf-8 -*-
"""入门册第 6 章插图：四条技术线的时间轴、四层栈。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figstyle as fs

fs.FIGDIR = os.path.join(HERE, "img")


# =====================================================================
# 图 6-1  四条线在 2015–2026 上的交汇
# =====================================================================
# (年份, 文字, +1 在上 / -1 在下, 对齐方式)
LANES = [
    ("参数化模型", fs.BLUE, 3.85,
     [(2015, "SMPL", 1, "center"), (2017, "FLAME / MANO", -1, "center"),
      (2019, "SMPL-X", 1, "center"), (2020, "STAR / GHUM", -1, "center"),
      (2025, "MHR", 1, "center")]),
    ("神经渲染", fs.GREEN, 2.85,
     [(2020, "NeRF", 1, "center"), (2022, "HumanNeRF", -1, "center"),
      (2023, "3DGS", 1, "center"), (2024, "GaussianAvatars", -1, "left")]),
    ("扩散与生成", fs.ACCENT, 1.85,
     [(2020, "DDPM", 1, "center"), (2022, "DreamFusion / SDS", 1, "left"),
      (2022, "MDM 动作生成", -1, "center"),
      (2024, "单图生成可动化身", -1, "left")]),
    ("视觉基础模型", fs.PURPLE, 0.85,
     [(2023, "SAM", 1, "center"), (2023, "SMPLer-X", -1, "center"),
      (2024, "DINOv2", 1, "left"), (2024.05, "深度·法向", -1, "left")]),
]


def fig_timeline():
    fig, ax = plt.subplots(figsize=(7.3, 4.45))
    ax.set_xlim(2014.25, 2027.15)
    ax.set_ylim(0.34, 4.92)

    ax.axvspan(2022.0, 2026.95, color=fs.PAPER, zorder=0)
    ax.text(2022.25, 4.70, "2022 年之后，四条线开始互相调用", fontsize=8.0,
            color=fs.GOLD, ha="left", va="center")

    for name, col, y, nodes in LANES:
        ax.plot([2014.55, 2026.85], [y, y], color=fs.FAINT, lw=0.9, zorder=1)
        ax.plot([2026.85], [y], marker=">", ms=4.2, color=fs.FAINT, zorder=1)
        for yr, lab, side, ha in nodes:
            ax.plot([yr, yr], [y, y + side * 0.135], color=col, lw=1.0,
                    alpha=0.55, zorder=2)
            ax.plot([yr], [y], marker="o", ms=5.4, color=col, mec="white",
                    mew=1.1, zorder=4)
            off = 0.0 if ha == "center" else (0.10 if ha == "left" else -0.10)
            ax.text(yr + off, y + side * 0.255, lab, fontsize=7.7,
                    color=fs.INK, ha=ha, va="center", zorder=5)

    ax.set_yticks([ln[2] for ln in LANES])
    ax.set_yticklabels([ln[0] for ln in LANES], fontsize=8.6)
    for tick, ln in zip(ax.get_yticklabels(), LANES):
        tick.set_color(ln[1])

    ax.set_xticks([2015, 2017, 2019, 2021, 2023, 2025])
    ax.set_xticks([2016, 2018, 2020, 2022, 2024, 2026], minor=True)
    ax.set_xticklabels(["2015", "2017", "2019", "2021", "2023", "2025"],
                       fontsize=8.4)
    ax.tick_params(axis="x", which="minor", length=0)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.tick_params(axis="x", length=2.5, pad=3, colors=fs.MUTED)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=fs.GRID, lw=0.7, zorder=0)

    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(fs.FAINT)

    fig.subplots_adjust(left=0.145, right=0.985, top=0.975, bottom=0.115)
    fs.save(fig, "06", "fig06-01")


# =====================================================================
# 图 6-2  四层栈：谁给谁提供什么
# =====================================================================
def fig_stack():
    fig, ax = fs.canvas(7.0, 4.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    bx, bw = 0.045, 0.400
    layers = [
        ("应用层", ["游戏 · 影视 · 直播 · 试衣 · 医疗"], 0.800, 0.125,
         fs.PURPLE, "white"),
        ("生成层", ["扩散 · SDS · 3DGS　造外观、造实例"], 0.600, 0.125,
         fs.ACCENT, "#FDF6EE"),
        ("参数层", ["SMPL 这一类　形状 + 姿势 + 骨架", "米 / 度：唯一有物理单位的一层"],
         0.375, 0.155, fs.GREEN, "#EEF6F2"),
        ("像素 / 特征层", ["分割 · 深度 · 法向 · DINOv2 特征"], 0.175, 0.125,
         fs.BLUE, "white"),
    ]

    for title, subs, y, bh, c, fc in layers:
        fs.box(ax, bx, y, bw, bh, "", fc=fc, ec=c, lw=1.3)
        ax.text(bx + 0.020, y + bh - 0.032, title, fontsize=9.2, color=c,
                ha="left", va="center", weight="bold", zorder=6)
        for i, s in enumerate(subs):
            ax.text(bx + 0.020, y + bh - 0.032 - 0.052 - i * 0.040, s,
                    fontsize=7.8, color=fs.INK if i == 0 else fs.GREEN,
                    ha="left", va="center", zorder=6)

    # 层间：实线向上（下层交上去），虚线向下（上层回头改下层）
    cx = bx + bw * 0.26
    dx = bx + bw * 0.60
    pairs = [(0.800, 0.725), (0.600, 0.530), (0.375, 0.300)]
    for top, bot in pairs:
        fs.arrow(ax, (cx, (top + bot) / 2 - 0.020), (cx, (top + bot) / 2 + 0.020),
                 color=fs.MUTED, lw=1.2)
        fs.arrow(ax, (dx, (top + bot) / 2 + 0.020), (dx, (top + bot) / 2 - 0.020),
                 color=fs.FAINT, lw=1.1, ls=(0, (3, 2)))

    # 右侧注释
    tx = 0.500
    notes = [
        (0.7625, "外观与实例", "驱动信号：一串关节角", fs.ACCENT),
        (0.5650, "骨架、静止姿态、绑定关系", "生成的 3D 要拟合回参数才能动", fs.GREEN),
        (0.3375, "证据：这块是人、多远、朝哪", "上层需要什么样的证据", fs.BLUE),
    ]
    for y, up, dn, col in notes:
        ax.plot([bx + bw + 0.004, tx - 0.014], [y, y], color=fs.FAINT, lw=0.8,
                zorder=1)
        ax.text(tx + 0.002, y + 0.028, "↑", fontsize=10.5, color=col,
                ha="left", va="center", zorder=6)
        ax.text(tx + 0.032, y + 0.028, up, fontsize=8.2, color=fs.INK,
                ha="left", va="center", zorder=6)
        ax.text(tx + 0.002, y - 0.040, "↓", fontsize=10.5, color=fs.MUTED,
                ha="left", va="center", zorder=6)
        ax.text(tx + 0.032, y - 0.040, dn, fontsize=8.2, color=fs.MUTED,
                ha="left", va="center", zorder=6)

    ax.text(tx, 0.962, "下层交给上层什么", fontsize=8.4, color=fs.INK,
            ha="left", va="center", weight="bold")
    ax.text(tx, 0.925, "实线向上，虚线是上层回头改下层", fontsize=7.6,
            color=fs.MUTED, ha="left", va="center")

    ax.plot([0.045, 0.955], [0.108, 0.108], color=fs.GRID, lw=0.9)
    ax.text(0.045, 0.062,
            "越往上越贴近应用，越往下越通用；中间那层是所有人都读得懂的格式",
            fontsize=8.0, color=fs.MUTED, ha="left", va="center")

    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    fs.save(fig, "06", "fig06-02")


if __name__ == "__main__":
    fig_timeline()
    fig_stack()
