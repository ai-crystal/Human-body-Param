# -*- coding: utf-8 -*-
"""生成正封与封底（210×297mm，约 290 DPI）。

视觉来源：根目录 logo/ 下的三张星际图（logo1/2/3），
正封取 logo3（星云 + 轨道流线），封底取 logo1（银河 + 光束）。
用法: python make_covers.py
输出: book/assets/cover_front.png, cover_back.png
"""
import base64
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent      # book/build
BOOK = HERE.parent                          # book
ROOT = BOOK.parent                          # 仓库根
ASSETS = BOOK / "images" / "cover"           # 输出：book/images/cover/
LOGO_DIR = ROOT / "_private" / "art" / "logos"


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

FRONT = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
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
    <div class="kicker">PARAMETRIC HUMAN MODELS</div>
    <div class="rule"></div>
    <h1>人体参数化技术</h1>
    <div class="sub">从零基础到前沿</div>
    <div class="sub2">人体 · 人脸 · 人手 · 动物</div>
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
    <div class="edition">2026 年 · 第一版　·　27 章 + 4 附录　·　83 幅插图　·　CC BY-NC-SA 4.0</div>
  </div>
</div></body></html>"""

BACK = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
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
      <div class="lead">从 1995 年的统计形状模型讲到今天的扩散模型与基础模型：先用<em>平均形状 + 形变基 + 骨架蒙皮</em>把「人」压缩成几十个参数，再用可微渲染把它和图像连起来。人体、人脸、人手、动物四条主线共享同一套数学，只是换了对象与关节。</div>
      <ul class="toc">
        <li><b>第一篇　地基</b><span>向量与最小二乘 · 概率与 PCA · 三维表示与旋转 · LBS · ASM → 3DMM</span></li>
        <li><b>第二篇　人体</b><span>SCAPE · SMPL 逐项拆公式 · SMPL 家族 · 单图与视频重建 · 着装与动作生成</span></li>
        <li><b>第三篇　人脸</b><span>3DMM 深入与 Basel Face Model · FLAME · 高保真细节与纹理 · 驱动与神经头像</span></li>
        <li><b>第四篇　人手</b><span>手部解剖与 MANO · 单手重建 · 手物交互与接触</span></li>
        <li><b>第五篇　动物</b><span>SMAL 与玩具扫描 · 动物重建四代方法 · 鸟类 / 鱼类与跨物种生成</span></li>
        <li><b>第六篇　前沿与实战</b><span>扩散与基础模型 · 可运行的 PCA / LBS / 拟合 demo · 研究脉络</span></li>
      </ul>
    </div>
    <div class="quote">好的模型不是参数越多越好，而是把不该纠缠的因素分开。
      <small>—— 第 7 章　SCAPE</small></div>
  </div>
  <div class="bottom">
    <div class="who">Dr. Dezeming<br><span>2026 年 · 第一版　·　27 章 + 4 附录</span></div>
  </div>
</div></body></html>"""


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
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
        for name, html in (("cover_front.jpg", FRONT), ("cover_back.jpg", BACK)):
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=3)
            pg.set_content(html, wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(600)
            out = ASSETS / name
            pg.screenshot(path=str(out), type="jpeg", quality=90)
            print("saved", out, round(out.stat().st_size / 1e6, 2), "MB")
            pg.close()
        b.close()


if __name__ == "__main__":
    main()
