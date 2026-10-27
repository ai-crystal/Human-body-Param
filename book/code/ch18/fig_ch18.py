# -*- coding: utf-8 -*-
"""第 18 章插图：人脸驱动与神经头像。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import figstyle as fs

W = 6.7


def fig_two_routes():
    fig, ax = fs.canvas(W, 3.95)

    cols = [
        (0.020, "① 参数化路线", fs.BLUE,
         ["驱动信号\n（表情系数 / 音频）", "参数\n$\\psi,\\ \\theta$",
          "线性模型\nFLAME 网格", "光栅化渲染\n+ 贴图"],
         "可控性最强：能进引擎、\n能改参数、能重定向。\n细节受限于网格分辨率。"),
        (0.345, "② 神经路线", fs.PURPLE,
         ["多视角或单目视频", "逐场景优化\n（几分钟到几小时）",
          "NeRF / 3D 高斯\n隐式或离散场", "体渲染 / 泼溅\n合成像素"],
         "写实度最高：发丝、牙齿、\n皮肤都能重建。但场不懂\n“表情”，要驱动得另接模型。"),
        (0.670, "③ 混合路线", fs.ACCENT,
         ["FLAME 三角面\n作为骨架", "每个三角面挂\n一个 3D 高斯",
          "随三角面\n平移旋转缩放", "泼溅渲染\n实时"],
         "参数模型管“怎么动”，\n高斯管“长什么样”。\n代表：GaussianAvatars 等。"),
    ]

    for x0, title, col, steps, note in cols:
        fs.label(ax, x0 + 0.15, 0.945, title, fs=9.4, color=col, weight="bold")
        ax.plot([x0 + 0.02, x0 + 0.28], [0.912, 0.912], color=col, lw=1.4)
        ys = [0.780, 0.595, 0.410, 0.225]
        for i, (txt, y) in enumerate(zip(steps, ys)):
            fs.box(ax, x0 + 0.01, y - 0.065, 0.28, 0.130, txt,
                   fc="white", ec=col, fs=7.8, lw=0.95)
            if i:
                fs.arrow(ax, (x0 + 0.15, y + 0.145), (x0 + 0.15, y + 0.070),
                         color=col, lw=1.0, ms=7)
        fs.label(ax, x0 + 0.15, 0.080, note, fs=7.1, color=fs.MUTED, va="center")

    for x in (0.335, 0.660):
        ax.plot([x, x], [0.06, 0.93], color=fs.GRID, lw=0.9)
    fs.save(fig, "ch18", "fig18-01")


def fig_audio_pipeline():
    fig, ax = fs.canvas(W, 3.10)

    stages = ["音频波形\n48 kHz", "语音特征\n音素 / 表征",
              "运动生成\n唇形·表情·头姿", "3D 表示\n网格 / NeRF / 高斯",
              "渲染合成\n口内与背景"]
    cols = [fs.MUTED, fs.BLUE, fs.ACCENT, fs.GREEN, fs.PURPLE]
    fs.flow(ax, stages, y=0.815, h=0.150, fs=7.4, x0=0.02, x1=0.98, colors=cols)
    fs.label(ax, 0.5, 0.955,
             "所有语音驱动系统都是这条链，区别主要在“运动生成”这一段怎么学",
             fs=8.6, color=fs.INK)

    blocks = [
        (0.020, 0.560, "SadTalker", "ExpNet 把音频直接回归成\n3DMM 的表情与头姿系数", fs.ACCENT),
        (0.510, 0.560, "GeneFace", "在唇读语料上训练变分\n运动生成器，再驱动 NeRF", fs.ACCENT),
        (0.020, 0.320, "Media2Face", "用扩散模型生成表情潜码，\n可加文本与情绪条件", fs.ACCENT),
        (0.510, 0.320, "EMOTE", "把“说什么”与“怎么说”\n拆成两条支路分别建模", fs.ACCENT),
    ]
    for x, y, title, sub, col in blocks:
        fs.box(ax, x, y - 0.135, 0.470, 0.210, "", fc="white", ec=col, fs=7.6, lw=0.95)
        fs.label(ax, x + 0.030, y + 0.028, title, fs=8.4, color=col, ha="left", weight="bold")
        fs.label(ax, x + 0.030, y - 0.055, sub, fs=7.2, color=fs.MUTED, ha="left", va="center")

    fs.label(ax, 0.5, 0.112,
             "三种常见崩坏：口型与音素错位、口内被填成“一坨”、换语言后节奏全乱",
             fs=7.8, color=fs.MUTED)
    fs.label(ax, 0.5, 0.042,
             "根源都是“一对多”：同一段音频可以有多种合理表情，模型只能给出它学到的平均解",
             fs=7.8, color=fs.MUTED)
    fs.save(fig, "ch18", "fig18-03")


def fig_signal_spectrum():
    fig, ax = fs.canvas(W, 3.05)

    stages = [
        ("手动调参", "动画师拖滑块\n精确但昂贵", fs.MUTED),
        ("表演捕捉", "Face2Face\n演员自己演", fs.TEAL),
        ("视频重演", "Deep Video\nPortraits", fs.BLUE),
        ("语音驱动", "GeneFace\nSadTalker", fs.ACCENT),
        ("文本 · 多模态", "Media2Face\n“笑着说这句”", fs.PURPLE),
    ]
    n = len(stages)
    xs = np.linspace(0.092, 0.908, n)
    for i, ((name, sub, col), x) in enumerate(zip(stages, xs)):
        ax.add_patch(plt.Rectangle((x - 0.088, 0.362), 0.176, 0.205,
                                   facecolor="white", edgecolor=col, lw=1.2, zorder=3))
        fs.label(ax, x, 0.518, name, fs=8.2, color=col, weight="bold")
        fs.label(ax, x, 0.437, sub, fs=6.6, color=fs.MUTED)
        if i < n - 1:
            fs.arrow(ax, (x + 0.091, 0.468), (xs[i + 1] - 0.091, 0.468),
                     color=fs.FAINT, lw=1.0, ms=7)

    ax.annotate("", xy=(0.955, 0.700), xytext=(0.045, 0.700),
                arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=1.5))
    fs.label(ax, 0.50, 0.740, "对结果的控制精度：从“每一帧都指定”到“只给一句话”",
             fs=8.4, color=fs.GREEN)
    ax.annotate("", xy=(0.955, 0.215), xytext=(0.045, 0.215),
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.5))
    fs.label(ax, 0.50, 0.150, "驱动素材的获取成本：从“请一个演员”到“写一行字”",
             fs=8.4, color=fs.ACCENT)
    fs.label(ax, 0.50, 0.055, "两条箭头方向相反，这就是人脸驱动领域永恒的矛盾",
             fs=8.0, color=fs.MUTED)
    fs.save(fig, "ch18", "fig18-02")


if __name__ == "__main__":
    fig_two_routes()
    fig_audio_pipeline()
    fig_signal_spectrum()
