# -*- coding: utf-8 -*-
"""第 6 章补充插图：紧凑性与泛化性（图 6-6）。

在一组合成的二维轮廓上做 PCA，然后：
  - 紧凑性：前 k 个主成分解释的方差比例；
  - 泛化性：留一法——每次去掉一个样本训练，看它被 k 个主成分重建的误差。
所有数字由本脚本算出并打印，正文引用的是这里的输出。
"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

MATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fs.FIGDIR = os.path.join(MATH, "images")

RNG = np.random.default_rng(7)
N_PT = 10                      # 轮廓点个数（上半圈 + 下半圈）
SIG = np.array([0.06, 0.05, 0.03, 0.02])   # 四个生成方向的标准差
NOISE = 0.002


def base_shape():
    """一个像“脸”的闭合轮廓：上下两条抛物线拼起来。"""
    t = np.linspace(-1, 1, N_PT // 2)
    upper = np.stack([t, 0.62 * (1 - t ** 2)], axis=1)
    lower = np.stack([t[::-1], -0.38 * (1 - t[::-1] ** 2) - 0.12], axis=1)
    return np.vstack([upper, lower])


def modes():
    S = base_shape()
    x, y = S[:, 0], S[:, 1]
    m1 = np.stack([0.55 * x, np.zeros_like(y)], axis=1)         # 宽窄
    m2 = np.stack([np.zeros_like(x), 0.45 * y], axis=1)         # 高矮
    m3 = np.stack([np.zeros_like(x), 0.35 * (y > 0) * y], axis=1)  # 额头
    m4 = np.stack([0.30 * (y < -0.1) * x ** 3, np.zeros_like(y)], axis=1)  # 下巴
    return S, [m1, m2, m3, m4]


def sample(n):
    S, M = modes()
    out = []
    for _ in range(n):
        c = RNG.normal(0, SIG)
        p = S.copy()
        for k in range(4):
            p = p + c[k] * M[k]
        p = p + RNG.normal(0, NOISE, p.shape)
        out.append(p.reshape(-1))
    return np.array(out)


def pca_fit(X, k):
    mu = X.mean(0)
    Xc = X - mu
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    return mu, Vt[:k], (s ** 2) / (len(X) - 1)


def main():
    X = sample(60)
    mu, V, lam = pca_fit(X, X.shape[1])
    comp = np.cumsum(lam) / lam.sum()

    ks = np.arange(1, 11)
    gen = []
    for k in ks:
        err = 0.0
        for i in range(len(X)):
            Xtr = np.delete(X, i, axis=0)
            m, Vk, _ = pca_fit(Xtr, k)
            z = (X[i] - m) @ Vk.T
            rec = m + z @ Vk
            err += np.linalg.norm(X[i] - rec)
        gen.append(err / len(X))
    gen = np.array(gen)

    print("解释方差比例（前 10 个）:", np.round(comp[:10], 3))
    print("留一法平均误差（k=1..10）:", np.round(gen, 4))

    fig, axs = plt.subplots(1, 2, figsize=(6.9, 3.0), gridspec_kw=dict(wspace=0.42))

    ax = axs[0]
    fs.clean(ax, grid=True)
    ax.plot(ks, 100 * comp[:10], "o-", color=fs.BLUE, lw=1.6, ms=4)
    ax.axhline(95, color=fs.FAINT, lw=0.9, ls="--")
    ax.text(6.0, 96.0, "95%", fontsize=8.5, color=fs.MUTED)
    ax.set_xlabel("保留的主成分个数 $k$")
    ax.set_ylabel("累计解释方差（%）")
    ax.set_ylim(50, 102)
    ax.set_title("紧凑性：多少个主成分够用", fontsize=10)

    ax = axs[1]
    fs.clean(ax, grid=True)
    ax.plot(ks, 1000 * gen, "s-", color=fs.ACCENT, lw=1.6, ms=4)
    ax.set_xlabel("保留的主成分个数 $k$")
    ax.set_ylabel("留一法误差（毫米）")
    ax.set_title("泛化性：没见过的人能被重建多准", fontsize=10)
    ax.set_xlim(0.7, 10.3)

    fs.save(fig, "ch06", "fig06-07")


if __name__ == "__main__":
    main()
