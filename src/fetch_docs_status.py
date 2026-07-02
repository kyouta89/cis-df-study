#!/usr/bin/env python3
"""
教科書の出典取得の進捗表示＝再開ポイント確認用。
data/textbook/sources.json(キュー) と data/textbook/raw/<id>.md(取得済み) を突き合わせ、
未取得のページだけを一覧する。id = ファイル名の stem。取得は src/fetch_docs.py。

  python3 src/fetch_docs_status.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TB = ROOT / "data" / "textbook"
RAW = TB / "raw"
RAW.mkdir(parents=True, exist_ok=True)

src = json.loads((TB / "sources.json").read_text(encoding="utf-8"))
pages = src.get("pages", [])

done, pending = [], []
for p in pages:
    pid = Path(p["file"]).stem
    (done if (RAW / f"{pid}.md").exists() else pending).append((pid, p))

print(f"sources: {len(pages)}  done: {len(done)}  pending: {len(pending)}")
# 節ごとの内訳
by_sec = {}
for pid, p in pages and [(Path(p['file']).stem, p) for p in pages]:
    s = p.get("section", "?")
    by_sec.setdefault(s, [0, 0])
    by_sec[s][0 if (RAW / f"{pid}.md").exists() else 1] += 1
for s in sorted(by_sec):
    d, pe = by_sec[s]
    print(f"  {s}: done {d} / pending {pe}")

if pending:
    print("\n--- PENDING (未取得) ---")
    for pid, p in pending:
        print(f"  [{pid}]  {p['folder']}/{p['file']}")
