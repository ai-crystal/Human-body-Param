# -*- coding: utf-8 -*-
"""第 2 章 图 2-5：五类动物数据的成本—覆盖分布（示意）。"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = r"E:\Study\人体参数化技术\人体参数化技术学习\books\frontier\images"


def fig_data_map():
    fig = plt.figure(figsize=(7.0, 3.5))
    ax = fig.add_axes([0.075, 0.155, 0.545, 0.700])
    lg = fig.add_axes([0.660, 0.060, 0.330, 0.830])
    lg.set_xlim(0, 1); lg.set_ylim(0, 1); lg.axis("off")

    ax.set_xscale("log"); ax.set_yscale("log")

    items = [
        ("1", "网络图片集合", 0.55, 1100, fs.BLUE),
        ("2", "视频 / 行为数据", 3.0, 640, fs.TEAL),
        ("3", "图形学资产", 1.5, 150, fs.PURPLE),
        ("4", "玩具扫描", 6.5, 38, fs.ACCENT),
        ("5", "棚拍多视图", 22.0, 6, fs.GREEN),
    ]

    ax.add_patch(plt.Rectangle((0.4, 700), 1.4, 2600, facecolor=fs.GREEN, alpha=0.07,
                               edgecolor=fs.GREEN, lw=0.8, ls=(0, (4, 3)), zorder=0))
    fs.label(ax, 1.05, 2100, "理想区（便宜且广）", fs=7.4, color=fs.GREEN, z=1)

    for num, name, cost, cov, c in items:
        ax.scatter([cost], [cov], s=230, color=c, alpha=0.92, edgecolor="white",
                   linewidth=1.4, zorder=4)
        ax.text(cost, cov, num, fontsize=8.0, color="white", ha="center", va="center",
                weight="bold", zorder=6)

    ax.annotate("", xy=(30, 4.6), xytext=(3.4, 480),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0,
                                ls=(0, (5, 3)), connectionstyle="arc3,rad=-0.28"))
    fs.label(ax, 9.0, 300, "越想要的物种", fs=7.6, color=fs.MUTED)
    fs.label(ax, 9.0, 190, "越贵、越少", fs=7.6, color=fs.MUTED)

    ax.set_xlim(0.35, 45)
    ax.set_ylim(3.5, 4200)
    ax.set_xlabel("单个物种的标注成本（相对量，对数轴）", fontsize=8.2, labelpad=1)
    ax.set_ylabel("覆盖物种数（对数轴）", fontsize=8.2, labelpad=1)
    fs.clean(ax, grid=True)
    ax.grid(True, which="major", color=fs.GRID, lw=0.6)
    ax.grid(True, which="minor", color=fs.GRID, lw=0.3, alpha=0.7)
    ax.tick_params(labelsize=7.6)

    fs.label(lg, 0.0, 0.955, "五类数据源", fs=9.0, color=fs.INK, weight="bold", ha="left")
    notes = [("网络图片集合", "爬取 + 过滤，覆盖广但偏动物园棚拍", fs.BLUE),
             ("视频 / 行为数据", "姿态多样，但不带 3D 标注", fs.TEAL),
             ("图形学资产", "自带骨骼蒙皮，解剖有偏", fs.PURPLE),
             ("玩具扫描", "定形状空间，材质与真实差一截", fs.ACCENT),
             ("棚拍多视图", "最准，只覆盖家畜与宠物", fs.GREEN)]
    y = 0.845
    for num, (name, note, c), in zip([("1",), ("2",), ("3",), ("4",), ("5",)], notes):
        lg.add_patch(plt.Circle((0.048, y), 0.030, color=c, zorder=2))
        fs.label(lg, 0.048, y, num, fs=7.6, color="white", weight="bold", z=3)
        fs.label(lg, 0.115, y + 0.012, name, fs=7.9, color=c, ha="left", weight="bold")
        fs.label(lg, 0.115, y - 0.042, note, fs=7.2, color=fs.MUTED, ha="left")
        y -= 0.150

    fs.label(lg, 0.0, 0.045, "长尾物种在每个源里都缺", fs=7.6, color=fs.ACCENT, ha="left")

    fig.text(0.075, 0.945, "五类动物数据：越靠左上越理想", fontsize=9.4, color=fs.INK,
             weight="bold")
    fs.save(fig, "ch02", "fig02-05")


if __name__ == "__main__":
    fig_data_map()
