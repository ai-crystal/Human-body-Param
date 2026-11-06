# -*- coding: utf-8 -*-
"""用官方 SMPL 模型渲染「体型 β / 姿态 θ 到底改成什么样」的教学图。

依赖：numpy + matplotlib + Pillow；模型 pkl 需自行从 smpl.is.tue.mpg.de 申请
（本脚本不包含、也不再分发模型文件）。

用法:
    python render_smpl.py                       # 用默认路径找模型
    SMPL_MODEL="D:/models/basicModel_m_lbs_10_207_0_v1.0.0.pkl" python render_smpl.py

输出:
    book/images/08/fig08-04.png   （2×3：上排 β、下排 θ）
"""
import os
import pickle
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(os.path.dirname(HERE))       # book/
ROOT = os.path.dirname(BOOK)                        # 仓库根
OUT = os.path.join(BOOK, "images", "08", "fig08-04.png")

DEFAULT_MODELS = [
    os.environ.get("SMPL_MODEL", ""),
    r"E:/Study/人体参数化技术/SMPL-test/models/raw/basicModel_m_lbs_10_207_0_v1.0.0.pkl",
    r"E:/Study/人体参数化技术/SMPL-test/models/raw/basicModel_f_lbs_10_207_0_v1.0.0.pkl",
]


# ---------------------------------------------------------------- pkl 读取
class _Ch:
    """chumpy.Ch 的替身：真正的数组在 .x 里。"""

    def __setstate__(self, state):
        self.__dict__.update(state)


class _Stub:
    """scipy.sparse 的替身。"""

    def __new__(cls, *a, **k):
        o = object.__new__(cls)
        o._ctor_args = a
        return o

    def __setstate__(self, state):
        self.__dict__.update(state)


class _Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module.startswith("chumpy"):
            return _Ch
        if module.startswith("scipy"):
            return _Stub
        return super().find_class(module, name)


def as_array(obj):
    if isinstance(obj, np.ndarray):
        return obj
    if isinstance(obj, _Ch):
        for k in ("x", "a", "_data"):
            if k in obj.__dict__:
                return np.asarray(obj.__dict__[k])
    d = getattr(obj, "__dict__", {})
    if "data" in d and "indices" in d and "indptr" in d:      # scipy csc
        data, idx, ptr = np.asarray(d["data"]), np.asarray(d["indices"]), np.asarray(d["indptr"])
        shape = d.get("_shape") or getattr(obj, "_ctor_args", [None])[0]
        nrow, ncol = int(shape[0]), int(shape[1])
        out = np.zeros((nrow, ncol), dtype=data.dtype)
        for c in range(ncol):
            lo, hi = int(ptr[c]), int(ptr[c + 1])
            out[idx[lo:hi], c] = data[lo:hi]
        return out
    raise TypeError(type(obj))


def load_model(path):
    with open(path, "rb") as f:
        d = _Unpickler(f, encoding="latin1").load()
    m = {k: as_array(d[k]) for k in ("v_template", "shapedirs", "posedirs",
                                     "J_regressor", "weights", "f", "kintree_table")}
    m["f"] = m["f"].astype(np.int64)
    m["parents"] = m["kintree_table"][0].astype(np.int64)
    return m


# ---------------------------------------------------------------- SMPL 前向
def rodrigues(w):
    """轴角 -> 3x3 旋转，w 可以是 (3,) 或 (K,3)。"""
    w = np.atleast_2d(np.asarray(w, dtype=np.float64))
    th = np.linalg.norm(w, axis=1)
    K = w.shape[0]
    R = np.tile(np.eye(3), (K, 1, 1))
    nz = th > 1e-12
    if np.any(nz):
        k = w[nz] / th[nz, None]
        Kx = np.zeros((k.shape[0], 3, 3))
        Kx[:, 0, 1], Kx[:, 0, 2] = -k[:, 2], k[:, 1]
        Kx[:, 1, 0], Kx[:, 1, 2] = k[:, 2], -k[:, 0]
        Kx[:, 2, 0], Kx[:, 2, 1] = -k[:, 1], k[:, 0]
        s, c = np.sin(th[nz])[:, None, None], np.cos(th[nz])[:, None, None]
        R[nz] = np.eye(3) + s * Kx + (1 - c) * (Kx @ Kx)
    return R


