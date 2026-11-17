# -*- coding: utf-8 -*-
"""为每一册生成正封与封底（210×297mm，约 290 DPI）。

视觉来源：_private/art/logos 下的三张星际图（logo1/2/3），
正封取 logo3（星云 + 轨道流线），封底取 logo1（银河 + 光束）。
同一套版式，靠分册名与强调色区分六册。

用法: python make_covers.py            # 全部册
      python make_covers.py --book math
输出: books/<册>/images/cover_front.jpg, cover_back.jpg
"""
import base64
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent      # books/build
BOOKS = HERE.parent                         # books
ROOT = BOOKS.parent                         # 仓库根
LOGO_DIR = ROOT / "_private" / "art" / "logos"

# 各册：目录名、卷号、分册名、一句话、强调色
VOLUMES = [
    ("intro",     "01", "入门册", "概念与全局地图", "#F0C07A"),
    ("math",      "02", "数学册", "向量 · PCA · 旋转 · 蒙皮 · 优化", "#9BD6FF"),
    ("body",      "03", "人体册", "SCAPE · SMPL · SMPL 家族", "#8FE3B8"),
    ("recon",     "04", "重建册", "单图 · 视频 · 评估 · 动作", "#C6B4FF"),
    ("face-hand", "05", "脸手册", "3DMM · FLAME · MANO · 交互", "#FFB59B"),
    ("frontier",  "06", "前沿册", "SMAL · 扩散 · 基础模型", "#FFA8C8"),
]


def art(name):
    """把插图转成 data URI：set_content 的页面是 about:blank，file:// 子资源会被拦。"""
    p = LOGO_DIR / name
    if not p.exists():                     # 兼容旧目录
        p = ROOT / "_private" / "art" / "logo_figures" / name
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(p.read_bytes()).decode())


W, H = 794, 1123   # A4 @96dpi 的 CSS 像素
INK = "#F3F7FC"
ICE = "#9BD6FF"
GOLD = "#F0C07A"

BASE_CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{H}px;background:#050912;}}
.page{{
  width:{W}px;height:{H}px;position:relative;overflow:hidden;color:{INK};
  font-family:"Noto Serif SC","Source Han Serif SC","SimSun",serif;
  background:#050912;
}}
.bg{{position:absolute;inset:0;background-repeat:no-repeat;background-size:cover;}}
.scrim{{position:absolute;inset:0;}}
.frame{{position:absolute;inset:30px;border:1px solid rgba(207,232,255,.22);}}
.frame:before{{
  content:"";position:absolute;left:-1px;top:-1px;width:26px;height:26px;
  border-left:2px solid {GOLD};border-top:2px solid {GOLD};opacity:.85;
}}
.frame:after{{
  content:"";position:absolute;right:-1px;bottom:-1px;width:26px;height:26px;
  border-right:2px solid {ICE};border-bottom:2px solid {ICE};opacity:.7;
}}
.inner{{position:absolute;left:78px;right:78px;top:96px;}}
.kicker{{
  font-family:"Noto Sans SC","Microsoft YaHei",sans-serif;
  font-size:10.5px;letter-spacing:6.2px;color:{ICE};font-weight:400;
}}
.rule{{width:36px;height:1.5px;background:{GOLD};margin-top:20px;}}
h1{{
  font-size:76px;line-height:1.26;font-weight:600;letter-spacing:5px;
  color:#FCFEFF;margin-top:120px;
  text-shadow:0 3px 30px rgba(2,7,16,.92), 0 1px 2px rgba(2,7,16,.85), 0 0 46px rgba(4,12,26,.7);
}}
.vol{{font-size:31px;line-height:1.5;letter-spacing:8px;color:__ACC__;margin-top:26px;
  text-shadow:0 2px 20px rgba(2,7,16,.9);}}
