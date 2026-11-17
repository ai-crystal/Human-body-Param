# 构建说明

一套构建脚本，服务 `books/` 下的六册。

```text
build.bat                全部构建（先 gen_appendix，再逐册排版）
build.bat math           只构建 math 这一册
build.bat figures        重画全部插图
build.bat list           列出所有册
```

对应的 Python 调用：

```text
python books/build/gen_appendix.py            # 生成各册参考文献与时间线
python books/build/gen_appendix.py --book math
python books/build/build.py --all
python books/build/build.py --book books/math
python books/build/build.py --book math --html    # 只生成 HTML 预览
python books/build/make_covers.py                 # 重新生成六册封面
```

## 目录约定

```text
books/
├── build/            本目录：build.py、gen_appendix.py、make_covers.py、refs.json、assets/katex
├── code/figstyle.py  共用绘图风格
├── <册>/book.json        书名、副标题、作者、输出文件名、册序
├── <册>/structure.json   前后辅文、章序、附录（章序的唯一来源）
├── <册>/front/           扉页、版权页、前言、后记
├── <册>/chapters/        正文 ch01.md …
├── <册>/appendix/        附录（术语、数学补充、时间线、参考文献）
├── <册>/images/NN/       插图（正文里写 ../images/NN/x.png）
├── <册>/code/chNN/       该章的绘图脚本
output/               六册 PDF
```

## 几个要点

- **章序只看 `structure.json`**，不靠文件名排序。
- **图号与章号对齐**：`images/07/fig07-01.png` 对应第 7 章图 1；跨册搬章时要同时改目录名和文件名。
- **页码要收敛**：目录带页码后可能多占一页，`build.py` 会反复「排版 → 取页码 → 再排版」直到稳定（一般两轮）。
- **参考文献按册生成**：每册只列本册引用过的条目，编号从 [1] 开始。
- **中间产物**在 `_private/build/<册>/`，各册分开，交替构建不会互相覆盖。
