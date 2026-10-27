# 构建说明

这个目录只放构建与站点相关的脚本，**不影响书稿内容**。

## 目录

```
book/
  build/
    build_book.py      # Markdown → HTML → PDF（图片压缩、两遍排版取页码、书签、字体子集化）
    gen_appendix.py    # 生成附录 C 时间线、附录 D 参考文献、站点引用编号 cites.js
    make_covers.py     # 生成封面/封底（Playwright + Chrome/Edge，输出至 book/images/cover/）
    refs.json          # 参考文献元数据（标题/作者/年份/发表/arXiv/DOI）
    cites.js           # 由 gen_appendix.py 生成：正文 [@key] → 附录 D 的编号
    assets/            # 离线 MathJax（tex-svg-full.js）
    requirements.txt
    build-pdf.bat      # Windows 一键构建
  code/                # 每章插图代码（book/code/chNN/fig_chNN.py，共用 figstyle.py）
  images/              # 插图与封面（NN 为章号）
  front/ chapters/ appendix/   # 书稿：前后辅文 / 正文 / 附录
output/
  parametric-human-models.pdf    # 成书（约 18 MB，< 20 MB）
```

## 一键构建

Windows 下双击 `build-pdf.bat`。或手动：

```bash
python gen_appendix.py     # 先刷新附录 C/D 与 cites.js
python build_book.py       # 再出 PDF（图会自动压成 JPEG，超 20 MB 会继续降质量）
python make_covers.py      # 仅在需要改封面时运行
```

依赖：Python 3.12、Chrome 或 Edge、`pip install -r requirements.txt`。

## 要点

- 正文里的图片写成 `../images/NN/xxx.png`：这样 GitHub 网页端直接点开 md 也能显示；PDF 构建时会临时把它们替换成本机压缩后的 JPEG。
- 附录 C/D 的表格是**写进 md 文件**的（不是构建时替换的），因为网页端读的是同一份 md。
- 引用的编号按全书首次出现顺序自动生成；改完正文引用后务必重跑 `gen_appendix.py`，否则编号与附录 D 不符。
- PDF 体积控制：插图 `max_w=1400、JPEG q=82`；若超过 20 MB，`build_book.py` 会自动降到 74/66/58 重建。
