# -*- coding: utf-8 -*-
"""第 12 章插图：数据集时间线与评估指标。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_timeline():
    fig, ax = fs.canvas(6.9, 2.5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    items = [(2003, "CAESAR\n体型扫描", ""), (2014, "Human3.6M\n室内动作", ""),
             (2014, "FAUST\n对应基准", ""), (2017, "MPI-INF-3DHP\n野外动作", ""),
             (2018, "3DPW\n野外视频", ""), (2019, "AMASS\n动作统一", "")]
    fs.timeline(ax, items, y=0.50, fs=7.8)
    fs.save(fig, "ch12", "fig12-01")


def fig_metrics():
    fig, axs = plt.subplots(1, 2, figsize=(6.9, 3.1))
    rng = np.random.default_rng(5)
    gt = np.array([[0.2, 0.2], [0.5, 0.75], [0.8, 0.25], [0.35, 0.45], [0.65, 0.45]])
    pred = gt + rng.normal(0, 0.035, gt.shape)
    pred = pred * 1.25 + np.array([0.05, -0.02])   # 尺度与平移偏差

    for ax in axs:
        ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.0); ax.set_aspect("equal"); ax.axis("off")
        ax.scatter(gt[:, 0], gt[:, 1], s=40, color=fs.BLUE, label="真值", zorder=4)
        for i in range(len(gt)):
            for j in range(i + 1, len(gt)):
                ax.plot(gt[[i, j], 0], gt[[i, j], 1], color="#DBEAFE", lw=1.2, zorder=1)
    axs[0].scatter(pred[:, 0], pred[:, 1], s=40, color=fs.ACCENT, marker="x", label="预测", zorder=5)
    for i in range(len(gt)):
        axs[0].plot([gt[i, 0], pred[i, 0]], [gt[i, 1], pred[i, 1]], color=fs.MUTED, lw=0.8, ls=":")
    axs[0].set_title("直接比较：包含尺度/平移误差", fontsize=9.2)
    axs[0].legend(loc="lower left", fontsize=7.5)

    # Procrustes：去尺度、旋转、平移
    A = pred - pred.mean(0); B = gt - gt.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    R = (U @ Vt).T
    scale = S.sum() / (A ** 2).sum()
    aligned = scale * (A @ R.T) + gt.mean(0)
    axs[1].scatter(aligned[:, 0], aligned[:, 1], s=40, color=fs.GREEN, marker="^", label="对齐后", zorder=5)
    for i in range(len(gt)):
        axs[1].plot([gt[i, 0], aligned[i, 0]], [gt[i, 1], aligned[i, 1]], color=fs.MUTED, lw=0.8, ls=":")
    axs[1].set_title("Procrustes 对齐后：只看姿态", fontsize=9.2)
    axs[1].legend(loc="lower left", fontsize=7.5)
    fig.tight_layout()
    fs.save(fig, "ch12", "fig12-02")


def fig_metric_numbers():
    """同一组关节、两种对齐方式：MPJPE 与 PA-MPJPE 差在哪里（配合 12.5 节）。"""
    G = np.array([[0.00, 1.00], [0.00, 1.60], [0.45, 1.35],
                  [-0.45, 1.35], [0.10, 0.00]])      # 真值：骨盆 头 左手 右手 左脚
    A = 0.9 * G + np.array([0.05, 0.02])             # 预测：整体缩小 10% 再平移
    pred = A - A[0] + G[0]                           # 根节点对齐（指标里的第一步）

    p, g = A - A.mean(0), G - G.mean(0)
    U, S, Vt = np.linalg.svd(p.T @ g)
    R = (U @ Vt).T
    s = S.sum() / (p ** 2).sum()
    aligned = s * p @ R.T + G.mean(0)                # 相似变换对齐
    assert np.abs(aligned - G).max() < 1e-9

    bones = [(0, 1), (0, 2), (0, 3), (0, 4)]
    fig, axs = plt.subplots(1, 2, figsize=(6.9, 3.35))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.86, bottom=0.13, wspace=0.06)
    for ax in axs:
        ax.set_xlim(-0.80, 0.80); ax.set_ylim(-0.30, 1.92)
        ax.set_aspect("equal"); ax.axis("off")
        for i, j in bones:
            ax.plot(G[[i, j], 0], G[[i, j], 1], color=fs.BLUE, lw=2.6,
                    solid_capstyle="round", zorder=4)
        ax.scatter(G[:, 0], G[:, 1], s=30, color=fs.BLUE, zorder=6,
                   edgecolor="white", linewidth=0.8)

    # ---- 左：根节点对齐后直接相减 ----
    ax0 = axs[0]
    for i, j in bones:
        ax0.plot(pred[[i, j], 0], pred[[i, j], 1], color=fs.ACCENT, lw=1.8,
                 ls=(0, (4, 2)), zorder=5)
    ax0.scatter(pred[:, 0], pred[:, 1], s=26, color=fs.ACCENT, marker="x",
                linewidth=1.2, zorder=7)
    for k in range(1, 5):
        ax0.plot([G[k, 0], pred[k, 0]], [G[k, 1], pred[k, 1]],
                 color=fs.MUTED, lw=0.8, ls=":", zorder=3)
    ax0.set_title("根节点对齐后直接相减：MPJPE = 54.9 mm", fontsize=9.4, pad=6)
    ax0.text(-0.78, 1.85, "各关节误差：头 60、双手 57、左脚 100（mm）",
             fontsize=8.0, color=fs.MUTED, ha="left")
    ax0.text(0.10, -0.25, "整体缩小 10%，误差随离根节点的距离变大",
             fontsize=8.0, color=fs.ACCENT, ha="center")

    # ---- 右：相似变换对齐后 ----
    ax1 = axs[1]
    for i, j in bones:
        ax1.plot(aligned[[i, j], 0], aligned[[i, j], 1], color=fs.GREEN, lw=5.0,
                 alpha=0.30, solid_capstyle="round", zorder=3)
    ax1.scatter(aligned[:, 0], aligned[:, 1], s=70, color=fs.GREEN, alpha=0.30,
                zorder=4)
    ax1.set_title("相似变换对齐后：PA-MPJPE = 0.0 mm", fontsize=9.4, pad=6)
    ax1.text(-0.78, 1.85, "放大 1.111 倍、摆正后与真值重合",
             fontsize=8.0, color=fs.GREEN, ha="left")
    ax1.text(0.10, -0.25, "尺度、旋转、平移全被吸收，只剩“形状”",
             fontsize=8.0, color=fs.GREEN, ha="center")

    # 关节名（两幅图共用位置）
    tips = [(0.075, 0.905, "骨盆", "left"), (0.10, 1.715, "头", "left"),
            (0.56, 1.30, "左手", "left"), (-0.56, 1.30, "右手", "right"),
            (0.175, -0.035, "左脚", "left")]
    for ax in axs:
        for x, y, t, ha in tips:
            ax.text(x, y, t, fontsize=8.2, color=fs.INK, ha=ha, va="center")

    fig.text(0.5, 0.035,
             "对齐 = 用 SVD 解出最优的 s、R、t（共 7 个自由度），把“摆放”误差全部吸收",
             fontsize=8.2, color=fs.MUTED, ha="center")
    fs.save(fig, "ch12", "fig12-03")


if __name__ == "__main__":
    fig_timeline()
    fig_metrics()
    fig_metric_numbers()
