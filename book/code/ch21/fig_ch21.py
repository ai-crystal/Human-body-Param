# -*- coding: utf-8 -*-
"""第 21 章插图：接触状态与摩擦锥、数据集对比、表示演化。"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Wedge, Ellipse, FancyArrowPatch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import figstyle as fs

SKIN = "#F7F0E7"
OBJ = "#EFE7DC"


def _finger(ax, x_tip=0.52, y=0.50, length=0.42, hw=0.055, z=4, alpha=1.0):
    """从左向右伸出的手指（侧视），返回指尖中心。"""
    p0 = np.array([x_tip - length, y])
    p1 = np.array([x_tip, y])
    fs.limb(ax, p0, p1, hw * 2.2, hw * 1.9, color=SKIN, z=z, ec=fs.FAINT, alpha=alpha)
    ax.add_patch(Circle(p1, hw, facecolor=SKIN, edgecolor=fs.FAINT, lw=0.8,
                        zorder=z + 1, alpha=alpha))
    ax.add_patch(Circle((x_tip - length * 0.62, y), 0.010, facecolor=fs.ACCENT,
                        edgecolor="white", lw=0.9, zorder=z + 2))
    return p1


def _object(ax, x0=0.66, x1=0.94, y0=0.24, y1=0.76, fc=OBJ, ec=fs.INK, lw=1.0, z=3,
            taper=0.022):
    body = [(x0, y0), (x0 + taper, y1), (x1 - taper, y1), (x1, y0)]
    ax.add_patch(Polygon(body, closed=True, facecolor=fc, edgecolor=ec, lw=lw, zorder=z))
    ax.add_patch(Ellipse(((x0 + x1) / 2, y1), (x1 - x0) - 2 * taper, 0.05,
                         facecolor="white", edgecolor=ec, lw=lw, zorder=z + 1))
    return np.array([x0 + taper / 2, 0.0])


def fig21_01():
    fig = plt.figure(figsize=(6.6, 3.2))

    # ---------------- ① 悬空
    ax = fig.add_axes([0.012, 0.06, 0.315, 0.80])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.5, 1.00, "① 悬空：没有接触", fontsize=8.4, ha="center", va="top", weight="bold")
    _object(ax, x0=0.740, x1=0.985)
    tip = _finger(ax, x_tip=0.575)
    ax.annotate("", xy=(0.607, 0.600), xytext=(0.733, 0.600),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    fs.label(ax, 0.670, 0.655, r"$d>0$", fs=8.4, color=fs.MUTED)
    fs.label(ax, 0.5, 0.115, "两项损失都接近 0，", fs=7.2, color=fs.MUTED)
    fs.label(ax, 0.5, 0.065, "但“抓住”无从谈起", fs=7.2, color=fs.MUTED)

    # ---------------- ② 穿透
    ax = fig.add_axes([0.337, 0.06, 0.315, 0.80])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.5, 1.00, "② 穿透：有符号距离为负", fontsize=8.4, ha="center", va="top", weight="bold")
    _object(ax, x0=0.740, x1=0.985, fc="none", ec=fs.MUTED)
    tip = _finger(ax, x_tip=0.760, z=2)
    ax.add_patch(Circle(tip, 0.055, facecolor=fs.ACCENT, alpha=0.30, edgecolor=fs.ACCENT,
                        lw=0.9, zorder=5))
    ax.annotate("", xy=(0.738, 0.650), xytext=(0.878, 0.650),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=0.9))
    fs.label(ax, 0.855, 0.598, r"$d<0$", fs=8.4, color=fs.ACCENT)
    fs.label(ax, 0.5, 0.115, "式 (21.2) 惩罚陷进去的顶点，", fs=7.2, color=fs.MUTED)
    fs.label(ax, 0.5, 0.065, "网格必须被推回表面", fs=7.2, color=fs.MUTED)

    # ---------------- ③ 接触点放大：摩擦锥
    ax = fig.add_axes([0.662, 0.06, 0.325, 0.80])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.5, 1.00, "③ 接触点放大：摩擦锥", fontsize=8.4, ha="center", va="top", weight="bold")

    y_surf = 0.34
    ax.add_patch(Polygon([(0.08, y_surf), (0.94, y_surf), (0.94, 0.22), (0.08, 0.22)],
                         closed=True, facecolor=OBJ, edgecolor="none", zorder=1))
    ax.plot([0.08, 0.94], [y_surf, y_surf], color=fs.INK, lw=1.8, zorder=2)
    fs.label(ax, 0.92, 0.265, "物体表面", fs=7.0, color=fs.MUTED, ha="right")
    ax.add_patch(Ellipse((0.42, y_surf + 0.075), 0.26, 0.09, facecolor=SKIN,
                         edgecolor=fs.FAINT, lw=0.8, zorder=4))
    fs.label(ax, 0.615, y_surf + 0.105, "指腹（软接触）", fs=7.2, ha="left")

    cpt = (0.42, y_surf)
    mu = 0.5
    ang = np.degrees(np.arctan(mu))
    ax.add_patch(Wedge(cpt, 0.46, 90 - ang, 90 + ang, facecolor=fs.ACCENT, alpha=0.13,
                       edgecolor=fs.ACCENT, lw=0.7, zorder=3))
    ax.annotate("", xy=(0.42, 0.86), xytext=cpt,
                arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=1.1))
    fs.label(ax, 0.44, 0.875, r"法线 $\mathbf{n}$", fs=7.4, color=fs.BLUE, ha="left")

    th = np.deg2rad(64)
    fx, fy = 0.42 + 0.34 * np.cos(th), y_surf + 0.34 * np.sin(th)
    ax.annotate("", xy=(fx, fy), xytext=cpt,
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.1))
    fs.label(ax, fx + 0.02, fy, r"$\mathbf{f}$", fs=7.4, color=fs.ACCENT, ha="left")

    ax.add_patch(Wedge(cpt, 0.14, 90, 90 + ang, facecolor="none", edgecolor=fs.MUTED, lw=0.6))
    fs.label(ax, 0.28, y_surf + 0.135, r"$\arctan\mu$", fs=7.2, color=fs.MUTED, ha="right")
    fs.label(ax, 0.5, 0.115, "接触力必须落在锥内，", fs=7.2, color=fs.MUTED)
    fs.label(ax, 0.5, 0.065, "否则接触点会打滑（式 21.3）", fs=7.2, color=fs.MUTED)

    fs.save(fig, "ch21", "fig21-02")


def fig21_02():
    fig, ax = fs.canvas(6.6, 3.5, xlim=(0, 1), ylim=(0, 1))
    fs.label(ax, 0.5, 0.955, "四个代表性数据集：采集方式决定了能拿到什么", fs=9.8, weight="bold")

    cols = ["数据集", "输入模态", "规模", "物体", "标注方式"]
    widths = [0.135, 0.175, 0.205, 0.185, 0.265]
    rows = [
        ("ObMan", "合成 RGB", "14.1 万帧（训练）", "2772 个网格（8 类）", "仿真抓取 + 渲染，标注完美", fs.GOLD),
        ("GRAB", "真实 MoCap", "10 人 · 51 件物体", "真实扫描 + 接触图", "手背标记点，掌心无遮挡", fs.GREEN),
        ("HO-3D", "真实 RGB-D", "68 段 · 77558 帧", "10 件物体", "多视角联合优化标注", fs.BLUE),
        ("DexYCB", "真实 RGB-D × 8", "1000 段 · 58.2 万帧", "20 件 YCB 物体", "众包 2D 关键点 + 三角化", fs.PURPLE),
    ]

    x0, y0 = 0.035, 0.76
    hh = 0.115
    x = x0
    for w, c in zip(widths, cols):
        fs.label(ax, x + 0.008, y0 + hh * 0.55, c, fs=7.8, color=fs.MUTED, ha="left",
                 weight="bold")
        x += w
    ax.plot([x0, x0 + sum(widths)], [y0 + 0.006, y0 + 0.006], color=fs.INK, lw=0.9)

    for i, row in enumerate(rows):
        y = y0 - (i + 1) * hh
        if i % 2 == 0:
            ax.add_patch(Polygon([(x0, y + 0.012), (x0 + sum(widths), y + 0.012),
                                  (x0 + sum(widths), y + hh + 0.012), (x0, y + hh + 0.012)],
                                 closed=True, facecolor="#F7F5F1", edgecolor="none", zorder=1))
        x = x0
        for k, (w, cell) in enumerate(zip(widths, row[:5])):
            color = row[5] if k == 0 else fs.INK
            weight = "bold" if k == 0 else "normal"
            fs.label(ax, x + 0.008, y + hh * 0.52, cell, fs=7.3, color=color, ha="left",
                     weight=weight, z=4)
            x += w

    fs.label(ax, 0.035, 0.105,
             "共同困境：真实数据的规模被采集成本锁死，合成数据的真实度被渲染器锁死。",
             fs=7.4, color=fs.INK, ha="left")
    fs.label(ax, 0.035, 0.045,
             "注意 GRAB 的“掌心无标记”——只有这样才能采到真实的掌面接触，而掌面恰恰是抓取最关键的区域。",
             fs=7.2, color=fs.MUTED, ha="left")

    fs.save(fig, "ch21", "fig21-01")


def _cup_shape(cx=0.60, cy=0.50, w=0.34, h=0.42, taper=0.035):
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    return [(x0, y0), (x0 + taper, y1), (x1 - taper, y1), (x1, y0)], (x0, x1, y0, y1)


def fig21_03():
    fig = plt.figure(figsize=(6.6, 3.15))
    titles = ["① 已知模板 + MANO 拟合", "② 类别无关的隐式表面", "③ 关节化高斯点"]
    subs = ["物体是刚体网格，只有 6 个位姿自由度",
            "物体是 SDF 网络，拓扑自由、需多帧",
            "手与物体都是高斯点，手绑在骨架上"]

    for k in range(3):
        ax = fig.add_axes([0.015 + k * 0.327, 0.10, 0.31, 0.78])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        ax.text(0.5, 0.99, titles[k], fontsize=8.4, ha="center", va="top", weight="bold")

        body, (x0, x1, y0, y1) = _cup_shape()
        taper = 0.035

        if k == 0:
            ax.add_patch(Polygon(body, closed=True, facecolor=OBJ, edgecolor=fs.BLUE,
                                 lw=1.0, zorder=2))
            for i in range(1, 6):
                t = i / 6
                yy = y0 + t * (y1 - y0)
                ax.plot([x0 + taper * t + 0.004, x1 - taper * t - 0.004],
                        [yy, yy], color=fs.BLUE, lw=0.4, alpha=0.45, zorder=3)
            for i in range(1, 6):
                t = i / 6
                ax.plot([x0 + taper + t * (x1 - x0 - 2 * taper)] * 2, [y0, y1],
                        color=fs.BLUE, lw=0.4, alpha=0.35, zorder=3)
            ax.annotate("", xy=(x0 - 0.02, y0 - 0.03), xytext=(x1 + 0.02, y0 - 0.03),
                        arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.8))
            fs.label(ax, 0.60, y0 - 0.075, "6 DoF 位姿", fs=7.0, color=fs.MUTED)
        elif k == 1:
            ax.add_patch(Polygon(body, closed=True, facecolor="#F2EEF8", edgecolor=fs.PURPLE,
                                 lw=1.2, zorder=2))
            for s in (0.03, 0.065, 0.10):
                ax.add_patch(Polygon([(p[0] + (-s if p[0] < 0.6 else s),
                                       p[1] + (-s if p[1] < 0.5 else s)) for p in body],
                                     closed=True, facecolor="none", edgecolor=fs.PURPLE,
                                     lw=0.5, alpha=0.5, ls=(0, (3, 2)), zorder=1))
            fs.label(ax, 0.60, 0.50, r"$\mathrm{SDF}=0$", fs=7.2, color=fs.PURPLE)
            fs.label(ax, 0.60, 0.13, "等值面", fs=6.8, color=fs.PURPLE)
        else:
            rng = np.random.default_rng(5)
            for _ in range(190):
                t = rng.uniform(0, 1)
                yy = y0 + t * (y1 - y0)
                if rng.uniform() < 0.6:      # 靠近两侧壁
                    side = rng.choice([-1, 1])
                    xx = (x0 if side < 0 else x1) + side * taper * (1 - t) * 0
                    xx = (x0 + taper * t if side < 0 else x1 - taper * t) - side * rng.normal(0, 0.012)
                else:
                    xx = rng.uniform(x0 + taper, x1 - taper)
                ax.add_patch(Ellipse((xx, yy), 0.020, 0.013, angle=rng.uniform(0, 180),
                                     facecolor=fs.TEAL, alpha=0.40, edgecolor="none", zorder=2))
            ax.add_patch(Polygon(body, closed=True, facecolor="none", edgecolor=fs.TEAL,
                                 lw=0.7, ls=(0, (3, 2)), alpha=0.55, zorder=3))

        # 手指从左侧伸向物体
        tip = _finger(ax, x_tip=x0 + 0.02, y=0.56, length=0.30, hw=0.048, z=4)
        if k == 2:
            rng2 = np.random.default_rng(11)
            for _ in range(26):
                xx = rng2.uniform(0.14, 0.33)
                yy = 0.56 + rng2.normal(0, 0.035)
                ax.add_patch(Ellipse((xx, yy), 0.018, 0.012, angle=rng2.uniform(0, 180),
                                     facecolor=fs.PURPLE, alpha=0.45, edgecolor="none",
                                     zorder=6))

        fs.label(ax, 0.5, 0.075, subs[k], fs=6.9, color=fs.MUTED)

    fs.save(fig, "ch21", "fig21-03")


if __name__ == "__main__":
    fig21_01()
    fig21_02()
    fig21_03()
