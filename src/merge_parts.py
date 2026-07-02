#!/usr/bin/env python3
"""data/parts/out_*.json(サブエージェント出力)を translations.json へ取り込む。"""
import json, glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
trp = ROOT / "data" / "translations.json"
tr = json.loads(trp.read_text(encoding="utf-8"))

added, files_ok, files_bad = 0, [], []
for f in sorted(glob.glob(str(ROOT / "data" / "parts" / "out_*.json"))):
    try:
        d = json.loads(Path(f).read_text(encoding="utf-8"))
    except Exception as e:
        files_bad.append(f"{Path(f).name}: JSON parse error ({e})")
        continue
    n = 0
    for seq, v in d.items():
        if not str(seq).isdigit():
            continue
        if not isinstance(v, dict) or not v.get("q_ja"):
            continue
        v.setdefault("opts_ja", [])
        v.setdefault("opts_mt", [])
        tr[str(seq)] = v
        n += 1
        added += 1
    files_ok.append(f"{Path(f).name}: {n}問")

trp.write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
print("取り込みOK:", files_ok)
if files_bad:
    print("取り込み失敗:", files_bad)
print(f"追加合計: {added}問 / translations.json 総数: {sum(1 for k in tr if k.isdigit())}問")
