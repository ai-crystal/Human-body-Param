# -*- coding: utf-8 -*-
"""第 19 章插图：手部骨骼与 21 关键点、MANO 数据流、模型包含关系。"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import figstyle as fs

ASPECT = 6.5 / 4.6          # 画布宽高比，用于保证圆看起来是圆


def hand_geometry():
    """右手 21 个关键点的二维坐标（掌背视角，指尖朝上）。

    顺序沿用 MANO 约定：腕、食指、中指、小指、无名指、拇指，每指 4 点。
    """
    wrist = np.array([0.452, 0.150])
    fingers = {
        "index":  dict(base=(0.612, 0.452), ang=91.0,  L=0.300, w=(0.052, 0.045, 0.039)),
        "middle": dict(base=(0.528, 0.470), ang=89.0,  L=0.330, w=(0.055, 0.047, 0.040)),
        "ring":   dict(base=(0.446, 0.458), ang=87.0,  L=0.298, w=(0.051, 0.044, 0.038)),
        "pinky":  dict(base=(0.366, 0.424), ang=84.0,  L=0.240, w=(0.045, 0.039, 0.034)),
        "thumb":  dict(base=(0.378, 0.268), ang=138.0, L=0.238, w=(0.062, 0.052, 0.044)),
    }
    frac = (0.42, 0.29, 0.29)
    chains = {}
    for name, f in fingers.items():
        th = np.deg2rad(f["ang"])
        pts = [np.array(f["base"], float)]
        bend = -0.055 if name != "thumb" else -0.075
        for i, fr in enumerate(frac):
            dd = np.array([np.cos(th + bend * i), np.sin(th + bend * i)])
            pts.append(pts[-1] + dd * (f["L"] * fr))
        chains[name] = (np.array(pts), f["w"])
    return wrist, chains


def draw_hand(ax, numbers=True):
    wrist, chains = hand_geometry()
    skin, bone = "#F7F0E7", "#D8D0C4"

    # 手掌多边形：腕左 → 小指根 → 无名指根 → 中指根 → 食指根 → 掌右 → 回腕
    k = {n: chains[n][0][0] for n in chains}
    palm = [np.array([0.348, 0.168]),
            k["pinky"] + np.array([-0.012, 0.008]),
            k["ring"] + np.array([-0.004, 0.010]),
            k["middle"] + np.array([0.0, 0.010]),
            k["index"] + np.array([0.012, 0.006]),
            np.array([0.662, 0.196]),
            wrist + np.array([0.052, -0.012]),
            wrist + np.array([-0.048, -0.010])]
    ax.add_patch(Polygon(palm, closed=True, facecolor=skin, edgecolor=fs.FAINT, lw=0.9, zorder=1))

    # 拇指的掌部（大鱼际）：从腕侧连到拇指根
    ax.add_patch(Polygon([np.array([0.374, 0.212]), k["thumb"] + np.array([-0.012, 0.062]),
                          k["thumb"] + np.array([0.048, 0.020]), np.array([0.432, 0.206])],
                         closed=True, facecolor=skin, edgecolor=fs.FAINT, lw=0.9, zorder=1))

    for name, (pts, w) in chains.items():
        ww = list(w) + [w[-1] * 0.86]
        for i in range(len(pts) - 1):
            fs.limb(ax, pts[i], pts[i + 1], ww[i] * 2.05, ww[i + 1] * 2.05,
                    color=bone, z=2, ec=fs.FAINT)
    for name, (pts, w) in chains.items():
        ww = list(w) + [w[-1] * 0.86]
        for i in range(len(pts) - 1):
            fs.limb(ax, pts[i], pts[i + 1], ww[i] * 1.30, ww[i + 1] * 1.30,
                    color=skin, z=3, ec="none")

    # 关节（腕 + 每指 3 个）与指尖
    ax.add_patch(Circle(wrist, 0.014, facecolor=fs.ACCENT, edgecolor="white", lw=1.0, zorder=6))
    for name, (pts, w) in chains.items():
        for i in range(3):
            ax.add_patch(Circle(pts[i], 0.013, facecolor=fs.ACCENT, edgecolor="white",
                                lw=1.0, zorder=6))
        ax.add_patch(Circle(pts[3], 0.0115, facecolor=fs.BLUE, edgecolor="white", lw=1.0, zorder=6))

    if numbers:
        fs.label(ax, wrist[0] - 0.004, wrist[1] - 0.045, "0", fs=8.2, color=fs.MUTED)
        # 编号偏移方向：食指/中指朝右，小指/无名指朝左，拇指朝外
        side = {"index": +1, "middle": +1, "ring": -1, "pinky": -1, "thumb": -1}
        k = 1
        for name in ["index", "middle", "pinky", "ring", "thumb"]:
            pts, w = chains[name]
            s = side[name]
            for i in range(4):
                p = pts[i] if i < 3 else pts[3]
                if name == "thumb":
                    off = np.array([-0.028, -0.020]) if i >= 2 else np.array([-0.016, 0.030])
                else:
                    off = np.array([s * 0.036, -0.002 + 0.016 * (i % 2)])
                fs.label(ax, p[0] + off[0], p[1] + off[1], str(k), fs=8.2, color=fs.INK)
                k += 1

    return wrist, chains


def fig19_01():
    fig, ax = fs.canvas(4.9, 5.5, xlim=(0.01, 0.99), ylim=(0.00, 1.10))
    ax.set_aspect("equal", adjustable="box")
    draw_hand(ax)

    fs.label(ax, 0.02, 1.075, "21 个关键点的编号（MANO 约定）", fs=9.8, ha="left", weight="bold")
    fs.label(ax, 0.02, 1.028, "0 是腕点；其余每指 4 点：根部 → 第一关节 → 第二关节 → 指尖",
             fs=7.9, ha="left", color=fs.MUTED)

    # 右上角放一个紧凑图例（手部轮廓右侧留白处）
    from matplotlib.patches import Circle as _C
    ax.add_patch(_C((0.795, 0.905), 0.011, facecolor=fs.ACCENT, edgecolor="white", lw=1.0, zorder=8))
    fs.label(ax, 0.815, 0.905, "骨架关节", fs=7.9, ha="left")
    fs.label(ax, 0.815, 0.868, "腕 1 + 每指 3 = 16", fs=7.3, ha="left", color=fs.MUTED)
    ax.add_patch(_C((0.795, 0.800), 0.011, facecolor=fs.BLUE, edgecolor="white", lw=1.0, zorder=8))
    fs.label(ax, 0.815, 0.800, "指尖顶点", fs=7.9, ha="left")
    fs.label(ax, 0.815, 0.763, "不是关节，共 5 个", fs=7.3, ha="left", color=fs.MUTED)

    fs.label(ax, 0.02, 0.038,
             "1–4 食指　5–8 中指　9–12 小指　13–16 无名指　17–20 拇指",
             fs=7.6, ha="left", color=fs.MUTED)

    fs.save(fig, "ch19", "fig19-01")


def fig19_02():
    fig, ax = fs.canvas(6.6, 4.0, xlim=(0, 1), ylim=(0, 1))
    fs.label(ax, 0.5, 0.968, "MANO 的数据流：五组学到的量 → 一次前向 → 一只手的网格",
             fs=10.0, weight="bold")

    fs.label(ax, 0.037, 0.918, "训练阶段学到的五组量", fs=8.8, color=fs.MUTED,
             weight="bold", ha="left")
    left = [
        ("模板  $\\bar{\\mathbf{T}}$  778×3", fs.GOLD, 0.775),
        ("形状基  $\\mathbf{B}_S(\\boldsymbol{\\beta})$", fs.GREEN, 0.655),
        ("姿态基  $\\mathbf{B}_P(\\boldsymbol{\\theta})$", fs.GREEN, 0.535),
        ("蒙皮权重  $\\mathbf{W}$  778×16", fs.PURPLE, 0.415),
        ("关节回归  $\\mathbf{J}(\\boldsymbol{\\beta})$", fs.PURPLE, 0.295),
    ]
    for txt, c, y in left:
        fs.box(ax, 0.032, y, 0.272, 0.092, txt, ec=c, fs=8.4)

    fs.box(ax, 0.350, 0.648, 0.210, 0.082, "$T_P=\\bar{\\mathbf{T}}+\\mathbf{B}_S+\\mathbf{B}_P$",
           ec=fs.INK, fs=8.2)
    fs.box(ax, 0.350, 0.442, 0.210, 0.082, "LBS：$\\sum_k w_k G_k\\tilde{\\mathbf{t}}$",
           ec=fs.INK, fs=8.2)
    fs.box(ax, 0.332, 0.240, 0.246, 0.082, "网格：778 顶点 / 1538 面", ec=fs.ACCENT, fs=7.6)

    fs.arrow(ax, (0.306, 0.760), (0.396, 0.640), color=fs.FAINT)
    fs.arrow(ax, (0.306, 0.640), (0.400, 0.652), color=fs.FAINT)
    fs.arrow(ax, (0.306, 0.520), (0.360, 0.528), color=fs.FAINT)
    fs.arrow(ax, (0.455, 0.648), (0.455, 0.530), color=fs.INK)
    fs.arrow(ax, (0.306, 0.400), (0.360, 0.455), color=fs.FAINT)
    fs.arrow(ax, (0.455, 0.442), (0.455, 0.330), color=fs.INK)

    fs.label(ax, 0.737, 0.918, "推理时由用户提供", fs=8.8, color=fs.MUTED,
             weight="bold", ha="left")
    right = [("形状  $\\boldsymbol{\\beta}\\in\\mathbb{R}^{10}$", 0.775),
             ("姿态  $\\boldsymbol{\\theta}\\in\\mathbb{R}^{48}$", 0.650),
             ("或 6 维 PCA 系数", 0.545),
             ("全局旋转 + 平移", 0.420)]
    for txt, y in right:
        fs.box(ax, 0.737, y, 0.235, 0.082, txt, ec=fs.BLUE, fs=8.2)
    fs.arrow(ax, (0.737, 0.775), (0.565, 0.700), color=fs.FAINT)
    fs.arrow(ax, (0.737, 0.690), (0.568, 0.690), color=fs.FAINT)
    fs.arrow(ax, (0.737, 0.462), (0.568, 0.482), color=fs.FAINT)

    fs.box(ax, 0.270, 0.048, 0.430, 0.082,
           "16 个关节 + 5 个指尖顶点 = 21 个关键点", ec=fs.PINK, fs=8.4)
    fs.arrow(ax, (0.455, 0.240), (0.455, 0.136), color=fs.INK)

    fs.save(fig, "ch19", "fig19-02")


def fig19_03():
    fig = plt.figure(figsize=(6.6, 3.35))
    ax = fig.add_axes([0.0, 0.0, 0.63, 1.0])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.text(0.025, 0.935, "SMPL、MANO、SMPL+H、SMPL-X 的包含关系与参数预算",
             fontsize=9.6, weight="bold", color=fs.INK)

    W, H = 0.255, 0.215
    fs.box(ax, 0.040, 0.555, W, H,
           "SMPL\n6890 顶点 · 24 关节\n手是一片固定的板", ec=fs.BLUE, fs=7.6)
    fs.box(ax, 0.040, 0.245, W, H,
           "MANO\n778 顶点 · 16 关节\n只有手，没有身体", ec=fs.ACCENT, fs=7.6)
    fs.box(ax, 0.390, 0.555, W, H,
           "SMPL+H\nMANO 的手指部件\n插进 SMPL 身体", ec=fs.GREEN, fs=7.6)
    fs.box(ax, 0.390, 0.245, W, H,
           "SMPL-X\n10475 顶点 · 54 关节\n身体 + 手 + 脸", ec=fs.PURPLE, fs=7.6)
    fs.arrow(ax, (0.298, 0.663), (0.387, 0.663), color=fs.FAINT)
    fs.arrow(ax, (0.298, 0.353), (0.387, 0.353), color=fs.FAINT)
    fs.arrow(ax, (0.518, 0.552), (0.518, 0.463), color=fs.FAINT)
    fs.label(ax, 0.530, 0.508, "再并入脸（FLAME）", fs=7.4, color=fs.MUTED, ha="left")
    fs.label(ax, 0.045, 0.180, "SMPL 与 MANO 共享同一套 LBS 公式", fs=7.4, color=fs.MUTED, ha="left")
    fs.label(ax, 0.045, 0.135, "差异在：局部化正则、姿态 PCA、零姿态", fs=7.4, color=fs.MUTED, ha="left")

    ax2 = fig.add_axes([0.715, 0.215, 0.255, 0.555])
    labels = ["SMPL\n身体", "SMPL+H\n身体+双手", "SMPL-X\n全部", "SMPL-X\n单手"]
    vals = [82, 88, 119, 12]
    cols = [fs.BLUE, fs.GREEN, fs.PURPLE, fs.ACCENT]
    ypos = np.arange(len(vals))[::-1]
    ax2.barh(ypos, vals, color=cols, height=0.5)
    for v, y in zip(vals, ypos):
        ax2.text(v + 4, y, str(v), va="center", fontsize=7.8, color=fs.INK)
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(labels, fontsize=7.0)
    ax2.set_xlim(0, 155)
    ax2.set_ylim(-0.65, 3.65)
    ax2.set_xlabel("可用参数个数", fontsize=7.8)
    ax2.set_title("参数预算", fontsize=8.4, color=fs.INK, pad=4)
    fs.clean(ax2, grid=True, spines=("bottom",))
    ax2.tick_params(axis="y", length=0)
    ax2.tick_params(axis="x", labelsize=7.2)

    fs.save(fig, "ch19", "fig19-03")


if __name__ == "__main__":
    fig19_01()
    fig19_02()
    fig19_03()
