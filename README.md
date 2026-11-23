# 人体参数化技术

> 一套六册的中文书：**用几十个参数，描述一个高维的人**。

从 1995 年的主动形状模型一路讲到 2025 年的 ATLAS / MHR 与扩散模型。人体、人脸、人手、动物四条主线共用同一套数学：平均形状 + 形变基 + 骨架蒙皮。

作者：**Dr. Dezeming**　·　2026 年 · 第一版

> 📖 **在线阅读**：<https://ai-crystal.github.io/Human-body-Param/>
>
> 单册直达：`https://ai-crystal.github.io/Human-body-Param/#/books/intro/chapters/ch01`
>
> 也可以打开仓库里的 `index.html` 本地读，或直接看各册 PDF。

## 六册一览

| 内容 | 章 | 页 | PDF |
|---|---:|---:|---|
| **[入门册](books/intro/chapters/ch01.md)**　只讲概念、求全：参数化在做什么 · 参数从哪来 · 人怎么动 · 怎么从图像反推 · 模型家族全景 · 2020 年后的技术 · 应用与边界 · 怎么上手 | 8 | 63 | [PDF](output/php-intro.pdf) |
| **[数学册](books/math/chapters/ch01.md)**　向量与矩阵 · 最小二乘 · 概率与 PCA/SVD · 三维表示与旋转 · 李群与位姿优化 · LBS 与 DQS · 统计形状模型 · 动手实践 | 7 | 99 | [PDF](output/php-math.pdf) |
| **[人体册](books/body/chapters/ch01.md)**　SCAPE · SMPL 逐项拆公式 · SMPL 家族（STAR / ATLAS / MHR） · SMPL 是怎么训练出来的 | 4 | 52 | [PDF](output/php-body.pdf) |
| **[重建册](books/recon/chapters/ch01.md)**　优化法与回归法 · 视频、多人、度量尺度 · 数据集与评估 · 着装与神经渲染 · 动作与生成 | 5 | 45 | [PDF](output/php-recon.pdf) |
| **[脸手册](books/face-hand/chapters/ch01.md)**　3DMM 与 BFM · FLAME · 高保真细节与纹理 · 驱动与神经头像 · MANO · 单手重建 · 手物交互 | 7 | 69 | [PDF](output/php-face-hand.pdf) |
| **[前沿册](books/frontier/chapters/ch01.md)**　SMAL 与动物重建 · 跨物种 · 扩散与 3DGS · 人体基础模型 · 研究脉络 | 5 | 49 | [PDF](output/php-frontier.pdf) |

册名点进去就是在线阅读的第一章，最后一列是整册 PDF。合计 **36 章、377 页、约 22 MB**。每册末尾都有术语表与参考文献（数学册另有数学补充，前沿册另有论文时间线，入门册另有文献清单）。

## 怎么读

- **完全外行、想先有全貌**：只读入门册。八章、一个下午，读完能听懂这一行的对话，知道自己该往哪儿深入。
- **有图形或视觉基础**：直接看数学册的 PCA 与骨架蒙皮两章，再跳到人体册看 SMPL 的完整公式。
- **只做人体**：入门册 → 数学册 → 人体册 → 重建册。
- **只做人脸或手**：入门册 → 数学册（PCA 与蒙皮）→ 人体册（公式写法）→ 脸手册。
- **只做动物**：入门册 → 人体册 → 前沿册。

每册前言里都写明了前置知识与跳读建议；章末有「本章小结」，赶时间只看小结也够用。

## 这套书的特点

- **从零讲起**：不用先修线性代数。公式全部用 KaTeX 排版，网页上可以直接读，也能复制。
- **讲失败模式**：每个模型不只讲“它怎么工作”，也讲“它在什么情况下会坏”。
- **六册各自独立**：一本书内的所有引用都指向本书；要用到别处概念时会就地补一句解释，所以任意一册都能单独读、单独改。
- **插图全部由程序生成**：代码在 `books/<册>/code/`，可以改参数重画，不依赖任何受限的模型文件。
- **每个数字都有出处**：不确定的数值宁可留空，也不写没核对过的数字。

## 仓库结构

```text
books/
├── build/            构建脚本：build.py、gen_appendix.py、make_covers.py、refs.json
├── code/figstyle.py  六册共用的绘图风格
├── <册>/             六册各自一套：book.json、structure.json、chapters/、
│                     front/、appendix/、images/、code/
output/               六册 PDF
index.html            在线阅读站点（docsify）
```

构建方法见 [`books/build/README.md`](books/build/README.md)。Windows 下双击 `build.bat` 即可全部重建，`build-math.bat` 之类只重建一册。

## 约定

- 向量加粗、矩阵大写加粗、标量斜体；角度默认用弧度。
- 公式按章编号，例如“式 (3.8)”指本册第 3 章第 8 个公式。
- 引用用方括号数字，对应本册末尾的参考文献。
- “SMPL”指原始的身体模型，“SMPL-X”指包含手脸的扩展，二者不混用。

## 许可

本书文字与插图采用 **CC BY-NC-SA 4.0**（署名—非商业性使用—相同方式共享）许可发布。书中不包含任何受限的 SMPL / MANO / FLAME 模型文件；文中提及的论文版权归原作者与出版方所有。若要商用书中提到的模型，请自行确认各自的许可条款。

发现错漏欢迎提交 Issue。
