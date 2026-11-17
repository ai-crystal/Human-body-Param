# 附录 A 数学补充

> 本附录把正文用到但没展开的几个工具集中讲一遍：SVD 的几何意义、矩阵求导、概率的几条基本规则、四元数插值。它们不是“必须背下来”的公式，而是遇到问题时可以回来查的参考。

## A.1 SVD 的几何意义

任意矩阵 $\mathbf{X}\in\mathbb{R}^{m\times n}$ 都可以分解为

$$
\mathbf{X}=\mathbf{U}\mathbf{S}\mathbf{V}^\top,
\tag{A.1}
$$

其中 $\mathbf{U}$ 的列是 $m$ 维正交向量，$\mathbf{V}$ 的列是 $n$ 维正交向量，$\mathbf{S}$ 是“对角”矩阵，对角线上是奇异值 $s_1\ge s_2\ge\cdots\ge0$。

几何上，$\mathbf{V}^\top$ 先旋转输入空间，$\mathbf{S}$ 沿坐标轴拉伸/压缩，$\mathbf{U}$ 再旋转到输出空间。所以**任何线性变换都可以看成“旋转—拉伸—旋转”**。

对中心化的数据矩阵 $\tilde{\mathbf{X}}$（每行一个样本），SVD 与 PCA 的关系是：

$$
\mathbf{V}=[\mathbf{p}_1,\dots,\mathbf{p}_n],\qquad
\lambda_i=\frac{s_i^2}{n-1}.
\tag{A.2}
$$

也就是说，右奇异向量就是主成分，奇异值的平方除以 $n-1$ 就是特征值。这就是为什么 `sklearn` 的 PCA 默认用 SVD 实现。

## A.2 矩阵求导的三条规则

只要记住三条，就够读懂本书的推导。

**规则一：线性项。**

$$
\frac{\partial}{\partial\mathbf{x}}(\mathbf{a}^\top\mathbf{x})=\mathbf{a}.
\tag{A.3}
$$

**规则二：二次型。**

$$
\frac{\partial}{\partial\mathbf{x}}(\mathbf{x}^\top\mathbf{A}\mathbf{x})=(\mathbf{A}+\mathbf{A}^\top)\mathbf{x}.
\tag{A.4}
$$

如果 $\mathbf{A}$ 对称，就是 $2\mathbf{A}\mathbf{x}$。

**规则三：最小二乘。**

$$
\frac{\partial}{\partial\mathbf{w}}\|\mathbf{A}\mathbf{w}-\mathbf{y}\|^2
=2\mathbf{A}^\top(\mathbf{A}\mathbf{w}-\mathbf{y}).
\tag{A.5}
$$

令其为 0，就得到正规方程 $\mathbf{A}^\top\mathbf{A}\mathbf{w}=\mathbf{A}^\top\mathbf{y}$。

## A.3 概率的三条规则

**加法规则**（互斥事件）：

$$
p(A\ \text{或}\ B)=p(A)+p(B).
\tag{A.6}
$$

**乘法规则**：

$$
p(A,B)=p(A\mid B)p(B).
\tag{A.7}
$$

**贝叶斯公式**：

$$
p(A\mid B)=\frac{p(B\mid A)p(A)}{p(B)}.
\tag{A.8}
$$

在拟合问题里，$A$ 是“参数”，$B$ 是“观测”。贝叶斯公式告诉我们：**后验 ∝ 似然 × 先验**。第 10 章的姿态先验、第 3 章的高斯模型，都是这条公式的实例。

## A.4 四元数插值

单位四元数 $q=(\cos\frac{\theta}{2},\sin\frac{\theta}{2}\mathbf{n})$ 表示绕轴 $\mathbf{n}$ 转 $\theta$。两个四元数之间的插值用**球面线性插值**（SLERP）：

$$
\mathrm{slerp}(q_0,q_1,t)=\frac{\sin((1-t)\Omega)}{\sin\Omega}q_0+\frac{\sin(t\Omega)}{\sin\Omega}q_1,
\tag{A.9}
$$

其中 $\Omega=\arccos(q_0\cdot q_1)$ 是两个四元数的夹角。它保证插值过程中的角速度均匀，不会像欧拉角那样“忽快忽慢”。

## A.5 常用希腊字母与含义

| 符号 | 读法 | 本书含义 |
|---|---|---|
| $\alpha,\beta,\gamma$ | alpha, beta, gamma | 形状系数、角度 |
| $\theta$ | theta | 姿态参数（轴角） |
| $\lambda$ | lambda | 特征值、损失权重 |
| $\mu$ | mu | 均值 |
| $\sigma$ | sigma | 标准差 |
| $\boldsymbol{\psi}$ | psi | 表情参数 |
| $\boldsymbol{\Omega}$ | Omega | 角速度、旋转矩阵 |
| $\boldsymbol{\pi}$ | pi | 相机参数 |
| $\boldsymbol{\epsilon}$ | epsilon | 噪声 |

## A.6 推荐的自学顺序

1. 3Blue1Brown 的《线性代数的本质》（建立直觉）；
2. 任何一本工科线性代数教材的前四章（矩阵、秩、特征值）；
3. 概率论的前三章（随机变量、期望、方差）；
4. 把第 26 章的代码跑一遍，改参数；
5. 回来读第 3、5、8 章。

数学不是看会的，是用会的。每读一个公式，试着用 NumPy 写一遍，比抄十遍笔记有用。
