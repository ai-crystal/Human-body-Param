# -*- coding: utf-8 -*-
"""第 6 章：ASM 训练学到了什么（逐点灰度剖面）——图 6-5。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_profile():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9),
                             gridspec_kw={"width_ratios": [1.0, 1.15]})

    # ---------- 左：法线与采样 ----------
    ax = axes[0]
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    t = np.linspace(0.15, 0.85, 200)
    cx, cy, rx, ry = 0.5, 0.30, 0.34, 0.42
    ang = np.linspace(-0.55, 0.55, 200)
    xs = cx + rx * np.sin(ang)
    ys = cy + ry * np.cos(ang)
    ax.plot(xs, ys, color=fs.INK, lw=2.2)

    i0 = 100
    p = np.array([xs[i0], ys[i0]])
    tan = np.array([xs[i0 + 1] - xs[i0 - 1], ys[i0 + 1] - ys[i0 - 1]])
    tan /= np.linalg.norm(tan)
    nrm = p - np.array([cx, cy])            # 椭圆离心方向 = 朝外
    nrm = nrm / np.linalg.norm(nrm)

    ax.scatter([p[0]], [p[1]], s=26, color=fs.ACCENT, zorder=6)
    fs.arrow(ax, p - 0.02 * nrm, p + 0.13 * tan + 0.02 * nrm, color=fs.BLUE, lw=1.2)
    ax.text(*(p + 0.14 * tan + 0.04 * nrm), "切线", fontsize=8.0, color=fs.BLUE)
    fs.arrow(ax, p, p + 0.22 * nrm, color=fs.GREEN, lw=1.6)
    ax.text(*(p + 0.23 * nrm + 0.02), "法线 $\\mathbf{n}_i$", fontsize=8.4, color=fs.GREEN, va="bottom")

    ax.plot([(p - 0.20 * nrm)[0], (p + 0.24 * nrm)[0]],
            [(p - 0.20 * nrm)[1], (p + 0.24 * nrm)[1]],
            color=fs.FAINT, lw=0.7, ls=":", zorder=1)
    for d in np.linspace(-0.16, 0.20, 9):
        q = p + d * nrm
        ax.plot([q[0] - 0.012 * tan[0], q[0] + 0.012 * tan[0]],
                [q[1] - 0.012 * tan[1], q[1] + 0.012 * tan[1]],
                color=fs.MUTED, lw=0.8)
    ax.text(0.5, 0.05, "沿法线取 $2k+1$ 个灰度（图中 $k=3$）", fontsize=7.8,
            color=fs.MUTED, ha="center")
    ax.set_title("① 每个关键点：切线、法线、采样", fontsize=9.0, pad=2)

    # ---------- 右：训练得到平均剖面 ----------
    ax = axes[1]
    fs.clean(ax, grid=True)
    d = np.arange(-3, 4)
    rng = np.random.default_rng(3)
    base = np.array([0.62, 0.60, 0.58, 0.30, 0.62, 0.66, 0.68])   # 典型“先暗后亮”
    samples = [base + rng.normal(0, 0.06, base.size) for _ in range(8)]
    for s in samples:
        ax.plot(d, s, color="#CBD3DC", lw=0.9, zorder=1)
    mean = np.mean(samples, axis=0)
    sd = np.std(samples, axis=0)
    ax.fill_between(d, mean - sd, mean + sd, color=fs.BLUE, alpha=0.15, zorder=2)
    ax.plot(d, mean, color=fs.BLUE, lw=2.0, marker="o", ms=3, zorder=3)
    ax.axvline(0, color=fs.ACCENT, lw=1.0, ls=":", zorder=2)
    ax.text(0.12, 0.76, "偏移 0 = 当前点", fontsize=7.4, color=fs.ACCENT, va="top")
    ax.set_xlabel("沿法线的偏移 $\\delta$（像素）", fontsize=8.2)
    ax.set_ylabel("灰度（已归一化）", fontsize=8.2)
    ax.set_title("② 训练集学到的平均剖面与方差", fontsize=9.0, pad=2)
    ax.legend(["训练样本", "均值 $\\bar{g}_i$"], fontsize=7.4, frameon=False, loc="lower right")
    ax.tick_params(labelsize=7.6)

    fig.tight_layout(pad=0.5, w_pad=1.0)
    fs.save(fig, "ch06", "fig06-05")


if __name__ == "__main__":
    fig_profile()
