# -*- coding: utf-8 -*-
"""全书统一绘图风格与常用图元。所有插图脚本都应 import 本文件。"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, Circle, Ellipse,
                                Polygon, Rectangle, Arc, Wedge)
from matplotlib.lines import Line2D

# ---------- 配色 ----------
INK    = "#1F2937"   # 主文字
MUTED  = "#6B7280"   # 次要文字
FAINT  = "#9CA3AF"
ACCENT = "#C2410C"   # 陶土橙（强调）
BLUE   = "#1D4ED8"
GREEN  = "#047857"
PURPLE = "#6D28D9"
GOLD   = "#B45309"
PINK   = "#BE185D"
TEAL   = "#0F766E"
LIGHT  = "#F3F4F6"
PAPER  = "#FBF7F0"
GRID   = "#E5E7EB"

PALETTE = [ACCENT, BLUE, GREEN, PURPLE, GOLD, PINK, TEAL]

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIGDIR = os.path.join(ROOT, "book", "images")

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Microsoft YaHei", "Noto Sans SC", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "font.size": 10.5,
    "axes.titlesize": 12,
    "axes.labelsize": 10.5,
    "axes.edgecolor": "#9CA3AF",
    "axes.linewidth": 0.8,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.grid": False,
    "grid.color": GRID,
    "grid.linewidth": 0.7,
    "legend.frameon": False,
    "legend.fontsize": 9,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.12,
    "svg.fonttype": "none",
})


def new(w=6.6, h=3.7, ncols=1, nrows=1, **kw):
    fig, ax = plt.subplots(nrows, ncols, figsize=(w, h), **kw)
    return fig, ax


def clean(ax, grid=False, spines=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in spines)
    if grid:
        ax.grid(True, zorder=0)
        ax.set_axisbelow(True)
    return ax


def save(fig, chapter, name, dpi=220, facecolor="white"):
    """chapter 可以写 "ch07" 或 "07"，统一落到 book/images/07/。"""
    chap = chapter[2:] if chapter.startswith("ch") else chapter
    d = os.path.join(FIGDIR, chap)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name + ".png")
    fig.savefig(p, dpi=dpi, facecolor=facecolor)
    plt.close(fig)
    print("saved", os.path.relpath(p, ROOT))
    return p


def box(ax, x, y, w, h, text, fc="#FFFFFF", ec=INK, tc=INK, fs=9.5, lw=1.0,
        rounded=0.02, weight="normal", ha="center", va="center", alpha=1.0, z=3):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.006,rounding_size={rounded}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, alpha=alpha, zorder=z)
    ax.add_patch(p)
    ax.text(x + w / 2 if ha == "center" else x + 0.012, y + h / 2, text,
            ha=ha, va=va, fontsize=fs, color=tc, weight=weight, zorder=z + 1,
            linespacing=1.5)
    return p


def arrow(ax, p0, p1, color=MUTED, lw=1.2, style="-|>", ls="-", rad=0.0, z=2, ms=8):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color,
                        lw=lw, linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=z,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)
    return a


def canvas(w=6.6, h=3.7, xlim=(0, 1), ylim=(0, 1)):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


# ---------- 人体示意（2D 铰接图元，用于概念图） ----------
def limb(ax, p0, p1, w0, w1, color=INK, alpha=1.0, z=3, ec="none"):
    """画一条带锥度的肢体（用四边形+半圆端）。"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
    d = p1 - p0
    L = np.linalg.norm(d)
    if L < 1e-9:
        return
    n = np.array([-d[1], d[0]]) / L
    pts = [p0 + n * w0 / 2, p1 + n * w1 / 2, p1 - n * w1 / 2, p0 - n * w0 / 2]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=ec, lw=0.6,
                         alpha=alpha, zorder=z))
    ax.add_patch(Circle(p0, w0 / 2, facecolor=color, edgecolor=ec, lw=0.6, alpha=alpha, zorder=z))
    ax.add_patch(Circle(p1, w1 / 2, facecolor=color, edgecolor=ec, lw=0.6, alpha=alpha, zorder=z))


