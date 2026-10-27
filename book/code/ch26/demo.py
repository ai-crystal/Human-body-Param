# -*- coding: utf-8 -*-
"""第 26 章配套代码：一个不依赖 SMPL 文件的最小 demo。

运行:
    python ch26_demo.py
会生成 book/images/26/fig26-01.png 与 fig26-02.png
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import figstyle as fs

RNG = np.random.default_rng(2026)


# ---------- 1. 一个 12 个关键点的 2D “人” ----------
def body(params):
    """params: [height, shoulder_w, hip_w, arm_len, leg_len, pose_arm, pose_leg]"""
    h, sw, hw, al, ll, pa, pl = params
    cx = 0.5
    head = np.array([cx, 0.90 * h])
    neck = np.array([cx, 0.80 * h])
    sh_l = np.array([cx - sw / 2, 0.78 * h])
    sh_r = np.array([cx + sw / 2, 0.78 * h])
    hip_l = np.array([cx - hw / 2, 0.50 * h])
    hip_r = np.array([cx + hw / 2, 0.50 * h])
    el_l = sh_l + np.array([-np.sin(pa), -np.cos(pa)]) * al * 0.5
    el_r = sh_r + np.array([np.sin(pa), -np.cos(pa)]) * al * 0.5
    wr_l = el_l + np.array([-np.sin(pa * 1.4), -np.cos(pa * 1.4)]) * al * 0.5
    wr_r = el_r + np.array([np.sin(pa * 1.4), -np.cos(pa * 1.4)]) * al * 0.5
    kn_l = hip_l + np.array([-np.sin(pl), -np.cos(pl)]) * ll * 0.5
    kn_r = hip_r + np.array([np.sin(pl), -np.cos(pl)]) * ll * 0.5
    an_l = kn_l + np.array([0, -1]) * ll * 0.5
    an_r = kn_r + np.array([0, -1]) * ll * 0.5
    return np.array([head, neck, sh_l, sh_r, el_l, el_r, wr_l, wr_r,
                     hip_l, hip_r, kn_l, kn_r, an_l, an_r])


def draw_body(ax, P, color=fs.INK, lw=2.0, alpha=1.0, label=None):
    pairs = [(0, 1), (1, 2), (1, 3), (2, 4), (4, 6), (3, 5), (5, 7),
             (1, 8), (1, 9), (8, 10), (10, 12), (9, 11), (11, 13)]
    for i, j in pairs:
        ax.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]], color=color, lw=lw, alpha=alpha,
                solid_capstyle="round")
    ax.scatter(P[:, 0], P[:, 1], s=14, color=color, alpha=alpha, zorder=4)
    if label:
        fs.label(ax, P[0, 0], P[0, 1] + 0.06, label, fs=8, color=color)


# ---------- 2. 生成数据集并做 PCA ----------
BASE = np.array([1.0, 0.34, 0.26, 0.52, 0.72, 0.25, 0.10])


def sample(n=300):
    P = []
    for _ in range(n):
        q = BASE * (1 + RNG.normal(0, 0.06, size=7))
        q[5] += RNG.normal(0, 0.10)
        q[6] += RNG.normal(0, 0.06)
        P.append(body(q).ravel())
    return np.array(P)


def pca(X, k=3):
    mu = X.mean(0)
    Xc = X - mu
    w, V = np.linalg.eigh(Xc.T @ Xc / (len(X) - 1))
    idx = np.argsort(w)[::-1]
    w, V = w[idx], V[:, idx]
    return mu, V[:, :k], w[:k]


def fig_space():
    X = sample(400)
    mu, P, w = pca(X, 3)
    if P[1, 0] < 0:
        P[:, 0] *= -1
    if P[12, 1] < P[10, 1]:
        P[:, 1] *= -1
    fig, axs = plt.subplots(1, 2, figsize=(6.9, 3.0))
    for ax, k, title in zip(axs, [0, 1], ["第一主成分：整体高矮", "第二主成分：四肢比例"]):
        ax.set_xlim(0.02, 0.98); ax.set_ylim(-0.18, 1.12)
        ax.set_aspect("equal"); ax.axis("off")
        pts = mu.reshape(-1, 2)
        draw_body(ax, pts, color="#D1D5DB", lw=2.4)
        coef = 2 * np.sqrt(w[k])
        for i in range(len(pts)):
            d = coef * P[2 * i:2 * i + 2, k]
            if np.linalg.norm(d) < 0.01:
                continue
            ax.annotate("", xy=pts[i] + d, xytext=pts[i],
                        arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.1, alpha=0.85))
        ax.set_title(title, fontsize=9.2)
    fig.tight_layout()
    fs.save(fig, "ch26", "fig26-01")


# ---------- 3. 从 2D 关键点拟合形状参数 ----------
def fit(target, mu, P, w):
    def resid(z):
        return (mu + P @ z - target.ravel())
    z0 = np.zeros(P.shape[1])
    sol = least_squares(resid, z0, bounds=(-3 * np.sqrt(w), 3 * np.sqrt(w)))
    return sol.x, sol.cost, sol.nfev


def fig_fit():
    X = sample(300)
    mu, P, w = pca(X, 4)
    truth = BASE.copy()
    truth[0] *= 1.08
    truth[1] *= 0.90
    target = body(truth)
    z, cost, nfev = fit(target, mu, P, w)
    pred = (mu + P @ z).reshape(-1, 2)

    fig, axs = plt.subplots(1, 2, figsize=(6.9, 2.8))
    ax = axs[0]
    ax.set_xlim(0.15, 0.85); ax.set_ylim(0.05, 1.02); ax.axis("off"); ax.set_aspect("equal")
    draw_body(ax, target, color=fs.ACCENT, lw=2.2, alpha=0.9)
    draw_body(ax, pred, color=fs.BLUE, lw=2.0, alpha=0.8)
    fs.label(ax, 0.18, 0.98, "橙：目标　蓝：拟合", fs=8.4, color=fs.MUTED, ha="left")
    ax.set_title("拟合结果", fontsize=9)

    ax = axs[1]
    err = np.linalg.norm(pred - target, axis=1)
    fs.clean(ax, grid=True)
    ax.bar(np.arange(len(err)), err * 100, color=fs.BLUE, alpha=0.75)
    ax.set_xlabel("关键点编号"); ax.set_ylabel("误差（cm，假设身高 1.7m）")
    ax.set_title(f"逐点误差：平均 {err.mean()*170:.2f} cm", fontsize=9)
    fig.tight_layout()
    fs.save(fig, "ch26", "fig26-02")


if __name__ == "__main__":
    fig_space()
    fig_fit()
    print("done")
