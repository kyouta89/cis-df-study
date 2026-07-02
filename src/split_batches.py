#!/usr/bin/env python3
"""未翻訳の通常問題をバッチ入力ファイルに分割する(並列サブエージェント用)。"""
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH = 20

qs = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
tr = json.loads((ROOT / "data" / "translations.json").read_text(encoding="utf-8"))
done = {k for k in tr if k.isdigit()}

parts = ROOT / "data" / "parts"
parts.mkdir(exist_ok=True)

remaining = []
for q in qs:
    if q.get("is_drag"):
        continue
    if str(q["seq"]) in done:
        continue
    remaining.append({
        "seq": q["seq"], "number": q["number"], "topic": q["topic"],
        "question": q["question"],
        "options": [{"label": o["label"], "text": o["text"]} for o in q["options"]],
        "suggested_answer": q["suggested_answer"],
        "community_answer": q["community_answer"],
        "community_pct": q["community_pct"],
        "vote_total": q["vote_total"],
    })

nb = math.ceil(len(remaining) / BATCH) if remaining else 0
for k in range(nb):
    chunk = remaining[k*BATCH:(k+1)*BATCH]
    (parts / f"in_{k+1}.json").write_text(json.dumps(chunk, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"未翻訳の通常問題: {len(remaining)}問 → {nb}バッチ(各{BATCH}問)")
print("バッチ:", [f"in_{k+1}.json({len(remaining[k*BATCH:(k+1)*BATCH])}問)" for k in range(nb)])
