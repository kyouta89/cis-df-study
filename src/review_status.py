#!/usr/bin/env python3
"""
公式docエビデンス査読の進捗＝再開ポイント表示。
data/review_results.json(査読の累積=真実源, seqキー) と questions.json/verify_results.json を突合し、
優先順(Tier1: 盲検不一致∪バージョン依存 → Tier2: 残りlow → Tier3: medium → Tier4: high)で未査読を出す。
ドラッグ問題(is_drag)は別管理(add_drag系)のため既定で除外。1問ずつ review_results.json に追記すれば、
制限で中断しても失うのは最大1問。再開＝ここで残りと出た seq を上から査読する。

  python3 src/review_status.py            # サマリ＋次に査読する seq(優先順, 既定30件)
  python3 src/review_status.py 50         # 次の50件
  python3 src/review_status.py --tier1    # Tier1の残りだけ
"""
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows コンソールの cp932 で絵文字が落ちるのを回避
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
qs = {q["seq"]: q for q in json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))}
vr_path = ROOT / "data" / "verify_results.json"
vr = json.loads(vr_path.read_text(encoding="utf-8")) if vr_path.exists() else {}
rev = json.loads((ROOT / "data" / "review_results.json").read_text(encoding="utf-8"))

mismatch = {int(s) for s, v in vr.items() if not v.get("match")}
version = {int(s) for s, v in vr.items() if v.get("version_flag")}
tier1_set = mismatch | version

def tier(q):
    s = q["seq"]
    if q.get("is_drag"):
        return 9  # ドラッグは別管理
    if s in tier1_set:
        return 1
    if q["confidence"] == "low":
        return 2
    if q["confidence"] == "medium":
        return 3
    return 4  # high

done = set(int(s) for s in rev)
order = sorted(qs.values(), key=lambda q: (tier(q), q["seq"]))
pending = [q for q in order if q["seq"] not in done and tier(q) != 9]

# サマリ
labels = {1: "Tier1 不一致∪version", 2: "Tier2 残りlow", 3: "Tier3 medium", 4: "Tier4 high", 9: "(ドラッグ除外)"}
print(f"査読済み: {len(done)} / 非ドラッグ {sum(1 for q in qs.values() if not q.get('is_drag'))}問")
for t in (1, 2, 3, 4):
    grp = [q for q in qs.values() if tier(q) == t]
    d = sum(1 for q in grp if q["seq"] in done)
    print(f"  {labels[t]}: {d}/{len(grp)} 済")

if "--tier1" in sys.argv:
    pending = [q for q in pending if tier(q) == 1]

n = 30
for a in sys.argv[1:]:
    if a.isdigit():
        n = int(a)

print(f"\n=== 次に査読する seq(優先順, {min(n, len(pending))}/{len(pending)}件) ===")
for q in pending[:n]:
    sg = q.get("suggested_answer", "")
    extra = ""
    if q["seq"] in mismatch:
        extra += f" ⚠️提示{sg}→AI{vr[str(q['seq'])].get('ai_answer','')}"
    if q["seq"] in version:
        extra += " 🕒version"
    print(f"  T{tier(q)} #{q['seq']} [{q['topic']} Q{q['number']}] conf={q['confidence']} 提示={sg}{extra}")
