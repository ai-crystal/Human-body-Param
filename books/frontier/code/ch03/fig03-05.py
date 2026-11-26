# -*- coding: utf-8 -*-
"""第 3 章 图 3-5：新物种接入的六步检查单。"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = r"E:\Study\人体参数化技术\人体参数化技术学习\books\frontier\images"


def fig_checklist():
    fig, ax = fs.canvas(7.0, 3.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    fs.label(ax, 0.5, 0.955, "接入一个新物种：六步，前两步是否决项", fs=10.0,
             color=fs.INK, weight="bold")

    steps = [
        ("1", "拓扑能不能用", "拉伸模板出现\n非物理变形 → 否决", fs.ACCENT),
        ("2", "关节数对不对", "加关节不改权重\n→ 顶点跟着半身动", fs.ACCENT),
        ("3", "形状空间够不够", "外插超过 $4\\sigma$\n→ 结果不可信", fs.GOLD),
        ("4", "关键点语义", "两个标注者定义\n差 2 cm → 评估全乱", fs.GOLD),
        ("5", "尺度先验", "给成体肩高区间\n输出标注“推定值”", fs.GREEN),
        ("6", "评估集", "少于 20–30 张标注\n→ 无法判断变好没有", fs.GREEN),
    ]

    w, h = 0.286, 0.235
    xs = [0.030, 0.357, 0.684]
    ys = [0.610, 0.235]
    for i, (num, title, note, c) in enumerate(steps):
        x = xs[i % 3]
        y = ys[i // 3]
        fs.box(ax, x, y, w, h, "", fc="white", ec=c, lw=1.2)
        ax.add_patch(plt.Circle((x + 0.034, y + h - 0.040), 0.026, color=c, zorder=5))
        fs.label(ax, x + 0.034, y + h - 0.040, num, fs=8.2, color="white",
                 weight="bold", z=6)
        fs.label(ax, x + 0.070, y + h - 0.040, title, fs=8.2, color=c,
                 ha="left", va="center", weight="bold")
        fs.label(ax, x + 0.018, y + 0.062, note, fs=7.3, color=fs.INK, ha="left",
                 va="center")
        if i % 3 < 2:
            fs.arrow(ax, (x + w + 0.002, y + h / 2), (x + w + 0.024, y + h / 2),
                     color=fs.FAINT, lw=1.0)

    fs.label(ax, 0.030, 0.545, "结构级：决定“要不要换模型”", fs=7.8, color=fs.ACCENT,
             ha="left")
    fs.label(ax, 0.030, 0.170, "工程级：决定“结果能不能用”", fs=7.8, color=fs.GREEN,
             ha="left")
    fs.label(ax, 0.5, 0.055, "先定拓扑，再定关节数，最后重学形状空间——不要在旧模型上打补丁",
             fs=7.8, color=fs.MUTED)
    fs.save(fig, "ch03", "fig03-05")


if __name__ == "__main__":
    fig_checklist()
