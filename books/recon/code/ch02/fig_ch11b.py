# -*- coding: utf-8 -*-
"""第 2 章补充插图：时序平滑的两个副作用（图 2-4）。

左：指数滑动平均（EMA）的滞后与峰值削平——真实动作 vs 两种平滑系数。
右：旋转不能线性平均——170° 与 -170° 的“平均”并不是 180°。
"""
import sys
sys.path.insert(0, r"E:\Study\人体参数化技术\人体参数化技术学习\books\code")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as fs

fs.FIGDIR = r"E:\Study\人体参数化技术\人体参数化技术学习\books\recon\images"


def ema(x, a):
    y = np.empty_like(x)
    y[0] = x[0]
    for t in range(1, len(x)):
        y[t] = a * x[t] + (1 - a) * y[t - 1]
    return y


def fig_smoothing():
    fig = plt.figure(figsize=(6.9, 3.2))
    fig.subplots_adjust(left=0.065, right=0.975, top=0.86, bottom=0.26, wspace=0.34)

    # ---------------- 左：EMA 的滞后 ----------------
    ax = fig.add_axes([0.065, 0.27, 0.50, 0.55])
    T = 60
    t = np.arange(T)
    true = 60 * np.exp(-((t - 30) ** 2) / (2 * 6.0 ** 2))          # 一次抬手再放下
    y2 = ema(true, 0.2)
    y5 = ema(true, 0.5)
    ax.plot(t, true, color=fs.INK, lw=1.8, label="真实关节角")
    ax.plot(t, y5, color=fs.GREEN, lw=1.4, label=r"$\alpha$=0.5")
    ax.plot(t, y2, color=fs.ACCENT, lw=1.4, label=r"$\alpha$=0.2")
    ax.set_xlabel("帧（30 帧/秒）", fontsize=8.2)
    ax.set_ylabel("肩关节角度（度，示意）", fontsize=8.2)
    ax.set_xlim(0, T - 1); ax.set_ylim(0, 70)
    ax.set_title("平滑越强，峰值越低、到位越晚", fontsize=9.0, pad=6)
    ax.legend(fontsize=7.4, loc="upper left")
    ax.tick_params(labelsize=7.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    # 峰值与滞后标注
    pk_true = true.max(); pk_2 = y2.max()
    ax.annotate("", xy=(30, pk_true), xytext=(30, pk_2),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=0.8))
    ax.text(30.8, (pk_true + pk_2) / 2 - 3, "峰值被削 %.0f%%" % (100 * (1 - pk_2 / pk_true)),
            fontsize=7.2, color=fs.ACCENT, va="center",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    lag = int(np.argmax(y2) - np.argmax(true))
    ax.text(41, 66, "峰位后移 %d 帧" % lag, fontsize=7.2, color=fs.MUTED, va="top")
    ax.text(41, 60, "约 %d 毫秒" % (lag * 1000 // 30), fontsize=7.2, color=fs.MUTED, va="top")

    # ---------------- 右：旋转的平均 ----------------
    ax2 = fig.add_axes([0.655, 0.24, 0.315, 0.60])
    ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_xlim(-1.35, 1.35); ax2.set_ylim(-1.50, 1.30)
    ax2.add_patch(plt.Circle((0, 0), 1.0, fill=False, ec=fs.FAINT, lw=0.9))
    for deg, c, lab in [(170, fs.BLUE, "第 t 帧\n170°"), (-170, fs.GREEN, "第 t+1 帧\n-170°")]:
        a = np.deg2rad(deg)
        ax2.plot([0, np.sin(a)], [0, np.cos(a)], color=c, lw=1.8, zorder=3)
        ax2.scatter([np.sin(a)], [np.cos(a)], s=26, color=c, zorder=4)
        dx = -1.02 if deg > 0 else 1.02
        ax2.text(dx, -0.62, lab, fontsize=7.4, color=c,
                 ha="right" if deg > 0 else "left", va="center")
    ax2.plot([0, 0], [0, -1.0], color=fs.ACCENT, lw=1.8, ls="-", zorder=3)
    ax2.scatter([0], [-1.0], s=26, color=fs.ACCENT, zorder=4)
    ax2.text(0, -1.38, "真中间朝向 180°", fontsize=7.4, color=fs.ACCENT, ha="center")
    ax2.scatter([0], [1.0], s=40, color=fs.MUTED, marker="x", zorder=5)
    ax2.annotate("线性平均得 0°", xy=(0.06, 1.0), xytext=(0.30, 1.20), fontsize=7.4,
                 color=fs.MUTED, ha="left",
                 arrowprops=dict(arrowstyle="-", color=fs.MUTED, lw=0.6))
    ax2.set_title("旋转不能直接相加除以 2", fontsize=9.0, pad=2)

    fig.text(0.5, 0.055,
             "左图：一阶低通群延迟约 (1-α)/α 帧；右图：轴角差 340° 时，线性平均落在反方向",
             fontsize=7.8, color=fs.MUTED, ha="center")
    fs.save(fig, "ch02", "fig02-04")


if __name__ == "__main__":
    fig_smoothing()