def smpl_forward(model, beta=None, pose=None, trans=None):
    """betas: (10,)，pose: (24,3) 轴角，trans: (3,)。返回 (6890,3)。"""
    betas = np.zeros(10) if beta is None else np.asarray(beta, dtype=np.float64).reshape(-1)[:10]
    pose = np.zeros((24, 3)) if pose is None else np.asarray(pose, dtype=np.float64)
    trans = np.zeros(3) if trans is None else np.asarray(trans, dtype=np.float64)

    V = model["v_template"] + model["shapedirs"][:, :, :10] @ betas
    J = model["J_regressor"] @ V
    parents = model["parents"]

    R = rodrigues(pose.reshape(-1, 3))                  # (24,3,3)
    G = np.zeros((24, 4, 4))
    G[0, :3, :3], G[0, :3, 3], G[0, 3, 3] = R[0], J[0], 1.0
    for i in range(1, 24):
        p = parents[i]
        Gp = G[p]
        T = np.eye(4)
        T[:3, :3] = R[i]
        T[:3, 3] = J[i] - J[p]
        G[i] = Gp @ T

    # pose blendshape：(207,) = 23 个关节的旋转矩阵减去单位阵后展平
    Rflat = (R[1:] - np.eye(3)).reshape(-1)
    V_posed = V + model["posedirs"] @ Rflat

    W = model["weights"]
    T = np.einsum("nk,kij->nij", W, G)                   # (N,4,4)
    Vh = np.concatenate([V_posed, np.ones((V_posed.shape[0], 1))], axis=1)
    out = np.einsum("nij,nj->ni", T, Vh)[:, :3] + trans
    return out


