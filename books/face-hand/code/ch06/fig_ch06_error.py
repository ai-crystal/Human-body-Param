# -*- coding: utf-8 -*-
"""第 6 章新插图：五类误差来源（深度歧义、自遮挡、尺度、左右手混淆、关节顺序）。"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, FancyBboxPatch

sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import figstyle as fs

fs.FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "images")

SKIN = "#F2E8DC"
DARK = "#D8C7B2"


def hand_icon(ax, cx, cy, s=1.0, mirror=False, fc=SKIN, ec=fs.MUTED, lw=0.9, z=3):
    """极简手掌图标：手掌椭圆 + 四指 + 拇指。mirror=True 得到镜像手。"""
    k = -1 if mirror else 1
    ax.add_patch(Ellipse((cx, cy), 0.30 * s, 0.22 * s, facecolor=fc, edgecolor=ec,
                         lw=lw, zorder=z))
    for dx, ang, ln in [(-0.075, 0.02, 0.20), (-0.020, 0.0, 0.23),
                        (0.035, -0.02, 0.22), (0.085, -0.05, 0.18)]:
        p0 = np.array([cx + k * dx * s, cy + 0.09 * s])
        p1 = p0 + np.array([k * ang * s, ln * s])
        fs.limb(ax, p0, p1, 0.045 * s, 0.040 * s, color=fc, z=z, ec=ec)
    p0 = np.array([cx - k * 0.13 * s, cy - 0.02 * s])
    p1 = p0 + np.array([-k * 0.10 * s, 0.14 * s])
    fs.limb(ax, p0, p1, 0.050 * s, 0.045 * s, color=fc, z=z, ec=ec)


def _panel(fig, rect, title, note):
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.0, 0.99, title, fontsize=8.2, ha="left", va="top", weight="bold")
    ax.text(0.5, 0.02, note, fontsize=6.9, color=fs.MUTED, ha="center", va="bottom")
    return ax


def fig06_03():
    fig = plt.figure(figsize=(6.8, 3.7))
    fig.text(0.02, 0.985, "五类误差来源", fontsize=9.8, weight="bold")

    # ---------------- ① 深度歧义 -------------------------------
    ax = _panel(fig, [0.015, 0.50, 0.295, 0.43],
                "① 深度歧义",
                "投影多对一：沿视线平移，投影不动")
    ax.plot([0.10, 0.10], [0.20, 0.80], color=fs.INK, lw=1.4, zorder=4)
    fs.label(ax, 0.115, 0.19, "图像平面", fs=6.6, color=fs.MUTED, ha="left", va="bottom")
    # 一条视线，两个不同深度的指尖落在同一条视线上
    ax.annotate("", xy=(0.94, 0.52), xytext=(0.10, 0.52),
                arrowprops=dict(arrowstyle="-", color=fs.BLUE, lw=0.8,
                                linestyle=(0, (3, 2))))
    for xa, lab in [(0.42, "姿态 A"), (0.82, "姿态 B")]:
        fs.limb(ax, (xa - 0.22, 0.52), (xa, 0.52), 0.085, 0.070, color=SKIN, z=3,
                ec=fs.MUTED)
        ax.add_patch(Circle((xa, 0.52), 0.030, facecolor=DARK, edgecolor=fs.MUTED,
                            lw=0.8, zorder=5))
        fs.label(ax, xa - 0.10, 0.38, lab, fs=6.8, color=fs.INK)
    fs.label(ax, 0.62, 0.70, "指尖沿视线平移", fs=6.8, color=fs.BLUE, ha="center")
    ax.annotate("", xy=(0.79, 0.60), xytext=(0.45, 0.60),
                arrowprops=dict(arrowstyle="<->", color=fs.BLUE, lw=0.9,
                                shrinkA=0, shrinkB=0))
    ax.add_patch(Circle((0.10, 0.52), 0.024, facecolor=fs.BLUE, alpha=0.30,
                        edgecolor=fs.BLUE, lw=0.8, zorder=6))

    # ---------------- ② 自遮挡 ---------------------------------
    ax = _panel(fig, [0.345, 0.50, 0.295, 0.43],
                "② 自遮挡",
                "证据缺失：被挡的部分只能靠先验补")
    # 前面一根手指（横），后面一根手指（竖，中段被挡）
    for y0, y1 in [(0.88, 0.56), (0.14, 0.44)]:
        fs.limb(ax, (0.50, y0), (0.50, y1), 0.105, 0.098, color=SKIN, z=3, ec=fs.MUTED)
    fs.limb(ax, (0.10, 0.50), (0.86, 0.50), 0.15, 0.135, color=SKIN, z=4, ec=fs.MUTED)
    ax.plot([0.50, 0.50], [0.56, 0.44], color=fs.MUTED, lw=0.9, ls=(0, (2.5, 2)),
            zorder=5)
    ax.add_patch(FancyBboxPatch((0.452, 0.430), 0.096, 0.140,
                                boxstyle="round,pad=0.004,rounding_size=0.012",
                                facecolor="none", edgecolor=fs.ACCENT, lw=1.0,
                                linestyle=(0, (2.5, 2)), zorder=6))
    ax.annotate("被挡住的段", xy=(0.552, 0.50), xytext=(0.64, 0.30),
                fontsize=6.8, color=fs.ACCENT, ha="left",
                arrowprops=dict(arrowstyle="-", color=fs.ACCENT, lw=0.8))

    # ---------------- ③ 尺度 -----------------------------------
    ax = _panel(fig, [0.675, 0.50, 0.295, 0.43],
                "③ 尺度",
                "单目不可判：远近不同的手投影同宽")
    cam = (0.06, 0.50)
    ax.add_patch(Polygon([cam, (0.22, 0.60), (0.22, 0.40)], closed=True,
                         facecolor=fs.GRID, edgecolor=fs.MUTED, lw=0.8, zorder=2))
    for x0, h, lab in [(0.42, 0.16, "近·小"), (0.86, 0.356, "远·大")]:
        ax.plot([x0, x0], [0.50 - h / 2, 0.50 + h / 2], color=fs.INK, lw=2.4,
                solid_capstyle="round", zorder=4)
        for sgn in (1, -1):
            ax.plot([cam[0], x0], [cam[1], 0.50 + sgn * h / 2], color=fs.FAINT,
                    lw=0.7, zorder=1)
        fs.label(ax, x0, 0.50 - h / 2 - 0.075, lab, fs=6.6, color=fs.MUTED)
    ax.plot([0.22, 0.22], [0.464, 0.536], color=fs.BLUE, lw=2.6, zorder=5)
    fs.label(ax, 0.235, 0.72, "投影宽度相同", fs=6.8, color=fs.BLUE, ha="left")
    fs.label(ax, 0.09, 0.20, "同一个相机", fs=6.6, color=fs.MUTED, ha="center")

    # ---------------- ④ 左右手混淆 -----------------------------
    ax = _panel(fig, [0.015, 0.06, 0.295, 0.38],
                "④ 左右手混淆",
                "镜像轮廓近似对称，朝向错了看不出来")
    hand_icon(ax, 0.26, 0.56, s=0.58, mirror=False, z=3)
    hand_icon(ax, 0.74, 0.56, s=0.58, mirror=True, z=3)
    ax.plot([0.50, 0.50], [0.28, 0.86], color=fs.ACCENT, lw=0.9, ls=(0, (3, 2)),
            zorder=5)
    fs.label(ax, 0.535, 0.80, "镜像轴", fs=6.6, color=fs.ACCENT, ha="left")
    fs.label(ax, 0.26, 0.26, "右手？", fs=6.8, color=fs.INK)
    fs.label(ax, 0.74, 0.26, "左手？", fs=6.8, color=fs.INK)

    # ---------------- ⑤ 关节顺序 -------------------------------
    ax = _panel(fig, [0.345, 0.06, 0.295, 0.38],
                "⑤ 关节顺序不一致",
                "编号错位：损失降不下去，手指“拧”着")
    names_pred = ["腕", "食指", "中指", "小指", "无名", "拇指"]
    names_gt = ["腕", "拇指", "食指", "中指", "无名", "小指"]
    w, gap, x0 = 0.122, 0.010, 0.145
    for names, yy, color, tag in [(names_pred, 0.66, fs.BLUE, "预测"),
                                  (names_gt, 0.40, fs.PURPLE, "标注")]:
        fs.label(ax, 0.03, yy + 0.05, tag, fs=6.6, color=color, ha="left")
        for i, nm in enumerate(names):
            fs.box(ax, x0 + i * (w + gap), yy - 0.05, w, 0.20, nm, ec=color, fs=6.4,
                   lw=0.8)
    for i, j in [(1, 2), (2, 4)]:
        xa = x0 + i * (w + gap) + w / 2
        xb = x0 + j * (w + gap) + w / 2
        ax.plot([xa, xb], [0.60, 0.51], color=fs.ACCENT, lw=0.9, zorder=6)
    fs.label(ax, 0.55, 0.28, "拇指被当成食指", fs=6.8, color=fs.ACCENT, ha="center")

    # ---------------- 右下：图例说明 ---------------------------
    ax = fig.add_axes([0.675, 0.08, 0.295, 0.34])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fs.box(ax, 0.02, 0.04, 0.96, 0.92, "", fc="#FBF9F5", ec=fs.GRID)
    fs.label(ax, 0.08, 0.84, "上下两组，修法不同", fs=7.6, weight="bold", ha="left")
    fs.label(ax, 0.08, 0.64, "①②③ 观测不足", fs=7.2, color=fs.INK, ha="left")
    fs.label(ax, 0.08, 0.51, "加观测（深度、视角、时序）", fs=6.8, color=fs.MUTED, ha="left")
    fs.label(ax, 0.08, 0.40, "或加强先验，无法根治", fs=6.8, color=fs.MUTED, ha="left")
    fs.label(ax, 0.08, 0.22, "④⑤ 标签与约定", fs=7.2, color=fs.INK, ha="left")
    fs.label(ax, 0.08, 0.10, "查一遍编号即可消除", fs=6.8, color=fs.MUTED, ha="left")

    fs.save(fig, "ch06", "fig06-03", dpi=230)


if __name__ == "__main__":
    fig06_03()
