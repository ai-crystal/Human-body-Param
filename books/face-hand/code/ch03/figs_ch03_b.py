# -*- coding: utf-8 -*-
"""第 3 章补充插图：UV 位移图的两层表示、外观的四张图。"""
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "E:/Study/人体参数化技术/人体参数化技术学习/books/code")
import figstyle as fs

fs.FIGDIR = "E:/Study/人体参数化技术/人体参数化技术学习/books/face-hand/images"


def fig_uv_displacement():
    """基网格 → UV 展开 → 位移图 → 还原顶点。"""
    fig, ax = fs.canvas(6.9, 3.6)
    fs.label(ax, 0.5, 0.958, "细节存在 UV 图里：基网格给骨架，位移图给表面",
             fs=10.2, color=fs.INK, weight="bold")

    # ① 基网格
    fs.mesh_disk(ax, cx=0.135, cy=0.55, rx=0.085, ry=0.115, n=12, color="#CBD5E1",
                 ec=fs.BLUE, lw=0.5, z=2, seed=2)
    fs.label(ax, 0.135, 0.345, "① 基网格\n26317 顶点\n间距约 2 mm", fs=7.8)
    fs.arrow(ax, (0.235, 0.55), (0.300, 0.55), color=fs.FAINT)
    fs.label(ax, 0.268, 0.585, "展开", fs=7.4, color=fs.MUTED)

    # ② UV 图
    ax.add_patch(plt.Rectangle((0.315, 0.44), 0.145, 0.22, facecolor="#E8EDF3",
                               edgecolor=fs.MUTED, lw=0.7, zorder=2))
    rng = np.random.default_rng(5)
    for _ in range(90):
        x = 0.315 + rng.uniform(0.006, 0.139)
        y = 0.44 + rng.uniform(0.006, 0.214)
        ax.add_patch(plt.Circle((x, y), 0.0035, facecolor=fs.BLUE, edgecolor="none", zorder=3))
    fs.label(ax, 0.3875, 0.345, "② UV 展开图\n1024 × 1024 个采样\n间距约 0.3 mm", fs=7.8)
    fs.arrow(ax, (0.475, 0.55), (0.540, 0.55), color=fs.FAINT)

    # ③ 位移图
    ax.add_patch(plt.Rectangle((0.555, 0.44), 0.145, 0.22, facecolor="#FBEFE6",
                               edgecolor=fs.ACCENT, lw=0.7, zorder=2))
    xs = np.linspace(0, 1, 60)
    for k in range(7):
        yy = 0.455 + k * 0.030
        ax.plot(0.560 + 0.135 * xs, yy + 0.004 * np.sin(9 * xs + k),
                color=fs.ACCENT, lw=0.7, zorder=3)
    fs.label(ax, 0.6275, 0.345, "③ 位移图 $\\Delta(u,v)$\n每像素一个数\n范围 ±1 cm", fs=7.8)
    fs.arrow(ax, (0.715, 0.55), (0.780, 0.55), color=fs.FAINT)

    # ④ 还原
    fs.mesh_disk(ax, cx=0.875, cy=0.55, rx=0.085, ry=0.115, n=12, color="#F2C9AE",
                 ec=fs.ACCENT, lw=0.5, z=2, seed=2, jitter=0.006)
    fs.label(ax, 0.875, 0.345, "④ 加回几何\n$\\mathbf{v}_i=\\bar{\\mathbf{v}}_i+\\Delta\\,\\mathbf{n}_i$\n误差 < 0.3 mm", fs=7.8)

    fs.box(ax, 0.045, 0.075, 0.91, 0.135,
           "为什么划算：202 万个数（1024×1024）换回毛孔级细节，"
           "只相当于原始网格数据量的约 2%；\n"
           "而且位移图是在二维平面上学的，可以直接用卷积网络、生成对抗网络去建模",
           ec=fs.GREEN, fs=8.2)
    fs.label(ax, 0.5, 0.025, "数字取自 FaceScape 论文的报告值；顶点间距为按头高估算的量级",
             fs=7.4, color=fs.FAINT)
    fs.save(fig, "ch03", "fig03-02")


if __name__ == "__main__":
    fig_uv_displacement()
