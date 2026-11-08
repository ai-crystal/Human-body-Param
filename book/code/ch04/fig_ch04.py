# -*- coding: utf-8 -*-
"""第 4 章插图：三维表示、旋转、相机投影。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyArrowPatch
import figstyle as fs


def rot2(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s], [s, c]])


def fig_rotation():
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.set_aspect("equal"); fs.clean(ax, grid=True)
    ax.set_xlim(-0.6, 2.6); ax.set_ylim(-0.6, 2.6)
    ax.axhline(0, color=fs.MUTED, lw=0.8); ax.axvline(0, color=fs.MUTED, lw=0.8)
    sq = np.array([[0, 0], [1.3, 0], [1.3, 1.3], [0, 1.3]])
    th = np.deg2rad(32)
    R = rot2(th)
    sq2 = sq @ R.T
    ax.add_patch(Polygon(sq, closed=True, fill=False, ls="--", ec="#9CA3AF", lw=1.2))
    ax.add_patch(Polygon(sq2, closed=True, fill=True, fc=fs.ACCENT, alpha=0.14, ec=fs.ACCENT, lw=1.6))
    for i, (p, q) in enumerate(zip(sq[1:3], sq2[1:3])):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=1.0, ls=":"))
    ax.annotate("", xy=R @ [1, 0], xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=2))
    fs.label(ax, *(R @ [1.05, 0] + 0.08), "旋转后的 $x$ 轴", fs=8.5, color=fs.BLUE)
    ax.annotate("", xy=R @ [0, 1], xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=2))
    fs.label(ax, *(R @ [0, 1.1] + 0.08), "旋转后的 $y$ 轴", fs=8.5, color=fs.GREEN)
    # 角度弧
    arc = np.linspace(0, th, 40)
    ax.plot(0.45 * np.cos(arc), 0.45 * np.sin(arc), color=fs.ACCENT, lw=1.2)
    fs.label(ax, 0.36, 0.16, r"$\theta$", fs=11, color=fs.ACCENT)
    ax.set_title("二维旋转：形状整体转动，边长与夹角不变", fontsize=10)
    fs.save(fig, "ch04", "fig04-01")



def _rot_axis(n, a):
    n = np.asarray(n, float); n = n / np.linalg.norm(n)
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K


def fig_pinhole():
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.set_xlim(-0.35, 4.05); ax.set_ylim(-0.55, 3.75)
    ax.set_aspect("equal"); ax.axis("off")

    OY = 0.20          # 光轴高度
    F = 1.00           # 焦距（像平面到光心的水平距离）
    X, Z = 2.70, 2.60  # 三维点的水平位置与高度

    # 光心（留出左边距，避免圆点被裁掉）
    ax.add_patch(Circle((0, OY), 0.055, color=fs.INK, zorder=6))
    fs.label(ax, 0.0, OY - 0.10, "光心 $O$", fs=9, va="top")

    # 光轴
    ax.plot([-0.25, 3.75], [OY, OY], color="#C9CDD3", lw=0.9, ls=":")

    # 像平面
    ax.plot([F, F], [OY, 1.85], color=fs.BLUE, lw=2.2, zorder=4)
    fs.label(ax, F - 0.05, 1.95, "像平面", fs=9, color=fs.BLUE, ha="right")

    # 三维点与光线
    ax.plot([0, X], [OY, Z], color=fs.MUTED, lw=1.1, ls="--", zorder=2)
    ax.plot([X, X], [OY, Z], color="#D1D5DB", lw=0.8, ls=":")
    ax.plot([0, X], [OY, OY], color="#D1D5DB", lw=0.8, ls=":")
    ax.scatter([X], [Z], s=34, color=fs.ACCENT, zorder=6)
    fs.label(ax, X + 0.10, Z + 0.06, "三维点 $(Y,Z)$", fs=9.2, ha="left",
             va="bottom", color=fs.ACCENT)

    # 像点：光线与像平面的交点（y = f·Y/Z）
    y_img = OY + (Z - OY) * F / X
    ax.scatter([F], [y_img], s=28, color=fs.ACCENT, zorder=6)
    fs.label(ax, F + 0.08, y_img - 0.16, "像点 $y=fY/Z$", fs=8.8, ha="left",
             va="top", color=fs.ACCENT)

    # 焦距 f：贴在光轴上方（避开光心标签与光线）
    yf = OY + 0.075
    ax.annotate("", xy=(F, yf), xytext=(0, yf),
                arrowprops=dict(arrowstyle="<->", color=fs.BLUE, lw=1.0))
    fs.label(ax, F / 2, yf + 0.025, "焦距 $f$", fs=8.8, color=fs.BLUE, va="bottom")

    # 深度 Z：再往下一层
    yz = OY - 0.40
    ax.annotate("", xy=(X, yz), xytext=(0, yz),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    fs.label(ax, X / 2, yz - 0.04, "$Z$（深度）", fs=8.8, color=fs.MUTED, va="top")

    # 高度 Y
    ax.annotate("", xy=(3.55, OY), xytext=(3.55, Z),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    fs.label(ax, 3.64, (OY + Z) / 2, "$Y$", fs=9, color=fs.MUTED, ha="left")

    fs.label(ax, -0.30, 3.55,
             "针孔相机（侧视图）：三维点沿光线压到像平面，深度 $Z$ 越大，像越小",
             fs=9.4, ha="left", color=fs.INK)
    fs.save(fig, "ch04", "fig04-02")


def fig_mesh():
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    ax.set_aspect("equal"); ax.axis("off")
    pts = np.array([[0.1, 0.2], [0.45, 0.1], [0.7, 0.4], [0.62, 0.78], [0.3, 0.88], [0.05, 0.6]])
    tris = [[0, 1, 2], [0, 2, 5], [2, 3, 4], [2, 4, 5]]
    for t in tris:
        ax.add_patch(Polygon(pts[t], closed=True, fill=True, fc="#FDF6EC", ec=fs.ACCENT, lw=1.2))
    ax.scatter(pts[:, 0], pts[:, 1], s=26, color=fs.BLUE, zorder=5)
    for i, p in enumerate(pts):
        ax.text(p[0], p[1] + 0.05, f"v{i}", fontsize=8, color=fs.BLUE, ha="center")
    # 法线
    for t in tris[:3]:
        c = pts[t].mean(0)
        ax.annotate("", xy=c + np.array([0.10, 0.10]), xytext=c,
                    arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=1.2))
    fs.label(ax, 0.88, 0.82, "面片", fs=9, color=fs.ACCENT)
    fs.label(ax, 0.86, 0.68, "顶点 $\\mathbf{v}_i\\in\\mathbb{R}^3$", fs=9, color=fs.BLUE)
    fs.label(ax, 0.86, 0.54, "法线 $\\mathbf{n}$", fs=9, color=fs.GREEN)
    ax.set_xlim(0, 1.15); ax.set_ylim(0, 1.0)
    ax.set_title("三角网格：顶点 + 边 + 面；每个面有朝向，每个顶点可带法线", fontsize=9.8)
    fs.save(fig, "ch04", "fig04-03")


if __name__ == "__main__":
    fig_rotation()
    fig_pinhole()
    fig_mesh()
