#!/usr/bin/env python3
"""低確度(low)・非ドラッグ問題を「盲検」入力に分割。提示正解・投票は含めない。"""
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH = 20
qs = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))

targets = [q for q in qs if q["confidence"] == "low" and not q.get("is_drag")]
parts = ROOT / "data" / "verify"
parts.mkdir(exist_ok=True)

slim = [{
    "seq": q["seq"], "topic": q["topic"], "number": q["number"],
    "question": q["question"],
    "options": [{"label": o["label"], "text": o["text"]} for o in q["options"]],
} for q in targets]

nb = math.ceil(len(slim) / BATCH) if slim else 0
for k in range(nb):
    chunk = slim[k*BATCH:(k+1)*BATCH]
    (parts / f"vin_{k+1}.json").write_text(json.dumps(chunk, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"盲検対象(low・非ドラッグ): {len(slim)}問 → {nb}バッチ")
print("バッチ:", [f"vin_{k+1}({len(slim[k*BATCH:(k+1)*BATCH])})" for k in range(nb)])
