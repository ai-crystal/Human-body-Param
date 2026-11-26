# -*- coding: utf-8 -*-
"""第 7 章的自检脚本：把正文里“你应该看到什么”的数字全算一遍。

运行:
    python lab_checks.py

它会打印四组数字，正文中引用的就是这里的输出：
    1) 五个点手算 PCA 的中间量与最终坐标；
    2) 14 点迷你人体的方差比；
    3) 一个顶点的 LBS 手算核对；
    4) 10 个关键点拟合的逐点误差。
"""
import numpy as np
from scipy.optimize import least_squares

RNG = np.random.default_rng(2026)


# ---------- 1. 五个点的 PCA ----------
def five_points():
    X = np.array([[1.0, 1.0], [2.0, 3.0], [3.0, 2.0], [4.0, 5.0], [5.0, 4.0]])
    mu = X.mean(0)
    Xc = X - mu
    C = Xc.T @ Xc / (len(X) - 1)
    w, V = np.linalg.eigh(C)
    idx = np.argsort(w)[::-1]
    w, V = w[idx], V[:, idx]
    z = Xc @ V[:, 0]
    print("== 1. 五个点 ==")
    print("均值:", mu)
    print("协方差:\n", np.round(C, 3))
    print("特征值:", np.round(w, 3), " 方差比:", np.round(100 * w / w.sum(), 1))
    print("第一主方向 (列):", np.round(V[:, 0], 3))
    print("投影坐标 z1:", np.round(z, 2))
    print("只保留 PC1 的重建:\n", np.round(mu + np.outer(z, V[:, 0]), 2))
    rec = mu + np.outer(z, V[:, 0])
    print("逐点重建误差:", np.round(np.linalg.norm(X - rec, axis=1), 3))


# ---------- 2. 迷你人体的方差比 ----------
import demo


def body_space():
    X = demo.sample(400)          # 与 demo.fig_space 一致
    mu, P, w_all = demo.pca(X, 28)
    ratio = 100 * w_all / w_all.sum()
    print("\n== 2. 14 点迷你人体（28 维）==")
    print("前 6 个方差比:", np.round(ratio[:6], 1))
    print("前 3 个累计:", round(float(ratio[:3].sum()), 1))
    print("标准差 sqrt(lambda):", np.round(np.sqrt(w_all[:4]), 4))


# ---------- 3. LBS 手算核对 ----------
def lbs_check():
    elbow = np.array([0.55, 0.30])
    p = np.array([0.91, 0.37])
    th = np.pi / 2
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    only_fore = (p - elbow) @ R.T + elbow
    blended = 0.3 * p + 0.7 * only_fore
    print("\n== 3. LBS 核对（肘弯 90°，权重 0.3/0.7）==")
    print("只随前臂:", np.round(only_fore, 3))
    print("混合结果:", np.round(blended, 3))
    print("到肘距离: 原 %.3f → 新 %.3f（缩短 %.1f%%）"
          % (np.linalg.norm(p - elbow), np.linalg.norm(blended - elbow),
             100 * (1 - np.linalg.norm(blended - elbow) / np.linalg.norm(p - elbow))))


# ---------- 4. 拟合误差 ----------
def fit_check():
    X = demo.sample(300)
    mu, P, w = demo.pca(X, 4)
    truth = demo.BASE.copy()
    truth[0] *= 1.08
    truth[1] *= 0.90
    target = demo.body(truth)
    z, cost, _ = demo.fit(target, mu, P, w)
    pred = (mu + P @ z).reshape(-1, 2)
    err = np.linalg.norm(pred - target, axis=1)
    print("\n== 4. 拟合 10 个关键点 ==")
    print("解出的系数 z:", np.round(z, 3), " 允许范围 ±3σ:", np.round(3 * np.sqrt(w), 3))
    print("逐点误差 (cm, 身高按 1.7 m):", np.round(err * 170, 2))
    print("平均误差: %.2f cm，最大 %.2f cm（第 %d 号点）"
          % (err.mean() * 170, err.max() * 170, int(err.argmax()) + 1))


if __name__ == "__main__":
    five_points()
    body_space()
    lbs_check()
    fit_check()
