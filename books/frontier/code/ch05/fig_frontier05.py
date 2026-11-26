# -*- coding: utf-8 -*-
"""前沿册第 5 章插图：表示的三代、表示灵活度 × 先验强度。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(BOOK), "code"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
import figstyle as fs

FIGDIR = os.path.join(BOOK, "images")


def fig_generations():
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    fs.clean(ax, grid=True)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("单位样本的表达自由度（示意）", fontsize=8.6)
    ax.set_ylabel("是否保留顶点对应", fontsize=8.6)
    ax.set_yticks([0, 10])
    ax.set_yticklabels(["无对应", "有对应"], fontsize=8.4)
    ax.set_xticks([])
    ax.tick_params(labelsize=8.2)

    pts = [
        (1.95, 8.1, "固定拓扑扫描", "骨架与网格对应", fs.BLUE, 2.9, 1.5),
        (4.75, 7.0, "参数化模型", "SMPL · FLAME · MANO", fs.ACCENT, 3.3, 1.55),
        (7.75, 8.2, "隐式场 · 高斯", "表达力最强", fs.PURPLE, 2.6, 1.4),
        (7.5, 2.2, "点云 / 体素", "丢掉对应", fs.GREEN, 2.4, 1.35),
    ]
    for x, y, name, sub, c, w, h in pts:
        ax.add_patch(Ellipse((x, y), w, h, ec=c, fc="white", lw=1.2, alpha=0.95, zorder=3))
        ax.text(x, y + 0.30, name, ha="center", va="center", fontsize=8.0, color=c, zorder=4)
        ax.text(x, y - 0.36, sub, ha="center", va="center", fontsize=6.4,
                color=fs.MUTED, zorder=4)

    # 空位：既要自由度又要对应
    ax.add_patch(Ellipse((7.55, 4.85), 4.05, 1.6, ec=fs.FAINT, fc="none", lw=1.0,
                         ls=(0, (3, 2.4)), zorder=3))
    ax.text(7.55, 4.85, "既要自由度又要对应\n还没有成熟方案", ha="center", va="center",
            fontsize=6.6, color=fs.FAINT, zorder=4, linespacing=1.7)

    ax.add_patch(FancyArrowPatch((3.0, 7.9), (3.4, 7.5), arrowstyle="-|>",
                                 mutation_scale=10, color=fs.FAINT, lw=1.0, zorder=2))
    ax.add_patch(FancyArrowPatch((6.2, 7.1), (6.7, 7.9), arrowstyle="-|>",
                                 mutation_scale=10, color=fs.FAINT, lw=1.0, zorder=2,
                                 linestyle=(0, (3, 2.4))))
    ax.text(0.2, 9.9, "表示的三代：越往右上，能表达的细节越多，代价是对应与控制越弱",
            fontsize=8.6, color=fs.INK, va="top")
    fig.tight_layout(pad=0.5)
    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch05", "fig05-02")


def fig_plane():
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    fs.clean(ax, grid=True)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("表示的灵活度 →", fontsize=8.6)
    ax.set_ylabel("先验的强度 →", fontsize=8.6)
    ax.set_xticks([]); ax.set_yticks([])

    # 对角线
    ax.plot([0.6, 9.4], [0.6, 9.4], color="#E5E7EB", lw=1.2, ls=(0, (4, 3)), zorder=1)
    ax.text(2.2, 2.9, "表示与先验匹配", fontsize=7.4, color=fs.FAINT, rotation=39, ha="left")

    groups = [
        (1.6, 2.0, "参数化 + 线性先验", "SMPL + PCA", fs.ACCENT, 2.6, 1.3),
        (5.2, 5.0, "参数化 + 学习先验", "SMPL + 神经网络", fs.GOLD, 3.0, 1.4),
        (8.2, 8.4, "隐式/高斯 + 生成先验", "扩散 / 3DGS", fs.PURPLE, 2.8, 1.5),
        (8.4, 2.2, "强表示 + 弱先验", "细节丰富但形状荒谬", fs.GREEN, 2.8, 1.4),
        (2.2, 8.4, "弱表示 + 强先验", "细节被磨平", fs.BLUE, 2.8, 1.4),
    ]
    for x, y, name, sub, c, w, h in groups:
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    ec=c, fc="white", lw=1.1, zorder=3))
        ax.text(x, y + 0.24, name, ha="center", va="center", fontsize=7.6, color=c, zorder=4)
        ax.text(x, y - 0.34, sub, ha="center", va="center", fontsize=6.8,
                color=fs.MUTED, zorder=4)

    ax.text(0.2, 9.7, "对角线附近的方法最容易落地：表示和先验的强弱要匹配",
            fontsize=8.8, color=fs.INK, va="top")
    ax.text(8.9, 0.35, "位置为示意，只表示相对关系", fontsize=6.8, color=fs.FAINT,
            ha="right")
    fig.tight_layout(pad=0.5)
    fs.FIGDIR = FIGDIR
    fs.save(fig, "ch05", "fig05-03")


if __name__ == "__main__":
    fig_generations()
    fig_plane()
