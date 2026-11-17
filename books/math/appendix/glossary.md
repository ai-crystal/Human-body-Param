# 附录 B 术语中英对照

> 按拼音/字母混排，方便查阅。括号里是本书第一次出现时的章节。

| 中文 | 英文 | 一句话解释 |
|---|---|---|
| 主动形状模型 | Active Shape Model (ASM) | 用 PCA 约束关键点搜索的经典方法（第 6 章） |
| 主动外观模型 | Active Appearance Model (AAM) | 同时建模形状与纹理（第 6 章） |
| 仿射变换 | affine transformation | 线性变换 + 平移，保持平行线 |
| 轴角 | axis-angle | 用“单位轴 + 转角”表示旋转（第 4 章） |
| 绑定姿势 | bind pose / rest pose | 蒙皮前的参考姿势（第 5 章） |
| 混合权重 | blend weights | 每个顶点受各关节影响的权重（第 5 章） |
| blendshape | blend shape | 用一组预定义形变的线性组合表示表情/形状（第 6、8 章） |
| 相机内参 | camera intrinsics | 焦距、主点、畸变（第 4 章） |
| 相机外参 | camera extrinsics | 相机在世界坐标中的旋转与平移（第 4 章） |
| 蒙皮 | skinning | 让顶点跟随骨架变形（第 5 章） |
| 线性混合蒙皮 | Linear Blend Skinning (LBS) | 对多个刚体变换做加权平均（第 5 章） |
| 对偶四元数蒙皮 | Dual Quaternion Skinning (DQS) | 用四元数插值替代矩阵插值，缓解体积损失 |
| 糖纸效应 | candy wrapper effect | 扭转时肢体被拧细的伪影（第 5 章） |
| 协方差 | covariance | 两个变量“一起变”的程度（第 3 章） |
| 协方差矩阵 | covariance matrix | 所有两两协方差排成的对称矩阵（第 3 章） |
| 主成分分析 | Principal Component Analysis (PCA) | 找方差最大方向的降维方法（第 3 章） |
| 特征向量 | eigenvector | 被矩阵作用后方向不变的方向（第 2、3 章） |
| 特征值 | eigenvalue | 特征向量方向上的缩放倍数/方差（第 3 章） |
| 奇异值分解 | Singular Value Decomposition (SVD) | 任意矩阵分解为旋转—缩放—旋转（第 2 章） |
| 对应 | correspondence | 不同网格顶点之间的解剖级一一对应（第 6 章） |
| 非刚性配准 | non-rigid ICP | 让模板变形去贴合扫描的迭代方法（第 6 章） |
| 三维形变模型 | 3D Morphable Model (3DMM) | 人脸形状/纹理的 PCA 参数化模型（第 6、15 章） |
| 双线性模型 | bilinear model | 用两组系数分别控制身份与表情（第 15 章） |
| 表情基 | expression basis | 描述表情变化的向量基（第 16 章） |
| 关节回归 | joint regression | 从形状顶点回归关节位置（第 8 章） |
| 前向运动学 | forward kinematics (FK) | 由关节角算出关节世界位置（第 5 章） |
| 逆运动学 | inverse kinematics (IK) | 由末端位置反推关节角 |
| 重投影误差 | reprojection error | 三维点投影到二维后与观测的差（第 4、10 章） |
| 可微渲染 | differentiable rendering | 对渲染过程求导，把图像误差反传到几何（第 4 章） |
| 分析—合成 | analysis-by-synthesis | 反复“渲染—比较—更新”的拟合思路（第 10 章） |
| 弱透视相机 | weak-perspective camera | 用缩放+平移近似透视，忽略深度引起的尺寸变化（第 10 章） |
| 度量尺度 | metric scale | 以米为单位的真实尺寸（第 11 章） |
| 世界坐标 | world coordinates | 以场景（重力/地面）为参考的坐标（第 11 章） |
| 足部接触 | foot contact | 脚是否踩地，用于恢复世界位移（第 11 章） |
| 单阶段多人 | one-stage multi-person | 一次前向输出所有人参数（第 11 章） |
| 自顶向下 | top-down | 先检测再逐人拟合（第 11 章） |
| 平均关节位置误差 | MPJPE | 关节位置的平均欧氏误差（第 12 章） |
| Procrustes 对齐 | Procrustes alignment | 去掉旋转/缩放/平移后再比较（第 12 章） |
| 每顶点误差 | PVE | 网格顶点平均误差（第 12 章） |
| 正确关键点比例 | PCK | 误差小于阈值的关节占比（第 12 章） |
| 加速度误差 | acceleration error | 衡量动作抖动的指标（第 11、12 章） |
| 神经辐射场 | Neural Radiance Field (NeRF) | 用 MLP 表示空间颜色与密度（第 13、25 章） |
| 3D 高斯泼溅 | 3D Gaussian Splatting (3DGS) | 用高斯椭球表示场景，实时渲染（第 13、25 章） |
| 有符号距离场 | Signed Distance Field (SDF) | 每个点到表面的有符号距离（第 13 章） |
| 隐式表面 | implicit surface | 用函数零等值面表示表面（第 13 章） |
| 扩散模型 | diffusion model | 学习“加噪—去噪”的生成模型（第 25 章） |
| 分数蒸馏采样 | Score Distillation Sampling (SDS) | 用 2D 扩散模型指导 3D 优化（第 25 章） |
| 变分自编码器 | Variational Autoencoder (VAE) | 学习低维隐空间的生成模型（第 14、25 章） |
| 姿态先验 | pose prior | 限制姿态“像人”的概率模型（第 10、14 章） |
| 运动先验 | motion prior | 限制动作连续、符合动力学的模型（第 14 章） |
| 重定向 | retargeting | 把动作从一套骨架迁移到另一套（第 14 章） |
| 数字人 | digital human / avatar | 可驱动、可渲染的虚拟人（第 13、18 章） |
| 化身 | avatar | 同上，常指带外观的个体化模型 |
| 服饰位移 | clothing displacement | 衣服相对裸体表面的偏移（第 13 章） |
| 参数化 | parametric | 用少量参数描述高维对象 |
| 拓扑 | topology | 顶点/边/面的连接关系（第 4 章） |
| 流形 | manifold | 局部像欧氏空间的曲面（第 4 章） |
| 测地距离 | geodesic distance | 沿表面的最短路径长度（第 5 章） |
| 薄板样条 | Thin Plate Spline (TPS) | 一种平滑的非刚性变换（第 6 章） |
| 高斯混合模型 | Gaussian Mixture Model (GMM) | 多个高斯叠加的概率模型（第 10 章） |
| 岭回归 | ridge regression | 带 L2 正则的最小二乘（第 2 章） |
| 伪逆 | pseudo-inverse | 非方阵/奇异矩阵的“广义逆”（第 2 章） |
