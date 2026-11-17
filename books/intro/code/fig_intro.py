# -*- coding: utf-8 -*-
"""入门册第 3、4 章插图：骨架树、蒙皮权重、扭转、三种监督、两条路线。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs
fs.FIGDIR = os.path.join(HERE, "img")

from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PolyCollection
import matplotlib.colors as mcolors


# =====================================================================
# 图 3-1  骨架是一棵树
# =====================================================================
def fig_tree():
    fig, ax = fs.canvas(7.0, 4.1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")

    J = dict(
        pelvis=(0.340, 0.360),
        s1=(0.340, 0.440), s2=(0.340, 0.520), s3=(0.340, 0.600),
        neck=(0.340, 0.680), head=(0.340, 0.772),
        lsh_p=(0.340, 0.615),
        lsh=(0.262, 0.612), lel=(0.218, 0.490), lwr=(0.178, 0.374),
        rsh=(0.418, 0.612), rel=(0.462, 0.490), rwr=(0.502, 0.374),
        lhip=(0.306, 0.320), lkn=(0.286, 0.190), lan=(0.272, 0.070),
        rhip=(0.374, 0.320), rkn=(0.394, 0.190), ran=(0.408, 0.070),
    )
    SPINE, ARM, LEG, HEAD = fs.INK, fs.BLUE, fs.GREEN, fs.PURPLE
    edges = [
        ("pelvis", "s1", SPINE), ("s1", "s2", SPINE), ("s2", "s3", SPINE),
        ("s3", "neck", SPINE), ("neck", "head", HEAD),
        ("lsh_p", "lsh", ARM), ("lsh", "lel", ARM), ("lel", "lwr", ARM),
        ("lsh_p", "rsh", ARM), ("rsh", "rel", ARM), ("rel", "rwr", ARM),
        ("pelvis", "lhip", LEG), ("lhip", "lkn", LEG), ("lkn", "lan", LEG),
        ("pelvis", "rhip", LEG), ("rhip", "rkn", LEG), ("rkn", "ran", LEG),
    ]
    for a, b, c in edges:
        p, q = J[a], J[b]
        ax.plot([p[0], q[0]], [p[1], q[1]], color=c, lw=1.8, alpha=0.9,
                solid_capstyle="round", zorder=2)

    jcolor = {}
    for k in ("pelvis", "s1", "s2", "s3", "neck"):
        jcolor[k] = SPINE
    jcolor["head"] = HEAD
    for k in ("lsh", "lel", "lwr", "rsh", "rel", "rwr"):
        jcolor[k] = ARM
    for k in ("lhip", "lkn", "lan", "rhip", "rkn", "ran"):
        jcolor[k] = LEG
    for k, p in J.items():
        if k == "lsh_p":
            continue
        r = 0.0132 if k == "pelvis" else 0.0090
        fc = fs.ACCENT if k == "pelvis" else "white"
        ax.add_patch(Circle(p, r, facecolor=fc, edgecolor=jcolor[k], lw=1.5,
                            zorder=6))

    lab = dict(
        pelvis=(-0.020, 0.000, "right", "骨盆"),
        s2=(0.013, 0.000, "left", "脊柱"),
        s3=(0.013, 0.004, "left", "胸"),
        neck=(0.013, 0.000, "left", "颈"),
        head=(0.000, 0.031, "center", "头"),
        lsh=(-0.012, 0.011, "right", "肩"), lel=(-0.012, 0.000, "right", "肘"),
        lwr=(-0.012, 0.000, "right", "腕"),
        rsh=(0.012, 0.011, "left", "肩"), rel=(0.012, 0.000, "left", "肘"),
        rwr=(0.012, 0.000, "left", "腕"),
        lhip=(-0.019, -0.016, "right", "髋"), lkn=(-0.015, 0.000, "right", "膝"),
        lan=(-0.015, 0.000, "right", "踝"),
        rhip=(0.019, -0.016, "left", "髋"), rkn=(0.015, 0.000, "left", "膝"),
        ran=(0.015, 0.000, "left", "踝"),
    )
    for k, (dx, dy, ha, txt) in lab.items():
        p = J[k]
        ax.text(p[0] + dx, p[1] + dy, txt, fontsize=8.3, color=fs.INK,
                ha=ha, va="center", zorder=8)

    ax.text(0.600, 0.912, "一个关节只管三个角", fontsize=9.7, color=fs.INK,
            ha="left", va="top", weight="bold")
    ax.text(0.600, 0.848, "向前弯、向侧面展、绕自己转，各一个",
            fontsize=8.1, color=fs.MUTED, ha="left", va="top")
    ax.text(0.600, 0.752, "24 × 3 = 72", fontsize=13.5, color=fs.ACCENT,
            ha="left", va="top", weight="bold")
    ax.text(0.600, 0.672, "整个人摆出的姿势，就是这 72 个数",
            fontsize=8.1, color=fs.MUTED, ha="left", va="top")
    ax.text(0.600, 0.565, "转一根骨头，下游整条链跟着走",
            fontsize=8.1, color=fs.MUTED, ha="left", va="top")
    ax.text(0.600, 0.492, "这是“树”而不是“网”的好处",
            fontsize=8.1, color=fs.MUTED, ha="left", va="top")

    ax.plot([0.606], [0.408], marker="o", ms=7.5, color=fs.ACCENT,
            mec="white", mew=1.2, zorder=4)
    ax.text(0.664, 0.408, "根关节（其余都是它的子孙）", fontsize=8.1,
            color=fs.MUTED, ha="left", va="center")
    for yy, cc, tt in ((0.345, SPINE, "躯干链"), (0.288, ARM, "手臂链"),
                       (0.231, LEG, "腿链"), (0.174, HEAD, "头部")):
        ax.plot([0.600, 0.652], [yy, yy], color=cc, lw=2.4,
                solid_capstyle="round", zorder=3)
        ax.text(0.664, yy, tt, fontsize=8.1, color=fs.MUTED, ha="left",
                va="center")

    fs.save(fig, "03", "fig03-01")


# =====================================================================
# 图 3-2  蒙皮权重沿肢体从 1 渐变到 0
# =====================================================================
def _arm_geometry():
    sh = np.array([0.150, 0.315])
    el = np.array([0.500, 0.315])
    bend = np.deg2rad(62.0)
    d2 = np.array([np.cos(bend), np.sin(bend)])
    wr = el + 0.300 * d2

    pos, rad, tan = [], [], []
    n1, n2 = 8, 8
    for i in range(n1):
        t = i / (n1 - 1)
        pos.append(sh + (el - sh) * t)
        tan.append((el - sh) / np.linalg.norm(el - sh))
        rad.append(0.0570 + (0.0430 - 0.0570) * t)
    for i in range(1, n2 + 1):
        t = i / n2
        pos.append(el + (wr - el) * t)
        tan.append(d2 / np.linalg.norm(d2))
        rad.append(0.0430 + (0.0270 - 0.0430) * t)
    pos = np.array(pos)
    rad = np.array(rad)
    tan = np.array(tan)
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(pos, axis=0), axis=1))])
    return pos, rad, tan, s


def _smooth_weight(s, s0, band):
    u = np.clip((s - (s0 - band)) / (2 * band), 0.0, 1.0)
    return u * u * (3 - 2 * u)


def fig_weights():
    pos, rad, tan, s = _arm_geometry()
    n = len(pos)
    nrm = np.column_stack([-tan[:, 1], tan[:, 0]])
    i_el = n // 2
    s_elbow = s[i_el]
    band = 0.19 * s[-1]
    w = _smooth_weight(s, s_elbow, band)

    top = pos + nrm * rad[:, None]
    bot = pos - nrm * rad[:, None]

    fig = plt.figure(figsize=(7.1, 3.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.36, 1.00], wspace=0.17)
    ax = fig.add_subplot(gs[0, 0])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(0.00, 0.80)
    ax.set_ylim(0.10, 0.88)

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "w", [fs.BLUE, "#8A6BA8", fs.ACCENT])

    quads, cols = [], []
    for i in range(n - 1):
        quads.append([top[i], top[i + 1], bot[i + 1], bot[i]])
        cols.append(cmap(0.5 * (w[i] + w[i + 1])))
    ax.add_collection(PolyCollection(quads, facecolors=cols, edgecolors="none",
                                     zorder=3))
    for i in range(n):
        ax.plot([top[i][0], bot[i][0]], [top[i][1], bot[i][1]],
                color="white", lw=0.7, alpha=0.95, zorder=4)
    for i in range(n - 1):
        ax.plot([top[i][0], top[i + 1][0]], [top[i][1], top[i + 1][1]],
                color="white", lw=0.7, alpha=0.95, zorder=4)
        ax.plot([bot[i][0], bot[i + 1][0]], [bot[i][1], bot[i + 1][1]],
                color="white", lw=0.7, alpha=0.95, zorder=4)
    ax.plot(np.r_[top[:, 0], bot[::-1, 0]], np.r_[top[:, 1], bot[::-1, 1]],
            color=fs.INK, lw=1.1, zorder=5, alpha=0.8)

    ax.plot([pos[0][0], pos[i_el][0]], [pos[0][1], pos[i_el][1]],
            color=fs.INK, lw=1.0, ls=(0, (4, 3)), alpha=0.6, zorder=2)
    ax.plot([pos[i_el][0], pos[-1][0]], [pos[i_el][1], pos[-1][1]],
            color=fs.INK, lw=1.0, ls=(0, (4, 3)), alpha=0.6, zorder=2)
    ax.plot([pos[i_el][0]], [pos[i_el][1]], marker="o", ms=3.6, color=fs.INK,
            zorder=6)
    ax.text(pos[i_el][0] - 0.004, pos[i_el][1] - 0.075, "肘", fontsize=8.3,
            color=fs.MUTED, ha="center", va="top")
    ax.text(pos[0][0], pos[0][1] - 0.078, "肩", fontsize=8.3,
            color=fs.MUTED, ha="center", va="top")
    ax.text(pos[-1][0] + 0.030, pos[-1][1] + 0.020, "腕", fontsize=8.3,
            color=fs.MUTED, ha="left", va="center")

    k = int(np.argmin(np.abs(w - 0.70)))
    px, py = bot[k]
    ax.plot([px], [py], marker="o", ms=5.2, color="white", mec=fs.INK,
            mew=1.2, zorder=8)
    ax.annotate("这个顶点受两根骨头拉扯\n前臂 0.7 ＋ 上臂 0.3",
                xy=(px, py), xytext=(0.560, 0.170),
                fontsize=8.2, color=fs.INK, ha="left", va="center",
                linespacing=1.8, zorder=9,
                arrowprops=dict(arrowstyle="-|>", color=fs.INK, lw=0.9,
                                shrinkA=4, shrinkB=5,
                                connectionstyle="arc3,rad=-0.16"))

    cax = ax.inset_axes([0.02, 0.045, 0.30, 0.030])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal", ticks=[0, 0.5, 1])
    cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=7.4, length=2.2, pad=1.4)
    cb.set_label("前臂权重 $w$", fontsize=8.0, labelpad=1.0)

    ax2 = fig.add_subplot(gs[0, 1])
    fs.clean(ax2, spines=("left", "bottom"))
    sf = np.linspace(0, 1, 400)
    wf = _smooth_weight(sf * s[-1], s_elbow, band)
    ax2.fill_between([(s_elbow - band) / s[-1], (s_elbow + band) / s[-1]],
                     0, 1, color=fs.FAINT, alpha=0.16, lw=0, zorder=0)
    ax2.plot(sf, wf, color=fs.ACCENT, lw=1.9, zorder=3)
    ax2.plot(s / s[-1], w, "o", ms=3.4, color="white", mec=fs.ACCENT,
             mew=1.0, zorder=4)
    ax2.axhline(0.5, color=fs.FAINT, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.04, 1.12)
    ax2.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax2.set_xlabel("沿肢体的位置（0 = 肩，1 = 腕）", fontsize=8.4)
    ax2.set_ylabel("前臂权重 $w$", fontsize=8.4)
    ax2.tick_params(labelsize=8)
    ax2.text(0.02, 0.94, "只跟上臂", fontsize=8.0, color=fs.BLUE, ha="left",
             va="top")
    ax2.text(0.98, 0.07, "只跟前臂", fontsize=8.0, color=fs.ACCENT, ha="right",
             va="bottom")
    ax2.annotate("关节处各占一半", xy=(0.5, 0.5), xytext=(0.545, 0.245),
                 fontsize=7.9, color=fs.MUTED, ha="left", va="center",
                 arrowprops=dict(arrowstyle="-", color=fs.FAINT, lw=0.8))

    fig.subplots_adjust(left=0.015, right=0.985, top=0.975, bottom=0.135)
    fs.save(fig, "03", "fig03-02")


# =====================================================================
# 图 3-3  扭转与截面半径（真算）
# =====================================================================
def _twist_matrix(theta, w):
    c, s = np.cos(theta), np.sin(theta)
    Rx = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    return (1 - w) * np.eye(3) + w * Rx


def _section(theta, w, npts=720):
    """把静止截面（单位圆）用混合矩阵搬过去，返回点与半径（真算）。"""
    phi = np.linspace(0, 2 * np.pi, npts, endpoint=False)
    P = np.stack([np.zeros_like(phi), np.cos(phi), np.sin(phi)])
    Q = _twist_matrix(theta, w) @ P
    r = np.hypot(Q[1], Q[2])
    return Q, float(r.mean()), float(r.std())


def fig_twist():
    fig = plt.figure(figsize=(7.1, 3.35))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.16, 1.00], wspace=0.25)

    ax = fig.add_subplot(gs[0, 0])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.05, 5.85)
    ax.set_ylim(-1.72, 1.42)

    angles = [0, 90, 120, 180]
    cols = [fs.BLUE, fs.GREEN, fs.ACCENT, fs.PURPLE]
    for i, (deg, c) in enumerate(zip(angles, cols)):
        th = np.deg2rad(deg)
        Q, r, sd = _section(th, 0.5)
        cx = i * 1.56
        ax.add_patch(Circle((cx, 0), 1.0, facecolor="none", edgecolor=fs.FAINT,
                            lw=0.9, ls=(0, (3, 3)), zorder=1))
        if r > 0.02:
            ax.add_patch(Polygon(np.column_stack([cx + Q[1], Q[2]]), closed=True,
                                 facecolor=c, alpha=0.20, edgecolor=c, lw=1.5,
                                 zorder=3))
            ax.plot([cx, cx + Q[1][0]], [0, Q[2][0]], color=c, lw=1.2,
                    zorder=4, alpha=0.9)
        else:
            ax.plot([cx], [0], marker="o", ms=7.0, color=c, zorder=4)
        ax.plot([cx], [0], marker="+", ms=6, color=fs.MUTED, mew=0.9, zorder=5)
        ax.text(cx, -1.42, f"{deg}°", fontsize=9.6, color=c, ha="center",
                va="center", weight="bold")
        ax.text(cx, -1.65, f"半径 {r:.2f}", fontsize=8.2, color=fs.MUTED,
                ha="center", va="center")
    ax.text(-1.00, 1.30, "同一根管子，中段扭转不同角度之后的横截面",
            fontsize=8.8, color=fs.INK, ha="left", va="center")

    ax2 = fig.add_subplot(gs[0, 1])
    fs.clean(ax2, spines=("left", "bottom"))
    ths = np.linspace(0, np.pi, 300)
    r5 = np.array([_section(t, 0.5)[1] for t in ths])
    r7 = np.array([_section(t, 0.7)[1] for t in ths])
    ax2.plot(np.rad2deg(ths), r7, color=fs.MUTED, lw=1.4, ls=(0, (5, 2)),
             label="权重 0.7 / 0.3")
    ax2.plot(np.rad2deg(ths), r5, color=fs.ACCENT, lw=2.0,
             label="权重各 0.5")
    ax2.axhline(0.5, color=fs.FAINT, lw=0.9, ls=(0, (4, 3)))
    for deg, c in [(90, fs.GREEN), (120, fs.ACCENT), (180, fs.PURPLE)]:
        r = _section(np.deg2rad(deg), 0.5)[1]
        ax2.plot([deg], [r], "o", ms=5.0, color="white", mec=c, mew=1.5,
                 zorder=5)
    ax2.set_xlim(0, 180)
    ax2.set_ylim(0, 1.12)
    ax2.set_xticks([0, 45, 90, 135, 180])
    ax2.set_xlabel("扭转角 $\\theta$（度）", fontsize=8.6)
    ax2.set_ylabel("截面半径（相对静止时）", fontsize=8.6)
    ax2.tick_params(labelsize=8)
    ax2.legend(loc="lower left", fontsize=8.0, handlelength=1.9,
               labelspacing=0.45, borderaxespad=0.3)
    ax2.text(0.98, 0.965, "90°  0.71\n120° 0.50\n180° 0.00",
             transform=ax2.transAxes, fontsize=8.2, color=fs.MUTED,
             ha="right", va="top", linespacing=1.9)

    fig.subplots_adjust(left=0.035, right=0.985, top=0.965, bottom=0.115)
    fs.save(fig, "03", "fig03-03")


# =====================================================================
# 图 4-1  三种监督
# =====================================================================
def _body():
    """返回简笔人形的肢体胶囊列表与关节位置。"""
    hip = np.array([0.50, 0.44])
    neck = np.array([0.50, 0.71])
    head = np.array([0.50, 0.815])
    limbs, joints = [], {}
    limbs.append((hip, neck, 0.115, 0.105))
    joints["骨盆"] = hip
    joints["颈"] = neck
    joints["头"] = head
    joints["头顶"] = head + np.array([0, 0.030])
    limbs.append((neck, head - np.array([0, 0.042]), 0.042, 0.040))
    for side in (-1, 1):
        sh = np.array([0.50 + side * 0.048, 0.700])
        sh_j = np.array([0.50 + side * 0.086, 0.700])
        el = np.array([sh_j[0] + side * 0.072, 0.586])
        wr = np.array([el[0] + side * 0.030, 0.470])
        limbs.append((sh, el, 0.060, 0.047))
        limbs.append((el, wr, 0.047, 0.034))
        joints["肩"] = sh_j
        joints["肘"] = el
        joints["腕"] = wr
        hj = hip + np.array([side * 0.050, -0.004])
        kn = hj + np.array([side * 0.012, -0.190])
        an = kn + np.array([side * 0.006, -0.185])
        limbs.append((hj, kn, 0.084, 0.062))
        limbs.append((kn, an, 0.062, 0.040))
        joints["髋"] = hj
        joints["膝"] = kn
        joints["踝"] = an
    return limbs, joints


def _capsule_mask(X, Y, limbs, pad=0.0):
    m = np.zeros_like(X, dtype=bool)
    for p0, p1, w0, w1 in limbs:
        p0 = np.asarray(p0, float)
        p1 = np.asarray(p1, float)
        d = p1 - p0
        L2 = d @ d
        t = np.clip(((X - p0[0]) * d[0] + (Y - p0[1]) * d[1]) / L2, 0, 1)
        px = p0[0] + t * d[0]
        py = p0[1] + t * d[1]
        r = w0 / 2 + (w1 / 2 - w0 / 2) * t
        m |= (X - px) ** 2 + (Y - py) ** 2 <= (r + pad) ** 2
    return m


def fig_supervision():
    limbs, joints = _body()
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.05))
    titles = ["① 关键点对齐", "② 轮廓对齐", "③ 像素颜色对齐"]
    notes = ["几个位置对上了\n便宜，但约束很松",
             "整圈边线对上了\n中等，要靠分割",
             "每个格子的颜色都对上\n最贵，渲染必须可微"]
    ng = 700
    gx, gy = np.meshgrid(np.linspace(0, 1, ng), np.linspace(0, 1, ng))
    m = _capsule_mask(gx, gy, limbs)

    for ax, t, note in zip(axes, titles, notes):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(t, fontsize=9.4, color=fs.INK, pad=5)
        ax.text(0.5, -0.02, note, fontsize=7.8, color=fs.MUTED,
                ha="center", va="top", linespacing=1.7)

    def silhouette(ax):
        for p0, p1, w0, w1 in limbs:
            fs.limb(ax, p0, p1, w0, w1, color="#D3D8E0")
        ax.add_patch(Circle(joints["头顶"] - np.array([0, 0.030]), 0.067,
                            facecolor="#D3D8E0", edgecolor="none"))

    ax = axes[0]
    silhouette(ax)
    seen = []
    for k, p in joints.items():
        if k == "头顶":
            continue
        if any(np.linalg.norm(p - q) < 1e-6 for q in seen):
            continue
        seen.append(p)
        ax.plot([p[0]], [p[1]], marker="o", ms=4.8, color=fs.ACCENT,
                mec="white", mew=1.1, zorder=6)

    ax = axes[1]
    silhouette(ax)
    ax.contour(gx, gy, m.astype(float), levels=[0.5], colors=[fs.ACCENT],
               linewidths=1.6, zorder=5)

    ax = axes[2]
    silhouette(ax)
    nc = 22
    cg = np.linspace(0, 1, nc + 1)
    cx, cy = np.meshgrid((cg[:-1] + cg[1:]) / 2, (cg[:-1] + cg[1:]) / 2)
    cm = _capsule_mask(cx, cy, limbs)
    ax.imshow(np.where(cm, 1.0, np.nan), extent=[0, 1, 0, 1], origin="lower",
              cmap=mcolors.ListedColormap([fs.ACCENT]), alpha=0.40,
              interpolation="nearest", zorder=4)
    for v in cg:
        ax.plot([v, v], [0, 1], color="white", lw=0.4, alpha=0.45, zorder=5)
        ax.plot([0, 1], [v, v], color="white", lw=0.4, alpha=0.45, zorder=5)

    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.215,
                        wspace=0.13)
    fs.save(fig, "04", "fig04-01")


# =====================================================================
# 图 4-2  优化与回归两条路线
# =====================================================================
def fig_two_routes():
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.25),
                             gridspec_kw=dict(width_ratios=[1.02, 1.0],
                                              wspace=0.15))

    # ---- 左：优化回路 ----
    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("优化法：一遍遍改，直到像为止", fontsize=9.2, color=fs.INK,
                 pad=6)
    fs.box(ax, 0.22, 0.725, 0.54, 0.150, "当前的一组参数 $\\beta,\\theta$",
           fc="#FDF6EE", ec=fs.ACCENT, fs=8.6)
    fs.box(ax, 0.55, 0.405, 0.40, 0.150, "渲染出模型", fc="white",
           ec=fs.INK, fs=8.6)
    fs.box(ax, 0.05, 0.405, 0.40, 0.150, "和照片比差距", fc="white",
           ec=fs.INK, fs=8.6)
    fs.arrow(ax, (0.665, 0.725), (0.745, 0.560), color=fs.MUTED, rad=-0.12)
    fs.arrow(ax, (0.545, 0.480), (0.455, 0.480), color=fs.MUTED)
    fs.arrow(ax, (0.130, 0.555), (0.330, 0.725), color=fs.ACCENT, rad=0.24)
    ax.text(0.345, 0.615, "梯度回传", fontsize=8.0, color=fs.ACCENT,
            ha="left", va="center")
    ax.text(0.50, 0.075, "慢。一次几秒到几分钟，要好初值，\n但只要监督信号够，结果最准。",
            fontsize=8.0, color=fs.MUTED, ha="center", va="center",
            linespacing=1.8)

    # ---- 右：回归 ----
    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("回归法：看一眼，直接说出参数", fontsize=9.2, color=fs.INK,
                 pad=6)
    fs.box(ax, 0.015, 0.815, 0.225, 0.135, "一张照片", fc="white", ec=fs.INK,
           fs=8.5)
    fs.box(ax, 0.335, 0.815, 0.315, 0.135, "神经网络", fc="#EEF3FC", ec=fs.BLUE,
           fs=8.5)
    fs.box(ax, 0.745, 0.815, 0.225, 0.135, "参数", fc="#FDF6EE", ec=fs.ACCENT,
           fs=8.5)
    fs.arrow(ax, (0.245, 0.882), (0.330, 0.882), color=fs.MUTED)
    fs.arrow(ax, (0.655, 0.882), (0.740, 0.882), color=fs.MUTED)
    ax.text(0.50, 0.755, "一次前向，几十毫秒", fontsize=7.9, color=fs.MUTED,
            ha="center", va="center")

    t = np.linspace(-1, 1, 9)
    xs = 0.480 + 0.290 * t
    ys = 0.120 + 0.200 * (1 - t ** 2)
    tt = np.linspace(-1, 1, 240)
    ax.plot(0.480 + 0.290 * tt, 0.120 + 0.200 * (1 - tt ** 2),
            color=fs.FAINT, lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.scatter(xs, ys, s=14, color=fs.BLUE, alpha=0.75, lw=0, zorder=3)
    mx, my = xs.mean(), ys.mean()
    ax.plot([mx], [my], marker="o", ms=7.1, color=fs.ACCENT, mec="white",
            mew=1.2, zorder=5)
    ax.annotate("用平方误差训练时，网络学到的是这组合理解的\n算术平均。它谁也不得罪，于是谁也不像",
                xy=(mx, my + 0.016), xytext=(0.500, 0.585),
                fontsize=7.9, color=fs.ACCENT, ha="center", va="center",
                linespacing=2.0,
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=0.9,
                                shrinkA=6, shrinkB=3,
                                connectionstyle="arc3,rad=0.0"))
    ax.text(0.50, 0.028, "快。但输入模糊时它只能给出一个“折中”答案",
            fontsize=8.0, color=fs.MUTED, ha="center", va="center")

    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.055)
    fs.save(fig, "04", "fig04-02")


if __name__ == "__main__":
    fig_tree()
    fig_weights()
    fig_twist()
    fig_supervision()
    fig_two_routes()
