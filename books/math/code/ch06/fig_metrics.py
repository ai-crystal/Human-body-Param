# -*- coding: utf-8 -*-
"""第 6 章插图：三条评价曲线（图 6-8）。

与 fig_eval.py 用完全相同的合成数据（同样的种子、同样的生成方向），
额外补上第三个指标——特异性（specificity）：

    从模型里随机采样形状，看它们离训练集有多远。
    太远说明模型能生成训练集里根本不存在的形状。

三个指标都随保留主成分个数 k 变化，脚本把每条曲线的数字打印出来，
正文引用的是这里的输出。
"""
import sys, os
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

MATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fs.FIGDIR = os.path.join(MATH, "images")

RNG = np.random.default_rng(7)
N_PT = 10
SIG = np.array([0.06, 0.05, 0.03, 0.02])
NOISE = 0.002
KS = np.arange(1, 11)


def base_shape():
    t = np.linspace(-1, 1, N_PT // 2)
    upper = np.stack([t, 0.62 * (1 - t ** 2)], axis=1)
    lower = np.stack([t[::-1], -0.38 * (1 - t[::-1] ** 2) - 0.12], axis=1)
    return np.vstack([upper, lower])


def modes():
    S = base_shape()
    x, y = S[:, 0], S[:, 1]
    m1 = np.stack([0.55 * x, np.zeros_like(y)], axis=1)
    m2 = np.stack([np.zeros_like(x), 0.45 * y], axis=1)
    m3 = np.stack([np.zeros_like(x), 0.35 * (y > 0) * y], axis=1)
    m4 = np.stack([0.30 * (y < -0.1) * x ** 3, np.zeros_like(y)], axis=1)
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


def specificity(mu, Vk, lam, X, n_gen=300, seed=11):
    """从模型采样，量它们离训练集最近的样本有多远（平均）。"""
    rng = np.random.default_rng(seed)
    k = Vk.shape[0]
    sd = np.sqrt(lam[:k])
    z = rng.normal(size=(n_gen, k)) * sd
    z = np.clip(z, -3 * sd, 3 * sd)   # 与拟合时的 ±3σ 一致
    G = mu + z @ Vk
    d2 = ((G[:, None, :] - X[None, :, :]) ** 2).sum(-1)
    return np.sqrt(d2.min(1)).mean()


def main():
    X = sample(60)
    mu, V, lam = pca_fit(X, X.shape[1])
    comp = np.cumsum(lam) / lam.sum()

    gen, spec = [], []
    for k in KS:
        err = 0.0
        for i in range(len(X)):
            m, Vk, _ = pca_fit(np.delete(X, i, axis=0), k)
            z = (X[i] - m) @ Vk.T
            err += np.linalg.norm(X[i] - (m + z @ Vk))
        gen.append(err / len(X))

        m, Vk, lk = pca_fit(X, k)
        spec.append(specificity(m, Vk, lk, X))

    gen = np.array(gen)
    spec = np.array(spec)

    print("紧凑性 累计解释方差 (%):", np.round(100 * comp[:10], 1))
    print("泛化性 留一误差 (mm)     :", np.round(1000 * gen, 1))
    print("特异性 生成样本到数据 (mm):", np.round(1000 * spec, 1))

    fig, axs = plt.subplots(1, 2, figsize=(6.9, 3.0), gridspec_kw=dict(wspace=0.40))

    # ---- (a) 特异性单独一条：随 k 上升 ----
    ax = axs[0]
    fs.clean(ax, grid=True)
    ax.plot(KS, 1000 * spec, "^-", color=fs.GREEN, lw=1.6, ms=4.5)
    ax.set_xlabel("保留的主成分个数 $k$")
    ax.set_ylabel("生成样本到最近训练样本（毫米）")
    ax.set_title("特异性：模型能“编”出多离谱的形状", fontsize=9.6, pad=8)
    for k, dx, dy in ((1, 13, 4), (4, 0, 10), (10, 0, -13)):
        ax.annotate(f"{1000*spec[k-1]:.1f}", (k, 1000 * spec[k - 1]),
                    textcoords="offset points", xytext=(dx, dy),
                    ha="center", fontsize=8.2, color=fs.GREEN)
    ax.set_xlim(0.6, 10.4)
    ax.set_ylim(14.2, 21.4)

    # ---- (b) 三条曲线归一化后同轴对照 ----
    ax = axs[1]
    fs.clean(ax, grid=True)
    gap = 1 - comp[:10]                       # 重建缺口：越小越好
    norm = lambda v: (v - v.min()) / (v.max() - v.min() + 1e-12)
    ax.plot(KS, norm(gap), "o-", color=fs.BLUE, lw=1.5, ms=4, label="紧凑性（1 − 解释方差）")
    ax.plot(KS, norm(gen), "s-", color=fs.ACCENT, lw=1.5, ms=4, label="泛化性（留一误差）")
    ax.plot(KS, norm(spec), "^-", color=fs.GREEN, lw=1.5, ms=4, label="特异性（采样离群）")
    ax.axvline(4, color=fs.GOLD, lw=1.0, ls="--", zorder=1)
    ax.text(4.12, 1.10, "$k=4$：紧凑性与泛化性从此变平", fontsize=8.2, color=fs.GOLD,
            ha="left", va="center")
    ax.set_xlabel("保留的主成分个数 $k$")
    ax.set_ylabel("各自归一化（0 = 该项最好）")
    ax.set_ylim(-0.06, 1.20)
    ax.set_xlim(0.6, 10.4)
    leg = ax.legend(loc="center left", bbox_to_anchor=(0.24, 0.42), fontsize=7.8)
    leg.get_frame().set_facecolor("white")
    leg.get_frame().set_alpha(0.95)
    leg.get_frame().set_edgecolor("#E5E7EB")
    ax.set_title("三条曲线一起读：谁定 $k$，谁做体检", fontsize=9.6, pad=8)

    fig.subplots_adjust(left=0.11, right=0.98, top=0.88, bottom=0.17, wspace=0.40)
    fs.save(fig, "ch06", "fig06-08")


if __name__ == "__main__":
    main()
