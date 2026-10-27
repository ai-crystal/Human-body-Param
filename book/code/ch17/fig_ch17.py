# -*- coding: utf-8 -*-
"""第 17 章插图：高保真人脸——细节、纹理与身份。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import figstyle as fs

W = 6.7


def fig_frequency():
    fig, ax = fs.new(W, 3.5)
    ax.set_xlim(0.02, 12.0)
    ax.set_ylim(0, 1.0)
    fs.clean(ax, spines=("left", "bottom"))

    f = np.linspace(0.05, 12, 600)
    amp = 1.0 / (1.0 + f ** 0.95)
    ax.fill_between(f, 0, amp, color="#EEF2F7", zorder=1)
    ax.plot(f, amp, color=fs.INK, lw=1.6, zorder=4)

    bands = [(0.05, 1.0, "#DBEAFE", "低频", "脸型、胖瘦、比例"),
             (1.0, 4.0, "#EDE9FE", "中频", "皱纹、眼袋"),
             (4.0, 12.0, "#FEE2E2", "高频", "毛孔、皮肤纹理")]
    for x0, x1, col, name, sub in bands:
        ax.axvspan(x0, x1, color=col, alpha=0.75, zorder=0, lw=0)
        xc = np.sqrt(x0 * x1)
        ax.text(min(max(xc, 0.16), 8.0), 0.92, name, ha="center", fontsize=9.5,
                color=fs.INK, weight="bold")
        ax.text(min(max(xc, 0.18), 6.5), 0.84, sub, ha="center", fontsize=8.0, color=fs.MUTED)

    ax.axvline(1.0, color=fs.BLUE, lw=1.1, ls=(0, (4, 2)), zorder=5)
    ax.annotate("", xy=(0.06, 0.130), xytext=(0.97, 0.130),
                arrowprops=dict(arrowstyle="<->", color=fs.BLUE, lw=1.2))
    ax.text(np.sqrt(0.06 * 0.97), 0.058, "线性 PCA 模型能覆盖的部分",
            ha="center", fontsize=8.4, color=fs.BLUE,
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.6))
    ax.annotate("", xy=(1.05, 0.130), xytext=(11.6, 0.130),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=1.2))
    ax.text(np.sqrt(1.05 * 11.6), 0.058, "需要位移图 / 生成网络接力",
            ha="center", fontsize=8.4, color=fs.ACCENT,
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.6))

    ax.set_xscale("log")
    ax.set_xlabel("空间频率（每厘米起伏次数，对数刻度）")
    ax.set_ylabel("该频率上的起伏幅度")
    ax.set_yticks([])
    ax.set_xticks([0.1, 0.3, 1, 3, 10])
    ax.set_xticklabels(["0.1", "0.3", "1", "3", "10"])
    ax.set_title("人脸几何的“频谱”：越细的变化幅度越小，但数量越多", fontsize=10.2, pad=8)
    fig.tight_layout()
    fs.save(fig, "ch17", "fig17-01")


def fig_hybrid():
    fig, ax = fs.canvas(W, 3.55)

    # 左：大规模低精度
    fs.box(ax, 0.025, 0.735, 0.30, 0.195,
           "大规模 · 低精度\n消费级深度相机，5–10 秒 / 人\n例：6 万帧 RGB-D",
           fc="#EFF6FF", ec=fs.BLUE, fs=7.8, lw=1.0)
    fs.arrow(ax, (0.175, 0.728), (0.175, 0.645), color=fs.BLUE, lw=1.1, ms=8)
    fs.box(ax, 0.025, 0.495, 0.30, 0.135,
           "基模型（线性 PCA）\n泛化好：性别、年龄、胖瘦",
           fc="white", ec=fs.BLUE, fs=8.0, lw=1.0)

    # 右：小规模高精度
    fs.box(ax, 0.365, 0.735, 0.30, 0.195,
           "小规模 · 高精度\n多相机阵列 / 结构光，毛孔级\n例：938 人 × 20 表情",
           fc="#FDF2F8", ec=fs.PINK, fs=7.8, lw=1.0)
    fs.arrow(ax, (0.515, 0.728), (0.515, 0.645), color=fs.PINK, lw=1.1, ms=8)
    fs.box(ax, 0.365, 0.495, 0.30, 0.135,
           "细节模型（位移图 / 生成网络）\n保真高：皱纹、毛孔、痣",
           fc="white", ec=fs.PINK, fs=8.0, lw=1.0)

    # 汇合
    fs.arrow(ax, (0.175, 0.492), (0.300, 0.400), color=fs.FAINT, lw=1.1, ms=8)
    fs.arrow(ax, (0.515, 0.492), (0.420, 0.400), color=fs.FAINT, lw=1.1, ms=8)
    fs.box(ax, 0.235, 0.245, 0.32, 0.150,
           "由粗到细的合成\n$S=S_{\\text{base}}+D(z_{\\text{detail}},\\ \\psi)$",
           fc="#FFF7ED", ec=fs.ACCENT, fs=8.2, lw=1.2)
    fs.arrow(ax, (0.395, 0.242), (0.445, 0.175), color=fs.ACCENT, lw=1.1, ms=8)
    fs.box(ax, 0.300, 0.055, 0.330, 0.115,
           "单图拟合：粗形状 + 细节一起解",
           fc="white", ec=fs.ACCENT, fs=8.0, lw=1.0)

    # 右侧说明
    ax.plot([0.685, 0.685], [0.06, 0.95], color=fs.GRID, lw=0.9)
    fs.label(ax, 0.705, 0.930, "为什么要两套数据？", fs=8.8, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 0.705, 0.870,
             "深度相机便宜、快、能扫几万人，\n但噪声大、分辨率低，\n只能撑住“粗形状”。\n\n"
             "多相机阵列贵、慢、只能扫几百人，\n但几何干净到能看见毛孔，\n正好用来学“细节”。\n\n"
             "两者相乘，才既有泛化又有保真。",
             fs=7.6, color=fs.MUTED, ha="left", va="top")
    fs.save(fig, "ch17", "fig17-02")


def _bumpy(n=192, seed=3):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:1:n * 1j, 0:1:n * 1j]
    h = np.zeros_like(x)
    for _ in range(90):
        cx, cy = rng.uniform(0, 1, 2)
        s = rng.uniform(0.02, 0.09)
        a = rng.uniform(-1, 1)
        h += a * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s * s))
    h += 0.25 * np.sin(2 * np.pi * (3 * x + 1.5 * y))
    return h


def fig_reflectance():
    n = 192
    h = _bumpy(n)
    gy, gx = np.gradient(h * 0.055, 1.0 / n)
    nz = np.ones_like(gx)
    ln = np.sqrt(gx ** 2 + gy ** 2 + nz ** 2)
    nx, ny, nzz = -gx / ln, -gy / ln, nz / ln

    alb = np.dstack([0.78 + 0.10 * h, 0.60 + 0.08 * h, 0.53 + 0.06 * h]).clip(0, 1)
    spec = (np.clip(h, 0, None) ** 2)
    spec = (spec / spec.max()) ** 2

    L = np.array([-0.5, 0.6, 0.62]); L = L / np.linalg.norm(L)
    ndl = np.clip(nx * L[0] + ny * L[1] + nzz * L[2], 0, 1)
    H = (L + np.array([0, 0, 1.0])); H = H / np.linalg.norm(H)
    ndh = np.clip(nx * H[0] + ny * H[1] + nzz * H[2], 0, 1)
    relit = (alb * (0.45 + 0.65 * ndl)[..., None]
             + 0.30 * (ndh ** 28)[..., None] * np.array([1.0, 0.98, 0.94])).clip(0, 1)

    nrm = np.dstack([nx, ny, nzz]) * 0.5 + 0.5
    spmap = np.dstack([spec, spec * 0.95, spec * 0.92])

    fig = plt.figure(figsize=(W, 2.55))
    panels = [("漫反射反照率 $a_d$", alb, "皮肤本色，去掉光照"),
              ("镜面反照率 $a_s$", spmap, "油光、汗湿的区域"),
              ("表面法线 $\\mathbf{n}$", nrm, "毛孔与皱纹的方向"),
              ("重新打光的结果", relit, "$a_d(\\mathbf{n}\\cdot\\mathbf{l})+a_s(\\mathbf{n}\\cdot\\mathbf{h})^s$")]
    for i, (title, img, sub) in enumerate(panels):
        x0 = 0.015 + i * 0.248
        axp = fig.add_axes([x0, 0.30, 0.205, 0.56])
        axp.imshow(img, interpolation="bilinear")
        axp.set_xticks([]); axp.set_yticks([])
        for s in axp.spines.values():
            s.set_edgecolor(fs.MUTED); s.set_linewidth(0.7)
        fig.text(x0 + 0.1025, 0.245, title, ha="center", fontsize=8.8, color=fs.INK)
        fig.text(x0 + 0.1025, 0.155, sub, ha="center", fontsize=7.4, color=fs.MUTED)
        if i < 3:
            fig.text(x0 + 0.225, 0.55, "+" if i in (0, 1) else "→",
                     ha="center", va="center", fontsize=13, color=fs.MUTED)
    fig.text(0.5, 0.045,
             "3DMM 只给一张低维彩色纹理；AvatarMe 这类工作把外观拆成逐像素的反照率与法线，才能换光源重渲",
             ha="center", fontsize=8.2, color=fs.INK)
    fs.save(fig, "ch17", "fig17-03")


if __name__ == "__main__":
    fig_frequency()
    fig_hybrid()
    fig_reflectance()
