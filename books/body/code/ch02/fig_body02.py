# -*- coding: utf-8 -*-
"""第 2 章（人体册）插图：SMPL 的五个部件，用官方模型实测

fig02-05  β1 = 1 到底改了多少：逐顶点位移分布 + 关键关节与尺寸的变化
fig02-06  关节回归器：权重有正有负，所以能落到凸包外；且关节位置对 β 严格仿射
fig02-07  一个姿态基干了什么：肘弯 90° 的位移场只出现在肘部附近

模型文件需自行申请，本脚本不含模型。找不到模型时只打印提示，不报错中断。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(os.path.dirname(HERE))          # books/body
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
sys.path.insert(0, HERE)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs
import render_smpl as rs

fs.FIGDIR = os.path.join(BOOK, "images")

CANDIDATES = [
    os.environ.get("SMPL_MODEL", ""),
    r"E:/Study/人体参数化技术/SMPL-test/models/raw/basicModel_m_lbs_10_207_0_v1.0.0.pkl",
    r"E:/Study/人体参数化技术/SMPL-test/models/raw/basicModel_f_lbs_10_207_0_v1.0.0.pkl",
]

JNAMES = ["骨盆", "左髋", "右髋", "腰椎", "左膝", "右膝", "胸椎", "左踝", "右踝",
          "上胸", "左脚", "右脚", "颈", "左锁", "右锁", "头", "左肩", "右肩",
          "左肘", "右肘", "左腕", "右腕", "左手", "右手"]


def load():
    for p in CANDIDATES:
        if p and os.path.exists(p):
            return rs.load_model(p), p
    return None, None


def main():
    m, path = load()
    if m is None:
        print("没有找到 SMPL 模型文件，跳过。设置环境变量 SMPL_MODEL 指向 pkl。")
        return
    V = m["v_template"]
    SD = m["shapedirs"][:, :, 0]
    JR = m["J_regressor"]
    PD = m["posedirs"]
    J0 = JR @ V

    # ---------------- 图 2-5 ----------------
    d = np.linalg.norm(SD, axis=1) * 1000.0            # β1 = 1 的逐顶点位移（毫米）
    dm = np.linalg.norm(SD.mean(axis=0)) * 1000.0      # 全身平均位移（向量平均，示意“整体平移量”）
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1),
                             gridspec_kw={"width_ratios": [1.15, 1.0]})
    ax = axes[0]
    cnt, _, _ = ax.hist(d, bins=60, color=fs.BLUE, alpha=0.75, edgecolor="white", linewidth=0.3)
    top = cnt.max()
    ax.set_ylim(0, top * 1.26)
    ax.axvline(np.median(d), color=fs.INK, lw=1.0, ls=(0, (4, 2)))
    ax.text(np.median(d) - 1.4, top * 1.16, "中位数 %.1f mm" % np.median(d), fontsize=8.4, color=fs.INK, ha="right")
    ax.axvline(d.max(), color=fs.ACCENT, lw=1.0, ls=(0, (4, 2)))
    ax.text(d.max() - 1.4, top * 1.04, "最大 %.1f mm" % d.max(), fontsize=8.4, color=fs.ACCENT, ha="right")
    ax.set_xlabel("单个顶点的位移 $|\\Delta\\mathbf{v}|$（毫米，$\\beta_1=1$）", fontsize=9)
    ax.set_ylabel("顶点数", fontsize=9)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    ax.set_title("① 一个 $\\beta_1$ 单位改了多少", fontsize=9.8, pad=5)

    # 右：几个可读的量随 β1 变化
    ax = axes[1]
    sweep = np.array([-3, -2, -1, 0, 1, 2, 3], float)
    w_shoulder, height, j_disp = [], [], []
    for b in sweep:
        Vb = V + SD * b
        Jb = JR @ Vb
        w_shoulder.append((Jb[16, 0] - Jb[17, 0]) * 1000)
        height.append((Vb[:, 1].max() - Vb[:, 1].min()) * 1000)
        j_disp.append(np.linalg.norm(Jb - J0, axis=1).mean() * 1000)
    ax.plot(sweep, np.array(w_shoulder) - w_shoulder[3], "o-", color=fs.ACCENT, lw=1.3, ms=3.5,
            label="肩宽变化")
    ax.plot(sweep, np.array(height) - height[3], "s-", color=fs.BLUE, lw=1.3, ms=3.2,
            label="身高变化")
    ax.plot(sweep, np.array(j_disp), "^-", color=fs.GREEN, lw=1.3, ms=3.2,
            label="关节平均位移")
    ax.axhline(0, color=fs.FAINT, lw=0.7)
    ax.axvline(0, color=fs.FAINT, lw=0.7)
    ax.set_xlabel("$\\beta_1$（单位：标准差）", fontsize=9)
    ax.set_ylabel("相对 $\\beta_1=0$ 的变化（毫米）", fontsize=9)
    ax.legend(loc="lower left", fontsize=7.8, handlelength=1.5)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    ax.set_title("② 同一个 $\\beta_1$ 对几种量的影响", fontsize=9.8, pad=5)
    fig.tight_layout(pad=0.4, w_pad=1.6)
    fig.text(0.5, -0.02,
             "官方 SMPL 男性模型实测：$\\beta_1=1$ 时最大位移 %.0f 毫米，肩宽变化约 %.1f 毫米，身高变化约 %.1f 毫米"
             % (d.max(), w_shoulder[3] - w_shoulder[4], height[3] - height[4]),
             ha="center", fontsize=8.2, color=fs.MUTED)
    fs.save(fig, "ch02", "fig02-05")

    # ---------------- 图 2-6 ----------------
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0),
                             gridspec_kw={"width_ratios": [1.0, 1.15]})
    ax = axes[0]
    # 示意：表面一圈顶点 + 体内关节，画出几个正负权重
    th = np.linspace(0, 2 * np.pi, 14, endpoint=False)
    pts = np.c_[0.42 * np.cos(th), 0.55 * np.sin(th)]
    ax.plot(np.r_[pts[:, 0], pts[0, 0]], np.r_[pts[:, 1], pts[0, 1]], color=fs.BLUE, lw=0.8, alpha=0.6)
    ax.scatter(pts[:, 0], pts[:, 1], s=14, color="white", edgecolor=fs.BLUE, zorder=4, linewidths=0.9)
    joint = np.array([0.02, 0.06])
    ax.plot(*joint, "o", ms=7, color=fs.ACCENT, zorder=5)
    ax.annotate("关节 $\mathbf{J}$", xy=joint, xytext=(0.26, -0.46), fontsize=9, color=fs.ACCENT, ha="left", arrowprops=dict(arrowstyle="-", color=fs.ACCENT, lw=0.8))
    wts = [0.9, 0.75, 0.5, 0.2, -0.15, -0.3, -0.1, 0.05, 0.3, 0.55, 0.8, 0.95, 0.7, 0.4]
    for p, w in zip(pts, wts):
        col = fs.GREEN if w > 0 else fs.PINK
        ax.annotate("", xy=joint, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=0.5 + 1.6 * abs(w),
                                    alpha=0.85, shrinkA=2, shrinkB=3))
    ax.set_xlim(-0.62, 0.62)
    ax.set_ylim(-0.66, 0.66)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("① 关节 = 顶点的加权和，权重可正可负", fontsize=9.6, pad=5)
    ax.text(0, -0.62, "绿色：正权重　粉色：负权重", ha="center", fontsize=8.0, color=fs.MUTED)

    ax = axes[1]
    for idx, col in [(16, fs.ACCENT), (4, fs.BLUE), (7, fs.GREEN)]:
        xs = np.linspace(-3, 3, 7)
        ys = [(JR @ (V + SD * b))[idx, 1] * 1000 for b in xs]
        ax.plot(xs, ys, "o-", color=col, lw=1.2, ms=3.0, label=JNAMES[idx])
    ax.set_xlabel("$\\beta_1$（标准差）", fontsize=9)
    ax.set_ylabel("关节高度（毫米）", fontsize=9)
    ax.legend(fontsize=8, loc="best", handlelength=1.4)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    ax.set_title("② 关节位置对 $\\beta$ 严格是一条直线", fontsize=9.6, pad=5)
    nnz = (JR > 1e-10).sum(1)
    fig.text(0.5, -0.02, "官方模型实测：$\\mathcal{J}$ 是 $24\\times6890$，每行只有 %d–%d 个非零权重；图上三条直线说明 $\\mathbf{J}=\\mathbf{A}\\boldsymbol{\\beta}+\\mathbf{b}$"
             % (nnz.min(), nnz.max()), ha="center", fontsize=8.2, color=fs.MUTED)
    fig.tight_layout(pad=0.4, w_pad=1.4)
    fs.save(fig, "ch02", "fig02-06")

    # ---------------- 图 2-7 ----------------
    pose = np.zeros((24, 3))
    pose[18, 0] = np.deg2rad(90.0)                     # 左肘
    R = rs.rodrigues(pose.reshape(-1, 3))[18]
    D = np.zeros(207)
    D[(18 - 1) * 9:18 * 9] = (R - np.eye(3)).reshape(9)
    disp = np.einsum("vcn,n->vc", PD, D)
    dn = np.linalg.norm(disp, axis=1) * 1000.0

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.4),
                            gridspec_kw={"width_ratios": [0.92, 1.15]})
    ax = axes[0]
    sc = ax.scatter(V[:, 0] * 1000, V[:, 1] * 1000, c=dn, s=2.4, cmap="YlOrRd",
                    vmin=0, vmax=max(dn.max(), 1e-6), linewidths=0)
    ax.plot(J0[18, 0] * 1000, J0[18, 1] * 1000, "o", ms=6, mfc="none", mec=fs.INK, mew=1.0)
    ax.text(J0[18, 0] * 1000 + 60, J0[18, 1] * 1000, "左肘", fontsize=8.4, color=fs.INK)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("① 肘弯 90° 时的姿态位移（正视）", fontsize=9.6, pad=5)
    cb = fig.colorbar(sc, ax=ax, fraction=0.035, pad=0.01)
    cb.set_label("位移大小（毫米）", fontsize=8)
    cb.ax.tick_params(labelsize=7.5)

    ax = axes[1]
    dist = np.linalg.norm(V - J0[18], axis=1) * 1000.0
    edges = np.linspace(0, min(1200, dist.max()), 25)
    idx = np.digitize(dist, edges) - 1
    mid, hi, lo = [], [], []
    for k in range(len(edges) - 1):
        sel = dn[idx == k]
        if sel.size < 20:
            mid.append(np.nan); hi.append(np.nan); lo.append(np.nan); continue
        mid.append(np.percentile(sel, 50))
        hi.append(np.percentile(sel, 99))
        lo.append(np.percentile(sel, 1))
    xc = (edges[:-1] + edges[1:]) / 2
    ax.scatter(dist, dn, s=1.6, color=fs.FAINT, alpha=0.30, linewidths=0)
    ax.plot(xc, hi, "-", color=fs.ACCENT, lw=1.5, label="99% 分位")
    ax.plot(xc, mid, "-", color=fs.BLUE, lw=1.5, label="中位数")
    ax.plot(xc, lo, "-", color=fs.GREEN, lw=1.2, ls=(0, (4, 2)), label="1% 分位")
    ax.set_xlabel("顶点到左肘的距离（毫米）", fontsize=9)
    ax.set_ylabel("姿态位移大小（毫米）", fontsize=9)
    ax.legend(fontsize=7.8, loc="upper right", handlelength=1.4)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    ax.set_title("② 越靠近肘部越大，但远处并不为零", fontsize=9.6, pad=5)
    ax.set_xlim(0, min(1200, dist.max()))
    fig.tight_layout(pad=0.4, w_pad=1.2)
    fig.text(0.5, -0.02,
             "官方模型实测：这一个姿态基最大 %.1f 毫米、平均 %.2f 毫米，超过 1 毫米的顶点 %d 个（共 6890 个）"
             % (dn.max(), dn.mean(), int((dn > 1).sum())),
             ha="center", fontsize=8.2, color=fs.MUTED)
    fs.save(fig, "ch02", "fig02-07")
    print("model:", path)


if __name__ == "__main__":
    main()
