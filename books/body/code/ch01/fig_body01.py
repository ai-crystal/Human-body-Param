# -*- coding: utf-8 -*-
"""第 1 章（人体册）插图：SCAPE 的形状/姿态分解

fig01-04  同一个弯 90° 的二维条带：顶点级 LBS 会把接头捏细，三角形级变形不会
fig01-05  式 (1.2) 的稀疏矩阵长什么样：一个小网格的 A 与每行的非零
fig01-06  SCAPE 的「学」与「用」两条流水线，以及它贵在哪里

所有数值都是本脚本现场算出来的示意值（几何单位，不是毫米），
不冒充论文数据。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(os.path.dirname(HERE))          # books/body
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PolyCollection
import figstyle as fs

fs.FIGDIR = os.path.join(BOOK, "images")

W_ROW = 0.22          # 条带半宽
NX = 24               # 沿骨轴的顶点列数
H_BLEND = 0.5         # 权重过渡带半宽
THETA = np.deg2rad(90.0)


def rot(a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])


def build_strip(nx=NX):
    xs = np.linspace(-1.0, 1.0, nx + 1)
    V = np.array([[x, y] for y in (-W_ROW, W_ROW) for x in xs])
    tris = []
    for r in range(1):
        for c in range(nx):
            a = r * len(xs) + c
            b, cc, d = a + 1, a + len(xs), a + len(xs) + 1
            tris += [(a, b, d), (a, d, cc)]
    return xs, V, np.array(tris)


def w_bone1(x):
    return np.clip(0.5 + x / (2 * H_BLEND), 0.0, 1.0)


def lbs_positions(V):
    out = []
    for x, y in V:
        w = w_bone1(x)
        p = np.array([x, y])
        out.append((1 - w) * p + w * (rot(THETA) @ p))
    return np.array(out)


def triangle_positions(V, tris, ang):
    """每个三角形按自己那圈的旋转 R_t 变换所有边，再全局最小二乘解顶点。"""
    rows, rhs = [], []
    for t in tris:
        a = float(np.mean(ang[t]))
        Rt = rot(a)
        for i, j in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            e = np.zeros((2, 2 * len(V)))
            e[0, 2 * i], e[0, 2 * j] = 1.0, -1.0
            e[1, 2 * i + 1], e[1, 2 * j + 1] = 1.0, -1.0
            rows.append(e)
            rhs.append(Rt @ (V[i] - V[j]))
    A, b = np.vstack(rows), np.concatenate(rhs)
    # 两根骨的根端各钉一个点，否则整体位置不定
    for i in (0, len(V) // 2):
        e = np.zeros((2, 2 * len(V)))
        e[0, 2 * i] = e[1, 2 * i + 1] = 60.0
        A = np.vstack([A, e])
        b = np.concatenate([b, 60.0 * V[i]])
    sol = np.linalg.lstsq(A, b, rcond=None)[0]
    return sol.reshape(-1, 2)


def draw_mesh(ax, V, tris, color, alpha=0.85, ec="white"):
    polys = [V[t] for t in tris]
    ax.add_collection(PolyCollection(polys, facecolors=color, edgecolors=ec,
                                     linewidths=0.45, alpha=alpha, zorder=3))
    ax.scatter(V[:, 0], V[:, 1], s=5, color="white", edgecolor=fs.INK,
               linewidths=0.5, zorder=4)


def joint_width(V, xs):
    i0 = len(xs) // 2
    return float(np.linalg.norm(V[i0] - V[len(xs) + i0]))


# ------------------------------------------------------------------ 图 1-4
def fig_lbs_vs_triangle():
    xs, V, tris = build_strip()
    V_lbs = lbs_positions(V)
    ang = np.array([w_bone1(x) * THETA for x, _ in V])
    V_tri = triangle_positions(V, tris, ang)

    w0 = joint_width(V, xs)
    w1_ = joint_width(V_lbs, xs)
    w2_ = joint_width(V_tri, xs)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    for ax, (Vp, title, col, wtxt) in zip(axes, [
        (V_lbs, "① 顶点级：两根骨的变换加权平均", fs.ACCENT, w1_),
        (V_tri, "② 三角形级：每个三角形有自己的 $\\mathbf{Q}_t$", fs.TEAL, w2_),
    ]):
        draw_mesh(ax, Vp, tris, col, alpha=0.30 if col == fs.ACCENT else 0.30)
        # 只用线框更能看清接头
        for t in tris:
            ax.add_patch(MplPolygon(Vp[t], closed=True, fill=False,
                                    edgecolor=col, lw=0.55, zorder=3))
        i0 = len(xs) // 2
        p_top, p_bot = Vp[len(xs) + i0], Vp[i0]
        ax.plot([p_top[0], p_bot[0]], [p_top[1], p_bot[1]], color=fs.INK,
                lw=1.1, ls=(0, (3, 2)), zorder=5)
        ax.annotate("", xy=p_top, xytext=p_bot,
                    arrowprops=dict(arrowstyle="<->", color=fs.INK, lw=0.9, shrinkA=0, shrinkB=0))
        mid = (p_top + p_bot) / 2
        ax.text(1.12, mid[1], f"宽度 {wtxt / w0 * 100:.0f}%", fontsize=9.0,
                color=col, weight="bold", va="center", ha="left", zorder=7,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9))
        ax.plot([0], [0], marker="o", ms=5, mfc="white", mec=fs.INK, mew=1.0, zorder=6)
        ax.set_title(title, fontsize=10.0, color=col, pad=4)
        ax.set_xlim(-1.15, 1.55)
        ax.set_ylim(-0.5, 1.22)
        ax.set_aspect("equal")
        ax.axis("off")

    fig.text(0.5, 0.012,
             "同一根二维条带弯 90°：接头处的宽度左图只剩 %.0f%%，右图 %.0f%%（示意几何，非毫米）"
             % (w1_ / w0 * 100, w2_ / w0 * 100),
             ha="center", fontsize=8.6, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-04")


# ------------------------------------------------------------------ 图 1-5
def fig_sparse_matrix():
    # 3x2 的小网格：6 个顶点、4 个三角形，只为了看清 A 的结构
    nx, ny = 3, 2
    pts = [(i, j) for j in range(ny) for i in range(nx)]
    V = np.array(pts, float)
    tris = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            b, c, d = a + 1, a + nx, a + nx + 1
            tris += [(a, b, d), (a, d, c)]
    tris = np.array(tris)

    edges = []
    for t in tris:
        for i, j in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            edges.append((i, j))
    A = np.zeros((len(edges) * 2, 2 * len(V)))
    for r, (i, j) in enumerate(edges):
        A[2 * r, 2 * i], A[2 * r, 2 * j] = 1.0, -1.0
        A[2 * r + 1, 2 * i + 1], A[2 * r + 1, 2 * j + 1] = 1.0, -1.0

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.4),
                             gridspec_kw={"width_ratios": [1.0, 1.35]})
    ax = axes[0]
    for t in tris:
        ax.add_patch(MplPolygon(V[t], closed=True, facecolor="#EEF2FF",
                                edgecolor=fs.BLUE, lw=0.9, alpha=0.9))
    for k, (x, y) in enumerate(V):
        ax.plot([x], [y], marker="o", ms=7, mfc="white", mec=fs.INK, mew=1.1, zorder=5)
        dy = 0.20 if y > 0.5 else -0.20
        ax.text(x, y + dy, f"$v_{{{k}}}$", ha="center", fontsize=9.5, color=fs.INK)
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.55, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("① 6 个顶点、4 个三角形、%d 条边" % len(edges), fontsize=9.6, pad=6)

    ax = axes[1]
    ax.imshow(np.abs(A), cmap="Blues", aspect="auto", interpolation="nearest",
              vmin=0, vmax=1.4)
    ax.set_xlabel("列 = 顶点坐标（$x_0,y_0,x_1,y_1,\\dots$）", fontsize=9)
    ax.set_ylabel("行 = 三角形的一条边（$x$、$y$ 各一行）", fontsize=9)
    ax.set_xticks(range(0, 2 * len(V), 2))
    ax.set_xticklabels([f"$v_{k}$" for k in range(len(V))], fontsize=8)
    ax.set_yticks(range(0, len(edges) * 2, 2))
    ax.set_yticklabels([f"$e_{k}$" for k in range(len(edges))], fontsize=6.5)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("② $\\mathbf{A}$ 的非零结构：行 %d，列 %d，每行恰好 2 个非零"
                 % (A.shape), fontsize=9.6, pad=6)
    for r in range(1, len(edges)):
        ax.axhline(2 * r - 0.5, color="white", lw=1.2)
    fig.text(0.5, 0.012, "一个顶点被好几条边共用，所以列方向会出现多个非零——这就是“必须全局折中”的来源",
             ha="center", fontsize=8.6, color=fs.MUTED)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fs.save(fig, "ch01", "fig01-05")


# ------------------------------------------------------------------ 图 1-6
def fig_pipelines():
    fig, ax = fs.canvas(7.2, 3.9)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    fs.label(ax, 0.26, 0.955, "学（离线，一次）", fs=10, color=fs.BLUE, weight="bold")
    fs.box(ax, 0.03, 0.78, 0.20, 0.11, "动作捕捉\n关节角序列", fc="#EEF2FF", ec=fs.BLUE, fs=8.2)
    fs.box(ax, 0.27, 0.78, 0.20, 0.11, "驱动骨架\n得到 模板-姿势配对", fc="white", ec=fs.BLUE, fs=8.0)
    fs.box(ax, 0.51, 0.78, 0.22, 0.11, "逐三角形算变形\n$\\mathbf{Q}_t(\\boldsymbol{\\theta})$", fc="#ECFEFF", ec=fs.TEAL, fs=8.0)
    fs.box(ax, 0.77, 0.78, 0.20, 0.11, "回归器\n角度 → 9 个数", fc="#ECFEFF", ec=fs.TEAL, fs=8.0)
    fs.arrow(ax, (0.23, 0.835), (0.27, 0.835), lw=1.0, color=fs.FAINT)
    fs.arrow(ax, (0.47, 0.835), (0.51, 0.835), lw=1.0, color=fs.FAINT)
    fs.arrow(ax, (0.73, 0.835), (0.77, 0.835), lw=1.0, color=fs.FAINT)

    fs.box(ax, 0.03, 0.60, 0.20, 0.11, "全身扫描\n（已配准）", fc="#F0FDF4", ec=fs.GREEN, fs=8.2)
    fs.box(ax, 0.27, 0.60, 0.20, 0.11, "摆到规范姿势\n再做 PCA", fc="white", ec=fs.GREEN, fs=8.0)
    fs.box(ax, 0.51, 0.60, 0.22, 0.11, "形状基\n$\\mathbf{D}(\\boldsymbol{\\beta})$", fc="#F0FDF4", ec=fs.GREEN, fs=8.4)
    fs.arrow(ax, (0.23, 0.655), (0.27, 0.655), lw=1.0, color=fs.FAINT)
    fs.arrow(ax, (0.47, 0.655), (0.51, 0.655), lw=1.0, color=fs.FAINT)

    fs.label(ax, 0.26, 0.50, "用（在线，每次生成）", fs=10, color=fs.ACCENT, weight="bold")
    fs.box(ax, 0.03, 0.33, 0.15, 0.11, "形状系数\n$\\boldsymbol{\\beta}$", fc="#F0FDF4", ec=fs.GREEN, fs=8.2)
    fs.box(ax, 0.03, 0.14, 0.15, 0.11, "关节角\n$\\boldsymbol{\\theta}$", fc="#EEF2FF", ec=fs.BLUE, fs=8.2)
    fs.box(ax, 0.22, 0.33, 0.17, 0.11, "顶点位移\n$\\mathbf{D}\\boldsymbol{\\beta}$", fc="white", ec=fs.GREEN, fs=8.0)
    fs.box(ax, 0.22, 0.14, 0.17, 0.11, "查表 / 插值\n得到每个 $\\mathbf{Q}_t$", fc="white", ec=fs.TEAL, fs=7.8)
    fs.box(ax, 0.45, 0.235, 0.19, 0.11, "解一次大线性系统\n$\\mathbf{A}^{\\top}\\mathbf{A}\\mathbf{V}=\\mathbf{A}^{\\top}\\mathbf{B}$", fc="#FEF2F2", ec=fs.ACCENT, fs=7.6)
    fs.box(ax, 0.69, 0.235, 0.13, 0.11, "网格\n$\\mathbf{V}$", fc="#F5F3FF", ec=fs.PURPLE, fs=8.6)
    fs.arrow(ax, (0.18, 0.385), (0.22, 0.385), lw=1.0, color=fs.FAINT)
    fs.arrow(ax, (0.18, 0.195), (0.22, 0.195), lw=1.0, color=fs.FAINT)
    fs.arrow(ax, (0.39, 0.385), (0.45, 0.31), lw=1.0, color=fs.FAINT)
    fs.arrow(ax, (0.39, 0.195), (0.45, 0.25), lw=1.0, color=fs.FAINT)
    fs.arrow(ax, (0.64, 0.29), (0.69, 0.29), lw=1.0, color=fs.FAINT)

    fs.box(ax, 0.85, 0.11, 0.145, 0.34,
           "贵在哪\n① 每次都要解\n② 稀疏系统\n③ 不可微\n④ 依赖动捕",
           fc="#FFF7ED", ec=fs.ACCENT, fs=7.2)
    fs.label(ax, 0.92, 0.045, "SMPL 把这一步\n换成两次矩阵乘", fs=7.4, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-06")


if __name__ == "__main__":
    fig_lbs_vs_triangle()
    fig_sparse_matrix()
    fig_pipelines()
