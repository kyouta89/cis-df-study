#!/usr/bin/env python3
"""
学習用HTML生成器。
data/translated.json(無ければ data/questions.json)を読み、
スマホ最適化の単一HTML(site/index.html)を生成する。
- 日英トグル / 信頼度バッジ・フィルタ / トピックフィルタ / 検索
- 学習モード(解答表示) / 暗記モード(解答を隠す→タップで開示)
- 進捗(解いた・要復習)は localStorage に保存
ビルド不要・依存なし。生成HTMLをそのまま開くだけ。
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── 試験ごとに変わるのはここだけ ──────────────────────────────────
# このブロック以外は CSA 版(CSA - Claude)の build_site.py と同一に保つこと。
# UI を改善したら「相手のファイルを丸ごとコピーして、このブロックだけ元に戻す」で移植できる。
# ls(localStorageプレフィックス)を試験ごとに変えるのは必須: 同一オリジンに2つ置くと進捗が混ざる。
# ⚠️ "cisdf." は既存の学習進捗(done/要復習)が入っているキー。変えると進捗が消えたように見える。
EXAM = {
    "title": "CIS-DF 学習",
    "ls": "cisdf.",
}
# ────────────────────────────────────────────────────────────────

src = ROOT / "data" / "translated.json"
if not src.exists():
    src = ROOT / "data" / "questions.json"
data = json.loads(src.read_text(encoding="utf-8"))

# 公式doc査読で問題ありと判定したものを成果物から完全に除外する。
# トグルで出し分けたりはしない——HTMLに一切埋め込まない。
#   defective  = 設問そのものが壊れている/古い(選択肢の破損・正解が選択肢に無い・旧UI前提)
#   unverified = 一次情報で裏が取れなかった(設問自体の欠陥ではないが、確信を持って学べない)
# 判定はデータ側(data/review_results.json の quality / quality_reason)にあり、ここは読むだけ。
# ※試験非依存の共通機能。CSA版と同期するときはこのブロックも一緒に運ぶこと(EXAM ブロック外)。
HIDE_QUALITY = {"defective", "unverified"}


def drop_flagged(rows):
    keep, dropped = [], []
    for q in rows:
        r = q.get("review_doc") or {}
        # dispute は公式docの正解を示せる最重要の問題なので、何があっても隠さない。
        if r.get("verdict") != "dispute" and r.get("quality") in HIDE_QUALITY:
            dropped.append(q)
        else:
            keep.append(q)
    if dropped:
        from collections import Counter
        why = Counter((q.get("review_doc") or {}).get("quality") for q in dropped)
        print(f"[filter] 非表示 {len(dropped)}問 / 残り {len(keep)}問")
        print(f"         内訳: {dict(why)}")
    return keep


data = drop_flagged(data)

# 画像を data URI で埋め込むか(True = HTML1枚で完結・site/images/ の持ち回りが不要)。
# ※試験非依存の共通機能。CIS-DF版と同期するときはこちらも一緒に移すこと(EXAM ブロック外)。
INLINE_IMAGES = True

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".webp": "image/webp"}


def inline_images(data):
    """questions の *_images("images/xxx.png")を data URI に置換する。
    base64 は英数字と + / = だけなので、JS側の esc(&<>のみ) でも壊れない。
    見つからない画像は元のパスのまま残す(警告を出して続行)。"""
    imgdir = ROOT / "site" / "images"
    cache, missing = {}, []

    def conv(rel):
        if not isinstance(rel, str) or not rel.startswith("images/"):
            return rel
        if rel in cache:
            return cache[rel]
        f = imgdir / Path(rel).name
        if not f.exists():
            missing.append(rel)
            cache[rel] = rel
            return rel
        b = base64.b64encode(f.read_bytes()).decode("ascii")
        cache[rel] = f"data:{MIME.get(f.suffix.lower(), 'application/octet-stream')};base64,{b}"
        return cache[rel]

    n = 0
    for q in data:
        for key in ("question_images", "answer_images"):
            if q.get(key):
                q[key] = [conv(x) for x in q[key]]
                n += len(q[key])
    if missing:
        print(f"[warn] 画像が見つからない({len(missing)}件): {', '.join(sorted(set(missing))[:5])} …")
    embedded = sum(len(v) for k, v in cache.items() if v.startswith("data:"))
    return n, len(cache) - len(set(missing)), embedded


if INLINE_IMAGES:
    refs, uniq, nbytes = inline_images(data)
    print(f"[images] {uniq}枚を埋め込み(参照{refs}箇所) +{nbytes/1024/1024:.2f}MB")

payload = json.dumps(data, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
<title>__TITLE__</title>
<style>
:root{--bg:#0f1115;--card:#1a1d24;--fg:#e8eaed;--mut:#9aa0a6;--line:#2a2e37;
  --hi:#34a853;--mid:#fbbc04;--lo:#ea4335;--accent:#8ab4f8;}
@media(prefers-color-scheme:light){:root{--bg:#f4f5f7;--card:#fff;--fg:#202124;--mut:#5f6368;--line:#e0e0e0;--accent:#1a73e8;}}
*{box-sizing:border-box}
html,body{overflow-x:hidden}
body{margin:0;width:100%;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif;
  background:var(--bg);color:var(--fg);line-height:1.6;-webkit-text-size-adjust:100%;overflow-wrap:anywhere;word-break:normal;}
header{position:sticky;top:0;z-index:10;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 12px;}
h1{font-size:16px;margin:0 0 8px;display:flex;justify-content:space-between;align-items:center;gap:8px}
.tblink{font-size:12px;font-weight:700;color:var(--accent);text-decoration:none;border:1px solid var(--accent);padding:3px 9px;border-radius:8px;white-space:nowrap}
.controls{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
select,input,button{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:7px 9px;font-size:13px}
input[type=search]{flex:1;min-width:120px}
.count{font-size:12px;color:var(--mut);font-weight:normal}
main{padding:10px 12px 80px;max-width:820px;margin:0 auto}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:0 0 12px}
.meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:12px;color:var(--mut);margin-bottom:8px}
.q{font-size:15px;white-space:pre-wrap;overflow-wrap:anywhere;margin:6px 0 10px}
ul.opts{list-style:none;padding:0;margin:0 0 10px}
ul.opts li{border:1px solid var(--line);border-radius:8px;padding:9px 11px;margin:6px 0;font-size:14px;display:flex;gap:8px}
ul.opts li .l{font-weight:700;color:var(--accent)}
li.correct{border-color:var(--hi);background:rgba(52,168,83,.12)}
li.voted .l::after{content:" ★";color:var(--mid)}
.ansrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:13px;margin:8px 0}
.ans{font-weight:700;color:var(--hi)}
.votebar{height:8px;border-radius:4px;background:var(--line);flex:1;min-width:80px;overflow:hidden}
.votebar>i{display:block;height:100%;background:var(--accent)}
.ai{border-left:3px solid var(--accent);background:rgba(138,180,248,.08);padding:8px 10px;border-radius:6px;margin:8px 0;font-size:13px;white-space:pre-wrap;overflow-wrap:anywhere}
.ai b{color:var(--accent)}
.rbadge{font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;white-space:nowrap}
.rb-ok{background:rgba(52,168,83,.15);color:var(--hi)}
.rb-med{background:rgba(251,188,4,.15);color:var(--mid)}
.rb-ver{background:rgba(251,188,4,.15);color:var(--mid)}
.rb-bad{background:rgba(234,67,53,.15);color:var(--lo)}
.rb-sub{font-weight:normal;opacity:.85;margin-left:3px}
details.srcfold{margin:6px 0 0}
details.srcfold>summary{cursor:pointer;color:var(--mut);font-size:12px;list-style:none}
details.srcfold>summary::-webkit-details-marker{display:none}
details.srcfold>summary::before{content:"▸ "}
details.srcfold[open]>summary::before{content:"▾ "}
.srcnote{font-size:12px;color:var(--fg);margin:6px 0;line-height:1.6}
.srclinks{font-size:12px;margin:4px 0 2px}
.srclinks a{color:var(--accent);word-break:break-all}
details summary{cursor:pointer;color:var(--mut);font-size:13px;margin:6px 0}
.cmt{border-top:1px dashed var(--line);padding:6px 0;font-size:12px;color:var(--mut)}
.cmt .h{color:var(--fg)}
.row{display:flex;gap:8px;margin-top:8px}
.row button{flex:1}
.done{opacity:.55}
.mark{outline:2px solid var(--mid)}
.hidden{display:none}
.lang-en{color:var(--mut);font-size:13px}
.imgs img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;margin:6px 0;background:#fff}
.pager{display:flex;gap:10px;align-items:center;justify-content:center;margin:12px 0;font-size:13px;flex-wrap:wrap}
.pager button{min-width:72px}
.pager button:disabled{opacity:.4}
footer{position:fixed;bottom:0;left:0;right:0;background:var(--bg);border-top:1px solid var(--line);
  padding:6px 12px;font-size:12px;color:var(--mut);display:flex;justify-content:space-between;align-items:center}
</style>
</head>
<body>
<header>
  <h1><span>__TITLE__ <span class="count" id="count"></span></span><a class="tblink" href="textbook.html">📘 教科書</a></h1>
  <div class="controls">
    <select id="topic"><option value="">全トピック</option></select>
    <input type="search" id="q" placeholder="検索(英/日)">
    <button id="lang">EN/JA</button>
    <button id="mode">暗記モード</button>
    <button id="onlymark">要復習のみ</button>
    <button id="onlytodo">未着手のみ</button>
    <select id="per" title="1ページの問題数"><option value="10">10問/頁</option><option value="20" selected>20問/頁</option><option value="50">50問/頁</option><option value="9999">全部</option></select>
  </div>
</header>
<main id="list"></main>
<footer>
  <span id="prog"></span>
  <button id="reset" style="font-size:11px;padding:4px 8px">進捗リセット</button>
</footer>
<script id="data" type="application/json">__PAYLOAD__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const savedF = JSON.parse(localStorage.getItem('__LS__filters')||'{}');
let state = {lang: localStorage.getItem('__LS__lang')||'ja', memo: !!savedF.memo, onlymark:!!savedF.onlymark,
  topic:savedF.topic||'', q:savedF.q||'', reveal:new Set(), onlytodo:!!savedF.onlytodo,
  page:0, per: parseInt(localStorage.getItem('__LS__per')||'20',10)};
function saveFilters(){localStorage.setItem('__LS__filters',JSON.stringify(
  {memo:state.memo,onlymark:state.onlymark,onlytodo:state.onlytodo,topic:state.topic,q:state.q}));}
let prog = JSON.parse(localStorage.getItem('__LS__prog')||'{}'); // {seq:{done,mark}}

const topics=[...new Set(DATA.map(d=>d.topic))].filter(Boolean).sort();
const tsel=document.getElementById('topic');
topics.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t;tsel.appendChild(o)});

const LANGLABEL={ja:'表示:日本語',mt:'表示:本番風',en:'表示:English'};
function qText(d,lang){
  if(lang==='ja') return (d.ja&&d.ja.question)||d.question;
  if(lang==='mt') return (d.ja_mt&&d.ja_mt.question)||(d.ja&&d.ja.question)||d.question;
  return d.question;
}
function optText(d,o,i,lang){
  const src = lang==='ja' ? d.ja : (lang==='mt' ? (d.ja_mt||d.ja) : null);
  if(src&&src.options&&src.options[i]&&src.options[i].text) return src.options[i].text;
  return o.text;
}
function setLangBtn(){const b=document.getElementById('lang');if(b)b.textContent=LANGLABEL[state.lang]||'表示:日本語';}

function matches(d){
  if(state.topic && d.topic!==state.topic) return false;
  if(state.onlymark && !(prog[d.seq]&&prog[d.seq].mark)) return false;
  if(state.onlytodo && prog[d.seq]&&prog[d.seq].done) return false;
  if(state.q){const s=state.q.toLowerCase();
    const jaopts=((d.ja&&d.ja.options)||[]).map(o=>o.text).join(' ');
    const mtopts=((d.ja_mt&&d.ja_mt.options)||[]).map(o=>o.text).join(' ');
    const hay=(d.question+' '+qText(d,'ja')+' '+jaopts+' '+qText(d,'mt')+' '+mtopts+' '
      +d.options.map(o=>o.text).join(' ')+' '+(d.ai_explanation||'')).toLowerCase();
    if(!hay.includes(s)) return false;}
  return true;
}

function pager(pages){
  const div=document.createElement('div'); div.className='pager';
  const cur=state.page;
  let opts='';
  for(let i=0;i<pages;i++) opts+=`<option value="${i}" ${i===cur?'selected':''}>${i+1}</option>`;
  div.innerHTML=`<button ${cur<=0?'disabled':''} onclick="gotoPage(${cur-1})">← 前</button>`+
    `<span>${pages>1?`<select onchange="gotoPage(+this.value)">${opts}</select> / ${pages} ページ`:'1 ページ'}</span>`+
    `<button ${cur>=pages-1?'disabled':''} onclick="gotoPage(${cur+1})">次 →</button>`;
  return div;
}
window.gotoPage=function(p){state.page=p;render();window.scrollTo({top:0});};
function render(){
  const list=document.getElementById('list'); list.innerHTML='';
  const items=DATA.filter(matches);
  document.getElementById('count').textContent='('+items.length+'問)';
  const per=state.per||20;
  const pages=Math.max(1, Math.ceil(items.length/per));
  if(state.page>=pages) state.page=pages-1;
  if(state.page<0) state.page=0;
  const start=state.page*per;
  const slice=items.slice(start, start+per);
  if(pages>1) list.appendChild(pager(pages));
  for(const d of slice) list.appendChild(card(d));
  list.appendChild(pager(pages));
  const done=Object.values(prog).filter(p=>p.done).length;
  document.getElementById('prog').textContent='進捗 '+done+' / '+DATA.length+' 完了 ・ 表示 '+items.length+'問';
}

function card(d){
  const el=document.createElement('div'); el.className='card';
  const p=prog[d.seq]||{}; if(p.done) el.classList.add('done'); if(p.mark) el.classList.add('mark');
  const showAns = !state.memo || state.reveal.has(String(d.seq));
  const sa=(d.suggested_answer||'').replace(/\s/g,'');
  const lang=state.lang;

  const qmain = qText(d,lang);
  const qsub  = (lang!=='en') ? d.question : null;

  let opts='';
  d.options.forEach((o,i)=>{
    const isC = showAns && sa.includes(o.label);
    const t = optText(d,o,i,lang);
    // ★(コミュ最多投票)も解答扱い: showAns でガードしないと暗記モードで答えが漏れる
    opts+=`<li class="${isC?'correct':''} ${(showAns&&o.community_most_voted)?'voted':''}"><span class="l">${o.label}.</span><span>${esc(t)}</span></li>`;
  });

  // 公式doc査読バッジ(小)
  let revbadge='';
  if(showAns && d.review_doc){
    const r=d.review_doc;
    // dispute = 公式docと提示正解が食い違う。✅を出すと誤答を保証してしまうので必ず最初に分岐する。
    if(r.verdict==='dispute') revbadge=`<span class="rbadge rb-bad">⚠️公式docと不一致`+
      (r.doc_answer?`<span class="rb-sub">doc: ${esc(r.doc_answer)}</span>`:'')+`</span>`;
    else if(r.verdict==='version') revbadge=`<span class="rbadge rb-ver">🕒版依存</span>`;
    else if(r.confidence!=='high') revbadge=`<span class="rbadge rb-med">✅公式doc<span class="rb-sub">確度中</span></span>`;
    else revbadge=`<span class="rbadge rb-ok">✅公式doc</span>`;
  }

  let ansrow='', ansimg='';
  if(showAns){
    if(d.is_drag){
      ansrow=`<div class="ansrow"><span class="ans">正解: 下の画像を参照</span>${revbadge}</div>`;
    } else {
      let bar = (d.community_pct!=null)
        ? `<div class="votebar"><i style="width:${d.community_pct}%"></i></div><span>コミュ ${d.community_answer} ${d.community_pct}% (${d.vote_total}票)</span>`
        : `<span style="color:var(--mut)">コミュ投票なし</span>`;
      ansrow=`<div class="ansrow"><span class="ans">正解: ${d.suggested_answer||'(なし)'}</span>${revbadge}${bar}</div>`;
    }
    ansimg = imgs(d.answer_images);
  } else {
    ansrow=`<div class="ansrow"><button onclick="revealCard('${d.seq}')">解答を表示</button></div>`;
  }

  let ai='';
  if(showAns && d.ai_explanation) ai=`<div class="ai"><b>解説</b>　${esc(d.ai_explanation)}</div>`;

  // 出典(折りたたみ)。version/確度中のときだけ補足noteも畳んで添える
  let revsrc='';
  if(showAns && d.review_doc){
    const r=d.review_doc;
    const ev=(r.evidence||[]).filter(e=>e.url);
    const links=ev.map(e=>`<a href="${esc(e.url)}" target="_blank" rel="noopener">${esc(e.source||'公式doc')}</a>`).join('　');
    const showNote=(r.verdict==='dispute'||r.verdict==='version'||r.confidence!=='high')&&r.note;
    if(links||showNote){
      revsrc=`<details class="srcfold"><summary>出典・補足${ev.length?`（公式doc ${ev.length}件）`:''}</summary>`+
        (showNote?`<div class="srcnote">${esc(r.note)}</div>`:'')+
        (links?`<div class="srclinks">📎 ${links}</div>`:'')+`</details>`;
    }
  }

  let disc='';
  if(showAns && d.discussion&&d.discussion.length){
    disc=`<details><summary>Discussion (${d.discussion.length})</summary>`+
      d.discussion.map(c=>`<div class="cmt"><span class="h">${esc(c.author||'?')}</span> ${c.selected_answer?('['+esc(c.selected_answer)+']'):''} 👍${esc(c.upvotes||'0')}<br>${esc(c.content||'')}</div>`).join('')+
      `</details>`;
  }

  el.innerHTML=`
    <div class="meta">
      <span>${d.topic} / Q${d.number}</span>
      <span>#${d.seq}</span>
    </div>
    <div class="q">${esc(qmain)}</div>
    ${qsub?`<div class="q lang-en">${esc(qsub)}</div>`:''}
    ${imgs(d.question_images)}
    <ul class="opts">${opts}</ul>
    ${ansrow}
    ${ansimg}
    ${ai}
    ${revsrc}
    ${disc}
    <div class="row">
      <button onclick="toggle('${d.seq}','done')">${p.done?'✓完了済':'完了にする'}</button>
      <button onclick="toggle('${d.seq}','mark')">${p.mark?'★復習解除':'要復習'}</button>
    </div>`;
  return el;
}
function esc(s){return (s==null?'':String(s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function imgs(arr){return (arr&&arr.length)?('<div class="imgs">'+arr.map(s=>`<img loading="lazy" src="${esc(s)}">`).join('')+'</div>'):''}
window.revealCard=function(seq){state.reveal.add(String(seq));render();};
window.toggle=function(seq,key){prog[seq]=prog[seq]||{};prog[seq][key]=!prog[seq][key];
  localStorage.setItem('__LS__prog',JSON.stringify(prog));render();}

tsel.onchange=e=>{state.topic=e.target.value;state.page=0;saveFilters();render()};
document.getElementById('q').oninput=e=>{state.q=e.target.value;state.page=0;saveFilters();render()};
document.getElementById('per').onchange=e=>{state.per=parseInt(e.target.value,10);localStorage.setItem('__LS__per',e.target.value);state.page=0;render()};
document.getElementById('lang').onclick=()=>{const order=['ja','mt','en'];state.lang=order[(order.indexOf(state.lang)+1)%3];localStorage.setItem('__LS__lang',state.lang);setLangBtn();render()};
setLangBtn();
document.getElementById('mode').onclick=e=>{state.memo=!state.memo;state.reveal.clear();e.target.textContent=state.memo?'学習モード':'暗記モード';saveFilters();render()};
function mkToggle(id,key,color){const b=document.getElementById(id);
  b.onclick=()=>{state[key]=!state[key];b.style.outline=state[key]?('2px solid '+color):'';state.page=0;saveFilters();render();};}
mkToggle('onlymark','onlymark','var(--mid)');
mkToggle('onlytodo','onlytodo','var(--accent)');
document.getElementById('reset').onclick=()=>{if(confirm('進捗を全消去しますか?')){prog={};localStorage.removeItem('__LS__prog');render()}};
// 保存済みフィルタをUIコントロールに反映
tsel.value=state.topic;
document.getElementById('q').value=state.q;
document.getElementById('per').value=String(state.per);
if(state.memo) document.getElementById('mode').textContent='学習モード';
if(state.onlymark) document.getElementById('onlymark').style.outline='2px solid var(--mid)';
if(state.onlytodo) document.getElementById('onlytodo').style.outline='2px solid var(--accent)';
render();
</script>
</body>
</html>
"""

out = ROOT / "site" / "index.html"
html = (HTML.replace("__TITLE__", EXAM["title"])
            .replace("__LS__", EXAM["ls"])
            .replace("__PAYLOAD__", payload))   # payload は最後(中身に __ が出ても壊さない)
out.write_text(html, encoding="utf-8")
print(f"[build] {len(data)} questions -> {out}")
