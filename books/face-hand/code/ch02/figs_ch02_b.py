# -*- coding: utf-8 -*-
"""第 2 章补充插图：一次前向的数值链条、累积误差曲线。"""
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "E:/Study/人体参数化技术/人体参数化技术学习/books/code")
import figstyle as fs

fs.FIGDIR = "E:/Study/人体参数化技术/人体参数化技术学习/books/face-hand/images"


def fig_forward_chain():
    """一次 FLAME 前向的五个阶段，每个阶段给一个顶点的示意数值。"""
    fig, ax = fs.canvas(6.8, 4.5)
    fs.label(ax, 0.5, 0.972, "一次前向的数值链条：以一个鼻尖顶点为例（数值为示意）",
             fs=10.2, color=fs.INK, weight="bold")
    fs.label(ax, 0.5, 0.930, "5023 个顶点各走一遍同样的五步；这里只跟踪其中一个顶点的 z 坐标",
             fs=8.2, color=fs.MUTED)

    stages = [
        (0.795, "① 模板 $\\bar{\\mathbf{T}}$", "零姿态的平均头，顶点在 (0.000, 0.021, 0.108)", fs.GOLD),
        (0.640, "② 加形状 $B_S(\\boldsymbol{\\beta})$", "$\\beta_1=+1.4$ 沿主成分给出 $\\Delta z=+2.1$ mm", fs.GREEN),
        (0.485, "③ 加表情 $B_E(\\boldsymbol{\\psi})$", "$\\psi_3=+0.9$ 让鼻翼外扩、鼻尖降 0.6 mm", fs.PURPLE),
        (0.330, "④ 加姿态矫正 $B_P(\\boldsymbol{\\theta})$", "颈转 12 度，矫正项补 0.3 mm 的皮肤拉伸", fs.BLUE),
        (0.175, "⑤ 蒙皮 $W$ 与关节 $J$", "按 4 个关节的权重刚体变换，得到最终位置", fs.ACCENT),
    ]
    for y, title, note, col in stages:
        fs.box(ax, 0.045, y, 0.30, 0.105, title, ec=col, fs=8.4)
        fs.box(ax, 0.365, y, 0.60, 0.105, note, ec=fs.FAINT, fs=8.0, lw=0.8)
        fs.arrow(ax, (0.195, y), (0.195, y - 0.048), color=fs.FAINT)
    fs.arrow(ax, (0.195, 0.175), (0.195, 0.105), color=fs.FAINT)
    fs.box(ax, 0.045, 0.028, 0.92, 0.075,
           "输出：5023 个顶点 = 15069 个坐标。输入只有 415 个数，压缩比约 36 : 1",
           ec=fs.ACCENT, fs=8.2)

    fs.save(fig, "ch02", "fig02-03")


def fig_cumulative_error():
    """累积误差曲线：横轴阈值，纵轴顶点占比。数值取自 FLAME 论文的对比实验。"""
    fig, ax = plt.subplots(figsize=(5.4, 3.5))
    thr = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0])
    # 用论文给出的两个锚点（0.5 mm 处 74/69/67，全主成分 94/92）构造示意曲线，
    # 曲线形状为示意，仅在 0.5 mm 处的数值来自论文。
    def curve(a, b, k):
        return a + (b - a) * (1 - np.exp(-k * thr))

    flame = curve(0.42, 0.985, 1.6)
    bfm = curve(0.37, 0.975, 1.5)
    fw = curve(0.35, 0.970, 1.45)
    flame[4], bfm[4], fw[4] = 0.74, 0.69, 0.67
    ax.plot(thr, flame * 100, color=fs.GREEN, lw=1.8, marker="o", ms=3.5, label="FLAME")
    ax.plot(thr, bfm * 100, color=fs.BLUE, lw=1.6, marker="s", ms=3.2, label="BFM")
    ax.plot(thr, fw * 100, color=fs.GOLD, lw=1.6, marker="^", ms=3.2, label="FaceWarehouse")
    ax.axvline(0.5, color=fs.ACCENT, lw=0.9, ls=(0, (4, 2)))
    ax.text(0.52, 22, "0.5 mm：74 / 69 / 67", fontsize=7.6, color=fs.ACCENT)
    ax.set_xlabel("顶点误差阈值（毫米）")
    ax.set_ylabel("误差小于阈值的顶点占比（%）")
    ax.set_title("累积误差曲线比单一平均值信息量大", fontsize=9.8, color=fs.INK)
    ax.set_ylim(0, 104)
    ax.set_xlim(0, 2.0)
    ax.legend(fontsize=8, loc="lower right")
    fs.clean(ax, grid=True)
    ax.text(0.02, 0.02, "曲线形状为示意；0.5 mm 处的三个数值取自 FLAME 论文的对比实验",
            transform=ax.transAxes, fontsize=6.8, color=fs.MUTED)
    fig.tight_layout()
    fs.save(fig, "ch02", "fig02-04")


if __name__ == "__main__":
    fig_forward_chain()
    fig_cumulative_error()