# ---------------------------------------------------------------- 光栅化
def render(verts, faces, W=340, H=620, yaw=-16.0, pitch=4.0, scale=None,
           color=(0.74, 0.76, 0.80), ss=2, bg=(1.0, 1.0, 1.0)):
    """正交相机 + 逐面 Lambert + z-buffer。返回 HxWx3 的 uint8。"""
    v = np.asarray(verts, dtype=np.float64)
    v = v - v.mean(axis=0)
    a, b = np.radians(yaw), np.radians(pitch)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    v = v @ (Ry @ Rx).T                      # 相机坐标：x 右、y 上、z 朝观察者

    if scale is None:
        scale = (H * 0.94 * ss) / (v[:, 1].max() - v[:, 1].min())
    px = v[:, 0] * scale + W * ss / 2
    py = -v[:, 1] * scale + H * ss / 2
    Wp, Hp = W * ss, H * ss

    tri = np.stack([px[faces], py[faces], v[faces][:, :, 2]], axis=-1)
    tri3 = v[faces]                                        # (F,3,3) 相机坐标
    fn = np.cross(tri3[:, 1] - tri3[:, 0], tri3[:, 2] - tri3[:, 0])
    fn /= np.maximum(np.linalg.norm(fn, axis=1, keepdims=True), 1e-12)
    front = fn[:, 2] > 0                                   # 法线朝向观察者
    tri, fn = tri[front], fn[front]

    light = np.array([-0.35, 0.55, 0.75])
    light /= np.linalg.norm(light)
    diff = np.clip(fn @ light, 0, 1)
    shade = 0.38 + 0.62 * diff
    base = np.array(color)[None, :] * shade[:, None]

    img = np.empty((Hp, Wp, 3))
    img[:] = np.array(bg)
    zbuf = np.full((Hp, Wp), -np.inf)

    for i in range(tri.shape[0]):
        p3 = tri[i]
        xmin = max(int(np.floor(p3[:, 0].min())), 0)
        xmax = min(int(np.ceil(p3[:, 0].max())), Wp - 1)
        ymin = max(int(np.floor(p3[:, 1].min())), 0)
        ymax = min(int(np.ceil(p3[:, 1].max())), Hp - 1)
        if xmin > xmax or ymin > ymax:
            continue
        xs, ys = np.meshgrid(np.arange(xmin, xmax + 1) + 0.5,
                             np.arange(ymin, ymax + 1) + 0.5)
        (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = p3
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-12:
            continue
        w0 = ((y1 - y2) * (xs - x2) + (x2 - x1) * (ys - y2)) / den
        w1 = ((y2 - y0) * (xs - x2) + (x0 - x2) * (ys - y2)) / den
        w2 = 1 - w0 - w1
        inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if not inside.any():
            continue
        z = w0 * z0 + w1 * z1 + w2 * z2
        sub_z = zbuf[ymin:ymax + 1, xmin:xmax + 1]
        upd = inside & (z > sub_z)
        if not upd.any():
            continue
        sub_z[upd] = z[upd]
        img[ymin:ymax + 1, xmin:xmax + 1][upd] = base[i]

    img = np.clip(img, 0, 1)
    small = Image.fromarray((img * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    return np.asarray(small)


# ---------------------------------------------------------------- 出图
def main():
    path = next((p for p in DEFAULT_MODELS if p and os.path.exists(p)), None)
    if path is None:
        print("找不到 SMPL 模型 pkl，请设置 SMPL_MODEL 环境变量。")
        sys.exit(1)
    model = load_model(path)
    print("模型:", path, "| 顶点", model["v_template"].shape[0], "| 面", model["f"].shape[0])

    W, H = 300, 560

    def unit_scale(verts, ss=2):
        v = np.asarray(verts, dtype=np.float64)
        return (H * 0.94 * ss) / (v[:, 1].max() - v[:, 1].min())

    # ---------- 上排：只改 β（T-pose 固定） ----------
    pose_T = np.zeros((24, 3))
    ref = smpl_forward(model, beta=np.zeros(10), pose=pose_T)
    sc = unit_scale(ref)                       # 三张图共用同一比例，体型差异才看得出来

    tiles, labels = [], []
    for b in (-4.0, 0.0, 4.0):
        beta = np.zeros(10); beta[0] = b
        v = smpl_forward(model, beta=beta, pose=pose_T)
        tiles.append(render(v, model["f"], W=W, H=H, scale=sc))
        labels.append(("$\\beta_1=%+.0f$" % b, "体型参数 β"))

    # ---------- 下排：只改 θ（β=0） ----------
    def mk(**kw):
        p = np.zeros((24, 3))
        for k, val in kw.items():
            p[int(k[1:])] = val
        return p

    poses = [
        ("抬右臂 45°（右肩）", mk(j17=[0, 0, -0.78])),
        ("屈左膝 45°（左膝）", mk(j4=[0.78, 0, 0])),
        ("上身前倾 30°（脊柱）", mk(j3=[0.5, 0, 0], j6=[0.3, 0, 0], j9=[0.2, 0, 0])),
    ]
    for name, p in poses:
        v = smpl_forward(model, pose=p)
        tiles.append(render(v, model["f"], W=W, H=H, scale=sc))
        labels.append((name, "姿态参数 θ"))

    # ---------- 拼图 ----------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    for cand in ("Microsoft YaHei", "SimHei", "SimSun", "Noto Sans SC"):
        if any(cand.lower() in f.name.lower() for f in font_manager.fontManager.ttflist):
            plt.rcParams["font.sans-serif"] = [cand]
            break
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(2, 3, figsize=(6.6, 5.2), dpi=220)
    for ax, tile, (title, sub) in zip(axes.ravel(), tiles, labels):
        ax.imshow(tile)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor("#E5E7EB")
        ax.set_title(title, fontsize=9.0, color="#1F2937", pad=2)
        ax.set_xlabel(sub, fontsize=7.6, color="#6B7280", labelpad=1)
    fig.tight_layout(pad=0.5, h_pad=1.6, w_pad=0.6)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, facecolor="white", bbox_inches="tight")
    print("saved", OUT)


if __name__ == "__main__":
    main()
