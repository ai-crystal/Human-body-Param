# -*- coding: utf-8 -*-
"""第 22 章插图：SMAL——四足动物的参数化。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle
import figstyle as fs


# ---------------- 参数化四足剪影（侧视，头朝右） ----------------
def chain(ax, p0, segs, w0, w1, color, alpha=1.0, z=3, joints=False,
          jcolor=fs.ACCENT, r=0.007):
    """按“长度 + 与竖直向下方向的夹角（度，正为向前）”画一条骨架链。

    角度约定：0 度指向正下方，90 度指向正前方，180 度指向正上方。
    """
    pts = [np.array(p0, float)]
    for (ang, ln) in segs:
        a = np.radians(ang)
        pts.append(pts[-1] + np.array([np.sin(a), -np.cos(a)]) * ln)
    n = len(pts) - 1
    for i in range(n):
        t0 = i / max(1, n - 1)
        t1 = (i + 1) / max(1, n - 1)
        fs.limb(ax, pts[i], pts[i + 1], w0 + (w1 - w0) * t0, w0 + (w1 - w0) * t1,
                color=color, alpha=alpha, z=z)
    if joints:
        for p in pts:
            ax.add_patch(Circle(p, r, facecolor=jcolor, edgecolor="white", lw=0.7,
                                zorder=z + 4))
    return pts


def quad(ax, cx=0.5, cy=0.5, s=1.0, body=1.0, leg=1.0, neck=20.0, head=1.0,
         tail=1.0, arch=0.0, color=fs.INK, alpha=1.0, z=3, joints=False,
         jcolor=fs.ACCENT, ear=1.0, stance=None, fl=1.0, bl=1.0,
         muzzle=1.0, tail_up=0.0, far=True, necklen=1.0):
    """画一只侧视四足动物，返回主要关节坐标。所有尺寸以 s 为单位。

    body 躯干长度倍数；leg 腿长倍数；neck 颈部相对竖直方向的前倾角（度）；
    head 头大小；tail 尾巴长度；arch 背部拱起；stance 摆腿角 (前, 后)；
    fl/bl 前/后腿长度倍数；muzzle 口鼻长度；tail_up 尾巴抬起角。
    """
    L = 0.225 * s * body
    H = 0.110 * s * body
    hip = np.array([cx - L / 2, cy + arch * s])
    sho = np.array([cx + L / 2, cy + 0.006 * s])
    lw = 0.030 * s

    # 远侧两条腿（先画，颜色淡，制造前后层次）
    st = stance or (0.0, 0.0)
    if far:
        chain(ax, sho + np.array([-0.016 * s, -H * 0.38]),
              [(st[0] + 9, 0.100 * s * leg * fl), (-st[0] * 0.8 - 5, 0.090 * s * leg * fl)],
              lw * 0.95, lw * 0.6, color, alpha * 0.40, z - 1)
        chain(ax, hip + np.array([0.016 * s, -H * 0.36]),
              [(-st[1] - 9, 0.092 * s * leg * bl), (st[1] * 0.9 + 5, 0.098 * s * leg * bl)],
              lw * 1.05, lw * 0.6, color, alpha * 0.40, z - 1)

    # 躯干：一段胶囊
    fs.limb(ax, hip, sho, H, H * 0.90, color=color, alpha=alpha, z=z)

    # 近侧腿：前肢 肩→肘→腕，后肢 髋→膝→踝
    fpts = chain(ax, sho + np.array([0, -H * 0.36]),
                 [(st[0], 0.100 * s * leg * fl), (-st[0] * 0.8, 0.090 * s * leg * fl)],
                 lw, lw * 0.62, color, alpha, z, joints=joints, jcolor=jcolor)
    bpts = chain(ax, hip + np.array([0, -H * 0.34]),
                 [(-st[1], 0.092 * s * leg * bl), (st[1] * 0.9, 0.098 * s * leg * bl)],
                 lw * 1.1, lw * 0.62, color, alpha, z, joints=joints, jcolor=jcolor)

    for p in (fpts[-1], bpts[-1]):
        ax.add_patch(Ellipse(p + np.array([0.008 * s, -0.006 * s]), 0.042 * s, 0.020 * s,
                             facecolor=color, edgecolor="none", alpha=alpha, zorder=z + 1))

    # 颈 + 头
    nb = sho + np.array([0.006 * s, H * 0.26])
    a_neck = 180 - neck
    npts = chain(ax, nb, [(a_neck, 0.085 * s * necklen)], lw * 1.75, lw * 1.45, color, alpha, z,
                 joints=joints, jcolor=jcolor)
    hc = npts[-1] + np.array([0.018 * s * head, 0.004 * s])
    tilt = 90 - a_neck
    ax.add_patch(Ellipse(hc, 0.070 * s * head, 0.052 * s * head, angle=tilt,
                         facecolor=color, edgecolor="none", alpha=alpha, zorder=z + 2))
    ax.add_patch(Ellipse(hc + np.array([0.030 * s * head, -0.010 * s * head]),
                         0.048 * s * head * muzzle, 0.028 * s * head, angle=tilt * 0.6,
                         facecolor=color, edgecolor="none", alpha=alpha, zorder=z + 2))
    if ear > 0:
        e0 = hc + np.array([-0.014 * s * head, 0.020 * s * head])
        ax.add_patch(Polygon([e0,
                              e0 + np.array([-0.008 * s, 0.030 * s * ear * head]),
                              e0 + np.array([0.020 * s, 0.016 * s * ear * head])],
                             closed=True, facecolor=color, edgecolor="none",
                             alpha=alpha, zorder=z + 3))

    # 尾巴：两节
    tb = hip + np.array([-0.008 * s, H * 0.26])
    tpts = chain(ax, tb,
                 [(180 - 8 - tail_up, 0.065 * s * tail),
                  (180 - 2 - tail_up * 1.3, 0.065 * s * tail)],
                 lw * 0.62, lw * 0.28, color, alpha, z, joints=joints, jcolor=jcolor)

    return dict(hip=hip, sho=sho, knee=bpts[1], ankle=bpts[2], elbow=fpts[1],
                wrist=fpts[2], neck=nb, head=hc, tail=tb, tail_tip=tpts[-1],
                all_pts=fpts + bpts + npts + tpts)


# ---------------- 图 22-1：骨架与姿态 ----------------
def fig_skeleton():
    fig, ax = fs.canvas(6.8, 3.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    quad(ax, cx=0.205, cy=0.615, s=1.02, body=1.0, leg=1.0, neck=30, arch=0.004,
         color=fs.INK, z=5, joints=True, stance=(5, -5), necklen=1.55, ear=0.65)
    quad(ax, cx=0.755, cy=0.615, s=0.96, body=1.05, leg=0.95, neck=14, arch=-0.004,
         color=fs.INK, z=5, joints=True, stance=(-32, 28), tail=1.4, tail_up=28,
         ear=0.45, head=0.95, necklen=1.45)

    fs.label(ax, 0.205, 0.115, "静止：33 个关节角都接近 0", fs=9.0, color=fs.MUTED)
    fs.label(ax, 0.755, 0.115, "奔跑：只改这 99 个数，顶点自动跟着走", fs=9.0, color=fs.MUTED)
    fs.label(ax, 0.205, 0.185, "前肢：肩 → 肘 → 腕　　后肢：髋 → 膝 → 踝　　尾：两节",
             fs=8.4, color=fs.MUTED)

    ax.plot([0.485, 0.485], [0.150, 0.900], color=fs.GRID, lw=0.9)
    fs.label(ax, 0.030, 0.952, "同一套骨架，两种姿态；橙色圆点是关节，线段是骨骼",
             fs=9.6, color=fs.ACCENT, weight="bold", ha="left", va="center")

    fs.arrow(ax, (0.318, 0.760), (0.352, 0.845), color=fs.PURPLE, lw=0.9, style="-", z=9)
    fs.label(ax, 0.354, 0.845, "颈 → 头", fs=8.6, color=fs.PURPLE, ha="left")
    fs.arrow(ax, (0.088, 0.700), (0.048, 0.845), color=fs.GOLD, lw=0.9, style="-", z=9)
    fs.label(ax, 0.046, 0.845, "尾根", fs=8.6, color=fs.GOLD, ha="left")

    fs.label(ax, 0.500, 0.048,
             r"$\boldsymbol{\theta}\in\mathbb{R}^{99}$（33×3）　"
             r"$\mathbf{t}\in\mathbb{R}^{3}$　$\boldsymbol{\beta}\in\mathbb{R}^{10\sim30}$",
             fs=9.6, color=fs.INK)
    fs.save(fig, "ch22", "fig22-02")


# ---------------- 图 22-2：SMAL 的构建流水线 ----------------
def fig_pipeline():
    fig, ax = fs.canvas(6.8, 3.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    y1, y2 = 0.78, 0.44
    w, h = 0.190, 0.150
    xs = [0.030, 0.262, 0.494, 0.726]
    row1 = [("41 个玩具扫描", "狮子、虎、斑马、牛…"),
            ("GLoSS 分段拟合", "33 段 + 缝合项"),
            ("ARAP 细化", "顶点吸到扫描面"),
            ("姿态归一化", "用 LBS 摆回同一姿态")]
    row2 = [("PCA 形状空间", "只剩体型差异"),
            ("联合配准", "模型反过来约束配准"),
            ("SMAL", "可采样、可驱动、可拟合")]
    for x, (t, sub) in zip(xs, row1):
        fs.box(ax, x, y1 - h / 2, w, h, t, fc="white", ec=fs.BLUE, fs=8.8, lw=1.1)
        fs.label(ax, x + w / 2, y1 - h / 2 - 0.055, sub, fs=8.0, color=fs.MUTED)
    for i in range(3):
        fs.arrow(ax, (xs[i] + w + 0.004, y1), (xs[i + 1] - 0.004, y1), color=fs.FAINT)

    for x, (t, sub) in zip([xs[3], xs[2], xs[1]], row2):
        fs.box(ax, x, y2 - h / 2, w, h, t, fc="white", ec=fs.GREEN, fs=8.8, lw=1.1)
        fs.label(ax, x + w / 2, y2 - h / 2 - 0.055, sub, fs=8.0, color=fs.MUTED)
    fs.arrow(ax, (xs[3] + w / 2, y1 - h / 2 - 0.080), (xs[3] + w / 2, y2 + h / 2 + 0.008),
             color=fs.FAINT)
    fs.arrow(ax, (xs[3] - 0.004, y2), (xs[2] + w + 0.004, y2), color=fs.FAINT)
    fs.arrow(ax, (xs[2] - 0.004, y2), (xs[1] + w + 0.004, y2), color=fs.FAINT)

    # 联合配准 → 新的形状空间（迭代）
    fs.arrow(ax, (xs[2] + w * 0.55, y2 + h / 2 + 0.006),
             (xs[3] + w * 0.45, y2 + h / 2 + 0.006), color=fs.ACCENT, lw=1.1,
             ls=(0, (4, 2)), rad=-0.55)
    fs.label(ax, xs[2] + w + 0.021, y2 + h / 2 + 0.082, "迭代 4 次", fs=8.2,
             color=fs.ACCENT)

    fs.label(ax, 0.5, 0.140, "真正难的不是 PCA，而是“把形状差十倍的动物配准到同一套顶点编号上”",
             fs=9.4, color=fs.INK)
    fs.label(ax, 0.5, 0.070, "配不准，后面所有统计都建立在错位的对应关系上", fs=8.8,
             color=fs.MUTED)
    fs.save(fig, "ch22", "fig22-01")


# ---------------- 图 22-3：跨物种形状空间 ----------------
def fig_shape_space():
    fig = plt.figure(figsize=(6.8, 3.5))
    axL = fig.add_axes([0.085, 0.15, 0.36, 0.70])
    axR = fig.add_axes([0.49, 0.00, 0.50, 0.94])
    axR.axis("off"); axR.set_xlim(0, 1); axR.set_ylim(0, 1)

    rng = np.random.default_rng(7)
    LP = {"猫科": (-2.05, 1.45), "犬科": (0.30, -1.75), "马科": (2.45, 1.60),
          "牛科": (3.00, -0.95), "河马科": (0.45, 2.80)}
    groups = [("猫科", fs.ACCENT, (-1.5, 0.5), 0.40),
              ("犬科", fs.BLUE, (0.4, -0.9), 0.44),
              ("马科", fs.GREEN, (1.5, 0.9), 0.46),
              ("牛科", fs.GOLD, (2.4, -0.3), 0.55),
              ("河马科", fs.PURPLE, (1.0, 1.9), 0.50)]
    for name, c, mu, sd in groups:
        P = rng.normal(mu, sd, (24, 2))
        axL.scatter(P[:, 0], P[:, 1], s=9, color=c, alpha=0.7, linewidths=0)
        tx, ty = LP[name]
        axL.annotate(name, xy=mu, xytext=(tx, ty), fontsize=8.4, color=c,
                     ha="center", va="center",
                     arrowprops=dict(arrowstyle="-", color=c, lw=0.7, alpha=0.6))
    axL.set_xlabel("第一主成分（≈ 整体尺度）", fontsize=8.6, labelpad=2)
    axL.set_ylabel("第二主成分", fontsize=8.6, labelpad=2)
    axL.set_xticks([]); axL.set_yticks([])
    axL.set_xlim(-2.6, 3.6); axL.set_ylim(-2.0, 3.1)
    fs.clean(axL, spines=("left", "bottom"))
    axL.set_title("形状系数：同一个空间里的五个科", fontsize=9.0, color=fs.INK, pad=5)

    specs = [("猫", dict(body=0.72, leg=0.62, neck=16, head=1.10, tail=1.45, arch=0.008, ear=1.4)),
             ("犬", dict(body=0.88, leg=0.85, neck=18, head=1.00, tail=0.95, arch=0.004, ear=1.0)),
             ("马", dict(body=1.02, leg=1.30, neck=44, head=0.92, tail=1.20, arch=-0.006, ear=0.9, necklen=1.5)),
             ("牛", dict(body=1.06, leg=0.80, neck=20, head=1.02, tail=1.10, arch=0.012, ear=1.15)),
             ("河马", dict(body=1.00, leg=0.46, neck=4, head=1.40, tail=0.45, arch=0.018,
                           ear=0.5, muzzle=1.5))]
    ys = [0.860, 0.674, 0.488, 0.302, 0.116]
    for (name, kw), y in zip(specs, ys):
        quad(axR, cx=0.575, cy=y + 0.012, s=0.48, color=fs.INK, z=3, far=False, **kw)
        fs.label(axR, 0.045, y + 0.010, name, fs=9.4, color=fs.MUTED, ha="left")

    axR.plot([1.00, 1.00], [0.03, 0.93], color=fs.GRID, lw=1.0)
    fs.label(axR, 0.50, 0.985, "同一条公式，不同的 $\\beta$", fs=9.2, color=fs.ACCENT,
             weight="bold")
    fs.save(fig, "ch22", "fig22-03")


if __name__ == "__main__":
    fig_skeleton()
    fig_pipeline()
    fig_shape_space()


def fig_registration():
    """图 22-4：配准的能量项与交替优化。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.0))
    for ax in axes:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # 左：能量项怎么拼起来
    ax = axes[0]
    fs.label(ax, 0.5, 0.95, "配准能量 = 四项加权相加", fs=9.4)
    items = [
        ("贴近表面", "点到面的距离最小化，但不指定“对应哪个点”", fs.BLUE),
        ("ARAP 局部刚性", "允许整片旋转，禁止被拉长压扁，细长部位不塌", fs.GREEN),
        ("正则项", "防止顶点整体乱跑：对应关系本身是病态的", fs.PURPLE),
        ("语义 / 初值", "分段刚体先把左右腿摆到正确位置，再谈配准", fs.ACCENT),
    ]
    ys = [0.72, 0.50, 0.28, 0.06]
    for (t, sub, c), y in zip(items, ys):
        fs.box(ax, 0.05, y, 0.90, 0.18, "", fc="white", ec=c, lw=1.1)
        fs.label(ax, 0.09, y + 0.125, t, fs=8.8, color=c, ha="left")
        fs.label(ax, 0.09, y + 0.055, sub, fs=7.6, color=fs.MUTED, ha="left")

    # 右：交替优化
    ax = axes[1]
    fs.label(ax, 0.5, 0.95, "交替优化：局部步与全局步轮流做", fs=9.4)
    fs.box(ax, 0.03, 0.60, 0.44, 0.26,
           "局部步" + "\n" + "固定顶点，闭式解 $\mathbf{R}_i$" + "\n" + "（每顶点一次 3×3 SVD）",
           fc="#EEF2FF", ec=fs.BLUE, fs=7.9)
    fs.box(ax, 0.53, 0.60, 0.44, 0.26,
           "全局步" + "\n" + "固定旋转，解全部顶点" + "\n" + "（大型稀疏线性系统）",
           fc="#ECFDF5", ec=fs.GREEN, fs=7.9)
    fs.arrow(ax, (0.47, 0.755), (0.53, 0.755), color=fs.ACCENT, lw=1.2)
    fs.arrow(ax, (0.53, 0.685), (0.47, 0.685), color=fs.ACCENT, lw=1.2)
    fs.label(ax, 0.5, 0.54, "反复迭代，直到能量不再下降", fs=8.2, color=fs.MUTED)
    fs.label(ax, 0.5, 0.40, "局部步便宜（每个顶点一次小 SVD），", fs=8.2)
    fs.label(ax, 0.5, 0.31, "全局步是一次线性求解，稀疏且可预分解。", fs=8.2)
    fs.box(ax, 0.02, 0.05, 0.96, 0.19,
           "别从“一个球”开始：先分段刚体（头 / 躯干 / 四肢 / 尾）" + "\n" + "再拼回全身，否则两条前腿可能配成一条",
           fc="#FDF6EC", ec=fs.ACCENT, fs=7.7)
    fig.tight_layout()
    fs.save(fig, "ch22", "fig22-04")


if __name__ == "__main__":
    fig_skeleton()
    fig_pipeline()
    fig_shape_space()
    fig_registration()
