# -*- coding: utf-8 -*-
"""第 4 章（数学与几何册）插图：旋转的李群视角与非线性优化

fig04-01 切空间与指数映射（SO(3) 画成半径 pi 的球）
fig04-02 三种参数化在奇异点附近的行为
fig04-03 高斯-牛顿 / 梯度下降 / LM 的迭代轨迹
fig04-04 位姿-路标问题的 H 矩阵块稀疏结构
"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\book\code")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, FancyArrowPatch
import figstyle as fs

fs.FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


# ---------------- 小工具（全部真算，不用手写数组） ----------------
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


def log_so3(R):
    c = np.clip((np.trace(R) - 1) / 2.0, -1.0, 1.0)
    th = np.arccos(c)
    if th < 1e-9:
        return np.zeros(3)
    if np.pi - th < 1e-5:                       # 接近 pi，用对称部分定轴
        B = (R + np.eye(3)) / 2.0
        v = np.sqrt(np.maximum(np.diag(B), 0.0))
        i = int(np.argmax(v))
        u = B[:, i] / max(v[i], 1e-12)
        return th * u / np.linalg.norm(u)
    return th / (2 * np.sin(th)) * np.array([R[2, 1] - R[1, 2],
                                             R[0, 2] - R[2, 0],
                                             R[1, 0] - R[0, 1]])


def Rz(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def Rx(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])


def Ry(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])


def euler_R(a, b, g):
    """R = Rz(a) Rx(b) Ry(g)，第二个角 b = +-90 度时万向锁。"""
    return Rz(a) @ Rx(b) @ Ry(g)


def euler_extract(R):
    """从矩阵反解 (a, b, g)。"""
    b = np.arcsin(np.clip(R[2, 1], -1.0, 1.0))
    a = np.arctan2(-R[0, 1], R[1, 1])
    g = np.arctan2(-R[2, 0], R[2, 2])
    return np.array([a, b, g])


def quat_from_axis(a, th):
    return np.r_[np.cos(th / 2.0), np.sin(th / 2.0) * a]


def quat_to_R(q):
    w, x, y, z = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                     [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                     [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]])


def third_sv(J):
    s = np.linalg.svd(J, compute_uv=False)
    return s[2] if len(s) >= 3 else 0.0


# ---------------- 图 4-1：切空间与指数映射 ----------------
def fig04_01():
    fig = plt.figure(figsize=(6.9, 3.05))
    axL = fig.add_axes([0.02, 0.10, 0.40, 0.78]); axL.axis("off")
    axR = fig.add_axes([0.53, 0.10, 0.40, 0.78]); axR.axis("off")
    axL.set_xlim(-1.35, 1.45); axL.set_ylim(-1.30, 1.30)
    axR.set_xlim(-1.45, 1.45); axR.set_ylim(-1.30, 1.30)
    axR.set_aspect("equal"); axL.set_aspect("equal")

    # 左：切空间 so(3) = R^3（平面示意）
    axL.add_patch(Polygon([(-1.18, -1.02), (1.22, -0.92), (1.28, 0.98), (-1.12, 0.92)],
                          closed=True, fc=fs.LIGHT, ec=fs.FAINT, lw=1.0, zorder=1))
    fs.label(axL, 0.06, 1.14, r"切空间 $\mathfrak{so}(3)\cong\mathbb{R}^3$", fs=9.6,
             color=fs.INK)
    fs.label(axL, 0.06, -1.16, "在平面里做加法：想走多远就走多远", fs=8.4, color=fs.MUTED)

    O = np.array([-0.55, -0.45]); W = np.array([0.35, 0.18]); W2 = np.array([0.86, 0.60])
    fs.arrow(axL, O, W, color=fs.INK, lw=1.3)
    fs.arrow(axL, W, W2, color=fs.ACCENT, lw=1.6)
    axL.scatter([O[0]], [O[1]], s=26, color=fs.INK, zorder=6)
    axL.scatter([W[0]], [W[1]], s=26, color=fs.BLUE, zorder=6)
    axL.scatter([W2[0]], [W2[1]], s=26, color=fs.ACCENT, zorder=6)
    fs.label(axL, O[0] - 0.13, O[1] - 0.16, r"$\mathbf{0}$（单位阵）", fs=8.2, color=fs.INK,
             ha="right")
    fs.label(axL, W[0] - 0.02, W[1] + 0.15, r"$\omega$", fs=9.6, color=fs.BLUE)
    fs.label(axL, W2[0] + 0.04, W2[1] + 0.13, r"$\omega+\Delta\omega$",
             fs=9.2, color=fs.ACCENT, ha="left")
    fs.label(axL, 0.44, -0.30, "增量", fs=8.4, color=fs.ACCENT, ha="left")
    fs.label(axL, 0.02, -0.62, r"直线段就是“匀速转”", fs=8.0, color=fs.MUTED)

    # 右：SO(3) 画成半径 pi 的球，边界对径点粘合
    axR.add_patch(Circle((0, 0), 1.0, fc="#FFFFFF", ec=fs.INK, lw=1.3, zorder=1))
    axR.add_patch(Ellipse((0, 0), 2.0, 0.62, fc="none", ec=fs.FAINT, lw=0.9,
                          ls=(0, (4, 3)), zorder=2))
    axR.add_patch(Ellipse((0, 0), 0.62, 2.0, fc="none", ec=fs.FAINT, lw=0.9,
                          ls=(0, (4, 3)), zorder=2))
    fs.label(axR, 0.0, 1.14, r"群 $SO(3)$：半径 $\pi$ 的球", fs=9.6, color=fs.INK)
    fs.label(axR, 0.0, -1.16, r"$\theta=\pi$ 的球面上，对径两点是同一个旋转", fs=8.2,
             color=fs.MUTED)

    th = np.radians(52.0)
    P = np.array([0.72 * np.cos(th), 0.72 * np.sin(th)])
    Phi = np.array([0.72 * np.cos(th), 0.72 * np.sin(th)])
    # 球内沿半径的测地线（在球模型里确实是直线）
    axR.plot([0, P[0]], [0, P[1]], color=fs.ACCENT, lw=1.6, zorder=4)
    axR.scatter([0], [0], s=26, color=fs.INK, zorder=6)
    axR.scatter([P[0]], [P[1]], s=26, color=fs.ACCENT, zorder=6)
    fs.label(axR, 0.09, 0.055, "单位阵", fs=8.2, color=fs.MUTED, ha="left", va="center")
    fs.label(axR, P[0] + 0.04, P[1] + 0.12, r"$\exp(\hat{\omega})$", fs=9.2,
             color=fs.ACCENT, ha="left")
    # 对径点
    Q = -P
    axR.plot([P[0], Q[0]], [P[1], Q[1]], color=fs.BLUE, lw=0.9, ls=(0, (2, 2)), zorder=3)
    axR.scatter([Q[0]], [Q[1]], s=22, color=fs.BLUE, zorder=6)
    fs.label(axR, Q[0] - 0.05, Q[1] - 0.13, r"$-\pi\mathbf{a}$", fs=8.4, color=fs.BLUE,
             ha="right", va="top")
    fs.label(axR, P[0] + 0.04, P[1] - 0.16, r"$\pi\mathbf{a}$", fs=8.4, color=fs.BLUE,
             ha="left", va="top")

    # 两个面板之间的 exp / log
    ar = FancyArrowPatch((0.435, 0.60), (0.515, 0.60), transform=fig.transFigure,
                         arrowstyle="-|>", mutation_scale=9, color=fs.ACCENT, lw=1.4)
    fig.add_artist(ar)
    ar2 = FancyArrowPatch((0.515, 0.42), (0.435, 0.42), transform=fig.transFigure,
                          arrowstyle="-|>", mutation_scale=9, color=fs.BLUE, lw=1.2,
                          linestyle=(0, (3, 2)))
    fig.add_artist(ar2)
    fig.text(0.475, 0.655, "exp", fontsize=9.0, color=fs.ACCENT, ha="center")
    fig.text(0.475, 0.335, "log", fontsize=9.0, color=fs.BLUE, ha="center")

    fs.save(fig, "ch04", "fig04-01")


# ---------------- 图 4-2：三种参数化的奇异行为 ----------------
def fig04_02():
    a_axis = np.array([0.3, -0.5, 0.8]); a_axis /= np.linalg.norm(a_axis)
    h = 1e-6
    al, gm = 0.2, 0.4

    degs = np.linspace(0.0, 180.0, 361)
    s_eu, s_rv, s_qt = [], [], []
    for d in degs:
        be = np.radians(d)
        # 欧拉角：参数 (al, be, gm) -> R，9x3 雅可比
        Je = np.zeros((9, 3))
        for i in range(3):
            e = np.zeros(3); e[i] = h
            Je[:, i] = (euler_R(al + e[0], be + e[1], gm + e[2])
                        - euler_R(al - e[0], be - e[1], gm - e[2])).ravel() / (2 * h)
        # 旋转向量：w = be * a
        w = a_axis * be
        Jr = np.zeros((9, 3))
        for i in range(3):
            e = np.zeros(3); e[i] = h
            Jr[:, i] = (exp_so3(w + e) - exp_so3(w - e)).ravel() / (2 * h)
        # 四元数：在单位四元数的切空间取三个正交方向
        q = quat_from_axis(a_axis, be)
        rng = np.random.default_rng(11)
        B = []
        for _ in range(3):
            v = rng.normal(size=4); v -= q * (q @ v); B.append(v / np.linalg.norm(v))
        B = np.linalg.qr(np.array(B).T)[0][:, :3]
        Jq = np.zeros((9, 3))
        for i in range(3):
            e = B[:, i] * h
            qp = q + e; qp = qp / np.linalg.norm(qp)
            qm = q - e; qm = qm / np.linalg.norm(qm)
            Jq[:, i] = (quat_to_R(qp) - quat_to_R(qm)).ravel() / (2 * h)
        s_eu.append(third_sv(Je)); s_rv.append(third_sv(Jr)); s_qt.append(third_sv(Jq))
    s_eu = np.maximum(np.array(s_eu), 1e-4)
    s_rv = np.array(s_rv); s_qt = np.array(s_qt)

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.85),
                             gridspec_kw={"width_ratios": [1.0, 1.05]})

    ax = axes[0]
    fs.clean(ax, grid=True)
    ax.semilogy(degs, s_eu, color=fs.ACCENT, lw=1.9, label="欧拉角")
    ax.semilogy(degs, s_rv, color=fs.BLUE, lw=1.9, label="旋转向量")
    ax.semilogy(degs, s_qt, color=fs.GREEN, lw=1.6, ls=(0, (5, 2)), label="四元数")
    ax.axvline(90, color=fs.FAINT, lw=0.9, ls=":")
    ax.set_xlim(0, 180); ax.set_ylim(5e-4, 6.0)
    ax.set_xlabel("转角（度）", fontsize=8.4)
    ax.set_ylabel(r"$\sigma_{\min}$（参数→旋转）", fontsize=8.4)
    ax.set_title("参数化的局部“敏感度底噪”", fontsize=9.4)
    ax.annotate("欧拉角在 90° 归零", xy=(90, 1.2e-3), xytext=(96, 6e-3),
                fontsize=8.0, color=fs.ACCENT,
                arrowprops=dict(arrowstyle="-", color=fs.ACCENT, lw=0.8))
    ax.legend(fontsize=8.0, loc="lower left", ncol=1, handlelength=1.8,
              bbox_to_anchor=(0.005, 0.02))
    ax.tick_params(labelsize=7.8)

    # 右：平滑扫过 beta=90°，反解出来的欧拉角会跳
    ax = axes[1]
    fs.clean(ax, grid=True)
    bdeg = np.linspace(60.0, 110.0, 201)
    rec = []
    for d in bdeg:
        al_t = 0.2 + 0.5 * (d - 60.0) / 50.0
        gm_t = 0.4 + 0.9 * (d - 60.0) / 50.0
        rec.append(np.degrees(euler_extract(euler_R(al_t, np.radians(d), gm_t))))
    rec = np.array(rec)
    ax.plot(bdeg, rec[:, 0], color=fs.ACCENT, lw=1.8, label=r"$\alpha$（反解）")
    ax.plot(bdeg, rec[:, 2], color=fs.BLUE, lw=1.8, ls=(0, (5, 2)), label=r"$\gamma$（反解）")
    ax.axvline(90, color=fs.FAINT, lw=0.9, ls=":")
    ax.set_xlim(60, 110); ax.set_ylim(-200, 130)
    ax.set_xlabel(r"真实转过的 $\beta$（度）", fontsize=8.4)
    ax.set_ylabel("反解出的角度（度）", fontsize=8.4)
    ax.set_title(r"$\beta$ 扫过 90°：两个角一起跳", fontsize=9.4)
    ax.annotate(r"跨过 90° 时 $\alpha,\gamma$ 同时跳到另一支",
                xy=(90, 25), xytext=(63, -95), fontsize=8.0, color=fs.MUTED,
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=0.8,
                                connectionstyle="arc3,rad=-0.25"))
    ax.legend(fontsize=8.0, loc="lower left", ncol=2, handlelength=1.6)
    ax.tick_params(labelsize=7.8)

    fig.tight_layout(pad=0.5, w_pad=1.4)
    fs.save(fig, "ch04", "fig04-02")


# ---------------- 图 4-3：GN / GD / LM 的迭代轨迹 ----------------
def _cost_quartic(t):
    r = t * t - 2.0
    return 0.5 * r * r


def _run_gn(t0, it=12):
    t, hist, cs = t0, [t0], [_cost_quartic(t0)]
    for _ in range(it):
        r = t * t - 2.0; j = 2 * t
        d = -(j * r) / (j * j)
        t = t + d
        hist.append(t); cs.append(_cost_quartic(t))
        if abs(d) < 1e-13:
            break
    return np.array(hist), np.array(cs)


def _run_gd(t0, it=200, eta=0.08):
    t, hist, cs = t0, [t0], [_cost_quartic(t0)]
    for _ in range(it):
        r = t * t - 2.0; j = 2 * t; g = j * r
        step = eta
        for _ in range(50):
            if _cost_quartic(t - step * g) < _cost_quartic(t) - 1e-4 * step * g * g:
                break
            step *= 0.5
        t = t - step * g
        hist.append(t); cs.append(_cost_quartic(t))
        if abs(step * g) < 1e-13:
            break
    return np.array(hist), np.array(cs)


def _run_lm(t0, it=12, lam=2.0):
    t, hist, cs = t0, [t0], [_cost_quartic(t0)]
    for _ in range(it):
        r = t * t - 2.0; j = 2 * t; g = j * r
        d = -g / (j * j + lam)
        if _cost_quartic(t + d) < _cost_quartic(t):
            t = t + d
            lam = max(lam * 0.3, 1e-12)
            hist.append(t); cs.append(_cost_quartic(t))
        else:
            lam *= 3.0
        if abs(d) < 1e-13:
            break
    return np.array(hist), np.array(cs)


def fig04_03():
    t0 = 0.1
    hg, cg = _run_gn(t0)
    hd, cd = _run_gd(t0)
    hl, cl = _run_lm(t0)

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.85),
                             gridspec_kw={"width_ratios": [1.0, 1.0]})

    # 左：代价曲线 + 三种方法的落点（只画落在窗口内的点）
    ax = axes[0]
    fs.clean(ax, grid=True)
    tt = np.linspace(0.02, 2.55, 600)
    ax.plot(tt, np.array([_cost_quartic(t) for t in tt]), color=fs.INK, lw=1.4)
    ax.axhline(0.0, color=fs.FAINT, lw=0.8)
    for h, c, col, lab in [(hd, cd, fs.BLUE, "梯度下降"),
                           (hl, cl, fs.GREEN, "LM"),
                           (hg, cg, fs.ACCENT, "高斯-牛顿")]:
        m = h <= 2.55
        ax.scatter(h[m], c[m], s=16, color=col, zorder=5, label=lab,
                   edgecolor="white", linewidth=0.5)
    ax.scatter([np.sqrt(2)], [0.0], s=46, marker="*", color=fs.GOLD, zorder=6)
    ax.set_xlim(0.0, 2.55); ax.set_ylim(-0.35, 4.2)
    ax.set_xlabel(r"参数 $t$", fontsize=8.4)
    ax.set_ylabel(r"代价 $f(t)=\frac{1}{2}(t^2-2)^2$", fontsize=8.4)
    ax.set_title(r"最优解在 $t=\sqrt{2}$", fontsize=9.4)
    fs.label(ax, 0.05, 3.30, r"谷底 $t=\sqrt{2}\approx 1.414$",
             fs=8.4, color=fs.GOLD, ha="left")
    ax.legend(fontsize=8.0, loc="upper right")
    ax.tick_params(labelsize=7.8)

    # 右：代价随迭代下降（对数纵轴，看 GN 的“先炸后收”）
    ax = axes[1]
    fs.clean(ax, grid=True)
    for h, c, col, lab, mk in [(hg, cg, fs.ACCENT, "高斯-牛顿", "o"),
                               (hd, cd, fs.BLUE, "梯度下降", None),
                               (hl, cl, fs.GREEN, "LM", "s")]:
        ax.semilogy(np.arange(len(c)), np.maximum(c, 1e-16), color=col, lw=1.7,
                    marker=mk, markersize=3.0, label=lab)
    ax.set_xlim(0, 46); ax.set_ylim(1e-16, 1e5)
    ax.set_xlabel("迭代次数", fontsize=8.4)
    ax.set_ylabel("代价（对数）", fontsize=8.4)
    ax.set_title("从同一点出发：一步的差别", fontsize=9.4)
    ax.annotate("GN 第一步\n把代价抬高\n约 2500 倍", xy=(1.0, 4.2e3), xytext=(5.2, 2.6e2),
                fontsize=7.6, color=fs.ACCENT, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=0.8,
                                connectionstyle="arc3,rad=0.25"))
    ax.legend(fontsize=7.8, loc="upper right", framealpha=0.92,
              edgecolor="#E5E7EB", borderpad=0.4)
    ax.tick_params(labelsize=7.8)

    fig.tight_layout(pad=0.5, w_pad=1.3)
    fs.save(fig, "ch04", "fig04-03")


# ---------------- 图 4-4：H 的块稀疏结构 ----------------
def fig04_04():
    rng = np.random.default_rng(2024)
    P, L = 6, 8                       # 位姿数、路标数
    vis = np.zeros((L, P), bool)
    for j in range(L):
        k = int(rng.integers(2, 5))
        vis[j, rng.choice(P, size=k, replace=False)] = True
    # 变量顺序：先 6 个位姿（每个 6 维），再 L 个路标（每个 3 维）
    ncol = 6 * P + 3 * L
    rows, cols, r = [], [], 0
    for j in range(L):
        for i in range(P):
            if not vis[j, i]:
                continue
            for _ in range(2):                       # 每个观测 2 行残差
                for k in range(6):
                    rows.append(r); cols.append(6 * i + k)
                for k in range(3):
                    rows.append(r); cols.append(6 * P + 3 * j + k)
                r += 1
    J = np.zeros((r, ncol))
    J[np.array(rows), np.array(cols)] = 1.0
    H = J.T @ J                                      # 真算，不是画上去的图案

    W = 6.0                                          # 每个位姿块的宽
    Hh = 3.0                                         # 每个路标块的宽
    xpos = [i * W for i in range(P)]
    xlm = [P * W + j * Hh for j in range(L)]
    xsplit = P * W

    fig, ax = plt.subplots(figsize=(5.0, 4.4))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-15.0, xsplit + L * Hh + 3.0)
    ax.set_ylim(xsplit + L * Hh + 18.0, -16.0)

    def blk(x0, y0, w, h, col, alpha=0.92):
        ax.add_patch(Rectangle((x0, y0), w, h, facecolor=col, edgecolor="white",
                               lw=0.6, alpha=alpha, zorder=3))

    # 位姿块（左上）：对角块 + 共同观测造成的非对角块
    for a in range(P):
        for b in range(P):
            sub = H[6 * a:6 * a + 6, 6 * b:6 * b + 6]
            if np.any(sub):
                blk(xpos[b], xpos[a], W, W, fs.ACCENT, 0.92 if a != b else 1.0)
    # 路标块（右下）：只有对角块
    for a in range(L):
        for b in range(L):
            sub = H[6 * P + 3 * a:6 * P + 3 * a + 3, 6 * P + 3 * b:6 * P + 3 * b + 3]
            if np.any(sub):
                blk(xlm[b], xlm[a], Hh, Hh, fs.GREEN)
    # 位姿–路标（右上 / 左下）
    for a in range(P):
        for b in range(L):
            sub = H[6 * a:6 * a + 6, 6 * P + 3 * b:6 * P + 3 * b + 3]
            if np.any(sub):
                blk(xlm[b], xpos[a], Hh, W, fs.BLUE, 0.85)
            if np.any(H[6 * P + 3 * b:6 * P + 3 * b + 3, 6 * a:6 * a + 6]):
                blk(xpos[a], xlm[b], W, Hh, fs.BLUE, 0.85)

    ax.plot([-6.0, xsplit + L * Hh + 1.0], [xsplit, xsplit], color=fs.INK, lw=1.0, zorder=4)
    ax.plot([xsplit, xsplit], [-6.0, xsplit + L * Hh + 1.0], color=fs.INK, lw=1.0, zorder=4)

    ax.text(xsplit * 0.5, -9.5, "位姿 %d 个（各 6 维）" % P, fontsize=8.4, color=fs.ACCENT,
            ha="center", va="center")
    ax.text(xsplit + L * Hh * 0.5, -9.5, "路标 %d 个（各 3 维）" % L, fontsize=8.4,
            color=fs.GREEN, ha="center", va="center")
    ax.text(-8.5, xsplit * 0.5, "位姿", fontsize=8.4, color=fs.ACCENT, rotation=90,
            ha="center", va="center")
    ax.text(-8.5, xsplit + L * Hh * 0.5, "路标", fontsize=8.4, color=fs.GREEN,
            rotation=90, ha="center", va="center")
    fig.suptitle(r"$\mathbf{H}=\mathbf{J}^{\top}\mathbf{J}$ 的块结构", fontsize=9.6,
                 color=fs.INK, y=0.985)

    fig.text(0.5, 0.072, "橙：位姿–位姿（严格分块对角）　　蓝：位姿–路标",
             fontsize=7.9, color=fs.MUTED, ha="center", va="bottom")
    fig.text(0.5, 0.032, "绿：路标–路标（严格分块对角，每块 3×3）",
             fontsize=7.9, color=fs.MUTED, ha="center", va="bottom")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.11)
    fs.save(fig, "ch04", "fig04-04")


if __name__ == "__main__":
    fig04_01()
    fig04_02()
    fig04_03()
    fig04_04()
