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


def fig_axis_angle():
    fig, axs = plt.subplots(1, 3, figsize=(6.9, 2.6),
                            subplot_kw={"projection": "3d"})
    titles = ["绕 z 轴转", "绕 x 轴转", "绕任意轴 n 转"]
    axes = [(2, 0.9), (0, 1.2), (1, 0.8)]
    for ax, title, (which, ang) in zip(axs, titles, axes):
        ax.set_title(title, fontsize=9.5, pad=0)
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
        ax.set_axis_off()
        ax.quiver(0, 0, 0, 1, 0, 0, color="#9CA3AF", arrow_length_ratio=0.12, lw=1)
        ax.quiver(0, 0, 0, 0, 1, 0, color="#9CA3AF", arrow_length_ratio=0.12, lw=1)
        ax.quiver(0, 0, 0, 0, 0, 1, color="#9CA3AF", arrow_length_ratio=0.12, lw=1)
        R = _rot_axis(np.eye(3)[which], ang)
        v = R @ np.array([0.9, 0.35, 0.55])
        ax.quiver(0, 0, 0, *v, color=fs.ACCENT, arrow_length_ratio=0.12, lw=2)
        ax.quiver(0, 0, 0, *np.eye(3)[which], color=fs.BLUE, arrow_length_ratio=0.14, lw=2.2)
    fig.tight_layout()
    fs.save(fig, "ch04", "fig04-02")


def _rot_axis(n, a):
    n = np.asarray(n, float); n = n / np.linalg.norm(n)
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K


def fig_pinhole():
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.set_xlim(0, 3.9); ax.set_ylim(0, 3.7)
    ax.set_aspect("equal"); ax.axis("off")
    # 相机
    ax.add_patch(Circle((0, 0.2), 0.05, color=fs.INK, zorder=5))
    fs.label(ax, 0.0, 0.02, "光心 O", fs=9, va="top")
    # 光轴
    ax.plot([0, 3.6], [0.2, 0.2], color="#D1D5DB", lw=0.9, ls=":")
    # 像平面
    ax.plot([1.0, 1.0], [0.2, 1.75], color=fs.BLUE, lw=2.2)
    fs.label(ax, 0.98, 1.9, "像平面", fs=9, color=fs.BLUE, ha="right")
    # 三维点
    X, Z = 2.7, 2.6
    ax.plot([0, X], [0.2, Z], color=fs.MUTED, lw=1.1, ls="--")
    ax.plot([X, X], [0.2, Z], color="#D1D5DB", lw=0.8, ls=":")
    ax.plot([X, 0], [0.2, 0.2], color="#D1D5DB", lw=0.8, ls=":")
    ax.scatter([X], [Z], s=32, color=fs.ACCENT, zorder=5)
    fs.label(ax, X + 0.10, Z, "三维点 $(Y,Z)$", fs=9.2, ha="left", color=fs.ACCENT)
    xi = 1.0 * X / Z
    ax.scatter([1.0], [0.2 + xi], s=26, color=fs.ACCENT, zorder=5)
    fs.label(ax, 1.06, 0.2 + xi + 0.16, "像点 $y=fY/Z$", fs=8.8, ha="left", color=fs.ACCENT)
    ax.annotate("", xy=(X, 0.08), xytext=(0, 0.08),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    fs.label(ax, X / 2, -0.02, "$Z$（深度）", fs=8.8, color=fs.MUTED, va="top")
    ax.annotate("", xy=(3.55, 0.2), xytext=(3.55, Z),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    fs.label(ax, 3.64, Z / 2, "$Y$", fs=9, color=fs.MUTED, ha="left")
    ax.annotate("", xy=(1.0, 0.55), xytext=(0, 0.55),
                arrowprops=dict(arrowstyle="<->", color=fs.BLUE, lw=1.0))
    fs.label(ax, 0.5, 0.44, "焦距 $f$", fs=8.8, color=fs.BLUE, va="top")
    fs.label(ax, 0.05, 3.45, "针孔相机（侧视图）：三维点沿光线压到像平面，深度 $Z$ 越大，像越小",
             fs=9.6, ha="left", color=fs.INK)
    fs.save(fig, "ch04", "fig04-03")


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
    fs.save(fig, "ch04", "fig04-04")


if __name__ == "__main__":
    fig_rotation()
    fig_axis_angle()
    fig_pinhole()
    fig_mesh()