.sub{{font-size:29px;line-height:1.5;letter-spacing:7px;color:#EFF7FE;margin-top:26px;
  text-shadow:0 2px 18px rgba(2,7,16,.85);}}
.sub2{{
  font-family:"Noto Sans SC",sans-serif;font-size:14.5px;letter-spacing:5.4px;
  color:rgba(226,242,255,.88);margin-top:16px;text-shadow:0 1px 12px rgba(2,7,16,.8);
}}
.barwrap{{margin-top:62px;}}
.bar{{height:3px;width:100%;
  background:linear-gradient(90deg,{ICE} 0%,#C6B4FF 46%,{GOLD} 100%);opacity:.92;}}
.ticks{{display:flex;justify-content:space-between;margin-top:10px;
  font-family:"Noto Sans SC",sans-serif;font-size:9.2px;letter-spacing:1.4px;
  color:rgba(232,244,255,.82);text-shadow:0 1px 10px rgba(2,7,16,.9);}}
.tag{{font-size:17.5px;line-height:1.95;letter-spacing:2.6px;color:#F3F9FF;margin-top:52px;
  text-shadow:0 2px 16px rgba(2,7,16,.9);padding-left:16px;border-left:2px solid {GOLD};}}
.tag i{{font-style:normal;color:{GOLD};}}
.bottom{{position:absolute;left:78px;right:78px;bottom:86px;}}
.author{{font-size:16px;letter-spacing:4px;color:#FBFDFF;}}
.edition{{font-family:"Noto Sans SC",sans-serif;font-size:10.5px;letter-spacing:2.4px;
  color:rgba(214,235,252,.55);margin-top:9px;}}
.orbits{{position:absolute;left:0;top:0;width:100%;height:100%;opacity:.34;}}
"""

FRONT_TPL = """<!doctype html><html><head><meta charset="utf-8"><style>{css}
.bg{{background-image:url("{art('logo3.png')}");background-position:32% 58%;}}
.scrim{{background:
  linear-gradient(102deg, rgba(3,8,19,.94) 0%, rgba(3,8,19,.80) 38%, rgba(3,8,19,.42) 66%, rgba(3,8,19,.16) 100%),
  linear-gradient(180deg, rgba(3,8,19,.62) 0%, rgba(3,8,19,.10) 34%, rgba(3,8,19,.28) 62%, rgba(2,6,14,.90) 100%);}}
</style></head><body><div class="page">
  <div class="bg"></div>
  <div class="scrim"></div>
  <svg class="orbits" viewBox="0 0 794 1123" fill="none">
    <ellipse cx="640" cy="700" rx="420" ry="150" stroke="{ICE}" stroke-width=".8" stroke-opacity=".55"
             transform="rotate(-18 640 700)"/>
    <ellipse cx="640" cy="700" rx="330" ry="112" stroke="{GOLD}" stroke-width=".7" stroke-opacity=".42"
             transform="rotate(-18 640 700)"/>
    <ellipse cx="640" cy="700" rx="520" ry="196" stroke="#C6B4FF" stroke-width=".6" stroke-opacity=".30"
             transform="rotate(-18 640 700)"/>
  </svg>
  <div class="frame"></div>
  <div class="inner">
    <div class="kicker">PARAMETRIC HUMAN MODELS　·　{volno}</div>
    <div class="rule"></div>
    <h1>人体参数化技术</h1>
    <div class="vol">{volume}</div>
    <div class="sub2">{tagline}</div>
    <div class="barwrap">
      <div class="bar"></div>
      <div class="ticks">
        <span>1995　统计形状</span><span>2005　形状 / 姿态</span><span>2015　SMPL</span><span>2026　前沿</span>
      </div>
    </div>
    <div class="tag">用<i>少量参数</i>，描述一个<i>高维的人</i>。</div>
  </div>
  <div class="bottom">
    <div class="author">Dr. Dezeming</div>
    <div class="edition">2026 年 · 第一版　·　{volume}　·　CC BY-NC-SA 4.0</div>
  </div>
</div></body></html>"""

BACK_TPL = """<!doctype html><html><head><meta charset="utf-8"><style>{css}
.bg{{background-image:url("{art('logo1.png')}");background-position:72% 58%;}}
.scrim{{background:
  radial-gradient(700px 520px at 80% 18%, rgba(8,20,40,.30), transparent 72%),
  linear-gradient(180deg, rgba(3,8,18,.82) 0%, rgba(3,8,18,.62) 30%, rgba(3,8,18,.78) 72%, rgba(2,6,14,.94) 100%);}}
h2{{font-size:44px;line-height:1.42;letter-spacing:3.4px;font-weight:600;color:#FBFDFF;
    margin-top:22px;text-shadow:0 2px 22px rgba(4,10,22,.6);}}
.panel{{
  margin-top:26px;padding:30px 30px 28px;border:1px solid rgba(207,232,255,.16);
  background:linear-gradient(180deg, rgba(8,18,34,.62), rgba(5,12,24,.72));
  backdrop-filter:blur(1.5px);
}}
.lead{{font-size:13.2px;line-height:2.05;letter-spacing:.6px;color:rgba(232,244,255,.90);}}
.lead em{{font-style:normal;color:{GOLD};}}
.toc{{margin-top:24px;list-style:none;}}
.toc li{{display:flex;gap:12px;align-items:baseline;padding:9px 0;
  border-top:1px solid rgba(207,232,255,.10);}}
.toc li b{{font-family:"Noto Sans SC",sans-serif;font-size:11.4px;letter-spacing:2.6px;
  color:{ICE};font-weight:500;white-space:nowrap;}}
.toc li span{{font-family:"Noto Sans SC",sans-serif;font-size:10.6px;line-height:1.75;
  letter-spacing:.8px;color:rgba(226,240,252,.74);}}
.quote{{margin-top:30px;font-size:16.5px;line-height:1.95;letter-spacing:2.2px;
  color:#F4F9FF;border-left:2px solid {GOLD};padding-left:16px;}}
.quote small{{display:block;margin-top:8px;font-family:"Noto Sans SC",sans-serif;
  font-size:9.8px;letter-spacing:2px;color:rgba(214,235,252,.55);}}
.bottom{{position:absolute;left:78px;right:78px;bottom:78px;}}
.who{{font-size:15px;letter-spacing:3.6px;color:#FBFDFF;line-height:1.8;}}
.who span{{font-family:"Noto Sans SC",sans-serif;font-size:10.4px;letter-spacing:2.2px;
  color:rgba(214,235,252,.55);}}
</style></head><body><div class="page">
  <div class="bg"></div>
  <div class="scrim"></div>
  <div class="frame"></div>
  <div class="inner">
    <div class="kicker">ABOUT THE BOOK</div>
    <div class="rule"></div>
    <h2>四类模型，一套方法。</h2>
    <div class="panel">
      <div class="lead">从 1995 年的统计形状模型讲到今天的扩散模型与基础模型：先用<em>平均形状 + 形变基 + 骨架蒙皮</em>把「人」压缩成几十个参数，再用可微渲染把它和图像连起来。人体、人脸、人手、动物四条主线共享同一套数学，只是换了对象与关节。<br><br>本册是<em>{volume}</em>：{blurb}</div>
      <ul class="toc">
        <li><b>入门册</b><span>什么是参数化 · 参数从哪来 · 人怎么动 · 怎么从照片反推 · 怎么用</span></li>
        <li><b>数学册</b><span>向量与最小二乘 · 概率与 PCA · 三维表示与旋转 · LBS 与 DQS · 统计形状模型 · 李群与优化</span></li>
        <li><b>人体册</b><span>SCAPE · SMPL 逐项拆公式 · SMPL 家族与最新模型</span></li>
        <li><b>重建册</b><span>优化与回归 · 视频与多人 · 数据集与评估 · 着装与神经渲染 · 动作生成</span></li>
        <li><b>脸手册</b><span>3DMM 与 BFM · FLAME · 高保真 · 驱动与头像 · MANO · 单手重建 · 手物交互</span></li>
        <li><b>前沿册</b><span>SMAL · 动物重建 · 跨物种 · 扩散与 3DGS · 人体基础模型 · 研究脉络</span></li>
      </ul>
    </div>
    <div class="quote">好的模型不是参数越多越好，而是把不该纠缠的因素分开。
      <small>—— 第 7 章　SCAPE</small></div>
  </div>
  <div class="bottom">
    <div class="who">Dr. Dezeming<br><span>2026 年 · 第一版　·　{volume}</span></div>
  </div>
</div></body></html>"""


BLURB = {
    "intro": "只建立概念，不推导公式。一小时读完，知道这门技术在做什么。",
    "math": "所有公式都从定义推起：最小二乘、PCA/SVD、旋转与相机、LBS 与 DQS、统计形状模型、李群与位姿优化。",
    "body": "SCAPE 为什么要作用在三角形上，SMPL 每一项怎么来，STAR / ATLAS / MHR 又改了什么。",
    "recon": "从一张照片到一段视频：优化法与回归法、度量尺度、评估指标、着装与神经渲染、动作生成。",
    "face-hand": "3DMM 与 Basel Face Model、FLAME、高保真细节、驱动与头像，加上 MANO、单手重建、手物交互。",
    "frontier": "SMAL 与跨物种、动物重建四代方法、扩散模型与 3DGS、人体基础模型，以及研究脉络。",
}


def fill(tpl, css, volno, volume, tagline, blurb):
    # 先把插图内联成 data URI（base64 里不含花括号），再把模板里为 f-string 转义的双花括号还原
    for nm in ("logo1.png", "logo2.png", "logo3.png"):
        tpl = tpl.replace("{art('%s')}" % nm, art(nm))
    html = tpl.replace("{{", "{").replace("}}", "}")
    html = html.replace("{css}", css)
    html = html.replace("{volno}", volno)
    html = html.replace("{volume}", volume)
    html = html.replace("{tagline}", tagline)
    html = html.replace("{blurb}", blurb)
    return html


def render(b, html, out):
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=3)
    pg.set_content(html, wait_until="load")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(600)
    pg.screenshot(path=str(out), type="jpeg", quality=90)
    print("saved", out, round(out.stat().st_size / 1e6, 2), "MB")
    pg.close()


def main():
    import sys
    only = None
    if "--book" in sys.argv:
        only = sys.argv[sys.argv.index("--book") + 1].rstrip("/\\")

    with sync_playwright() as p:
        args = ["--font-render-hinting=none", "--force-color-profile=srgb"]
        b = None
        for kw in ({"channel": "chrome"}, {"channel": "msedge"}, {}):
            try:
                b = p.chromium.launch(headless=True, args=args, **kw)
                print("browser:", kw.get("channel", "bundled"))
                break
            except Exception as e:
                print("launch fail", kw.get("channel", "bundled"), str(e)[:80])
        if b is None:
            raise SystemExit("没有可用的 Chromium/Chrome/Edge")

        for key, volno, volume, tagline, acc in VOLUMES:
            if only and key != only:
                continue
            bookdir = BOOKS / key
            if not bookdir.is_dir():
                print("! 跳过（没有目录）", key)
                continue
            css = BASE_CSS.replace("__ACC__", acc)
            front = fill(FRONT_TPL, css, volno, volume, tagline, BLURB[key])
            back = fill(BACK_TPL, css, volno, volume, tagline, BLURB[key])
            render(b, front, bookdir / "images" / "cover_front.jpg")
            render(b, back, bookdir / "images" / "cover_back.jpg")
        b.close()


if __name__ == "__main__":
    main()
