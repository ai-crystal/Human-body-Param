# 人体参数化技术（六册）

| 册 | 目录 | 内容 |
|---|---|---|
| 入门册 | [`intro/`](intro/chapters/ch01.md) | 只讲概念：参数化在做什么、参数从哪来、人怎么动、怎么从照片反推、怎么用 |
| 数学册 | [`math/`](math/chapters/ch01.md) | 向量与矩阵、最小二乘、概率与 PCA/SVD、三维表示与旋转、LBS/DQS、统计形状模型、李群与位姿优化 |
| 人体册 | [`body/`](body/chapters/ch01.md) | SCAPE、SMPL 逐项拆公式、SMPL 家族与最新模型 |
| 重建册 | [`recon/`](recon/chapters/ch01.md) | 优化与回归、视频与多人、数据集与评估、着装与神经渲染、动作生成 |
| 脸手册 | [`face-hand/`](face-hand/chapters/ch01.md) | 3DMM/BFM、FLAME、高保真、驱动、MANO、单手重建、手物交互 |
| 前沿册 | [`frontier/`](frontier/chapters/ch01.md) | SMAL、动物重建、跨物种、扩散与 3DGS、人体基础模型、研究脉络 |

每册的结构都一样：

```text
<册>/
├── book.json        书名、副标题、作者、输出文件名
├── structure.json   章序（唯一来源）
├── chapters/        正文
├── appendix/        术语、参考文献
├── images/NN/       插图（正文里写 ../images/NN/x.png）
└── code/chNN/       该章的绘图脚本
```

构建方式见 [`build/README.md`](build/README.md)。