def human(ax, cx=0.5, cy=0.5, s=1.0, pose=None, color=INK, alpha=1.0, z=3,
          width=1.0, show_joints=False, joint_color=ACCENT):
    """极简人体：头 + 颈 + 梯形躯干 + 四肢。

    会自动根据坐标轴的长宽比修正横向比例，保证在非等比例画布上也不会被拉扁。
    pose keys: l_arm, r_arm, l_leg, r_leg, lean, head
    """
    pose = pose or {}
    ang = lambda k, d=0.0: pose.get(k, d)
    # 横向补偿：1 个数据单位在屏幕上对应的英寸比
    try:
        fw, fh = ax.figure.get_size_inches()
        xr = ax.get_xlim()[1] - ax.get_xlim()[0]
        yr = ax.get_ylim()[1] - ax.get_ylim()[0]
        sx = (fh / yr) / (fw / xr)
    except Exception:
        sx = 1.0
    lean = ang("lean")
    hip = np.array([cx, cy - 0.02 * s])
    neck = hip + np.array([np.sin(lean) * 0.28 * sx, np.cos(lean) * 0.28]) * s
    head_c = neck + np.array([np.sin(lean + ang("head")) * 0.105 * sx,
                              np.cos(lean + ang("head")) * 0.105]) * s

    # 躯干：髋 → 胸 → 肩
    chest = hip + (neck - hip) * 0.72
    w_hip, w_chest, w_sh = 0.070, 0.082, 0.094
    pts = [(hip[0] - w_hip * s * width * sx, hip[1]),
           (chest[0] - w_chest * s * width * sx, chest[1]),
           (neck[0] - w_sh * s * width * sx, neck[1]),
           (neck[0] + w_sh * s * width * sx, neck[1]),
           (chest[0] + w_chest * s * width * sx, chest[1]),
           (hip[0] + w_hip * s * width * sx, hip[1])]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor="none",
                         alpha=alpha, zorder=z))
    # 脖子 + 头
    head_bottom = head_c - np.array([0, 0.036 * s])
    limb(ax, neck, head_bottom, 0.036 * s * sx, 0.030 * s * sx, color, alpha, z)
    ax.add_patch(Ellipse(head_c, 2 * 0.045 * s * sx, 2 * 0.045 * s,
                         facecolor=color, edgecolor="none", alpha=alpha, zorder=z + 1))
    # 手臂
    for side, key in ((-1, "l_arm"), (1, "r_arm")):
        a = ang(key, 0.16)
        th = np.pi - side * a
        sh = neck + np.array([side * 0.096 * s * sx, -0.042 * s])
        elbow = sh + np.array([np.sin(th) * 0.155 * s * sx, np.cos(th) * 0.155 * s])
        wrist = elbow + np.array([np.sin(th + side * 0.10) * 0.145 * s * sx,
                                  np.cos(th + side * 0.10) * 0.145 * s])
        limb(ax, sh, elbow, 0.056 * s * width * sx, 0.045 * s * width * sx, color, alpha, z)
        limb(ax, elbow, wrist, 0.045 * s * width * sx, 0.034 * s * width * sx, color, alpha, z)
    # 腿
    for side, key in ((-1, "l_leg"), (1, "r_leg")):
        a = ang(key, 0.08) * (1 if side == 1 else -1)
        knee = hip + np.array([side * 0.045 * s * sx + np.sin(a) * 0.22 * s * sx, -np.cos(a) * 0.22 * s])
        ankle = knee + np.array([np.sin(a * 0.5) * 0.21 * s * sx, -np.cos(a * 0.5) * 0.21 * s])
        limb(ax, hip + np.array([side * 0.045 * s * sx, 0]), knee,
             0.080 * s * width * sx, 0.061 * s * width * sx, color, alpha, z)
        limb(ax, knee, ankle, 0.061 * s * width * sx, 0.042 * s * width * sx, color, alpha, z)
        ax.add_patch(Ellipse(ankle + np.array([side * 0.012 * s * sx, -0.012 * s]),
                             0.085 * s * sx, 0.032 * s, facecolor=color, edgecolor="none",
                             alpha=alpha, zorder=z))
    if show_joints:
        for p in [hip, neck, head_c]:
            ax.add_patch(Circle(p, 0.011 * s * sx, facecolor=joint_color, edgecolor="white",
                                lw=0.8, zorder=z + 4))


def mesh_disk(ax, cx=0.5, cy=0.5, rx=0.25, ry=0.35, n=14, color="#CBD5E1",
              ec=BLUE, lw=0.5, z=2, alpha=1.0, jitter=0.0, seed=0):
    """在椭圆内生成三角网格，用于示意“网格/顶点”。"""
    rng = np.random.default_rng(seed)
    pts = [(cx, cy)]
    for r in np.linspace(0.35, 1.0, 4):
        k = max(6, int(n * r))
        for i in range(k):
            th = 2 * np.pi * i / k + r
            j = rng.normal(0, jitter) if jitter else 0
            pts.append((cx + rx * r * np.cos(th) + j, cy + ry * r * np.sin(th) + j))
    pts = np.array(pts)
    from matplotlib.tri import Triangulation
    tri = Triangulation(pts[:, 0], pts[:, 1])
    ax.triplot(tri, color=ec, lw=lw, zorder=z, alpha=alpha)
    ax.scatter(pts[:, 0], pts[:, 1], s=4, color=color, zorder=z + 1, alpha=alpha)
    return pts


def label(ax, x, y, text, fs=9, color=INK, ha="center", va="center", weight="normal", z=10, **kw):
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va, weight=weight, zorder=z,
            linespacing=1.5, **kw)


