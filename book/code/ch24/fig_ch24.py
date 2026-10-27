# -*- coding: utf-8 -*-
"""第 24 章插图：跨物种——鸟类、鱼类与动物生成。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, Wedge
import figstyle as fs


# ---------------- 三种拓扑的剪影 ----------------
def bird(ax, cx=0.5, cy=0.5, s=1.0, color=fs.INK, alpha=1.0, z=3, joints=False,
         jcolor=fs.ACCENT, fold=1.0):
    """侧视鸟：躯干 + 颈 + 头喙 + 折起的翅 + 两条腿 + 尾羽。"""
    body = np.array([cx, cy])
    ax.add_patch(Ellipse(body, 0.185 * s, 0.125 * s, angle=-6, facecolor=color,
                         alpha=alpha, edgecolor="none", zorder=z))
    # 尾羽（先画，压在躯干后面）
    for a in (-10, 0, 10):
        d = np.radians(184 + a)
        p0 = body + np.array([-0.070 * s, 0.004 * s])
        p1 = p0 + np.array([np.cos(d), np.sin(d)]) * 0.078 * s
        ax.add_patch(Polygon([p0, p1 + np.array([0.004 * s, 0.011 * s]),
                              p1 + np.array([0.004 * s, -0.011 * s])],
                             closed=True, facecolor=color, alpha=alpha * 0.85,
                             edgecolor="none", zorder=z - 1))
    # 颈 + 头 + 喙
    nb = body + np.array([0.058 * s, 0.056 * s])
    hp = nb + np.array([0.028 * s, 0.080 * s])
    fs.limb(ax, nb, hp, 0.046 * s, 0.034 * s, color=color, alpha=alpha, z=z + 1)
    ax.add_patch(Circle(hp + np.array([0.008 * s, 0.006 * s]), 0.029 * s,
                        facecolor=color, alpha=alpha, edgecolor="none", zorder=z + 2))
    ax.add_patch(Polygon([hp + np.array([0.028 * s, 0.008 * s]),
                          hp + np.array([0.080 * s, 0.002 * s]),
                          hp + np.array([0.028 * s, -0.008 * s])],
                         closed=True, facecolor=color, alpha=alpha, edgecolor="none",
                         zorder=z + 2))
    # 折起的翅：肩 → 肘 → 腕（贴着躯干）
    w0 = body + np.array([0.018 * s, 0.010 * s])
    w1 = w0 + np.array([-0.105 * s, -0.036 * s * fold])
    w2 = w1 + np.array([0.050 * s, -0.030 * s * fold])
    wc = "#4B5563"
    fs.limb(ax, w0, w1, 0.080 * s, 0.046 * s, color=wc, alpha=alpha, z=z + 2)
    fs.limb(ax, w1, w2, 0.044 * s, 0.022 * s, color=wc, alpha=alpha, z=z + 2)
    # 腿 + 爪
    for dx, sw in ((-0.020, -4), (0.030, 4)):
        h0 = body + np.array([dx * s, -0.058 * s])
        k = h0 + np.array([0.008 * s, -0.062 * s])
        f = k + np.array([sw * 0.002 * s, -0.055 * s])
        fs.limb(ax, h0, k, 0.022 * s, 0.016 * s, color=color, alpha=alpha, z=z - 1)
        fs.limb(ax, k, f, 0.016 * s, 0.012 * s, color=color, alpha=alpha, z=z - 1)
        ax.add_patch(Polygon([f + np.array([-0.016 * s, 0.006 * s]),
                              f + np.array([0.030 * s, 0.006 * s]),
                              f + np.array([0.004 * s, -0.008 * s])],
                             closed=True, facecolor=color, alpha=alpha, edgecolor="none",
                             zorder=z - 1))
    if joints:
        for p in (body, nb, hp, w0, w1, w2):
            ax.add_patch(Circle(p, 0.008, facecolor=jcolor, edgecolor="white", lw=0.7,
                                zorder=z + 5))
    return dict(body=body, head=hp, wing_tip=w2)


def fish(ax, cx=0.5, cy=0.5, s=1.0, color=fs.INK, alpha=1.0, z=3, joints=False,
         jcolor=fs.ACCENT):
    """侧视鱼：纺锤形躯干 + 尾鳍 + 背鳍 + 胸鳍，附一条脊柱曲线。"""
    t = np.linspace(0, 2 * np.pi, 200)
    x = cx + 0.135 * s * np.cos(t)
    y = cy + 0.062 * s * np.sin(t) * (1 - 0.25 * np.cos(t)) * 1.05
    ax.add_patch(Polygon(np.stack([x, y], axis=1), closed=True, facecolor=color,
                         alpha=alpha, edgecolor="none", zorder=z))
    # 尾鳍
    tf = cx - 0.128 * s
    ax.add_patch(Polygon([(tf, cy), (tf - 0.075 * s, cy + 0.062 * s),
                          (tf - 0.028 * s, cy), (tf - 0.075 * s, cy - 0.062 * s)],
                         closed=True, facecolor=color, alpha=alpha * 0.9,
                         edgecolor="none", zorder=z - 1))
    # 背鳍
    ax.add_patch(Polygon([(cx - 0.030 * s, cy + 0.055 * s), (cx + 0.030 * s, cy + 0.052 * s),
                          (cx - 0.005 * s, cy + 0.120 * s)],
                         closed=True, facecolor=color, alpha=alpha * 0.9,
                         edgecolor="none", zorder=z - 1))
    # 胸鳍
    ax.add_patch(Polygon([(cx + 0.030 * s, cy - 0.020 * s), (cx + 0.072 * s, cy - 0.030 * s),
                          (cx + 0.020 * s, cy - 0.070 * s)],
                         closed=True, facecolor=color, alpha=alpha * 0.8,
                         edgecolor="none", zorder=z + 1))
    ax.add_patch(Circle((cx + 0.088 * s, cy + 0.014 * s), 0.010 * s, facecolor="white",
                        edgecolor="none", zorder=z + 2))
    # 脊柱
    xs = np.linspace(cx + 0.115 * s, cx - 0.120 * s, 40)
    ax.plot(xs, cy + 0.012 * s * np.sin((xs - cx) / (0.06 * s)), color="white",
            lw=1.0, alpha=0.55, zorder=z + 3, ls=(0, (3, 2)))
    if joints:
        for p in ((cx + 0.10 * s, cy), (cx, cy), (cx - 0.12 * s, cy)):
            ax.add_patch(Circle(p, 0.008, facecolor=jcolor, edgecolor="white", lw=0.7,
                                zorder=z + 5))


def quad_simple(ax, cx=0.5, cy=0.5, s=1.0, color=fs.INK, alpha=1.0, z=3, joints=False,
                jcolor=fs.ACCENT):
    """四足：躯干胶囊 + 四条腿 + 颈头 + 尾（与第 22 章同构的简化版）。"""
    L, H = 0.215 * s, 0.095 * s
    hip = np.array([cx - L / 2, cy + 0.010 * s])
    sho = np.array([cx + L / 2, cy + 0.016 * s])
    fs.limb(ax, hip, sho, H, H * 0.92, color=color, alpha=alpha, z=z)
    legs = []
    for base, ang0, ang1 in ((sho, 6, -4), (hip, -6, 4)):
        p0 = base + np.array([0, -H * 0.35])
        a0, a1 = np.radians(ang0), np.radians(ang1)
        p1 = p0 + np.array([np.sin(a0), -np.cos(a0)]) * 0.105 * s
        p2 = p1 + np.array([np.sin(a1), -np.cos(a1)]) * 0.100 * s
        fs.limb(ax, p0, p1, 0.030 * s, 0.024 * s, color=color, alpha=alpha, z=z)
        fs.limb(ax, p1, p2, 0.024 * s, 0.018 * s, color=color, alpha=alpha, z=z)
        ax.add_patch(Ellipse(p2 + np.array([0.008 * s, -0.006 * s]), 0.040 * s, 0.018 * s,
                             facecolor=color, alpha=alpha, edgecolor="none", zorder=z))
        legs += [p0, p1, p2]
    nb = sho + np.array([0.006 * s, H * 0.26])
    hp = nb + np.array([0.032 * s, 0.092 * s])
    fs.limb(ax, nb, hp, 0.045 * s, 0.038 * s, color=color, alpha=alpha, z=z)
    ax.add_patch(Ellipse(hp + np.array([0.014 * s, 0.012 * s]), 0.070 * s, 0.052 * s,
                         angle=16, facecolor=color, alpha=alpha, edgecolor="none",
                         zorder=z + 1))
    ax.add_patch(Polygon([hp + np.array([0.040 * s, -0.004 * s]),
                          hp + np.array([0.078 * s, -0.012 * s]),
                          hp + np.array([0.040 * s, -0.020 * s])],
                         closed=True, facecolor=color, alpha=alpha, edgecolor="none",
                         zorder=z + 1))
    tb = hip + np.array([-0.008 * s, H * 0.24])
    t1 = tb + np.array([-0.062 * s, 0.028 * s])
    fs.limb(ax, tb, t1, 0.026 * s, 0.014 * s, color=color, alpha=alpha, z=z)
    if joints:
        for p in [hip, sho, nb, hp, tb] + legs:
            ax.add_patch(Circle(p, 0.008, facecolor=jcolor, edgecolor="white", lw=0.7,
                                zorder=z + 5))


# ---------------- 图 24-1：三种拓扑 ----------------
def fig_topo():
    fig, ax = fs.canvas(6.8, 3.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    quad_simple(ax, cx=0.175, cy=0.615, s=0.86, joints=True)
    bird(ax, cx=0.500, cy=0.605, s=0.86, joints=True)
    fish(ax, cx=0.805, cy=0.615, s=0.92, joints=True)

    for x, t in ((0.175, "四足（SMAL）"), (0.500, "鸟类"), (0.805, "鱼类")):
        fs.label(ax, x, 0.880, t, fs=9.4, color=fs.INK, weight="bold")

    notes = [(0.175, "33 个关节\n一条脊柱 + 四条腿 + 尾\n可以为“同科”共用一套拓扑"),
             (0.50, "翅 = 前肢，多一段“腕掌”\n喙与尾羽没有对应骨骼\n没有公认的统一模型"),
             (0.80, "没有四肢，没有关节\n身体靠脊柱连续弯曲\n“蒙皮”退化为整体形变")]
    for x, t in notes:
        fs.label(ax, x, 0.215, t, fs=8.4, color=fs.MUTED)

    ax.plot([0.335, 0.335], [0.300, 0.470], color=fs.GRID, lw=0.9)
    ax.plot([0.665, 0.665], [0.300, 0.470], color=fs.GRID, lw=0.9)
    fs.label(ax, 0.500, 0.055,
             "同一个问题在不同拓扑上要重新回答：哪一段是“刚体”，哪一段是“连续形变”？",
             fs=9.0, color=fs.ACCENT)
    fs.save(fig, "ch24", "fig24-01")


# ---------------- 图 24-2：形状空间的外插 ----------------
def fig_extrapolate():
    fig = plt.figure(figsize=(6.8, 3.4))
    axL = fig.add_axes([0.04, 0.10, 0.42, 0.74])
    axL.set_xlim(-2.4, 3.0); axL.set_ylim(-1.8, 2.0)
    axL.set_xticks([]); axL.set_yticks([])
    fs.clean(axL, spines=("left", "bottom"))
    axL.set_xlabel("形状参数 β 的方向 1（示意）", fontsize=8.4)
    axL.set_ylabel("方向 2", fontsize=8.4)

    th = np.linspace(0, 2 * np.pi, 200)
    hull = np.stack([0.9 + 1.35 * np.cos(th), 0.6 + 0.85 * np.sin(th)], axis=1)
    axL.add_patch(Polygon(hull, closed=True, facecolor=fs.BLUE, alpha=0.08,
                          edgecolor=fs.BLUE, lw=1.0, ls=(0, (4, 3))))
    rng = np.random.default_rng(3)
    P = rng.normal([0.9, 0.6], [0.55, 0.35], (22, 2))
    axL.scatter(P[:, 0], P[:, 1], s=12, color=fs.BLUE, alpha=0.7, linewidths=0)
    fs.label(axL, 0.55, 1.62, "训练集覆盖的 β 范围\n（狮、虎、狗、马、牛、河马）",
             fs=8.2, color=fs.BLUE)

    tx, ty = 2.15, -1.05
    axL.scatter([tx], [ty], s=48, marker="*", color=fs.ACCENT, zorder=5)
    fs.label(axL, tx - 0.05, ty - 0.26, "目标物种在包外\n（长颈鹿、大象、鲸）",
             fs=8.2, color=fs.ACCENT)
    fs.arrow(axL, (1.55, 0.10), (tx - 0.16, ty + 0.16), color=fs.ACCENT, lw=1.1,
             ls=(0, (4, 2)))
    fs.label(axL, 1.95, 0.22, "外插", fs=8.4, color=fs.ACCENT)
    axL.set_title("问题：目标物种不在训练集里", fontsize=9.2, color=fs.INK, pad=4)

    axR = fig.add_axes([0.50, 0.02, 0.49, 0.92])
    axR.set_xlim(0, 1); axR.set_ylim(0, 1); axR.axis("off")
    routes = [("① 类别级重训", "为这个科单独建一套形状空间\n数据少，容易过拟合", fs.BLUE, 0.720),
              ("② 逐实例位移场", "保留模板与关节，让顶点自由偏离\n能走出线性空间，但要多视图", fs.GREEN, 0.440),
              ("③ 学出来的先验", "从图像集合学“这类动物怎么动”\n不需要 3D 真值，需要大量图", fs.ACCENT, 0.160)]
    for t, sub, c, y in routes:
        fs.box(axR, 0.02, y - 0.075, 0.96, 0.150, "", fc="white", ec=c, lw=1.0)
        fs.label(axR, 0.055, y + 0.042, t, fs=8.8, color=c, ha="left", weight="bold")
        fs.label(axR, 0.055, y - 0.033, sub, fs=7.8, color=fs.MUTED, ha="left")
    fs.label(axR, 0.50, 0.955, "三条补救路径，代价各不相同", fs=9.2, color=fs.INK)
    fs.save(fig, "ch24", "fig24-02")


# ---------------- 图 24-3：从静态到 4D 的四级台阶 ----------------
def fig_ladder():
    fig, ax = fs.canvas(6.8, 3.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    steps = [("L1　单图 → 静态网格", "轮廓 + 关键点 + 形状先验", "SMALST / BARC / AniMer", 0.115, fs.BLUE),
             ("L2　多视图 → 更准的形状", "同一只动物的多张图、光度一致", "SMALR / 3D-Fauna", 0.315, fs.GREEN),
             ("L3　视频 → 4D：形状与运动", "时序、光流、关节轨迹", "BARC / LiveStock 一类流水线", 0.515, fs.PURPLE),
             ("L4　生成 → 任意物种与动作", "大规模图文 / 视频先验，弱监督", "扩散模型 + 参数化骨架", 0.715, fs.ACCENT)]
    h, w = 0.130, 0.400
    for t, sup, meth, y, c in steps:
        fs.box(ax, 0.040, y, w, h, t, fc="white", ec=c, fs=8.6, lw=1.1)
        fs.label(ax, 0.470, y + h * 0.68, sup, fs=8.2, color=fs.MUTED, ha="left")
        fs.label(ax, 0.470, y + h * 0.26, meth, fs=8.2, color=c, ha="left")
    for y in (0.115, 0.315, 0.515):
        fs.arrow(ax, (0.140, y + h + 0.004), (0.140, y + 0.200 - 0.004), color=fs.FAINT)
    fs.label(ax, 0.040, 0.950, "每上一级，都要多一类信息", fs=9.4, color=fs.INK, ha="left")
    fs.label(ax, 0.040, 0.045, "越往上，越依赖“先验”而不是“真值”；标注越少，先验要求越高",
             fs=9.0, color=fs.MUTED, ha="left")
    fs.save(fig, "ch24", "fig24-03")



def fig_gait():
    """图 24-4：步态相位与两类接触错误。"""
    fig = plt.figure(figsize=(6.9, 3.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.45, 1.0], hspace=0.32)

    # ---- 上：三种步态的四足着地时序 ----
    ax = fig.add_subplot(gs[0])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    gaits = [
        ("行走 walk", [[0.00, 0.30], [0.25, 0.55], [0.50, 0.80], [0.75, 1.00]]),
        ("小跑 trot", [[0.00, 0.45], [0.50, 0.95], [0.50, 0.95], [0.00, 0.45]]),
        ("袭步 gallop", [[0.00, 0.30], [0.12, 0.42], [0.45, 0.75], [0.58, 0.88]]),
    ]
    ys = [0.78, 0.47, 0.16]
    for (name, segs), y0 in zip(gaits, ys):
        fs.label(ax, 0.0, y0 + 0.142, name, fs=8.0, color=fs.MUTED, ha="left")
        for j, seg in enumerate(segs):
            y = y0 + 0.075 - j * 0.052
            ax.plot([0, 1], [y, y], color="#E8EAED", lw=3.2, solid_capstyle="butt", zorder=1)
            ax.plot(seg, [y, y], color=fs.ACCENT if j % 2 == 0 else fs.BLUE,
                    lw=3.2, solid_capstyle="butt", zorder=2)
    fs.label(ax, 1.0, 0.98, "每段四行自上而下：左前 / 右前 / 左后 / 右后", fs=7.2,
             color=fs.MUTED, ha="right")
    fs.label(ax, 0.5, 0.00, "横轴＝一个周期；深色段＝该足着地（示意，不按真实时长比例）", fs=7.8,
             color=fs.MUTED)

    # ---- 下：脚滑 与 穿地 ----
    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis("off")
    for x0, x1, tag in [(0.04, 0.46, "脚滑：着地时位置在变"), (0.54, 0.96, "穿地：脚陷进地里")]:
        ax2.plot([x0, x1], [0.42, 0.42], color=fs.INK, lw=1.6)
        for xx in np.arange(x0, x1, 0.045):
            ax2.plot([xx, xx - 0.02], [0.42, 0.35], color=fs.FAINT, lw=0.8)
        fs.label(ax2, (x0 + x1) / 2, 0.10, tag, fs=8.4, color=fs.MUTED)

    ax2.plot([0.14, 0.14], [0.42, 0.62], color=fs.BLUE, lw=3.0, solid_capstyle="round")
    ax2.plot([0.28, 0.28], [0.42, 0.62], color=fs.BLUE, lw=3.0, solid_capstyle="round", alpha=0.45)
    fs.arrow(ax2, (0.16, 0.70), (0.26, 0.70), color=fs.ACCENT, lw=1.1)
    fs.label(ax2, 0.21, 0.80, "着地期间位移应≈0", fs=7.8, color=fs.ACCENT)

    ax2.plot([0.62, 0.62], [0.42, 0.62], color=fs.BLUE, lw=3.0, solid_capstyle="round")
    ax2.plot([0.72, 0.72], [0.26, 0.62], color=fs.PURPLE, lw=3.0, solid_capstyle="round")
    ax2.plot([0.69, 0.75], [0.26, 0.26], color=fs.PURPLE, lw=2.0)
    fs.label(ax2, 0.76, 0.24, "z < 0", fs=7.8, color=fs.PURPLE, ha="left")
    fs.save(fig, "ch24", "fig24-04")


if __name__ == "__main__":
    fig_topo()
    fig_extrapolate()
    fig_ladder()
    fig_gait()
