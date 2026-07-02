#!/usr/bin/env python3
"""
教科書ジェネレータ(出版安全な独立HTML)。
data/textbook/chapters.json(目次) と data/textbook/content/<section>.md(本文) を読み、
スマホ最適化の単一HTML(site/textbook.html)を生成する。問題集(index.html)とは別ファイル。
- 本文は自作の解説＋公式出典(各md フロントマターの sources)。ExamTopics由来の問題は一切含めない。
- 章＝公式ブループリント加重ドメイン(weight%表示)。左に目次、本文に節アンカー＋出典リンク。
- 末尾に免責/帰属(非公式・個人の学習メモ / 出典 ServiceNow Docs=Apache-2.0 / 商標表記)。

ビルド時のみ Python-Markdown に依存(出力HTMLは依存なし・そのまま開ける)。
  python3 src/build_textbook.py
"""
import json
import re
from pathlib import Path
import markdown as md

ROOT = Path(__file__).resolve().parent.parent
TB = ROOT / "data" / "textbook"
CONTENT = TB / "content"

chapters = json.loads((TB / "chapters.json").read_text(encoding="utf-8"))


def parse_front(text):
    """先頭の --- ... --- フロントマターを軽量パース。sources は - title:/url: の連なり。"""
    fm, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return fm, body
    raw, body = m.group(1), m.group(2)
    sources, cur = [], None
    for line in raw.splitlines():
        if re.match(r"\s*-\s*title:", line):
            cur = {"title": line.split("title:", 1)[1].strip(), "url": ""}
            sources.append(cur)
        elif re.match(r"\s*url:", line) and cur is not None:
            cur["url"] = line.split("url:", 1)[1].strip()
        elif ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    if sources:
        fm["sources"] = sources
    return fm, body


def callout_classes(html):
    """blockquote を絵文字で色分け(⚠=warn / 📌=note)。"""
    def repl(m):
        inner = m.group(1)
        cls = "callout"
        if "⚠" in inner:
            cls += " warn"
        elif "📌" in inner:
            cls += " note"
        return f'<blockquote class="{cls}">{inner}</blockquote>'
    return re.sub(r"<blockquote>(.*?)</blockquote>", repl, html, flags=re.S)


def render_body(body):
    html = md.markdown(body, extensions=["tables", "fenced_code", "sane_lists", "md_in_html"])
    return callout_classes(html)


# 章・節を組み立て
toc_html, body_html = [], []
for ch in chapters["chapters"]:
    cid, dom, wt = ch["id"], ch["domain"], ch.get("weight")
    toc_secs = []
    sec_html = []
    for sec in ch["sections"]:
        sid, stitle = sec["id"], sec["title"]
        f = CONTENT / f"{sid}.md"
        if f.exists():
            fm, body = parse_front(f.read_text(encoding="utf-8"))
            inner = render_body(body)
            srcs = fm.get("sources", [])
            src_html = ""
            if srcs:
                items = "".join(
                    f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{s["title"]}</a></li>'
                    for s in srcs
                )
                src_html = f'<div class="sources"><span class="src-h">出典(ServiceNow 公式Docs)</span><ul>{items}</ul></div>'
            toc_secs.append(f'<li><a href="#{sid}">{stitle}</a></li>')
            sec_html.append(
                f'<section id="{sid}" class="sec"><div class="sec-body">{inner}</div>{src_html}</section>'
            )
        else:
            toc_secs.append(f'<li class="todo"><a href="#{sid}">{stitle}</a> <span class="soon">準備中</span></li>')
            sec_html.append(
                f'<section id="{sid}" class="sec todo"><h2>{stitle}</h2>'
                f'<p class="soon-body">この節は準備中です。</p></section>'
            )

    badge = f'<span class="wt">{wt}%</span>' if wt is not None else ""
    toc_html.append(
        f'<li class="ch"><a href="#{cid}">{dom} {badge}</a><ul>{"".join(toc_secs)}</ul></li>'
    )
    body_html.append(
        f'<div id="{cid}" class="chapter"><h1 class="ch-title">{dom} {badge}</h1>{"".join(sec_html)}</div>'
    )

