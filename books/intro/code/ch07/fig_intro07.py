# -*- coding: utf-8 -*-
"""入门册第 7 章插图：图 7-1 应用地图（八类场景 + 输出 + 精度/时延档位）。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figstyle as fs
fs.FIGDIR = os.path.join(HERE, "img")


CARDS = [
    # (场景, 一句话输出, 精度 / 时延档位, 颜色)
    ("游戏与影视",       "虚拟角色 · 动作迁移",   "厘米级 · 离线",        fs.BLUE),
    ("短视频与直播",     "数字人 · 虚拟主播",     "十厘米级 · 实时 30fps", fs.PINK),
    ("电商",             "虚拟试衣 · 尺码推荐",   "厘米级 · 秒级",        fs.GREEN),
    ("健身与运动",       "动作评估 · 姿态纠正",   "厘米级 · 实时",        fs.ACCENT),
    ("医疗与康复",       "体态评估 · 手术规划",   "亚厘米级 · 离线",      fs.PURPLE),
    ("安防与行为理解",   "异常行为 · 人群计数",   "十厘米级 · 实时",      fs.GOLD),
    ("机器人与具身智能", "从视频学动作 · 遥操作", "厘米级 · 实时",        fs.TEAL),
    ("AIGC 内容生产",    "文生角色 · 文生动作",   "厘米级 · 秒到分钟",    fs.INK),
]


def card(ax, x, y, w, h, title, body, tag, color):
    """一张卡片：标题与档位同一行，输出在下面一行，左侧一条色条。"""
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.014",
        linewidth=0.9, edgecolor="#D5D9DE", facecolor="white", zorder=3))
    ax.add_patch(FancyBboxPatch(
        (x + 0.009, y + 0.011), 0.008, h - 0.022,
        boxstyle="round,pad=0,rounding_size=0.004",
        linewidth=0, facecolor=color, zorder=4))

    y_title = y + h / 2 + 0.031
    y_body = y + h / 2 - 0.031
    fs.label(ax, x + 0.030, y_title, title, fs=10.3, color=fs.INK,
             weight="bold", ha="left", va="center", z=6)
    fs.label(ax, x + w - 0.026, y_title, tag, fs=7.8, color=color,
             ha="right", va="center", z=6)
    fs.label(ax, x + 0.030, y_body, body, fs=8.5, color=fs.MUTED,
             ha="left", va="center", z=6)


def fig_map():
    fig, ax = fs.canvas(6.9, 4.2)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    m, gap = 0.050, 0.050
    w = (1 - 2 * m - gap) / 2
    h = (1 - 2 * m - 3 * gap) / 4

    for i, (title, body, tag, color) in enumerate(CARDS):
        row, col = divmod(i, 2)
        x = m + col * (w + gap)
        y = 1 - m - (row + 1) * h - row * gap
        card(ax, x, y, w, h, title, body, tag, color)

    out = os.path.join(HERE, "img", "07", "fig07-01.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=220, facecolor="white")
    plt.close(fig)
    print("saved", out)


if __name__ == "__main__":
    fig_map()
