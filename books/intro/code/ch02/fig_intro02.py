# -*- coding: utf-8 -*-
"""入门册第 2 章插图：对应（配准）、参数空间直觉、主成分取舍。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))               # books/<册>
sys.path.insert(0, os.path.join(os.path.dirname(BOOK), "code"))      # books/code（共用 figstyle）
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import figstyle as fs

FIGDIR = os.path.join(BOOK, "images")


def ellipse_cloud(n=60, seed=7):
    """二维点云：沿 p1 方向拉长，沿 p2 方向很薄。"""
    rng = np.random.default_rng(seed)
    t = rng.normal(0, 1, n)
    s = rng.normal(0, 0.28, n)
    th = np.deg2rad(28)
    p1 = np.array([np.cos(th), np.sin(th)])
    p2 = np.array([-np.sin(th), np.cos(th)])
    pts = np.outer(t, p1) + np.outer(s, p2)
    return pts, p1, p2


# ---------------- 图 2-1 对应：同一编号必须落在同一个解剖位置 ----------------
def _body_points(cx=0.0, cy=0.0, rx=0.30, ry=0.42, n=8, seed=3, jitter=0.03):
    """一个人形轮廓上的若干“解剖点”，位置固定，编号由调用者给。"""
    rng = np.random.default_rng(seed)
    pts = []
    for i in range(n):
        th = 2 * np.pi * i / n + 0.28
        r = 1.0 + rng.normal(0, jitter)
        pts.append((cx + rx * r * np.cos(th) * 1.0, cy + ry * r * np.sin(th)))
    return np.array(pts)


def fig_correspondence():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))
    a = _body_points(cx=-0.62, seed=3)
    b = _body_points(cx=0.62, seed=11)

    good = np.arange(len(a))
    bad = np.array([0, 4, 1, 6, 2, 7, 3, 5])

    titles = ["① 编号对得上：差异就是体型", "② 编号错位：差异全是假的"]
    for ax, mapping, title, col in ((axes[0], good, titles[0], fs.GREEN),
                                    (axes[1], bad, titles[1], fs.ACCENT)):
        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-0.72, 0.62)
        ax.axis("off")
        ax.set_title(title, fontsize=9.3, pad=2, color=fs.INK)
        # 两个“人”的轮廓
        for pts, cc in ((a, "#DCE3EC"), (b, "#DCE3EC")):
            ax.add_patch(plt.Polygon(pts, closed=True, facecolor=cc, edgecolor="#B7C2D0",
                                     lw=1.0, zorder=1))
        # 对应关系连线
        for i, j in enumerate(mapping):
            ax.plot([a[i, 0], b[j, 0]], [a[i, 1], b[j, 1]], color=col,
                    lw=1.0, alpha=0.75, zorder=2)
        # 顶点与编号
        for pts, tag in ((a, "A"), (b, "B")):
            for i, (x, y) in enumerate(pts):
                ax.add_patch(Circle((x, y), 0.052, facecolor="white", edgecolor=col,
                                    lw=1.0, zorder=4))
                ax.text(x, y, str(i + 1), ha="center", va="center", fontsize=6.6,
                        color=fs.INK, zorder=5)
        ax.text(-0.62, 0.50, "体型 A", fontsize=7.6, color=fs.MUTED, ha="center")
        ax.text(0.62, 0.50, "体型 B", fontsize=7.6, color=fs.MUTED, ha="center")

    # 注释：放在两个面板底部，避免压住图形
    fs.label(axes[0], 0.0, -0.63, "连线两边平行 → 逐点相减得到真实的胖瘦",
             fs=7.9, color=fs.GREEN)
    fs.label(axes[1], 0.0, -0.63, "连线互相交叉 → 相减得到的只是一堆噪声",
             fs=7.9, color=fs.ACCENT)

    fig.tight_layout(pad=0.6, w_pad=1.6)
    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch02", "fig02-01")


# ---------------- 图 2-2 高维点云其实躺在一张薄片上 ----------------
def fig_space():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.1))
    pts, p1, p2 = ellipse_cloud()

    ax = axes[0]
    fs.clean(ax, grid=True)
    ax.scatter(pts[:, 0], pts[:, 1], s=9, color=fs.BLUE, alpha=0.55, lw=0)
    ax.set_title("① 一堆拉长的点云", fontsize=9.4, pad=4)
    ax.set_xlabel("$x_1$", fontsize=9)
    ax.set_ylabel("$x_2$", fontsize=9)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7.8)

    ax = axes[1]
    fs.clean(ax, grid=True)
    ax.scatter(pts[:, 0], pts[:, 1], s=9, color="#C9D3DF", alpha=0.85, lw=0)
    lo, hi = -2.2, 2.2
    ax.plot([lo * p1[0], hi * p1[0]], [lo * p1[1], hi * p1[1]],
            color=fs.ACCENT, lw=1.1, ls="--", alpha=0.8)
    ax.annotate("", xy=1.55 * p1, xytext=np.zeros(2),
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.8))
    ax.annotate("", xy=0.55 * p2, xytext=np.zeros(2),
                arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=1.5))
    ax.text(1.62 * p1[0] + 0.02, 1.62 * p1[1] + 0.13, "$\\mathbf{p}_1$",
            color=fs.ACCENT, fontsize=9.6, ha="center")
    ax.text(0.62 * p2[0] + 0.09, 0.62 * p2[1], "$\\mathbf{p}_2$",
            color=fs.GREEN, fontsize=9.6, ha="left", va="center")
    ax.set_title("② 换到 $\\mathbf{p}_1,\\mathbf{p}_2$ 看：几乎只剩一个方向",
                 fontsize=9.4, pad=4)
    ax.set_xlabel("$x_1$", fontsize=9)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7.8)

    fig.tight_layout(pad=0.5, w_pad=1.2)
    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch02", "fig02-02")


# ---------------- 图 2-3 平均人 + 三个滑块 = 一个人 ----------------
def fig_sliders():
    fig = plt.figure(figsize=(6.9, 2.9))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0.03, 0.14), 0.17, 0.60,
                                boxstyle="round,pad=0.008,rounding_size=0.02",
                                ec=fs.INK, fc="#F6F4EF", lw=1.0))
    ax.text(0.115, 0.66, "平均人", ha="center", fontsize=9.2, color=fs.INK)
    ax.text(0.115, 0.57, "$\\bar{\\mathbf{T}}$", ha="center", fontsize=11.5, color=fs.INK)
    ax.text(0.115, 0.36, "20670 个数", ha="center", fontsize=7.6, color=fs.MUTED)
    ax.text(0.115, 0.24, "固定不动", ha="center", fontsize=7.2, color=fs.FAINT)

    rows = [("$\\beta_1$", "高矮 / 胖瘦", 0.66, fs.ACCENT, 0.40),
            ("$\\beta_2$", "肩宽", 0.44, fs.BLUE, 0.335),
            ("$\\beta_3$", "腿身比", 0.22, fs.GREEN, 0.455)]
    for sym, name, y, c, pos in rows:
        ax.text(0.245, y, sym, fontsize=10.2, color=c, ha="left", va="center")
        ax.text(0.295, y, name, fontsize=8.0, color=fs.MUTED, ha="left", va="center")
        ax.plot([0.245, 0.505], [y - 0.075, y - 0.075], color="#D1D5DB", lw=3.0,
                solid_capstyle="round", zorder=1)
        ax.plot([0.245, pos], [y - 0.075, y - 0.075], color=c, lw=3.0,
                solid_capstyle="round", zorder=2)
        ax.plot([pos], [y - 0.075], marker="o", ms=7.0, color="white", mec=c,
                mew=1.8, zorder=3)

    ax.text(0.555, 0.44, "=", fontsize=17, color=fs.INK, ha="center", va="center")

    ax.add_patch(FancyBboxPatch((0.605, 0.14), 0.22, 0.60,
                                boxstyle="round,pad=0.008,rounding_size=0.02",
                                ec=fs.ACCENT, fc="#FDF6EE", lw=1.2))
    ax.text(0.715, 0.66, "具体的人", ha="center", fontsize=9.2, color=fs.ACCENT)
    ax.text(0.715, 0.53, "$\\bar{\\mathbf{T}}+\\sum_n \\beta_n \\mathbf{S}_n$",
            ha="center", fontsize=9.8, color=fs.INK)
    ax.text(0.715, 0.36, "体型由 10 个数决定", ha="center", fontsize=7.6, color=fs.MUTED)
    ax.text(0.715, 0.24, "再给 72 个姿态数\n就摆出任意姿势", ha="center",
            fontsize=7.2, color=fs.FAINT, va="center")

    ax.text(0.852, 0.66, "方向的分工", ha="left", fontsize=7.8, color=fs.MUTED)
    for i, (t, c) in enumerate([("前 10 个：体型", fs.ACCENT),
                                ("其余：细节与噪声", fs.FAINT)]):
        ax.text(0.852, 0.575 - i * 0.085, t, ha="left", fontsize=7.0, color=c)

    ax.text(0.03, 0.95, "一个平均形状，加上少数几个方向上的刻度",
            fontsize=9.4, color=fs.INK, va="top")
    ax.text(0.03, 0.865, "刻度就是参数，也就是界面上能拖动的那几根滑块",
            fontsize=8.2, color=fs.MUTED, va="top")

    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch02", "fig02-03")


# ---------------- 图 2-4 累计解释了多少差异（示意） ----------------
def fig_variance():
    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    k = np.arange(1, 26)
    # 只画形状：前几个方向贡献大，之后迅速变缓
    curve = 0.34 * (1 - np.exp(-(k - 0.6) / 1.5)) + 0.56 * (1 - np.exp(-(k - 0.6) / 9.0))
    curve = curve / curve[-1] * 0.97
    ax.plot(k, curve, color=fs.ACCENT, lw=1.8, zorder=3)
    ax.fill_between(k, 0, curve, color=fs.ACCENT, alpha=0.08, zorder=2)

    ax.axvline(10, color=fs.BLUE, lw=1.0, ls="--", zorder=4)
    ax.scatter([10], [curve[9]], s=36, color=fs.BLUE, zorder=5)
    ax.annotate("前 10 个方向\n覆盖了大部分差异",
                xy=(10, curve[9]), xytext=(12.2, curve[9] - 0.16),
                fontsize=8.4, color=fs.BLUE,
                arrowprops=dict(arrowstyle="-", color=fs.BLUE, lw=0.9))
    ax.annotate("后面的方向：一点点细节，加上噪声",
                xy=(20, curve[19]), xytext=(12.0, 0.30),
                fontsize=8.2, color=fs.MUTED,
                arrowprops=dict(arrowstyle="-", color=fs.FAINT, lw=0.9))

    ax.set_xlabel("保留的主成分个数（按方差从大到小排队）", fontsize=8.8)
    ax.set_ylabel("累计解释了多大比例的差异", fontsize=8.8, labelpad=6)
    ax.set_xticks([1, 5, 10, 15, 20, 25])
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_yticklabels(["0", "一半", "全部"])
    ax.set_xlim(1, 25)
    ax.set_ylim(0, 1.05)
    ax.tick_params(labelsize=8)
    ax.set_title("口径：曲线形状是示意，具体比例随数据集变", fontsize=8.4,
                 color=fs.MUTED, pad=6, loc="left")

    fig.tight_layout(pad=0.5)
    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch02", "fig02-04")


if __name__ == "__main__":
    fig_correspondence()
    fig_space()
    fig_sliders()
    fig_variance()