def cover(path=None):
    """生成书籍封面插画（无文字，文字由 HTML 叠加）。"""
    fig = plt.figure(figsize=(8, 11))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    # 背景渐变
    import matplotlib.colors as mcolors
    g = np.linspace(0, 1, 256).reshape(-1, 1)
    cmap = mcolors.LinearSegmentedColormap.from_list("bg", ["#FDFBF7", "#F1E8DC"])
    ax.imshow(g, extent=[0, 1, 0, 1], aspect="auto", cmap=cmap, origin="lower", zorder=0)
    # 装饰网格
    for i in range(28):
        ax.plot([0, 1], [i / 28, i / 28 + 0.35], color="#E7DCCB", lw=0.5, alpha=0.55, zorder=1)
    # 人体剪影序列
    poses = [dict(l_arm=0.25, r_arm=0.1, l_leg=0.18), dict(l_arm=0.1, r_arm=0.12),
             dict(l_arm=0.45, r_arm=0.3, l_leg=0.25, r_leg=0.1),
             dict(l_arm=0.15, r_arm=0.5, l_leg=0.1, r_leg=0.3)]
    cols = ["#E8D5C4", "#DCC3AE", "#C9A98F", "#A9785A"]
    for i, (p, c) in enumerate(zip(poses, cols)):
        human(ax, cx=0.19 + i * 0.21, cy=0.42, s=0.52, pose=p, color=c, alpha=1.0, z=2 + i)
    # 上方网格球
    mesh_disk(ax, cx=0.5, cy=0.795, rx=0.17, ry=0.13, n=16, color="#B08968", ec="#8B5E3C",
              lw=0.45, z=6, alpha=0.9)
    ax.plot([0.12, 0.88], [0.12, 0.12], color=ACCENT, lw=1.2, zorder=9)
    p = path or os.path.join(ROOT, "book", "images", "cover", "cover_front.jpg")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    fig.savefig(p, dpi=200, facecolor="white")
    plt.close(fig)
    print("saved", p)


if __name__ == "__main__":
    cover()


# ---------- 常用版式 ----------
def flow(ax, labels, y=0.5, w=None, h=0.22, gap=None, colors=None, fs=9, x0=0.04, x1=0.96):
    """横向流程：若干个圆角框 + 箭头。"""
    n = len(labels)
    if w is None:
        gap = gap if gap is not None else 0.022
        w = (x1 - x0 - gap * (n - 1)) / n
    else:
        gap = gap if gap is not None else 0.022
    xs = []
    for i, lab in enumerate(labels):
        x = x0 + i * (w + gap)
        c = (colors[i] if colors else INK)
        box(ax, x, y - h / 2, w, h, lab, fc="white", ec=c, fs=fs, lw=1.2)
        xs.append((x, x + w))
        if i:
            arrow(ax, (xs[i - 1][1] + 0.002, y), (x - 0.002, y), color=FAINT, lw=1.0)
    return xs


def timeline(ax, items, y=0.5, up=True, color=INK, accent=ACCENT, fs=8.6, span=None):
    """时间轴。items: [(year, label, sub)]，交替上下标注。"""
    years = [it[0] for it in items]
    lo, hi = (span or (min(years), max(years)))
    ax.plot([0.04, 0.96], [y, y], color=color, lw=1.3, zorder=2)
    for i, it in enumerate(items):
        yr, lab = it[0], it[1]
        sub = it[2] if len(it) > 2 else ""
        x = 0.07 + 0.86 * (yr - lo) / max(1e-9, (hi - lo))
        above = (i % 2 == 0)
        yy = y + 0.19 if above else y - 0.19
        ax.plot([x, x], [y, yy], color=FAINT, lw=0.8, zorder=1)
        ax.scatter([x], [y], s=22, color=accent, zorder=3, edgecolor="white", linewidth=0.8)
        va = "bottom" if above else "top"
        label(ax, x, yy + (0.05 if above else -0.05), f"{yr}", fs=fs + 0.2, color=accent,
              weight="bold", va=va)
        label(ax, x, yy + (0.13 if above else -0.13), lab, fs=fs, color=INK, va=va)
        if sub:
            label(ax, x, yy + (0.20 if above else -0.20), sub, fs=fs - 1.2, color=MUTED, va=va)


def human_row(ax, n=5, cy=0.48, s=0.75, widths=None, poses=None, colors=None, labels=None, gap=0.16):
    widths = widths or [1.0] * n
    for i in range(n):
        cx = 0.5 + (i - (n - 1) / 2) * gap
        c = colors[i] if colors else INK
        p = poses[i] if poses else {}
        human(ax, cx=cx, cy=cy, s=s, pose=p, color=c, width=widths[i], z=3)
        if labels:
            label(ax, cx, cy - 0.48 * s, labels[i], fs=8.6, color=MUTED)


def bracket(ax, x0, x1, y, text, color=MUTED, fs=8.6, dy=0.02):
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    label(ax, (x0 + x1) / 2, y + dy, text, fs=fs, color=color)
