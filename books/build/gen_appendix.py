# -*- coding: utf-8 -*-
"""为每一册生成附录里的参考文献表、时间线表，以及站点用的引用编号表。

为什么写回 Markdown 而不是排版时替换：
    PDF 构建时可以用占位符替换，但 GitHub 网页端（docsify）读的是同一份 md，
    占位符不会被填。所以把表直接写回 md，PDF 与网页共用同一份内容。

用法:
    python gen_appendix.py              # 全部册
    python gen_appendix.py --book math  # 只处理一册

幂等：内容写在 <!--REFS-->…<!--/REFS--> 与 <!--TIMELINE-->…<!--/TIMELINE--> 之间，
      每次重跑只替换这段，不重复追加。
"""
import os, re, sys, json, html, argparse

HERE = os.path.dirname(os.path.abspath(__file__))     # books/build
BOOKS = os.path.dirname(HERE)                          # books
ROOT = os.path.dirname(BOOKS)                          # 仓库根
REFS = os.path.join(HERE, "refs.json")
CITES_JS = os.path.join(HERE, "cites.js")


def esc(s):
    return html.escape(str(s), quote=False)


def load_refs():
    items = json.load(open(REFS, encoding="utf-8"))
    return {it["key"]: it for it in items}


def books():
    out = []
    for d in sorted(os.listdir(BOOKS)):
        p = os.path.join(BOOKS, d)
        if os.path.isfile(os.path.join(p, "book.json")):
            cfg = json.load(open(os.path.join(p, "book.json"), encoding="utf-8"))
            out.append((cfg.get("order", 999), p))
    out.sort()
    return [p for _, p in out]


def reading_order(bookdir):
    st = json.load(open(os.path.join(bookdir, "structure.json"), encoding="utf-8"))
    files = []
    for part in st.get("parts", []):
        files += ["chapters/" + f for f in part.get("chapters", [])]
    return files


def collect(bookdir, meta):
    order, seen = [], set()
    for rel in reading_order(bookdir):
        p = os.path.join(bookdir, rel)
        if not os.path.exists(p):
            print("  ! 缺少", rel)
            continue
        txt = open(p, encoding="utf-8").read()
        for m in re.finditer(r"\[@([A-Za-z0-9_,;\s]+)\]", txt):
            for k in re.split(r"[,;]\s*", m.group(1)):
                k = k.strip()
                if k and k not in seen:
                    seen.add(k)
                    order.append(k)
    missing = [k for k in order if k not in meta]
    if missing:
        print("  ! 引用了但 refs.json 里没有:", missing)
    return order


def author_str(r):
    au = r.get("authors") or []
    if not au:
        return ""
    txt = ", ".join(au[:3]) + ", et al." if len(au) > 3 else ", ".join(au)
    return txt.rstrip(".")


def ref_html(k, n, r):
    title = r.get("title") or k
    au = author_str(r)
    venue, year = r.get("venue") or "", r.get("year") or ""
    extra = f' arXiv:{r["arxiv"]}' if r.get("arxiv") else (f' DOI:{r["doi"]}' if r.get("doi") else "")
    tail = f'<span class="venue">{esc(venue)}, {esc(year)}.</span>' if venue else \
           (f'<span class="venue">{esc(year)}.</span>' if year else "")
    s = (esc(au) + ". " if au else "") + f"<i>{esc(title)}</i>. " + tail + esc(extra)
    return f'<div class="ref" id="ref-{n}"><span class="num">[{n}]</span>{s}</div>'


def replace_block(path, start, end, content):
    txt = open(path, encoding="utf-8").read()
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    block = f"{start}\n{content}\n{end}"
    if pat.search(txt):
        txt = pat.sub(lambda _: block, txt)
    elif start in txt:
        txt = txt.replace(start, block)
    else:
        txt = txt.rstrip() + "\n\n" + block + "\n"
    open(path, "w", encoding="utf-8").write(txt)


def code_letter(idx):
    return "ABCDEFGH"[idx]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book")
    a = ap.parse_args()
    meta = load_refs()

    targets = books()
    if a.book:
        targets = [t for t in targets
                   if os.path.basename(t) == os.path.basename(a.book.rstrip("/\\"))
                   or t == os.path.abspath(a.book)]
        if not targets:
            raise SystemExit("找不到册：" + a.book)

    site = {}
    for bookdir in targets:
        name = os.path.basename(bookdir)
        order = collect(bookdir, meta)
        num = {k: i + 1 for i, k in enumerate(order)}
        st = json.load(open(os.path.join(bookdir, "structure.json"), encoding="utf-8"))
        apps = st.get("appendices", [])

        for i, fn in enumerate(apps):
            p = os.path.join(bookdir, "appendix", fn)
            if not os.path.exists(p):
                continue
            if fn == "refs.md":
                body = "\n".join(ref_html(k, num[k], meta[k]) for k in order) or "（本册暂无引用）"
                replace_block(p, "<!--REFS-->", "<!--/REFS-->", body)
            elif fn == "timeline.md":
                rows = []
                for k, r in meta.items():
                    y = r.get("year") or ""
                    if not str(y).isdigit() or not r.get("have"):
                        continue
                    rows.append((int(y), k, r))
                rows.sort()
                trs = []
                for y, k, r in rows:
                    n = num.get(k)
                    cite = f' <a class="cite" href="#ref-{n}">[{n}]</a>' if n else ""
                    trs.append(f"<tr><td>{y}</td><td>{esc(r.get('title',''))}{cite}</td>"
                               f"<td>{esc(r.get('venue',''))}</td></tr>")
                table = ('<table><thead><tr><th style="width:12%">年份</th><th>论文</th>'
                         '<th style="width:22%">发表</th></tr></thead><tbody>\n'
                         + "\n".join(trs) + "\n</tbody></table>")
                replace_block(p, "<!--TIMELINE-->", "<!--/TIMELINE-->", table)
        site[name] = {k: {"n": num[k], "title": meta[k].get("title", "")} for k in order}
        print("%-10s 引用 %3d 条，附录 %d 个" % (name, len(order), len(apps)))

    with open(CITES_JS, "w", encoding="utf-8") as f:
        f.write("// 自动生成（gen_appendix.py）：正文 [@key] -> 各册参考文献编号\n")
        f.write("window.CITES_BY_BOOK = " + json.dumps(site, ensure_ascii=False) + ";\n")
    print("已写入 cites.js")


if __name__ == "__main__":
    main()
