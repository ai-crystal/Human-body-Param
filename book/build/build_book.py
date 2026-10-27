# -*- coding: utf-8 -*-
"""把 book/ 下的 Markdown 编译为 PDF（输出到 output/）。

用法:
    python build_book.py            # 完整构建（图片压缩 + 两遍排版 + 页码 + 书签 + 字体子集化）
    python build_book.py --html     # 只生成 HTML 预览
    python build_book.py --q 74     # 指定插图 JPEG 质量（默认 82）

目录约定:
    book/front/      封面、扉页、版权页、前言、篇首、后记、封底
    book/chapters/   正文（ch01.md …）
    book/appendix/   附录
    book/images/NN/  插图（正文里的路径写作 ../images/NN/xxx.png）
    book/code/chNN/  绘图代码
    book/build/      本脚本、make_covers.py、refs.json、assets/
    output/          成书 PDF
"""
import os, re, sys, json, glob, time, hashlib
from collections import OrderedDict

import markdown
from markdown.extensions.toc import TocExtension

HERE = os.path.dirname(os.path.abspath(__file__))          # book/build
BOOK = os.path.dirname(HERE)                               # book
ROOT = os.path.dirname(BOOK)                               # 仓库根
CH = os.path.join(BOOK, "chapters")
FRONT = os.path.join(BOOK, "front")
APP = os.path.join(BOOK, "appendix")
IMG = os.path.join(BOOK, "images")
OUT = os.path.join(ROOT, "output")
REFS = os.path.join(HERE, "refs.json")
MATHJAX = os.path.join(HERE, "assets", "tex-svg-full.js")
MATHJAX_URI = "file:///" + MATHJAX.replace(os.sep, "/")

# 构建中间产物：私有目录优先，公开仓库回落到 book/.build（已 gitignore）
WORK = os.path.join(ROOT, "_private", "build") if os.path.isdir(os.path.join(ROOT, "_private")) \
    else os.path.join(BOOK, ".build")
os.makedirs(WORK, exist_ok=True)
OUTDIR = OUT
os.makedirs(OUTDIR, exist_ok=True)

CFG = json.load(open(os.path.join(BOOK, "config.json"), encoding="utf-8"))
PDF_NAME = "parametric-human-models.pdf"
COVER_FRONT = os.path.join(IMG, "cover", "cover_front.jpg")
COVER_BACK = os.path.join(IMG, "cover", "cover_back.jpg")

CITED = OrderedDict()      # key -> 编号（按正文首次出现）
HEADINGS = []              # (id, level, text)


# ------------------------------------------------------------------ 参考文献
def load_refs():
    if not os.path.exists(REFS):
        return {}
    items = json.load(open(REFS, encoding="utf-8"))
    return {it["key"]: it for it in items}


PAPERMETA = load_refs()


def cite_html(keys):
    out = []
    for k in keys:
        k = k.strip()
        if not k:
            continue
        if k not in PAPERMETA:
            print("  ! 未在 refs.json 中的引用:", k)
        if k not in CITED:
            CITED[k] = len(CITED) + 1
        out.append(f'<a class="cite" href="#ref-{CITED[k]}">[{CITED[k]}]</a>')
    return "".join(out)


def repl_cite(m):
    return cite_html(re.split(r"[,;]\s*", m.group(1)))


def author_str(r):
    au = r.get("authors") or []
    if not au:
        return ""
    if len(au) > 3:
        return ", ".join(au[:3]) + ", et al."
    return ", ".join(au)


def ref_entry(k, n):
    r = PAPERMETA.get(k, {})
    title = r.get("title") or k
    au = author_str(r)
    venue = r.get("venue") or ""
    year = r.get("year") or ""
    extra = ""
    if r.get("arxiv"):
        extra = f' arXiv:{r["arxiv"]}'
    elif r.get("doi"):
        extra = f' DOI:{r["doi"]}'
    s = (f'{au}. ' if au else '') + f'<i>{esc(title)}</i>. '
    if venue:
        s += f'<span class="venue">{esc(venue)}, {year}.</span>'
    elif year:
        s += f'<span class="venue">{year}.</span>'
    s += extra
    return f'<div class="ref" id="ref-{n}"><span class="num">[{n}]</span>{s}</div>'


