# -*- coding: utf-8 -*-
"""入门册第 8 章图 8-2：三条深入路线怎么选。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(BOOK), "code"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figstyle as fs

FIGDIR = os.path.join(BOOK, "images")

CARDS = [
    ("① 几何与建模", fs.BLUE,
     "让模型本身更准、更可控",
     "形状空间、姿态修正、骨架解耦",
     "你要改骨长、做护具假肢，\n或者给引擎做资产"),
    ("② 从图像到人", fs.GREEN,
     "从照片或视频里把人读出来",
     "优化与回归、关键点与轮廓、\n可微渲染",
     "你要做试衣、健身、监控，\n或者替代一部分动捕"),
    ("③ 渲染与生成", fs.ACCENT,
     "做出照片级、可驱动的内容",
     "神经渲染、扩散、绑定与重定向",
     "你要做数字人、虚拟主播、\nAIGC 角色"),
]


def fig_route3():
    fig = plt.figure(figsize=(6.9, 3.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fs.label(ax, 0.04, 0.965, "跑通之后往哪走：三条路线，靠三个问题选",
             fs=9.8, color=fs.INK, ha="left", va="top")
    fs.label(ax, 0.04, 0.905, "问题一：你要改模型、读模型，还是生成内容？  问题二：你手上有没有数据？  问题三：下游是引擎还是论文？",
             fs=7.6, color=fs.MUTED, ha="left", va="top")

    w = 0.285
    x0, gap = 0.04, 0.0375
    y0, h = 0.085, 0.685
    body = [0.545, 0.360, 0.170]
    labels = ["这条线要什么", "先补哪些知识", "什么时候选它"]
    for i, (title, c, goal, learn, when) in enumerate(CARDS):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, y0), w, h,
                                    boxstyle="round,pad=0.006,rounding_size=0.02",
                                    ec=c, fc="#FFFFFF", lw=1.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y0 + h - 0.085), w, 0.085,
                                    boxstyle="round,pad=0.006,rounding_size=0.02",
                                    ec=c, fc=c, lw=1.2, alpha=0.13, zorder=3))
        fs.label(ax, x + 0.022, y0 + h - 0.045, title, fs=9.2, color=c,
                 ha="left", va="center", weight="bold")
        for k, (lab, txt) in enumerate(zip(labels, (goal, learn, when))):
            ly = body[k]
            fs.label(ax, x + 0.022, ly + 0.072, lab, fs=7.2, color=fs.FAINT, ha="left")
            fs.label(ax, x + 0.022, ly - 0.012, txt, fs=7.8,
                     color=fs.INK if k < 2 else fs.MUTED, ha="left", va="center")

    fs.label(ax, 0.04, 0.032, "三条线不冲突：多数人是“一条主线，另外两条够用就行”。",
             fs=7.8, color=fs.FAINT, ha="left")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch08", "fig08-02")


if __name__ == "__main__":
    fig_route3()
