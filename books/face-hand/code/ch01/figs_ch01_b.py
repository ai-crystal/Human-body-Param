# -*- coding: utf-8 -*-
"""第 1 章补充插图：三种建立稠密对应的做法、系数空间里的先验与损失谷。"""
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "E:/Study/人体参数化技术/人体参数化技术学习/books/code")
import figstyle as fs

fs.FIGDIR = "E:/Study/人体参数化技术/人体参数化技术学习/books/face-hand/images"

W, H = 6.7, 3.55


def fig_correspondence():
    """三种建立稠密对应的做法：人工标点 + 变形、柱面参数化 + 光流、非刚性配准。"""
    fig, ax = fs.canvas(W, H)
    fs.label(ax, 0.5, 0.962, "把第 1000 号顶点钉在“同一个位置”上：三种做法",
             fs=10.2, color=fs.INK, weight="bold")

    cols = [
        (0.030, "① 人工标点 + 全局变形", fs.BLUE,
         "标 30–80 个点\n薄板样条把模板拉过去",
         "快，一张几秒\n整张脸一次到位",
         "点太少，中间靠插值猜\n点标歪了整张脸跟着歪"),
        (0.355, "② 柱面参数化 + 光流", fs.ACCENT,
         "扫描仪输出柱面深度图\n配准退化成二维光流",
         "能直接用二维的\n多分辨率、插值算法",
         "只适用于“能摊平”的扫描\n换台设备就得重写"),
        (0.680, "③ 非刚性配准（模板形变）", fs.GREEN,
         "模板顶点直接对扫描求形变\n加光滑项与关键点约束",
         "精度最高，能处理表情\n4D 序列基本只能这么办",
         "慢，且需要好的初值\n参数调不好会局部翻折"),
    ]
    for x, title, col, how, good, bad in cols:
        fs.box(ax, x, 0.845, 0.29, 0.078, title, ec=col, fs=8.6)
        fs.box(ax, x, 0.560, 0.29, 0.205, "做法\n" + how, ec=fs.FAINT, fs=7.8, lw=0.8)
        fs.box(ax, x, 0.330, 0.29, 0.175, "好处\n" + good, ec=fs.GREEN, fs=7.6, lw=0.8)
        fs.box(ax, x, 0.120, 0.29, 0.160, "代价\n" + bad, ec=fs.ACCENT, fs=7.6, lw=0.8)

    fs.label(ax, 0.5, 0.048,
             "三者目标相同：让“第 i 号顶点”在每张脸上都指同一个解剖位置。对应错了，后面的 PCA 全部失效。",
             fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-03")


def fig_prior_valley():
    """左：系数空间里的先验椭圆与外插点；右：狭长损失谷造成的参数不可辨识。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.25))
    ax = axes[0]
    rng = np.random.default_rng(3)
    A = np.array([[0.030, 0.004], [0.004, 0.012]])
    P = rng.normal(size=(140, 2)) @ A
    ax.scatter(P[:, 0], P[:, 1], s=7, color="#CBD5E1", zorder=2)
    th = np.linspace(0, 2 * np.pi, 240)
    for s, ls, lab in ((1.0, "-", "1σ"), (2.0, "--", "2σ")):
        ell = A @ np.array([np.cos(th), np.sin(th)]) * s
        ax.plot(ell[0], ell[1], color=fs.BLUE, lw=1.0, ls=ls, zorder=3,
                label=lab + " 先验边界")
    ax.scatter([0.108], [0.056], s=46, color=fs.ACCENT, zorder=5, marker="X")
    ax.annotate("无正则的解：\n系数跑出椭圆", xy=(0.104, 0.052), xytext=(-0.125, 0.090),
                fontsize=7.2, color=fs.ACCENT, va="top",
                arrowprops=dict(arrowstyle="->", color=fs.ACCENT, lw=0.9))
    ax.annotate("", xy=(0.061, 0.028), xytext=(0.104, 0.050),
                arrowprops=dict(arrowstyle="->", color=fs.BLUE, lw=1.0, ls=(0, (3, 2))))
    ax.text(-0.125, -0.052, "先验把它拉回边界上\n（虚线箭头）", fontsize=7.2, color=fs.BLUE,
            va="bottom", ha="left")
    ax.set_xlabel("系数 " + r"$\alpha_1$")
    ax.set_ylabel("系数 " + r"$\alpha_2$")
    ax.set_title("系数空间：真人几乎都落在椭圆里", fontsize=9.4, color=fs.INK, pad=8)
    ax.legend(fontsize=7.0, loc="lower right")
    ax.set_xlim(-0.13, 0.135)
    ax.set_ylim(-0.075, 0.115)
    fs.clean(ax, grid=True)

    ax = axes[1]
    xs = np.linspace(-1, 1, 240)
    ys = np.linspace(-1, 1, 240)
    X, Y = np.meshgrid(xs, ys)
    U = (X + Y) / np.sqrt(2)
    V = (Y - X) / np.sqrt(2)
    L = 0.15 * U ** 2 + 3.0 * V ** 2
    cs = ax.contour(X, Y, L, levels=[0.02, 0.08, 0.2, 0.45, 0.9],
                    colors=fs.FAINT, linewidths=0.9)
    ax.clabel(cs, fmt="%.2f", fontsize=6.4, inline=True)
    ax.plot([-0.95, 0.95], [0.95, -0.95], color=fs.ACCENT, lw=1.1, ls=(0, (5, 2)))
    ax.scatter([-0.62, 0.60], [-0.55, 0.68], s=32, color=fs.ACCENT, zorder=5)
    kw = dict(fontsize=7.0, color=fs.ACCENT,
              bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.9))
    ax.annotate("鼻子高 2 mm\n+ 光偏上", xy=(-0.62, -0.55), xytext=(-0.96, -0.96),
                va="bottom", ha="left",
                arrowprops=dict(arrowstyle="->", color=fs.ACCENT, lw=0.8), **kw)
    ax.annotate("鼻子矮 2 mm\n+ 光偏正", xy=(0.60, 0.68), xytext=(0.34, 0.86),
                va="bottom", ha="left",
                arrowprops=dict(arrowstyle="->", color=fs.ACCENT, lw=0.8), **kw)
    ax.set_xlabel("形状参数（鼻高）")
    ax.set_ylabel("光照参数")
    ax.set_title("损失地形：沿虚线的谷底一样好", fontsize=9.4, color=fs.INK, pad=8)
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.16)
    fs.clean(ax)

    fig.tight_layout()
    fs.save(fig, "ch01", "fig01-05")


if __name__ == "__main__":
    fig_correspondence()
    fig_prior_valley()
