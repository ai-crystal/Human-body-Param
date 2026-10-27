# -*- coding: utf-8 -*-
"""生成附录 C 的时间线表格、附录 D 的参考文献表，以及站点用的引用编号表。

为什么要生成到 Markdown 里：
    PDF 构建时可以用占位符替换，但 GitHub 网页端（docsify）读的是同一份 md，
    占位符不会被填。所以把这两张表直接写回 md，PDF 与网页共用同一份内容。

用法:
    python gen_appendix.py
幂等：内容写在 <!--TIMELINE-->…<!--/TIMELINE--> 与 <!--REFS-->…<!--/REFS--> 之间，
      每次重跑只替换这段，不重复追加。
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)
ROOT = os.path.dirname(BOOK)
CFG = json.load(open(os.path.join(BOOK, "config.json"), encoding="utf-8"))
REFS = os.path.join(HERE, "refs.json")
CITES_JS = os.path.join(HERE, "cites.js")


def esc(s):
    return html.escape(str(s), quote=False)


def load_refs():
    items = json.load(open(REFS, encoding="utf-8"))
    return {it["key"]: it for it in items}


def reading_order():
    files = []
    for part in CFG["parts"]:
        files += ["chapters/" + f for f in part["chapters"]]
    return files


def collect_citations(meta):
    order, seen = [], set()
    for rel in reading_order():
        txt = open(os.path.join(BOOK, rel), encoding="utf-8").read()
        for m in re.finditer(r"\[@([A-Za-z0-9_,;\s]+)\]", txt):
            for k in re.split(r"[,;]\s*", m.group(1)):
                k = k.strip()
                if k and k not in seen:
                    seen.add(k); order.append(k)
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
    else:
        if start in txt:
            txt = txt.replace(start, block)
        else:
            txt = txt.rstrip() + "\n\n" + block + "\n"
    open(path, "w", encoding="utf-8").write(txt)


def main():
    meta = load_refs()
    order = collect_citations(meta)
    num = {k: i + 1 for i, k in enumerate(order)}

    # ---- 附录 D ----
    refs = "\n".join(ref_html(k, num[k], meta[k]) for k in order)
    replace_block(os.path.join(BOOK, "appendix", "appD.md"),
                  "<!--REFS-->", "<!--/REFS-->", refs)

    # ---- 附录 C 时间线 ----
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
    replace_block(os.path.join(BOOK, "appendix", "appC.md"),
                  "<!--TIMELINE-->", "<!--/TIMELINE-->", table)

    # ---- 站点用：key -> 编号 ----
    payload = {k: {"n": num[k], "title": meta[k].get("title", "")} for k in order}
    with open(CITES_JS, "w", encoding="utf-8") as f:
        f.write("// 自动生成（gen_appendix.py）：正文 [@key] -> 附录 D 的编号\n")
        f.write("window.CITES = " + json.dumps(payload, ensure_ascii=False) + ";\n")

    print("引用 %d 条；时间线 %d 行；已写入 appC.md / appD.md / cites.js" % (len(order), len(rows)))


if __name__ == "__main__":
    main()
