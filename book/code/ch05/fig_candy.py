# -*- coding: utf-8 -*-
"""第 5 章新增两图：
   fig05-04 糖纸效应（截面缩小 + 沿肢体的半径曲线）
   fig05-05 LBS 与 DQS 的半径对比
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import figstyle as fs


def fig_candy():
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.0),
                             gridspec_kw={"width_ratios": [1.05, 1.0]})
    ax = axes[0]
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.85, 4.35); ax.set_ylim(-1.05, 1.10)

    cases = [(0.0, "0°"), (90.0, "90°"), (180.0, "180°")]
    for i, (deg, lab) in enumerate(cases):
        cx = i * 1.70
        s = abs(np.cos(np.radians(deg) / 2))
        ax.add_patch(Circle((cx, 0), 0.72, fill=False, ec="#D1D5DB", lw=1.0, ls="--"))
        if s > 0.02:
            ax.add_patch(Circle((cx, 0), 0.72 * s, fill=True, fc=fs.BLUE, alpha=0.22,
                                ec=fs.BLUE, lw=1.4))
        else:
            ax.scatter([cx], [0], s=28, color=fs.ACCENT, zorder=5)
            fs.label(ax, cx, -0.18, "塌成一点", fs=7.6, color=fs.ACCENT, va="top")
        ax.plot([cx - 0.90, cx + 0.90], [0, 0], color="#E5E7EB", lw=0.7, zorder=0)
        fs.label(ax, cx, 0.95, "扭转 " + lab, fs=8.8, color=fs.INK)
        fs.label(ax, cx, -0.92, "半径 %.2f$R$" % s, fs=8.0, color=fs.MUTED)
    ax.set_title(r"权重各半的那个截面（实心）= $\cos(\theta/2)$ 倍", fontsize=9.2,
                 color=fs.BLUE, pad=6)

    # 右：沿肢体方向的半径曲线
    ax = axes[1]
    fs.clean(ax, grid=True)
    s = np.linspace(0, 1, 400)
    w = np.clip((s - 0.3) / 0.4, 0, 1)          # 0.3→0.7 之间权重从 0 线性到 1
    for deg, color, lab in [(90, fs.BLUE, "90°"), (120, fs.GREEN, "120°"), (180, fs.ACCENT, "180°")]:
        th = np.radians(deg)
        r = np.sqrt(np.maximum(0, 1 - 4 * w * (1 - w) * np.sin(th / 2) ** 2))
        ax.plot(s, r, color=color, lw=1.8, label="扭转 " + lab)
    ax.axhline(1.0, color=fs.FAINT, lw=0.8, ls=":")
    ax.set_xlim(0, 1); ax.set_ylim(-0.03, 1.12)
    ax.set_xlabel("沿肢体的位置（0 = 固定端，1 = 扭转端）", fontsize=8.4)
    ax.set_ylabel("截面半径 / 原半径", fontsize=8.4)
    ax.set_title("权重过渡带中间出现一个“腰”", fontsize=9.2)
    # 直接在曲线最低点标注，省掉图例
    for deg, color, dx in [(90, fs.BLUE, 0.02), (120, fs.GREEN, 0.02), (180, fs.ACCENT, 0.02)]:
        y = abs(np.cos(np.radians(deg) / 2))
        ax.annotate("扭转 %d°" % deg, xy=(0.5, y), xytext=(0.5 + dx + 0.03, y + 0.05),
                    fontsize=8.0, color=color)
    ax.tick_params(labelsize=7.8)

    fig.tight_layout(pad=0.5, w_pad=1.2)
    fs.save(fig, "ch05", "fig05-04")


def fig_lbs_vs_dqs():
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    fs.clean(ax, grid=True)
    s = np.linspace(0, 1, 400)
    w = np.clip((s - 0.30) / 0.40, 0, 1)
    th = np.radians(180)
    r_lbs = np.sqrt(np.maximum(0, 1 - 4 * w * (1 - w) * np.sin(th / 2) ** 2))
    ax.plot(s, r_lbs, color=fs.BLUE, lw=2.0, label="LBS：中段半径 → 0（网格自交）")
    ax.plot(s, np.ones_like(s), color=fs.ACCENT, lw=2.0, ls="--",
            label="DQS：只混合旋转，半径保持 1")
    ax.fill_between(s, r_lbs, 1.0, color=fs.BLUE, alpha=0.08)
    ax.annotate("", xy=(0.50, 0.0), xytext=(0.50, 1.0),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9, ls=":"))
    fs.label(ax, 0.53, 0.5, "被“平均”掉的半径", fs=8.2, color=fs.MUTED, ha="left")
    ax.axvline(0.30, color=fs.FAINT, lw=0.8, ls=":")
    ax.axvline(0.70, color=fs.FAINT, lw=0.8, ls=":")
    fs.label(ax, 0.30, 1.06, "纯上臂", fs=7.8, color=fs.MUTED, ha="right")
    fs.label(ax, 0.70, 1.06, "纯前臂", fs=7.8, color=fs.MUTED, ha="left")
    ax.set_xlim(0, 1); ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel("沿肢体的位置", fontsize=8.4)
    ax.set_ylabel("截面半径 / 原半径", fontsize=8.4)
    ax.set_title("扭转 180°：LBS 把腰掐断，DQS 不会", fontsize=9.4)
    ax.legend(fontsize=8.0, frameon=False, loc="lower right")
    ax.tick_params(labelsize=7.8)
    fig.tight_layout(pad=0.5)
    fs.save(fig, "ch05", "fig05-05")


if __name__ == "__main__":
    fig_candy()
    fig_lbs_vs_dqs()
