# -*- coding: utf-8 -*-
"""第 7 章插图：同一根“手臂”，三种权重（图 7-4）。

一条二维带状网格（上臂 0.05–0.55，前臂 0.55–0.95，肘在 0.55），
肘弯 90°，只改前臂权重沿长度的分布：
  (a) 硬切换 0/1        → 关节处裂开
  (b) 只在关节处 0.5     → 关节处被捏细
  (c) 平滑过渡            → 弯曲自然，但仍有体积损失
脚本把三种情况的带状面积变化打印出来，正文引用这里的输出。
"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import figstyle as fs

MATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fs.FIGDIR = os.path.join(MATH, "images")

ELBOW = np.array([0.55, 0.0])
HALF = 0.075
NX = 17


def blend(w):
    """权重 0 → 蓝，1 → 橙。"""
    c0 = np.array([29, 78, 216]) / 255
    c1 = np.array([194, 65, 12]) / 255
    c = (1 - w) * c0 + w * c1
    return tuple(c)


def weights_a(x):
    return 0.0 if x < ELBOW[0] else 1.0


def weights_b(x):
    if x < ELBOW[0] - 0.06:
        return 0.0
    if x > ELBOW[0] + 0.06:
        return 1.0
    return 0.5


def weights_c(x):
    return float(np.clip((x - 0.47) / 0.16, 0.0, 1.0))


def deform(p, w, ang=np.pi / 2):
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    moved = (p - ELBOW) @ R.T + ELBOW
    return (1 - w) * p + w * moved


def strip(wfun):
    xs = np.linspace(0.05, 0.95, NX)
    top = np.stack([xs, HALF * np.ones_like(xs)], axis=1)
    bot = np.stack([xs, -HALF * np.ones_like(xs)], axis=1)
    ws = np.array([wfun(x) for x in xs])
    T = np.array([deform(p, w) for p, w in zip(top, ws)])
    B = np.array([deform(p, w) for p, w in zip(bot, ws)])
    return T, B, ws


def area(T, B):
    P = np.vstack([T, B[::-1]])
    x, y = P[:, 0], P[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def draw(ax, T, B, ws):
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.34, 0.74)
    # 静止姿态的轮廓（虚线参考）
    ax.plot([0.05, 0.95, 0.95, 0.05, 0.05],
            [HALF, HALF, -HALF, -HALF, HALF],
            color="#D1D5DB", lw=0.9, ls=(0, (4, 3)), zorder=1)
    for i in range(len(T) - 1):
        quad = np.array([T[i], T[i + 1], B[i + 1], B[i]])
        w = 0.5 * (ws[i] + ws[i + 1])
        ax.add_patch(Polygon(quad, closed=True, facecolor=blend(w),
                             edgecolor="white", lw=0.7, zorder=2))
    ax.plot(T[:, 0], T[:, 1], color=fs.INK, lw=0.8, zorder=3)
    ax.plot(B[:, 0], B[:, 1], color=fs.INK, lw=0.8, zorder=3)
    ax.plot([ELBOW[0]], [ELBOW[1]], "o", ms=4.5, mfc="white", mec=fs.INK, mew=1.0, zorder=4)


def main():
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.35),
                            gridspec_kw=dict(wspace=0.05))
    cases = [
        (weights_a, "（a）硬切换 0 / 1", "关节处裂开：两侧顶点各走各的", "^"),
        (weights_b, "（b）关节处一律 0.5", "关节被捏细：两个位置平均到弦上", "v"),
        (weights_c, "（c）平滑过渡 0 → 1", "弯曲自然，但仍有轻微变细", "o"),
    ]
    a0 = None
    for ax, (fun, title, note, _) in zip(axs, cases):
        T, B, ws = strip(fun)
        draw(ax, T, B, ws)
        ax.set_title(title, fontsize=9.0, pad=4)
        fs.label(ax, 0.5, -0.22, note, fs=7.5, color=fs.MUTED)
        ar = area(T, B)
        if a0 is None:
            a0 = ar
        print(f"{title}: 面积 {ar:.4f}，相对静止 {100*(ar/a0-1):+.1f}%")

    fs.label(axs[1], 0.5, 0.685, "颜色 = 前臂权重（蓝 0 → 橙 1）；虚线 = 静止姿态",
             fs=7.6, color=fs.MUTED)

    fs.save(fig, "ch07", "fig07-03")


if __name__ == "__main__":
    main()