TOC = "".join(toc_html)
BODY = "".join(body_html)

HTML = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
<title>CIS-DF 教科書</title>
<style>
:root{--bg:#0f1115;--card:#1a1d24;--fg:#e8eaed;--mut:#9aa0a6;--line:#2a2e37;
  --hi:#34a853;--mid:#fbbc04;--lo:#ea4335;--accent:#8ab4f8;}
@media(prefers-color-scheme:light){:root{--bg:#f4f5f7;--card:#fff;--fg:#202124;--mut:#5f6368;--line:#e0e0e0;--accent:#1a73e8;}}
*{box-sizing:border-box}
html,body{overflow-x:hidden}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif;
  background:var(--bg);color:var(--fg);line-height:1.75;overflow-wrap:anywhere;-webkit-text-size-adjust:100%;}
header{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 14px;display:flex;align-items:center;gap:10px}
header h1{font-size:16px;margin:0;flex:1}
header .sub{font-size:11px;color:var(--mut);font-weight:normal}
header .qlink{font-size:12px;font-weight:700;color:var(--accent);text-decoration:none;border:1px solid var(--accent);padding:4px 10px;border-radius:8px;white-space:nowrap}
#menubtn{display:none;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:14px;cursor:pointer}
.wrap{display:flex;max-width:1100px;margin:0 auto}
nav{width:300px;flex:none;border-right:1px solid var(--line);padding:14px 10px 60px;height:calc(100vh - 52px);position:sticky;top:52px;overflow:auto}
nav ul{list-style:none;margin:0;padding:0}
nav li.ch>a{display:block;font-weight:700;color:var(--fg);text-decoration:none;padding:7px 8px;border-radius:8px;margin-top:6px}
nav li.ch>a:hover{background:var(--card)}
nav .wt{font-size:10px;font-weight:700;color:#000;background:var(--accent);border-radius:999px;padding:1px 7px;margin-left:4px}
nav li.ch>ul li{margin:1px 0}
nav li.ch>ul a{display:block;color:var(--mut);text-decoration:none;font-size:13px;padding:5px 8px 5px 16px;border-radius:8px}
nav li.ch>ul a:hover{background:var(--card);color:var(--fg)}
nav li.todo a{opacity:.7}
nav .soon{font-size:10px;color:var(--mid)}
main{flex:1;min-width:0;padding:14px 18px 100px;max-width:760px}
.chapter{margin-bottom:30px}
.ch-title{font-size:20px;border-bottom:2px solid var(--accent);padding-bottom:8px;margin:26px 0 6px;scroll-margin-top:60px}
.ch-title .wt{font-size:12px;color:#000;background:var(--accent);border-radius:999px;padding:2px 9px;margin-left:6px;vertical-align:middle}
.sec{scroll-margin-top:60px;padding:6px 0 4px}
.sec h2{font-size:17px;margin:22px 0 8px;color:var(--accent)}
.sec h3{font-size:15px;margin:18px 0 6px}
.sec p{margin:10px 0}
.sec ul,.sec ol{padding-left:1.3em;margin:8px 0}
.sec li{margin:4px 0}
.sec code{background:var(--card);border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:.9em;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.sec strong{color:var(--fg)}
.sec a{color:var(--accent)}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
th{background:var(--card);font-weight:700}
blockquote.callout{margin:12px 0;padding:10px 12px;border-radius:8px;border-left:4px solid var(--accent);
  background:rgba(138,180,248,.08);font-size:14px}
blockquote.callout>*:first-child{margin-top:0}blockquote.callout>*:last-child{margin-bottom:0}
blockquote.callout.warn{border-left-color:var(--lo);background:rgba(234,67,53,.10)}
blockquote.callout.note{border-left-color:var(--mid);background:rgba(251,188,4,.10)}
.sources{margin:14px 0 6px;border-top:1px dashed var(--line);padding-top:8px}
.sources .src-h{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}
.sources ul{list-style:none;padding:0;margin:6px 0 0}
.sources li{margin:3px 0;font-size:12px}
.sources a{color:var(--accent);word-break:break-all}
.soon-body{color:var(--mut)}
figure.diagram{margin:16px 0;text-align:center}
figure.diagram svg{max-width:100%;height:auto;border:1px solid var(--line);border-radius:10px;background:rgba(127,127,127,.04);padding:8px}
figure.diagram figcaption{font-size:12px;color:var(--mut);margin-top:6px}
.diagram .box{fill:var(--card);stroke:var(--line);stroke-width:1.5}
.diagram .root{fill:var(--accent);stroke:none}
.diagram .hlbox{fill:var(--card);stroke:var(--lo);stroke-width:2}
.diagram .t{fill:var(--fg);font-size:13px;font-weight:600}
.diagram .tw{fill:#06121f;font-size:13px;font-weight:700}
.diagram .sub{fill:var(--mut);font-size:11px}
.diagram .hl{fill:var(--lo);font-size:11px;font-weight:700}
.diagram .ln{stroke:var(--line);stroke-width:1.5;fill:none}
.diagram .arrow{stroke:var(--accent);stroke-width:2;fill:none;marker-end:url(#ah)}
.diagram .ahfill{fill:var(--accent)}
.sec details{margin:12px 0;border:1px solid var(--line);border-radius:8px;background:rgba(127,127,127,.05)}
.sec details>summary{cursor:pointer;padding:9px 12px;font-weight:600;color:var(--accent);font-size:13px;list-style:none}
.sec details>summary::-webkit-details-marker{display:none}
.sec details>summary::before{content:"▸ ";color:var(--mut)}
.sec details[open]>summary::before{content:"▾ "}
.sec details[open]>summary{border-bottom:1px solid var(--line)}
.sec details>:not(summary){margin-left:12px;margin-right:12px}
footer{border-top:1px solid var(--line);padding:14px 18px 30px;font-size:11px;color:var(--mut);max-width:1100px;margin:0 auto;line-height:1.6}
footer b{color:var(--mut)}
@media(max-width:760px){
  #menubtn{display:block}
  .wrap{display:block}
  nav{position:fixed;left:0;top:52px;bottom:0;width:80%;max-width:320px;background:var(--bg);z-index:30;
    transform:translateX(-105%);transition:transform .2s;border-right:1px solid var(--line);height:auto}
  nav.open{transform:translateX(0)}
  main{max-width:none}
  #scrim{display:none;position:fixed;inset:52px 0 0 0;background:rgba(0,0,0,.5);z-index:25}
  #scrim.open{display:block}
}
</style>
</head>
<body>
<header>
  <button id="menubtn" aria-label="目次">☰</button>
  <h1>CIS-DF 教科書 <span class="sub">— CMDB &amp; CSDM データ基盤</span></h1>
  <a class="qlink" href="index.html">📝 問題集</a>
</header>
<div class="wrap">
  <nav id="nav"><ul>__TOC__</ul></nav>
  <main>__BODY__</main>
</div>
<div id="scrim"></div>
<footer>
  <b>非公式・個人の学習メモです。</b> ServiceNow, Inc. とは無関係で、公式の保証はありません。<br>
  本文の出典は ServiceNow 公式製品ドキュメント(<a href="https://github.com/ServiceNow/ServiceNowDocs" target="_blank" rel="noopener" style="color:var(--accent)">ServiceNow/ServiceNowDocs</a>, Apache-2.0)。各節の出典リンク先を参照。<br>
  ServiceNow, CMDB, CSDM, CIS-DF 等は ServiceNow, Inc. の商標です。
</footer>
<script>
var nav=document.getElementById('nav'),scrim=document.getElementById('scrim'),btn=document.getElementById('menubtn');
function closeNav(){nav.classList.remove('open');scrim.classList.remove('open');}
btn.onclick=function(){nav.classList.toggle('open');scrim.classList.toggle('open');};
scrim.onclick=closeNav;
nav.addEventListener('click',function(e){if(e.target.tagName==='A')closeNav();});
</script>
</body>
</html>
"""

out = ROOT / "site" / "textbook.html"
out.write_text(HTML.replace("__TOC__", TOC).replace("__BODY__", BODY), encoding="utf-8")
n_done = len(list(CONTENT.glob("*.md"))) if CONTENT.exists() else 0
print(f"[textbook] {n_done} sections -> {out}")
