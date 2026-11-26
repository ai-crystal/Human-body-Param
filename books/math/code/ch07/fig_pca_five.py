# -*- coding: utf-8 -*-
"""第 7 章插图：五个点上的 PCA，从二维到一维（图 7-3）。

用的就是正文手算的那 5 个点：
    (1,1) (2,3) (3,2) (4,5) (5,4)
均值 (3,3)，协方差 [[2.5,2.0],[2.0,2.5]]，特征值 4.5 与 0.5。
左图画点、均值、两条主方向与投影；右图把投影后的坐标画成一根数轴——
降维之后，5 个二维点变成了 5 个数。脚本把数字打印出来，正文引用这里的输出。
"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figstyle as fs

MATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fs.FIGDIR = os.path.join(MATH, "images")

X = np.array([[1.0, 1.0], [2.0, 3.0], [3.0, 2.0], [4.0, 5.0], [5.0, 4.0]])


def main():
    n = len(X)
    mu = X.mean(0)
    Xc = X - mu
    C = Xc.T @ Xc / (n - 1)
    w, V = np.linalg.eigh(C)
    idx = np.argsort(w)[::-1]
    w, V = w[idx], V[:, idx]
    # 统一符号：第一主成分朝右上，第二主成分朝左上
    if V[0, 0] < 0:
        V[:, 0] *= -1
    if V[0, 1] > 0:
        V[:, 1] *= -1

    z1 = Xc @ V[:, 0]
    z2 = Xc @ V[:, 1]
    print("均值:", mu)
    print("协方差:\n", np.round(C, 3))
    print("特征值:", np.round(w, 3), " 方差比(%):", np.round(100 * w / w.sum(), 1))
    print("主方向:\n", np.round(V, 3))
    print("第一主成分坐标 z1:", np.round(z1, 2))
    print("第二主成分坐标 z2:", np.round(z2, 2))
    print("z1 的方差:", round(z1.var(ddof=1), 3), " z2 的方差:", round(z2.var(ddof=1), 3))

    fig, axs = plt.subplots(1, 2, figsize=(6.9, 3.0),
                            gridspec_kw=dict(width_ratios=[1.25, 1.0], wspace=0.30))

    # ---------- (a) 二维 ----------
    ax = axs[0]
    fs.clean(ax, grid=True)
    ax.set_aspect("equal")
    ax.set_xlim(0.2, 6.0); ax.set_ylim(0.2, 6.0)

    s = np.sqrt(w)                       # 箭头长度 = 一个标准差
    for k, c, lab in ((0, fs.ACCENT, "$\\mathbf{p}_1$"), (1, fs.BLUE, "$\\mathbf{p}_2$")):
        ax.annotate("", xy=mu + s[k] * V[:, k], xytext=mu,
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.6))
        ax.annotate("", xy=mu - s[k] * V[:, k], xytext=mu,
                    arrowprops=dict(arrowstyle="-", color=c, lw=1.2, ls=(0, (4, 3))))
        nrm = np.array([-V[1, k], V[0, k]])          # 法向，用来放标签
        ax.text(*(mu + (s[k] + 0.45) * V[:, k]), lab, color=c, fontsize=9.5,
                ha="center", va="center")

    # 投影到第一主成分
    for i in range(n):
        foot = mu + z1[i] * V[:, 0]
        ax.plot([X[i, 0], foot[0]], [X[i, 1], foot[1]], color=fs.FAINT, lw=0.8, ls=":")
        ax.plot([foot[0]], [foot[1]], "o", ms=3.6, mfc="white", mec=fs.ACCENT, mew=1.0)
        ax.annotate(f"{i+1}", X[i], textcoords="offset points", xytext=(7, 5),
                    fontsize=8.2, color=fs.MUTED)

    ax.scatter(X[:, 0], X[:, 1], s=42, color=fs.INK, zorder=5)
    ax.plot([mu[0]], [mu[1]], marker="X", ms=9, color=fs.GOLD, zorder=6)
    ax.annotate("均值", mu, textcoords="offset points", xytext=(6, -12),
                fontsize=8.2, color=fs.GOLD)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_title("五个点与两条主方向（箭头长 = 一个标准差）", fontsize=9.2, pad=6)

    # ---------- (b) 一维 ----------
    ax = axs[1]
    fs.clean(ax, spines=())
    ax.set_ylim(-1.05, 1.15); ax.set_xlim(-3.6, 3.6)
    ax.set_yticks([]); ax.set_xticks([])
    ax.annotate("", xy=(3.5, 0), xytext=(-3.5, 0),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.1))
    ax.text(3.55, -0.20, "$z_1$", fontsize=9.5, color=fs.MUTED, ha="left")

    seen = {}                      # 同一位置上的点：一个向上标，一个向下标
    for i in range(n):
        z = float(z1[i])
        j = seen.get(round(z, 2), 0)
        seen[round(z, 2)] = j + 1
        sgn = 1 if j == 0 else -1
        ax.plot([z, z], [0, sgn * 0.15], color=fs.ACCENT, lw=1.0)
        ax.plot([z], [0], "o", ms=5.5, color=fs.ACCENT, zorder=4)
        ax.annotate(f"{z:+.2f}", (z, sgn * 0.15), textcoords="offset points",
                    xytext=(0, 6 if sgn > 0 else -13), ha="center",
                    fontsize=8.2, color=fs.ACCENT)
    ax.plot([-np.sqrt(w[0]), np.sqrt(w[0])], [-0.50, -0.50], color=fs.FAINT, lw=0.9)
    for sgn in (-1, 1):
        ax.plot([sgn * np.sqrt(w[0])] * 2, [-0.56, -0.44], color=fs.FAINT, lw=0.9)
    ax.text(0, -0.74, f"$\\pm\\sqrt{{\\lambda_1}}=\\pm{np.sqrt(w[0]):.2f}$（一个标准差）",
            ha="center", fontsize=8.2, color=fs.MUTED)
    ax.set_title(f"投影后：5 个点变成 5 个数（解释 {100*w[0]/w.sum():.0f}% 方差）",
                 fontsize=9.2, pad=6)
    ax.text(0, 1.02, "第二主成分只剩 $\\lambda_2$ = %.2f，占 %.0f%%"
            % (w[1], 100 * w[1] / w.sum()), ha="center", fontsize=8.0, color=fs.BLUE)

    fs.save(fig, "ch07", "fig07-01")


if __name__ == "__main__":
    main()