def build_refs():
    if not CITED:
        return "<p>（暂无引用）</p>"
    return "\n".join(ref_entry(k, n) for k, n in sorted(CITED.items(), key=lambda kv: kv[1]))


def timeline_table():
    rows = []
    for k, r in PAPERMETA.items():
        y = r.get("year") or ""
        if not str(y).isdigit() or not r.get("have"):
            continue
        rows.append((int(y), k, r))
    rows.sort()
    trs = []
    for y, k, r in rows:
        n = CITED.get(k)
        cite = f'<a class="cite" href="#ref-{n}">[{n}]</a>' if n else ""
        trs.append(f"<tr><td>{y}</td><td>{esc(r.get('title',''))}{cite}</td>"
                   f"<td>{esc(r.get('venue',''))}</td></tr>")
    return ('<table><thead><tr><th style="width:12%">年份</th><th>论文</th>'
            '<th style="width:22%">发表</th></tr></thead><tbody>' + "\n".join(trs) +
            "</tbody></table>")


# ------------------------------------------------------------------ 图片压缩
_IMAP = {}


def prepare_images(quality=82, max_w=1400):
    """把 PNG 插图转成压缩 JPEG（缓存到 WORK/img），返回 {相对 book/images 的路径: file URI}。"""
    from PIL import Image
    cache = os.path.join(WORK, "img")
    os.makedirs(cache, exist_ok=True)
    mapping = {}
    files = []
    for pat in ("*/*.png", "*/*.jpg", "*.png", "*.jpg"):
        files += glob.glob(os.path.join(IMG, pat))
    for src in sorted(set(files)):
        rel = os.path.relpath(src, IMG).replace("\\", "/")
        stem = re.sub(r"[^0-9A-Za-z]+", "-", rel)[:60]
        tag = hashlib.md5(f"{rel}|{quality}|{max_w}".encode()).hexdigest()[:8]
        dst = os.path.join(cache, f"{stem}-q{quality}-{tag}.jpg")
        if not os.path.exists(dst):
            try:
                im = Image.open(src).convert("RGB")
                if im.width > max_w:
                    im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
                im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
            except Exception as e:
                print("  ! 图片压缩失败", rel, e)
                dst = src
        mapping[rel] = "file:///" + dst.replace("\\", "/")
    print(f"图片压缩：{len(mapping)} 张（q={quality}, max_w={max_w}）")
    return mapping


def img_uri(rel):
    return _IMAP.get(rel, "file:///" + os.path.join(IMG, rel).replace("\\", "/"))


