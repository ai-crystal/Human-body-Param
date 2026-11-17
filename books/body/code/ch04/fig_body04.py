# -*- coding: utf-8 -*-
"""第 4 章（人体册）插图：SMPL 是怎么训练出来的

fig04-01  训练数据与数据矩阵（N x 20670），以及 SVD 取前 10 行
fig04-02  只靠 LBS 的收缩：用真实的 LBS 加权矩阵算出来
fig04-03  9K 个姿态特征从哪来：为什么是 9 个元素而不是 3 个角
fig04-04  训练流程与交替优化
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs
fs.FIGDIR = os.path.join(HERE, "img")

from matplotlib.patches import Rectangle, Arc, Polygon

R_TUBE = 0.052


# ---------------- 小工具 ----------------
def hat(w):
    w = np.asarray(w, float)
    return np.array([[0.0, -w[2], w[1]],
                     [w[2], 0.0, -w[0]],
                     [-w[1], w[0], 0.0]])


def exp_so3(w):
    w = np.asarray(w, float)
    th = np.linalg.norm(w)
    if th < 1e-14:
        return np.eye(3) + hat(w)
    A = hat(w / th)
    return np.eye(3) + np.sin(th) * A + (1 - np.cos(th)) * (A @ A)


def rot_z(deg):
    t = np.deg2rad(deg)
    return np.array([[np.cos(t), -np.sin(t), 0.0],
                     [np.sin(t), np.cos(t), 0.0],
                     [0.0, 0.0, 1.0]])


def design9(R):
    """把一个 3x3 旋转矩阵减去单位阵，展开成 9 个数。"""
    return (R - np.eye(3)).reshape(9)


# ---------------- 图 4-1 ----------------
def fig01():
    fig, ax = fs.canvas(7.4, 3.6)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.075, 1.0)

    # 左上：一摞已配准扫描
    fs.label(ax, 0.113, 0.962, "N 个已配准扫描", fs=10.2, weight="bold")
    fs.label(ax, 0.113, 0.912, "同一拓扑、同一基准姿势", fs=8.3, color=fs.MUTED)

    for dx, dy, al in [(0.022, -0.018, 0.30), (0.011, -0.009, 0.55), (0.0, 0.0, 1.0)]:
        ax.add_patch(Rectangle((0.038 + dx, 0.660 + dy), 0.150, 0.180,
                               facecolor="#EEF3FF", edgecolor=fs.BLUE,
                               lw=0.7, alpha=al, zorder=2))
    for i in range(7):
        for j in range(9):
            ax.plot(0.050 + i * 0.020, 0.672 + j * 0.0185, "o", ms=1.5,
                    color=fs.BLUE, alpha=0.7, zorder=8)
    fs.label(ax, 0.113, 0.605, "6890 个顶点", fs=8.4, color=fs.MUTED)
    fs.label(ax, 0.113, 0.560, "20670 个数", fs=8.4, color=fs.MUTED)

    fs.arrow(ax, (0.205, 0.750), (0.288, 0.750), color=fs.FAINT, lw=1.1)
    fs.label(ax, 0.247, 0.788, "展开", fs=8.0, color=fs.MUTED)

    # 数据矩阵
    mx0, mx1, my0, my1 = 0.295, 0.500, 0.455, 0.815
    ax.add_patch(Rectangle((mx0, my0), mx1 - mx0, my1 - my0,
                           facecolor="#FCFCFD", edgecolor=fs.INK, lw=1.0, zorder=3))
    for i in range(1, 9):
        yy = my0 + (my1 - my0) * i / 9.0
        ax.plot([mx0, mx1], [yy, yy], color=fs.FAINT, lw=0.35, zorder=4)
    fs.label(ax, (mx0 + mx1) / 2, (my0 + my1) / 2 + 0.012, r"$\tilde{\mathbf{X}}$", fs=16)
    fs.label(ax, (mx0 + mx1) / 2, (my0 + my1) / 2 - 0.062, "已中心化", fs=8.0, color=fs.MUTED)
    fs.label(ax, mx0 - 0.028, (my0 + my1) / 2, "N 行", fs=8.3, color=fs.MUTED, rotation=90)
    fs.label(ax, (mx0 + mx1) / 2, my0 - 0.038, "20670 列", fs=8.3, color=fs.MUTED)

    fs.arrow(ax, (0.512, 0.750), (0.545, 0.750), color=fs.FAINT, lw=1.1)
    fs.label(ax, 0.528, 0.788, "SVD", fs=8.0, color=fs.MUTED)

    # SVD 三块
    ux0, ux1 = 0.556, 0.592
    sx0, sx1 = 0.606, 0.638
    vx0, vx1 = 0.652, 0.905
    ax.add_patch(Rectangle((ux0, my0), ux1 - ux0, my1 - my0,
                           facecolor="#E8EEFF", edgecolor=fs.BLUE, lw=0.9, zorder=3))
    for i in range(1, 7):
        yy = my0 + (my1 - my0) * i / 7.0
        ax.plot([ux0, ux1], [yy, yy], color=fs.BLUE, lw=0.35, alpha=0.7, zorder=4)
    fs.label(ax, (ux0 + ux1) / 2, my0 - 0.038, r"$\mathbf{U}$", fs=9.5)
    fs.label(ax, (ux0 + ux1) / 2, my1 + 0.030, "N", fs=8.3, color=fs.MUTED)

    ax.add_patch(Rectangle((sx0, my0), sx1 - sx0, my1 - my0,
                           facecolor="white", edgecolor=fs.INK, lw=0.9, zorder=3))
    ax.plot([sx0, sx1], [my1, my0], color=fs.FAINT, lw=0.6, zorder=4)
    fs.label(ax, (sx0 + sx1) / 2, my0 - 0.038, r"$\mathbf{\Sigma}$", fs=9.5)

    ax.add_patch(Rectangle((vx0, my0), vx1 - vx0, my1 - my0,
                           facecolor="#FDF8EE", edgecolor=fs.GOLD, lw=0.9, zorder=3))
    for i in range(1, 12):
        yy = my0 + (my1 - my0) * i / 12.0
        ax.plot([vx0, vx1], [yy, yy], color=fs.GOLD, lw=0.35, alpha=0.6, zorder=4)
    hb = (my1 - my0) * 4.0 / 12.0
    ax.add_patch(Rectangle((vx0, my1 - hb), vx1 - vx0, hb,
                           facecolor=fs.ACCENT, alpha=0.22, lw=0.0, zorder=5))
    fs.label(ax, (vx0 + vx1) / 2, my0 - 0.038, r"$\mathbf{V}^{\top}$", fs=9.5)
    fs.label(ax, vx1 + 0.006, my1 - hb / 2, "前", fs=8.0, color=fs.ACCENT, ha="left")
    fs.label(ax, vx1 + 0.006, my1 - hb / 2 - 0.045, "10", fs=8.0, color=fs.ACCENT, ha="left")
    fs.label(ax, vx1 + 0.006, my1 - hb / 2 - 0.090, "行", fs=8.0, color=fs.ACCENT, ha="left")
    fs.label(ax, (vx0 + vx1) / 2, my1 + 0.030, "20670 列", fs=8.3, color=fs.MUTED)

    # 下方左：维度算式
    ax.add_patch(Rectangle((0.272, 0.230), 0.252, 0.115,
                           facecolor="white", edgecolor=fs.BLUE, lw=1.0, zorder=3))
    fs.label(ax, 0.3975, 0.305, r"$6890\times 3 = 20670$", fs=10.0, color=fs.BLUE)
    fs.label(ax, 0.3975, 0.262, "一张网格摊平成一列", fs=8.0, color=fs.MUTED)
    fs.arrow(ax, (0.3975, 0.443), (0.3975, 0.352), color=fs.FAINT, lw=1.0)

    # 下方右：前 10 行折回位移场
    n_bar = 10
    bx0, bw, bg = 0.610, 0.020, 0.009
    for i in range(n_bar):
        ax.add_patch(Rectangle((bx0 + i * (bw + bg), 0.150), bw, 0.145,
                               facecolor=fs.ACCENT, alpha=0.16,
                               edgecolor=fs.ACCENT, lw=0.8, zorder=3))
    fs.label(ax, 0.610 + (n_bar * bw + (n_bar - 1) * bg) / 2, 0.320,
             r"$\mathbf{S}_1\ \ \mathbf{S}_2\ \ \cdots\ \ \mathbf{S}_{10}$", fs=9.5)
    fs.label(ax, 0.610 + (n_bar * bw + (n_bar - 1) * bg) / 2, 0.108,
             "每个都是一张 6890×3 的位移场", fs=8.0, color=fs.MUTED)

    fs.arrow(ax, (0.862, 0.443), (0.862, 0.345), color=fs.FAINT, lw=1.0)

    return fs.save(fig, "04", "fig04-01")


# ---------------- 图 4-2 ----------------
def fig02():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.4),
                             gridspec_kw=dict(width_ratios=[1.0, 1.18], wspace=0.30))
    ax0, ax1 = axes

    # ---- (a) 关节环截面：用真实 LBS 加权和算，不是手写一个椭圆 ----
    ph = np.linspace(0.0, 2.0 * np.pi, 400)
    ax0.plot(R_TUBE * np.cos(ph), R_TUBE * np.sin(ph), color=fs.FAINT, lw=1.0,
             ls=(0, (4, 3)), zorder=2)

    # 两根骨：上臂 G=I，前臂 G=Rz(90)，关节环处权重各一半
    P0 = np.stack([np.zeros_like(ph), R_TUBE * np.cos(ph), R_TUBE * np.sin(ph)], axis=1)
    Qi = np.zeros_like(P0)
    for wk, Gk in zip([0.5, 0.5], [np.eye(3), rot_z(90.0)]):
        Qi = Qi + wk * (P0 @ Gk.T)
    # 投影到弯曲平面（取径向，符号跟随 p 在弯曲平面内的朝向）与弯曲轴方向
    rho = np.sign(P0[:, 1]) * np.linalg.norm(Qi[:, :2], axis=1)
    k90 = np.cos(np.deg2rad(90.0) / 2.0)
    print("[fig04-02] 弯曲平面内最大半径 / r = %.6f" % (np.max(np.abs(rho)) / R_TUBE))
    ax0.plot(rho, Qi[:, 2], color=fs.ACCENT, lw=1.9, zorder=4)
    ax0.plot([-R_TUBE * k90, R_TUBE * k90], [0, 0], "o", ms=3.6, color=fs.ACCENT, zorder=6)

    ax0.annotate("", xy=(-R_TUBE * 1.40, 0.0), xytext=(R_TUBE * 1.40, 0.0),
                 arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.8), zorder=3)
    ax0.annotate("", xy=(0.0, R_TUBE * 1.40), xytext=(0.0, -R_TUBE * 1.40),
                 arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.8), zorder=3)
    fs.label(ax0, R_TUBE * 1.47, 0.0, "内 / 外", fs=8.2, color=fs.MUTED, ha="left")
    fs.label(ax0, 0.0, R_TUBE * 1.47, "沿弯曲轴", fs=8.2, color=fs.MUTED, ha="center", va="bottom")

    fs.label(ax0, -R_TUBE * k90 - 0.012, -0.024, r"$0.707\,r$", fs=8.4, color=fs.ACCENT, ha="right")
    fs.label(ax0, 0.0, R_TUBE * 1.04, r"$r$", fs=8.8, color=fs.INK, ha="center", va="bottom")
    fs.label(ax0, 0.0, -R_TUBE * 1.95, r"虚线圆：未弯曲　实线：弯曲 $90^\circ$",
             fs=8.0, color=fs.MUTED, ha="center")

    ax0.set_xlim(-R_TUBE * 2.35, R_TUBE * 2.35)
    ax0.set_ylim(-R_TUBE * 2.30, R_TUBE * 2.05)
    ax0.set_aspect("equal")
    ax0.axis("off")

    # ---- (b) 半径随弯曲角 ----
    ths = np.arange(0.0, 121.0, 2.0)
    r_lbs = np.cos(np.deg2rad(ths) / 2.0)

    th_fit = np.array([5.0, 12.0, 20.0, 30.0, 42.0, 55.0, 70.0, 88.0, 105.0, 120.0])
    feat = np.array([design9(rot_z(t)) for t in th_fit])
    A = np.hstack([np.ones((len(feat), 1)), feat])
    p0 = np.array([0.0, R_TUBE, 0.0])
    d_tr = np.array([p0 - 0.5 * (p0 + rot_z(t) @ p0) for t in th_fit])
    coef, *_ = np.linalg.lstsq(A, d_tr, rcond=None)
    r_corr = []
    for t in ths:
        phi = np.concatenate([[1.0], design9(rot_z(t))])
        q = 0.5 * (p0 + rot_z(t) @ p0) + phi @ coef
        r_corr.append(np.linalg.norm(q) / R_TUBE)
    r_corr = np.array(r_corr)
    res = np.max(np.abs(A @ coef - d_tr)) / R_TUBE
    print("[fig04-02] 9 元素修正的最大残差（相对 r）：%.3e" % res)

    ax1.fill_between(ths, r_lbs, 1.0, color=fs.ACCENT, alpha=0.10, lw=0)
    ax1.plot(ths, r_lbs, color=fs.BLUE, lw=1.9, label="只做 LBS（关节环，弯曲平面内）")
    ax1.plot(ths, r_corr, color=fs.ACCENT, lw=1.7, ls=(0, (6, 3)),
             label="加姿态修正项之后")

    ax1.plot([90, 90], [0.60, np.cos(np.pi / 4)], color=fs.FAINT, lw=0.8, ls=":")
    ax1.plot([0, 90], [np.cos(np.pi / 4)] * 2, color=fs.FAINT, lw=0.8, ls=":")
    ax1.plot([90], [np.cos(np.pi / 4)], "o", ms=4, color=fs.BLUE, zorder=6)
    fs.label(ax1, 56, 0.862, "修正项要补的缺口", fs=8.8, color=fs.ACCENT)

    fs.clean(ax1, grid=True, spines=("left", "bottom"))
    ax1.set_xlim(0, 120)
    ax1.set_ylim(0.60, 1.06)
    ax1.set_xticks([0, 30, 60, 90, 120])
    ax1.set_xlabel("关节弯曲角（度）")
    ax1.set_ylabel("关节环半径 / 未弯曲半径")
    ax1.legend(loc="lower left", bbox_to_anchor=(0.010, 0.020), handlelength=2.6)

    return fs.save(fig, "04", "fig04-02")


# ---------------- 图 4-3 ----------------
def fig03():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.4),
                             gridspec_kw=dict(width_ratios=[1.0, 1.34], wspace=0.26))
    ax0, ax1 = axes

    # ---- (a) 9 个元素 ----
    ax0.set_xlim(0, 1)
    ax0.set_ylim(0, 1)
    ax0.axis("off")

    wv = np.array([0.35, 0.55, 0.30])
    R = exp_so3(wv)
    M = R - np.eye(3)
    S = 0.5 * (M + M.T)
    A = 0.5 * (M - M.T)

    cw, ch = 0.162, 0.130
    x0, y0 = 0.070, 0.615
    for i in range(3):
        for j in range(3):
            sym = abs(S[i, j]) >= abs(A[i, j])
            fc = "#EAEFFE" if sym else "#FCF1E2"
            ax0.add_patch(Rectangle((x0 + j * cw, y0 - (i + 1) * ch), cw, ch,
                                    facecolor=fc, edgecolor=fs.FAINT, lw=0.7, zorder=3))
            fs.label(ax0, x0 + (j + 0.5) * cw, y0 - (i + 0.5) * ch,
                     "%.3f" % M[i, j], fs=7.6, color=fs.INK)

    fs.label(ax0, x0 + 1.5 * cw, y0 + 0.040, r"$\mathbf{R}-\mathbf{I}$ 的 9 个元素", fs=9.0)
    fs.label(ax0, x0 + 1.5 * cw, y0 - 3 * ch - 0.070,
             r"对称：$1-\cos\theta$（二阶）", fs=8.2, color=fs.BLUE)
    fs.label(ax0, x0 + 1.5 * cw, y0 - 3 * ch - 0.128,
             r"反对称：$\sin\theta$（一阶）", fs=8.2, color=fs.GOLD)
    fs.label(ax0, x0 + 1.5 * cw, y0 - 3 * ch - 0.210,
             r"$9\times 23 = 207$", fs=11.5, color=fs.ACCENT, weight="bold")

    # ---- (b) 位移是 sin/cos 的组合，不是角度的线性函数 ----
    deg = np.linspace(0.0, 180.0, 300)
    t = np.deg2rad(deg)
    ax1.plot(deg, np.sin(t), color=fs.BLUE, lw=1.9, label=r"$\sin\theta$（矩阵元素）")
    ax1.plot(deg, 0.5 * (1 - np.cos(t)), color=fs.GOLD, lw=1.9,
             label=r"$(1-\cos\theta)/2$（矩阵元素）")
    ax1.plot(deg, deg / 180.0, color=fs.ACCENT, lw=1.8, ls=(0, (6, 3)),
             label=r"$\theta/180^\circ$（轴角本身）")

    ax1.plot([90, 90], [0.0, 1.0], color=fs.FAINT, lw=0.7, ls=":")
    fs.label(ax1, 92, 1.045, r"$90^\circ$", fs=8.2, color=fs.MUTED, ha="left")


    ax1.text(0.415, 0.030,
             "3 个轴角线性拟合位移的残差\n90° 时 18%，180° 时 33%\n9 个元素线性拟合：机器精度",
             transform=ax1.transAxes, fontsize=8.0, color=fs.INK, va="bottom",
             bbox=dict(boxstyle="round,pad=0.42", facecolor="white",
                       edgecolor=fs.FAINT, lw=0.7))

    fs.clean(ax1, grid=True, spines=("left", "bottom"))
    ax1.set_xlim(0, 180)
    ax1.set_ylim(0, 1.45)
    ax1.set_xticks([0, 45, 90, 135, 180])
    ax1.set_xlabel("关节旋转角（度）")
    ax1.set_ylabel("归一化后的取值")
    ax1.legend(loc="upper center", bbox_to_anchor=(0.52, 1.005), handlelength=2.4, ncol=1)

    return fs.save(fig, "04", "fig04-03")


# ---------------- 图 4-4 ----------------
def fig04():
    fig, ax = fs.canvas(7.6, 4.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = [0.030, 0.265, 0.500, 0.735]
    wb, hb = 0.205, 0.215
    y1, y2 = 0.630, 0.215

    rows = [
        (y1, [
            ("① 已配准扫描\nN × 6890 × 3\n同一拓扑与姿势", fs.BLUE),
            ("② 中心化 + SVD\n取前 10 个右奇异向量\n得到 10 个形状基", fs.BLUE),
            ("③ 关节回归 J\n蒙皮权重 W\n稀疏、非负、和为 1", fs.GREEN),
            ("④ 姿态与位移对\n（θ, d）\n扫描减去模板", fs.GREEN),
        ]),
        (y2, [
            ("不达标就回头\n改配准、改权重", fs.ACCENT),
            ("⑦ 评估\n留出集重建误差\n外插、自交检查", fs.ACCENT),
            ("⑥ 模型 M(β, θ)\n6890 个顶点\n可微、可批量", fs.PURPLE),
            ("⑤ 解 207 个 P 系数\n正规方程 + 正则项", fs.PURPLE),
        ]),
    ]

    for y, items in rows:
        for i, (txt, col) in enumerate(items):
            fs.box(ax, xs[i], y, wb, hb, txt, fc="white", ec=col, fs=8.6, lw=1.2)

    yc1 = y1 + hb / 2
    yc2 = y2 + hb / 2
    for i in range(3):
        fs.arrow(ax, (xs[i] + wb + 0.004, yc1), (xs[i + 1] - 0.004, yc1),
                 color=fs.FAINT, lw=1.1)
        fs.arrow(ax, (xs[i + 1] - 0.004, yc2), (xs[i] + wb + 0.004, yc2),
                 color=fs.FAINT, lw=1.1)
    fs.arrow(ax, (xs[3] + wb / 2, y1 - 0.004), (xs[3] + wb / 2, y2 + hb + 0.004),
             color=fs.FAINT, lw=1.1)
    fs.arrow(ax, (xs[0] + wb / 2, y2 + hb + 0.004), (xs[0] + wb / 2, y1 - 0.004),
             color=fs.ACCENT, lw=1.0, ls=(0, (4, 3)))

    fs.label(ax, 0.5, 0.958, "四个量交替求解，每一轮只动一个", fs=10.6, weight="bold")
    fs.label(ax, 0.5, 0.908,
             "固定形状解姿态修正，固定姿态修正解权重，再回头修正形状",
             fs=8.6, color=fs.MUTED)
    fs.label(ax, 0.5, 0.112,
             "两到三轮之后残差不再下降，此时才把权重与回归器一起放开",
             fs=8.2, color=fs.MUTED)

    return fs.save(fig, "04", "fig04-04")


if __name__ == "__main__":
    fig01()
    fig02()
    fig03()
    fig04()
