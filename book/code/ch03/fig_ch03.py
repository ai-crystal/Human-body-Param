# -*- coding: utf-8 -*-
"""第 3 章插图：概率、协方差、PCA。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import figstyle as fs


def fig_mean_var():
    rng = np.random.default_rng(11)
    x = np.array([1.6, 1.9, 2.0, 2.1, 2.15, 2.2, 2.3, 2.4, 2.45, 2.6, 3.4])
    mu, sd = x.mean(), x.std(ddof=1)
    fig, ax = plt.subplots(figsize=(6.6, 2.1))
    ax.set_xlim(1.2, 3.8); ax.set_ylim(-0.5, 1.1); ax.axis("off")
    for i, v in enumerate(x):
        ax.plot([v, v], [0.28, 0.42], color=fs.BLUE, lw=1.0, alpha=0.55)
        ax.scatter([v], [0.35], s=26, color=fs.BLUE, zorder=3)
    ax.annotate("", xy=(mu, 0.62), xytext=(mu, 0.18),
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.6))
    fs.label(ax, mu, 0.70, "均值 $\\mu$", fs=9.5, color=fs.ACCENT)
    ax.annotate("", xy=(mu - sd, 0.12), xytext=(mu + sd, 0.12),
                arrowprops=dict(arrowstyle="<->", color=fs.GREEN, lw=1.1))
    fs.label(ax, mu, 0.02, "标准差 $\\sigma$", fs=9, color=fs.GREEN)
    ax.plot([mu - sd, mu + sd], [0.35, 0.35], color=fs.GREEN, lw=2.4, alpha=0.35)
    ax.text(1.25, 0.92, "同样一批身高数据：均值告诉你“中心在哪”，标准差告诉你“有多分散”",
            fontsize=9.2, color=fs.INK)
    fs.save(fig, "ch03", "fig03-01")


def _ellipse(ax, cov, mean, nstd=2, color=fs.ACCENT, **kw):
    w, v = np.linalg.eigh(cov)
    order = w.argsort()[::-1]
    w, v = w[order], v[:, order]
    ang = np.degrees(np.arctan2(v[1, 0], v[0, 0]))
    for k in range(1, nstd + 1):
        e = Ellipse(mean, 2 * k * np.sqrt(w[0]), 2 * k * np.sqrt(w[1]), angle=ang,
                    fill=False, edgecolor=color, lw=1.0, alpha=0.45 if k > 1 else 0.9, **kw)
        ax.add_patch(e)


def fig_covariance():
    rng = np.random.default_rng(4)
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 3.1))
    cases = [("正相关：$\\rho>0$", np.array([[1, 0.85], [0.85, 1]])),
             ("负相关：$\\rho<0$", np.array([[1, -0.75], [-0.75, 1]]))]
    for ax, (title, C) in zip(axs, cases):
        P = rng.multivariate_normal([0, 0], C, 220)
        ax.scatter(P[:, 0], P[:, 1], s=6, color=fs.BLUE, alpha=0.55, linewidths=0)
        _ellipse(ax, C, [0, 0], 2, fs.ACCENT)
        fs.clean(ax, grid=True)
        ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    fig.tight_layout()
    fs.save(fig, "ch03", "fig03-02")


def fig_pca_axes():
    rng = np.random.default_rng(1)
    C = np.array([[1.0, 0.6], [0.6, 0.7]])
    P = rng.multivariate_normal([0, 0], C, 160)
    P -= P.mean(0)
    w, V = np.linalg.eigh(np.cov(P.T))
    idx = w.argsort()[::-1]; w, V = w[idx], V[:, idx]

    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.scatter(P[:, 0], P[:, 1], s=8, color=fs.BLUE, alpha=0.55, linewidths=0)
    ax.axhline(0, color="#E5E7EB", lw=0.8); ax.axvline(0, color="#E5E7EB", lw=0.8)
    for i, c in enumerate([fs.ACCENT, fs.GREEN]):
        ax.annotate("", xy=V[:, i] * np.sqrt(w[i]) * 2.2, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2))
        fs.label(ax, V[0, i] * np.sqrt(w[i]) * 2.4, V[1, i] * np.sqrt(w[i]) * 2.4,
                 f"$\\mathbf{{p}}_{i+1}$", fs=11, color=c)
    p = P[7]
    proj = (p @ V[:, 0]) * V[:, 0]
    ax.scatter(*p, s=30, color=fs.INK, zorder=5)
    ax.plot([p[0], proj[0]], [p[1], proj[1]], color=fs.MUTED, lw=1.0, ls="--")
    ax.scatter(*proj, s=30, color=fs.ACCENT, zorder=5)
    fs.label(ax, p[0] + 0.1, p[1] + 0.15, "一个样本", fs=8.5, ha="left")
    fs.label(ax, proj[0] - 0.1, proj[1] - 0.3, "它在 $\\mathbf{p}_1$ 上的投影", fs=8.5, ha="left", color=fs.ACCENT)
    fs.clean(ax, grid=False)
    ax.set_aspect("equal"); ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.2, 2.2)
    ax.set_title("PCA 找到方差最大的方向 $\\mathbf{p}_1$，以及与它垂直的 $\\mathbf{p}_2$", fontsize=9.6)
    fig.tight_layout()
    fs.save(fig, "ch03", "fig03-03")


def fig_scree():
    var = np.array([42, 23, 12, 8, 5, 3.5, 2.5, 1.8, 1.2, 0.9, 0.6, 0.5])
    cum = np.cumsum(var) / var.sum() * 100
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    fs.clean(ax, grid=True)
    ax.bar(np.arange(1, len(var) + 1), var, color="#D9B48F", edgecolor="white", width=0.7,
           label="单个主成分解释的方差")
    ax.set_xlabel("主成分编号 k"); ax.set_ylabel("解释方差（%）")
    ax2 = ax.twinx()
    ax2.plot(np.arange(1, len(var) + 1), cum, color=fs.ACCENT, marker="o", ms=3.5, lw=1.5,
             label="累计解释方差")
    ax2.set_ylim(0, 105); ax2.set_ylabel("累计（%）", color=fs.ACCENT)
    ax2.tick_params(axis="y", colors=fs.ACCENT)
    ax2.spines["top"].set_visible(False)
    ax.axvline(5.5, color=fs.BLUE, ls="--", lw=1.0)
    fs.label(ax, 6.2, 33, "保留前 5 个：约 90%", fs=8.5, color=fs.BLUE, ha="left")
    ax.set_title("碎石图：前几个主成分吃掉大部分方差，后面迅速变小", fontsize=10)
    fig.tight_layout()
    fs.save(fig, "ch03", "fig03-04")


def fig_reconstruction():
    rng = np.random.default_rng(8)
    C = np.array([[1.0, 0.8], [0.8, 1.0]])
    P = rng.multivariate_normal([0, 0], C, 90)
    mu = P.mean(0); Q = P - mu
    w, V = np.linalg.eigh(np.cov(Q.T))
    idx = w.argsort()[::-1]; w, V = w[idx], V[:, idx]

    fig, axs = plt.subplots(1, 3, figsize=(6.9, 2.7))
    for ax, k, title in zip(axs, [0, 1, 2], ["k=0：只剩均值", "k=1：沿主轴投影", "k=2：完全重建"]):
        ax.scatter(P[:, 0], P[:, 1], s=6, color="#CBD5E1", alpha=0.7, linewidths=0)
        R = np.tile(mu, (len(P), 1))
        if k >= 1:
            R = R + (Q @ V[:, :k]) @ V[:, :k].T
        ax.scatter(R[:, 0], R[:, 1], s=7, color=fs.ACCENT, alpha=0.8, linewidths=0)
        if k == 1:
            t = np.linspace(-2.6, 2.6, 2)
            ax.plot(mu[0] + V[0, 0] * t, mu[1] + V[1, 0] * t, color=fs.BLUE, lw=1.1, ls="--")
        ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.8, 2.8); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#D1D5DB")
        ax.set_title(title, fontsize=9.5)
    fig.tight_layout()
    fs.save(fig, "ch03", "fig03-05")


def fig_human_pca():
    fig, ax = fs.canvas(6.9, 2.7)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    labels = ["$-2\\sigma$", "$-1\\sigma$", "均值", "$+1\\sigma$", "$+2\\sigma$"]
    widths = [0.78, 0.9, 1.0, 1.12, 1.26]
    for i, (lab, wd) in enumerate(zip(labels, widths)):
        cx = 0.13 + i * 0.185
        fs.human(ax, cx=cx, cy=0.52, s=0.78, width=wd, color="#C9A98F" if i != 2 else fs.ACCENT)
        fs.label(ax, cx, 0.10, lab, fs=9, color=fs.MUTED)
    fs.label(ax, 0.5, 0.94, "第一主成分：体型宽窄", fs=9.6, color=fs.INK)
    fs.label(ax, 0.5, 0.02, "真实模型里，每个主成分都是全身 6890 个顶点的一次协同位移", fs=8.2, color=fs.MUTED)
    fs.save(fig, "ch03", "fig03-06")


if __name__ == "__main__":
    fig_mean_var()
    fig_covariance()
    fig_pca_axes()
    fig_scree()
    fig_reconstruction()
    fig_human_pca()