# ------------------------------------------------------------------ Markdown
def protect_math(text):
    box = []

    def keep(m):
        box.append(m.group(0))
        return f"@@MATH{len(box)-1}@@"

    codes = []

    def keep_code(m):
        codes.append(m.group(0))
        return f"@@CODE{len(codes)-1}@@"

    text = re.sub(r"```.*?```", keep_code, text, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$", keep, text, flags=re.S)
    text = re.sub(r"(?<!\\)\$[^$\n]+?\$", keep, text)
    for i, c in enumerate(codes):
        text = text.replace(f"@@CODE{i}@@", c)
    return text, box


def restore_math(html_text, box):
    for i, m in enumerate(box):
        html_text = html_text.replace(f"@@MATH{i}@@", m)
    return html_text


def md2html(text):
    text, box = protect_math(text)
    md = markdown.Markdown(extensions=[
        "extra", "sane_lists", "md_in_html", "attr_list", "tables", "footnotes",
        "admonition", TocExtension(baselevel=1, permalink=False),
    ], extension_configs={"toc": {"toc_depth": "1-3"}})
    out = md.convert(text)
    out = restore_math(out, box)
    out = re.sub(r"\[@([A-Za-z0-9_,;\s]+)\]", repl_cite, out)
    return out


def add_heading_ids(html_text, chap_id, part=False):
    counters = [0]

    def sub(m):
        level, attrs, inner = int(m.group(1)), m.group(2), m.group(3)
        attrs = re.sub(r'\s*id="[^"]*"', "", attrs)
        plain = re.sub(r"<[^>]+>", "", re.sub(r"⟦[^⟧]+⟧", "", inner)).strip()
        if level == 1:
            hid = chap_id
        else:
            counters[0] += 1
            hid = f"{chap_id}-s{counters[0]}"
        HEADINGS.append((hid, level, plain))
        mark = f'<span class="pgmark">⟦{hid}⟧</span>'
        return f'<h{level} id="{hid}"{attrs}>{mark}{inner}</h{level}>'

    return re.sub(r"<h([123])([^>]*)>(.*?)</h\1>", sub, html_text, flags=re.S)


def rewrite_images(raw):
    """../images/NN/x.png -> 本机构建好的压缩 JPEG 的 file URI。"""
    return re.sub(r"\.\./images/([^\"')\s]+)",
                  lambda m: img_uri(m.group(1)), raw)


def render_page(rel, kind="chapter"):
    """rel 相对 book/，例如 chapters/ch07.md。"""
    path = os.path.join(BOOK, rel)
    if not os.path.exists(path):
        print("  ! 缺少文件", rel)
        return None
    raw = open(path, encoding="utf-8").read()
    title_m = re.search(r"^#\s+(.+)$", raw, flags=re.M)
    title = title_m.group(1).strip() if title_m else os.path.basename(rel)
    raw = rewrite_images(raw)
    body = md2html(raw)
    pid = os.path.splitext(os.path.basename(rel))[0]
    body = add_heading_ids(body, pid)
    if kind == "chapter":
        body = re.sub(r'<h1 id="%s">(.*?)</h1>' % pid,
                      lambda m: f'<div class="chap-open"><h1 id="{pid}">{m.group(1)}</h1></div>',
                      body, count=1, flags=re.S)
    elif kind == "part":
        body = f'<section class="part">{body}</section>'
    elif kind == "front":
        base = pid
        if base in ("titlepage", "copyright", "afterword", "cover", "backcover"):
            body = f'<div class="{base}">{body}</div>'
    elif kind == "appendix":
        body = re.sub(r'<h1 id="%s">(.*?)</h1>' % pid,
                      lambda m: f'<div class="chap-open appendix-open"><h1 id="{pid}">{m.group(1)}</h1></div>',
                      body, count=1, flags=re.S)
    return dict(id=pid, title=title, html=body, kind=kind)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ------------------------------------------------------------------ CSS
CSS = r"""
@page { size: A4; margin: 21mm 19mm 19mm 19mm; }

:root{
  --ink:#1F2937; --muted:#5B6472; --faint:#8A93A0;
  --accent:#B45309; --accent2:#C2410C; --line:#E5E0D8; --paper:#FFFFFF;
}
*{ box-sizing:border-box; }
html,body{ margin:0; padding:0; }
body{
  font-family:"SimSun","Source Han Serif SC","SimSun",serif;
  font-size:10.4pt; line-height:1.85; color:var(--ink);
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
p{ margin:.42em 0; text-indent:2em; text-align:justify; hyphens:auto; }
p.noindent, .noindent{ text-indent:0; }
strong{ font-weight:700; color:#111827; }
em{ font-style:normal; color:var(--accent2); font-weight:600; }
a{ color:inherit; text-decoration:none; }
sup{ font-size:.75em; }

/* ---------- 分页标记（供两遍排版取页码，视觉上不可见） ---------- */
.pgmark{ font-size:0.6pt; color:#FFFFFF; letter-spacing:0; }

/* ---------- 扉页 ---------- */
.titlepage{ page-break-after:always; height:240mm; padding-top:72mm; text-align:center; }
.titlepage h1{ font-size:34pt; letter-spacing:.14em; margin:0 0 10mm; border:none; padding:0; text-indent:0; }
.titlepage p{ text-indent:0; text-align:center; }
.titlepage p:nth-of-type(1){ font-family:"Microsoft YaHei",sans-serif; font-size:12.5pt;
  color:var(--muted); letter-spacing:.06em; }
.titlepage p:nth-of-type(2){ margin-top:42mm; font-size:14pt; letter-spacing:.18em; }
.titlepage p:nth-of-type(3){ margin-top:7mm; font-family:"Microsoft YaHei",sans-serif;
  font-size:9.6pt; color:var(--faint); letter-spacing:.1em; }

/* ---------- 版权页 ---------- */
.copyright{ page-break-after:always; padding-top:140mm; font-family:"Microsoft YaHei",sans-serif;
  font-size:9.2pt; color:var(--muted); line-height:2.0; }
.copyright p{ text-indent:0; margin:.5em 0; }
.copyright strong{ color:#374151; }

/* ---------- 目录 ---------- */
.toc{ page-break-before:always; page-break-after:always; }
.toc h1{ font-family:"Microsoft YaHei",sans-serif; font-size:22pt; font-weight:600;
  margin:0 0 8mm; padding-bottom:3mm; border-bottom:2pt solid var(--accent); text-indent:0; }
.toc .tocpart{ font-family:"Microsoft YaHei",sans-serif; font-size:10.5pt; font-weight:700;
  page-break-after:avoid; margin:5mm 0 1.6mm; color:var(--accent); letter-spacing:.05em; }
.toc .row{ overflow:hidden; border-bottom:.5pt dotted #DCD5C9; padding:.9mm 0 .8mm; }
.toc .l1{ font-family:"Microsoft YaHei",sans-serif; font-size:9.6pt; font-weight:600; margin-top:1.8mm; }
.toc .l2{ font-size:8.8pt; margin-left:7mm; color:#374151; }
.toc .tt{ display:block; padding-right:12mm; }
.toc .pg{ float:right; font-family:"Microsoft YaHei",sans-serif; font-size:8.8pt; color:var(--muted); min-width:8mm; text-align:right; }

/* ---------- 篇章页 ---------- */
.part{ page-break-before:always; page-break-after:always; min-height:210mm; padding-top:52mm; }
.part h1{ font-family:"SimSun",serif; font-size:27pt; margin:0 0 6mm; text-indent:0;
  letter-spacing:.08em; border:none; padding:0; }
.part blockquote{ border:none; background:none; padding:0; margin:0 0 14mm; color:var(--muted);
  font-size:10.5pt; line-height:1.9; max-width:112mm; }
.part ul{ list-style:none; margin:0; padding:0; font-family:"Microsoft YaHei",sans-serif;
  font-size:9.4pt; line-height:2.05; color:#4B5563; }
.part li{ margin:0; text-align:left; }
.part li::before{ content:""; }

/* ---------- 章节 ---------- */
.chap-open{ page-break-before:always; margin:0 0 8mm; padding-top:14mm; }
.chap-open::before{ content:""; display:block; width:26mm; height:2pt; background:var(--accent);
  margin-bottom:7mm; }
h1{ font-family:"SimSun",serif; font-size:24pt; line-height:1.4; font-weight:700;
  margin:0 0 6mm; text-indent:0; letter-spacing:.02em; }
h2{ font-family:"Microsoft YaHei",sans-serif; font-size:13.6pt; font-weight:600; margin:9mm 0 3mm;
  padding-left:3mm; border-left:3pt solid var(--accent); text-indent:0; page-break-after:avoid;
  line-height:1.5; }
h3{ font-family:"Microsoft YaHei",sans-serif; font-size:11pt; font-weight:600; margin:6mm 0 2mm;
  color:#374151; text-indent:0; page-break-after:avoid; }
h4{ font-family:"Microsoft YaHei",sans-serif; font-size:10.2pt; font-weight:600; margin:4mm 0 1.5mm;
  color:#4B5563; text-indent:0; }

blockquote{
  margin:5mm 0; padding:4mm 5mm; background:#FBF7F0; border-left:2.5pt solid #D9B48F;
  font-family:"Microsoft YaHei",sans-serif; font-size:9.3pt; line-height:1.85; color:#4B5563;
  page-break-inside:avoid;
}
blockquote p{ text-indent:0; margin:.2em 0; }
blockquote strong{ color:var(--accent); }

ul,ol{ margin:.4em 0 .6em 1.4em; padding-left:1em; }
li{ margin:.18em 0; text-align:justify; }
li p{ text-indent:0; }

hr{ border:none; border-top:.5pt solid var(--line); margin:7mm 0; }

/* ---------- 图 ---------- */
figure.fig{ margin:6mm 0 7mm; page-break-inside:avoid; text-align:center; }
figure.fig img{ max-width:100%; max-height:110mm; object-fit:contain; }
figure.fig figcaption{
  font-family:"Microsoft YaHei",sans-serif; font-size:8.7pt; color:var(--muted);
  margin-top:2.5mm; line-height:1.65; text-indent:0; text-align:center;
}
figure.fig figcaption b{ color:var(--accent); font-weight:600; }
p img{ max-width:100%; }

/* ---------- 表 ---------- */
table{ border-collapse:collapse; width:100%; margin:5mm 0; font-size:8.7pt;
  font-family:"Microsoft YaHei",sans-serif; page-break-inside:auto; }
tr{ page-break-inside:avoid; }
thead{ display:table-header-group; }
th,td{ border-bottom:.5pt solid #D1D5DB; padding:1.7mm 2mm; text-align:left; vertical-align:top; }
th{ background:#F5F1EA; font-weight:600; border-top:1pt solid #9CA3AF; }
tr:nth-child(even) td{ background:#FCFAF6; }

/* ---------- 代码 ---------- */
pre{ background:#F7F7F5; border:.5pt solid #E5E7EB; border-radius:2pt; padding:3mm 4mm;
  font-family:"Cascadia Mono","Consolas","Noto Sans Mono",monospace; font-size:8pt;
  line-height:1.6; overflow:auto; page-break-inside:avoid; margin:4mm 0; }
code{ font-family:"Cascadia Mono","Consolas",monospace; font-size:8.6pt; background:#F3F4F6;
  padding:0 1mm; border-radius:2pt; }
pre code{ background:none; padding:0; font-size:inherit; }

/* ---------- 公式 ---------- */
mjx-container{ font-size:100% !important; }
mjx-container[display="true"]{ margin:3.2mm 0 !important; }

/* ---------- 引用与参考文献 ---------- */
a.cite{ color:var(--accent2); font-family:"Microsoft YaHei",sans-serif; font-size:7.8pt;
  vertical-align:super; line-height:0; }
.ref{ font-size:8.6pt; line-height:1.62; margin:0 0 1.6mm; padding-left:11mm; text-indent:-11mm;
  font-family:"Microsoft YaHei",sans-serif; }
.ref .num{ color:var(--accent); margin-right:2mm; }
.ref .venue{ color:var(--muted); }
.ref i{ font-style:italic; }

/* ---------- 后记 ---------- */
.afterword{ page-break-before:always; }
.afterword p:nth-last-of-type(-n+2){ text-indent:0; text-align:right;
  font-family:"Microsoft YaHei",sans-serif; font-size:10pt; color:var(--muted); line-height:1.9; }
.afterword p:last-of-type{ margin-top:1mm; }
"""


# ------------------------------------------------------------------ 组装
def build_html(pagemap=None):
    """pagemap 非空时用于目录页码（第二遍）。"""
    HEADINGS.clear()
    CITED.clear()
    front = []
    for rel in CFG.get("front", []):
        p = render_page(rel, kind="front")
        if p:
            front.append(p)

    parts = []
    for part in CFG["parts"]:
        pg = render_page(part["page"], kind="part") if part.get("page") else None
        chs = [render_page("chapters/" + fn) for fn in part["chapters"]]
        parts.append((part, pg, [c for c in chs if c]))

    apps = [render_page("appendix/" + fn, kind="appendix") for fn in CFG.get("appendices", [])]
    apps = [a for a in apps if a]
    back = [render_page(rel, kind="front") for rel in CFG.get("back", [])]
    back = [b for b in back if b]

    if pagemap:
        ids = [c["id"] for _, _, chs in parts for c in chs]
        firsts = [pagemap[i] for i in ids if i in pagemap]
        off = (min(firsts) - 1) if firsts else 0
        pagemap = {k: v - off for k, v in pagemap.items()}

    # ---- 目录 ----
    toc = ['<section class="toc"><h1>目　录</h1>']
    for p in front:
        if p["id"] in ("preface",):
            _fp = (pagemap or {}).get(p["id"], "")
            if isinstance(_fp, int) and _fp < 1:
                _fp = ""
            toc.append(f'<div class="row l1"><span class="pg">{_fp}</span>'
                       f'<span class="tt">{esc(re.sub(r"\s+", " ", p["title"]))}</span></div>')
    for part, pg, chs in parts:
        toc.append(f'<div class="tocpart">{esc(part["no"])}　{esc(part["title"].replace(part["no"], "").strip())}</div>')
        for c in chs:
            num = re.match(r"第\s*(\d+)\s*章", c["title"])
            short = re.sub(r"^第\s*\d+\s*章\s*", "", c["title"])
            p = (pagemap or {}).get(c["id"], "")
            if isinstance(p, int) and p < 1:
                p = ""
            toc.append(f'<div class="row l1"><span class="pg">{p}</span>'
                       f'<span class="tt">{esc(num.group(1)) if num else ""}　{esc(short)}</span></div>')
            for m in re.finditer(r'<h2 id="([^"]+)"[^>]*>.*?⟦[^⟧]+⟧(.*?)</h2>', c["html"], flags=re.S):
                hid, t = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
                t = re.sub(r"^\d+(\.\d+)*\s*", "", t)
                p2 = (pagemap or {}).get(hid, "")
                toc.append(f'<div class="row l2"><span class="pg">{p2}</span>'
                           f'<span class="tt">{esc(t)}</span></div>')
    for b in back:
        pgno = (pagemap or {}).get(b["id"], "")
        if isinstance(pgno, int) and pgno < 1:
            pgno = ""
        toc.append(f'<div class="row l1" style="margin-top:4mm"><span class="pg">{pgno}</span>'
                   f'<span class="tt">{esc(re.sub(r"\s+", " ", b["title"]))}</span></div>')
    if apps:
        toc.append('<div class="tocpart">附　录</div>')
        for c in apps:
            p = (pagemap or {}).get(c["id"], "")
            if isinstance(p, int) and p < 1:
                p = ""
            toc.append(f'<div class="row l1"><span class="pg">{p}</span>'
                       f'<span class="tt">{esc(c["title"])}</span></div>')
    toc.append("</section>")

    # ---- 正文 ----
    body = [p["html"] for p in front]
    body += toc
    for part, pg, chs in parts:
        if pg:
            body.append(pg["html"])
        body += [c["html"] for c in chs]
    body += [c["html"] for c in apps]
    body += [b["html"] for b in back]

    body_html = "\n".join(body)
    # 附录 C/D 的表格由 gen_appendix.py 直接写进 md（GitHub 网页端也要读同一份）

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>{esc(CFG['title'])}</title>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['$','$']], displayMath: [['$$','$$']], tags: 'none',
          macros: {{ RR: '\\\\mathbb{{R}}', bm: ['\\\\boldsymbol{{#1}}',1], T: '^\\\\top' }} }},
  svg: {{ fontCache: 'global', scale: 0.98 }},
  options: {{ enableMenu: false }},
  startup: {{
    ready() {{
      MathJax.startup.defaultReady();
      MathJax.startup.promise.then(() => {{ window.__mjdone = true; }});
    }}
  }}
}};
</script>
<script src="{MATHJAX_URI}" id="MathJax-script"></script>
<style>{CSS}</style>
</head><body>
{body_html}
</body></html>"""
    out = os.path.join(WORK, "_build.html")
    open(out, "w", encoding="utf-8").write(html_doc)
    print("HTML ->", out, len(html_doc) // 1024, "KB")
    return out, parts, apps


# ------------------------------------------------------------------ PDF
def render_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    url = "file:///" + html_path.replace("\\", "/")
    args = ["--allow-file-access-from-files", "--font-render-hinting=none"]
    with sync_playwright() as p:
        b = None
        for kw in ({"channel": "chrome"}, {"channel": "msedge"}, {}):
            try:
                b = p.chromium.launch(headless=True, args=args, **kw)
                break
            except Exception:
                continue
        if b is None:
            raise RuntimeError("找不到可用浏览器：请安装 Chrome 或 Edge。")
        pg = b.new_page()
        pg.goto(url, wait_until="load", timeout=240000)
        pg.wait_for_function("window.__mjdone === true", timeout=240000)
        pg.wait_for_function(
            "Promise.all(Array.from(document.images).map(i => i.complete ? 1 : new Promise(r => {i.onload=r;i.onerror=r;}))).then(()=>true)",
            timeout=180000)
        pg.evaluate("document.fonts.ready.then(()=>true)")
        time.sleep(1.0)
        pg.pdf(path=pdf_path, format="A4", print_background=True,
               prefer_css_page_size=True, display_header_footer=False)
        b.close()
    print("PDF ->", pdf_path)


def read_pagemap(pdf_path):
    import pymupdf
    doc = pymupdf.open(pdf_path)
    pm = {}
    pat = re.compile(r"⟦([A-Za-z0-9\-]+)⟧")
    for i, page in enumerate(doc):
        for m in pat.finditer(page.get_text()):
            pm.setdefault(m.group(1), i + 1)
    doc.close()
    return pm


def decorate(pdf_path, pagemap, parts, apps, headings):
    import pymupdf
    doc = pymupdf.open(pdf_path)
    # 章节/篇首/附录起始页
    anchors = []
    for part, pg, chs in parts:
        if pg and pg["id"] in pagemap:
            anchors.append((pagemap[pg["id"]], pg["id"], part["no"] + "　" + part["title"].replace(part["no"], "").strip()))
        for c in chs:
            if c["id"] in pagemap:
                anchors.append((pagemap[c["id"]], c["id"], c["title"]))
    for c in apps:
        if c["id"] in pagemap:
            anchors.append((pagemap[c["id"]], c["id"], c["title"]))
    anchors.sort()
    if not anchors:
        return
    start = anchors[0][0]
    offset = start - 1

    for i, page in enumerate(doc):
        if i == 0 or i + 1 < start or i == len(doc) - 1:
            continue
        cur = None
        for pno, pid, title in anchors:
            if pno <= i + 1:
                cur = title
            else:
                break
        if cur:
            m = re.match(r"第\s*(\d+)\s*章", cur)
            t = (f"第 {m.group(1)} 章　{re.sub(r'^第\s*\d+\s*章\s*', '', cur)}") if m else cur
            page.insert_text((19 * 72 / 25.4, 12.5 * 72 / 25.4), t,
                             fontname="china-s", fontsize=7.6, color=(0.55, 0.55, 0.58))
        n = i + 1 - offset
        s = f"— {n} —"
        w = pymupdf.get_text_length(s, fontname="china-s", fontsize=8.5)
        page.insert_text(((210 * 72 / 25.4 - w) / 2, 288 * 72 / 25.4), s,
                         fontname="china-s", fontsize=8.5, color=(0.45, 0.45, 0.5))

    toc = [[1, "封面", 1], [1, "扉页", 2]]
    for pno, pid, title in anchors:
        toc.append([1, re.sub(r"\s+", " ", title), pno])
    for hid, level, text in headings:
        if level == 2 and hid in pagemap:
            toc.append([2, text, pagemap[hid]])
    toc.sort(key=lambda x: (x[2], x[0]))
    doc.set_toc(toc)
    doc.set_metadata({"title": CFG["title"], "author": CFG["author"],
                      "subject": CFG["subtitle"], "creator": "Markdown + Chromium"})
    tmp = pdf_path + ".tmp"
    doc.save(tmp, garbage=4, deflate=True, clean=True)
    doc.close()
    atomic_replace(tmp, pdf_path)
    chk = pymupdf.open(pdf_path); npages = chk.page_count; chk.close()   # 用完必须关，否则 Windows 锁文件
    print("decorated ->", pdf_path, "pages:", npages)


def add_covers(body_pdf, out_pdf):
    import pymupdf
    body = pymupdf.open(body_pdf)
    rect = body[0].rect
    doc = pymupdf.open()
    for img in (COVER_FRONT, None, COVER_BACK):
        if img is None:
            doc.insert_pdf(body)
            continue
        page = doc.new_page(width=rect.width, height=rect.height)
        if os.path.exists(img):
            page.insert_image(page.rect, filename=img)
        else:
            print("  ! 缺少封面图", img)
    doc.set_metadata({"title": CFG["title"], "author": CFG["author"],
                      "subject": CFG["subtitle"]})
    tmp = out_pdf + ".new"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close(); body.close()
    atomic_replace(tmp, out_pdf)  # Windows 下直接覆盖已存在的 PDF 可能被占用
    print("covers merged ->", out_pdf)


def finalize(pdf_path):
    """字体子集化 + 清理，尽量压小体积。"""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    try:
        doc.subset_fonts(verbose=False)
    except Exception as e:
        print("  ! 字体子集化跳过:", e)
    tmp = pdf_path + ".tmp"
    # garbage=4 + clean 在 200 页中文 PDF 上要 2~3 分钟，收益却几乎为零，故用 3 + deflate
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    atomic_replace(tmp, pdf_path)
    chk = pymupdf.open(pdf_path); npages = chk.page_count; chk.close()
    print("font subset done:", npages, "pages,", round(os.path.getsize(pdf_path) / 1e6, 2), "MB")


def build_once(quality, max_w=1400):
    global _IMAP
    _IMAP = prepare_images(quality, max_w)
    html_path, parts, apps = build_html(None)
    pass1 = os.path.join(WORK, "_pass1.pdf")
    render_pdf(html_path, pass1)
    pm = read_pagemap(pass1)
    print("pagemap entries:", len(pm))
    if pm:
        html_path, parts, apps = build_html(pm)
    body_pdf = os.path.join(WORK, "_body.pdf")
    render_pdf(html_path, body_pdf)
    pm2 = read_pagemap(body_pdf)
    target = os.path.join(OUTDIR, PDF_NAME)
    add_covers(body_pdf, target)
    decorate(target, {k: v + 1 for k, v in pm2.items()}, parts, apps, HEADINGS)
    finalize(target)
    for f in (pass1, body_pdf):
        try:
            os.remove(f)
        except OSError:
            pass
    return target


def atomic_replace(src, dst, tries=12, delay=0.5):
    """Windows 上目标文件常被杀毒/索引短暂占用，重试替换。"""
    last = None
    for _ in range(tries):
        try:
            os.replace(src, dst)
            return True
        except PermissionError as e:
            last = e
            try:
                if os.path.exists(dst):
                    os.chmod(dst, 0o666)
                    os.remove(dst)
                    os.replace(src, dst)
                    return True
            except Exception:
                pass
            time.sleep(delay)
    raise last


def main():
    if "--html" in sys.argv:
        prepare_images(82, 1400)
        build_html(None)
        return
    quality = 82
    if "--q" in sys.argv:
        quality = int(sys.argv[sys.argv.index("--q") + 1])
    target = build_once(quality)
    size_mb = os.path.getsize(target) / 1e6
    print("成书:", target, round(size_mb, 2), "MB")
    if size_mb > 20:
        for q in (74, 66, 58):
            print(f"超过 20 MB，降质量重build：q={q}")
            target = build_once(q)
            size_mb = os.path.getsize(target) / 1e6
            print("成书:", round(size_mb, 2), "MB")
            if size_mb <= 20:
                break


if __name__ == "__main__":
    main()
