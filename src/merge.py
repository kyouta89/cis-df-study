#!/usr/bin/env python3
"""
data/questions.json(原文) + data/translations.json(翻訳蓄積) を合成し
data/translated.json を生成する。
translations.json のキー = seq(文字列)。フィールド:
  q_ja / opts_ja  : 綺麗な訳(学習用)
  q_mt / opts_mt  : 本番風(機械翻訳調)
  ai              : AI解説
  needs_review    : 任意フラグ
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
qs = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
tr = json.loads((ROOT / "data" / "translations.json").read_text(encoding="utf-8"))
vr_path = ROOT / "data" / "verify_results.json"
vr = json.loads(vr_path.read_text(encoding="utf-8")) if vr_path.exists() else {}
rev_path = ROOT / "data" / "review_results.json"
rev = json.loads(rev_path.read_text(encoding="utf-8")) if rev_path.exists() else {}

done = 0
for q in qs:
    t = tr.get(str(q["seq"]))
    if not t:
        continue
    if t.get("q_ja"):
        q["ja"] = {"question": t["q_ja"],
                   "options": [{"text": x} for x in (t.get("opts_ja") or [])]}
    if t.get("q_mt"):
        q["ja_mt"] = {"question": t["q_mt"],
                      "options": [{"text": x} for x in (t.get("opts_mt") or [])]}
    if t.get("ai"):
        q["ai_explanation"] = t["ai"]
    if t.get("needs_review"):
        q["needs_review"] = True
    v = vr.get(str(q["seq"]))
    if v:
        q["verify"] = v
    r = rev.get(str(q["seq"]))
    if r:
        q["review_doc"] = r
    if t.get("q_ja") or t.get("ai"):
        done += 1

(ROOT / "data" / "translated.json").write_text(
    json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[merge] translations applied: {done} / {len(qs)} -> data/translated.json")
