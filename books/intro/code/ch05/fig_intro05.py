# -*- coding: utf-8 -*-
"""入门册第 5 章插图：模型家族时间线、规模对照。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(BOOK), "code"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figstyle as fs

FIGDIR = os.path.join(BOOK, "images")

# (年份, 名称, 泳道)
LANES = ["身体", "人脸", "人手", "动物"]
COLORS = {"身体": fs.ACCENT, "人脸": fs.BLUE, "人手": fs.GREEN, "动物": fs.PURPLE}
NODES = [
    (1999, "3DMM", "人脸"),
    (2009, "BFM", "人脸"),
    (2015, "SMPL", "身体"),
    (2017, "SMPL+H", "身体"),
    (2017, "FLAME", "人脸"),
    (2017, "MANO", "人手"),
    (2017, "SMAL", "动物"),
    (2019, "SMPL-X", "身体"),
    (2020, "STAR", "身体"),
    (2020, "GHUM", "身体"),
    (2022, "BARC", "动物"),
    (2023, "HaMeR", "人手"),
    (2023, "MagicPony", "动物"),
    (2024, "AniMer", "动物"),
    (2025, "ATLAS", "身体"),
    (2025, "MHR", "身体"),
]


def fig_timeline():
    fig = plt.figure(figsize=(6.9, 3.7))
    ax = fig.add_axes([0.078, 0.085, 0.905, 0.83])
    ax.set_xlim(1997, 2027)
    ax.set_ylim(-2.6, 14.4)
    ax.axis("off")

    gap = 3.6
    lanes_y = {lane: gap * (len(LANES) - 1 - i) for i, lane in enumerate(LANES)}

    for lane in LANES:
        y = lanes_y[lane]
        ax.plot([1997.4, 2026.6], [y, y], color="#E8EAED", lw=1.0, zorder=1)
        ax.text(1997.0, y, lane, ha="right", va="center", fontsize=8.8,
                color=COLORS[lane])

    tiers = [(0.95, "bottom"), (-1.05, "top")]
    for lane in LANES:
        y = lanes_y[lane]
        own = sorted([n for n in NODES if n[2] == lane], key=lambda t: t[0])
        used_x = [None] * len(tiers)          # 每条标注带最近一次占用的年份
        for year, name, _ in own:
            col = COLORS[lane]
            ax.plot([year], [y], marker="o", ms=6.8, color="white", mec=col,
                    mew=1.7, zorder=4)
            # 贪心选一条不撞的标注带：与同带上一个标签至少隔 2.6 年
            pick, shift = None, 0.0
            for ti in range(len(tiers)):
                if used_x[ti] is None or year - used_x[ti] >= 2.6:
                    pick = ti
                    break
            if pick is None:                      # 两条带都挤满了：往右挪一点
                pick = min(range(len(tiers)), key=lambda ti: used_x[ti])
                shift = 1.35
            used_x[pick] = year
            dy, va = tiers[pick]
            ax.plot([year, year], [y, y + dy * 0.72], color=col, lw=0.7,
                    alpha=0.45, zorder=2)
            ax.text(year + shift, y + dy, name,
                    ha="left" if shift else "center", va=va, fontsize=7.4,
                    color=col, zorder=5)

    for yr in (1999, 2005, 2010, 2015, 2020, 2025):
        ax.plot([yr, yr], [-2.2, 11.4], color="#F3F4F6", lw=0.6, zorder=0)
        ax.text(yr, -2.35, str(yr), ha="center", va="top", fontsize=7.0, color=fs.FAINT)

    ax.text(1997.0, 14.3, "四类对象，一条相似的演化路线", fontsize=9.6,
            color=fs.INK, va="top")
    ax.text(1997.0, 13.4, "越靠右越新；同一年份的模型上下错开标注", fontsize=7.6,
            color=fs.MUTED, va="top")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch05", "fig05-01")


def fig_scale():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9),
                             gridspec_kw={"width_ratios": [1.0, 0.85]})

    # 左：顶点数（对数横轴）
    ax = axes[0]
    fs.clean(ax, grid=True)
    data = [("MANO", 778, fs.GREEN), ("FLAME", 5023, fs.BLUE),
            ("SMPL", 6890, fs.ACCENT), ("SMPL-X", 10475, fs.ACCENT),
            ("MHR", 73639, fs.PURPLE), ("ATLAS", 115000, fs.PURPLE)]
    ys = np.arange(len(data))[::-1]
    for y, (name, v, c) in zip(ys, data):
        ax.barh(y, v, height=0.55, color=c, alpha=0.85, zorder=2)
        ax.text(v * 1.12, y, "%s" % format(v, ","), va="center", fontsize=7.4,
                color=fs.MUTED)
    ax.set_yticks(ys)
    ax.set_yticklabels([d[0] for d in data], fontsize=8.0)
    ax.set_xscale("log")
    ax.set_xlim(400, 400000)
    ax.set_xlabel("顶点数（对数轴）", fontsize=8.2)
    ax.set_title("网格的规模差两个数量级", fontsize=9.2, pad=4)
    ax.tick_params(labelsize=7.4)

    # 右：关节数
    ax = axes[1]
    fs.clean(ax, grid=True)
    jd = [("FLAME", 4, fs.BLUE), ("MANO", 16, fs.GREEN), ("SMPL", 24, fs.ACCENT),
          ("SMAL", 33, fs.PURPLE), ("SMPL-X", 54, fs.ACCENT),
          ("ATLAS", 77, fs.PURPLE), ("MHR", 127, fs.PURPLE)]
    ys = np.arange(len(jd))[::-1]
    for y, (name, v, c) in zip(ys, jd):
        ax.barh(y, v, height=0.55, color=c, alpha=0.85, zorder=2)
        ax.text(v + 2.4, y, str(v), va="center", fontsize=7.4, color=fs.MUTED)
    ax.set_yticks(ys)
    ax.set_yticklabels([d[0] for d in jd], fontsize=8.0)
    ax.set_xlim(0, 150)
    ax.set_xlabel("关节数", fontsize=8.2)
    ax.set_title("关节越多，控制越细也越难拟合", fontsize=9.2, pad=4)
    ax.tick_params(labelsize=7.4)

    fig.tight_layout(pad=0.5, w_pad=1.4)
    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch05", "fig05-02")


if __name__ == "__main__":
    fig_timeline()
    fig_scale()
