# -*- coding: utf-8 -*-
"""第 3 章补充插图：平均值掩盖长尾（图 3-4）。

900 个简单样本 + 100 个困难样本；两种改进方案的均值几乎一样，
但尾部差异巨大：累积误差曲线在 90 分位之后分开。
"""
import sys
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = r"E:\Study\人体参数化技术\人体参数化技术学习\books\recon\images"

rng = np.random.default_rng(7)


def sample(mu_easy, mu_hard, sd_hard):
    easy = rng.normal(40, 8, 900)
    hard = rng.normal(mu_hard, sd_hard, 100)
    x = np.clip(np.concatenate([easy, hard]), 5, None)
    return x


def fig_tail():
    A = sample(40, 200, 40)
    B = sample(40, 150, 30)
    p95 = lambda x: np.percentile(x, 95)

    fig, axs = plt.subplots(1, 2, figsize=(6.9, 3.1))
    fig.subplots_adjust(left=0.075, right=0.975, top=0.84, bottom=0.24, wspace=0.28)

    bins = np.linspace(10, 300, 60)
    ax = axs[0]
    ax.hist(A, bins=bins, color=fs.BLUE, alpha=0.45, label="方案 A")
    ax.hist(B, bins=bins, color=fs.ACCENT, alpha=0.40, label="方案 B")
    ax.set_xlim(10, 300)
    ax.set_xlabel("单样本误差（毫米）", fontsize=8.4)
    ax.set_ylabel("样本数", fontsize=8.4)
    ax.set_title("分布：尾部才是差别所在", fontsize=9.0, pad=6)
    ax.legend(fontsize=7.6, loc="upper right")
    ax.tick_params(labelsize=7.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.annotate("困难样本的 10%", xy=(160, 6), xytext=(150, 60), fontsize=7.4,
                color=fs.MUTED,
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=0.7))

    ax2 = axs[1]
    for x, c, lab in [(A, fs.BLUE, "方案 A"), (B, fs.ACCENT, "方案 B")]:
        xs = np.sort(x)
        ys = np.arange(1, len(xs) + 1) / len(xs) * 100
        ax2.plot(xs, ys, color=c, lw=1.5, label=lab)
    ax2.axhline(90, color=fs.FAINT, lw=0.8, ls=":")
    ax2.set_xlim(10, 300); ax2.set_ylim(0, 101)
    ax2.set_xlabel("误差阈值（毫米）", fontsize=8.4)
    ax2.set_ylabel("落在此阈值内的样本比例（%）", fontsize=8.4)
    ax2.set_title("累积曲线：90 分位之后分开", fontsize=9.0, pad=6)
    ax2.legend(fontsize=7.6, loc="lower right")
    ax2.tick_params(labelsize=7.6)
    for sp in ("top", "right"):
        ax2.spines[sp].set_visible(False)
    ax2.text(20, 92, "90% 分位", fontsize=7.2, color=fs.MUTED)

    fig.text(0.5, 0.075,
             "均值 A = %.1f、B = %.1f 毫米（只差 %.0f%%）；95 分位 A = %.0f、B = %.0f 毫米（差 %.0f%%）"
             % (A.mean(), B.mean(), 100 * (A.mean() / B.mean() - 1),
                p95(A), p95(B), 100 * (p95(A) / p95(B) - 1)),
             fontsize=7.8, color=fs.MUTED, ha="center")
    fs.save(fig, "ch03", "fig03-04")


if __name__ == "__main__":
    fig_tail()
