#!/usr/bin/env python3
"""
教科書の出典(公式Markdown)を GitHub から取得する。トークン非消費(ただのHTTP DL)。
data/textbook/sources.json の pages[] を読み、各ファイルを
  https://raw.githubusercontent.com/<repo>/<branch>/<base>/<folder>/<file>
から取得し data/textbook/raw/<id>.md へ保存する(id = ファイル名の stem)。

再開可能: 既に raw/<id>.md がある項目はスキップ。1ファイル取得ごとに即保存するので、
中断しても失うのは最大1ファイル。失敗は記録して次へ(部分実行に強い)。

  python3 src/fetch_docs.py            # 未取得を全部DL
  python3 src/fetch_docs.py --force    # 既存も再取得(更新反映)
"""
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TB = ROOT / "data" / "textbook"
RAW = TB / "raw"
RAW.mkdir(parents=True, exist_ok=True)

src = json.loads((TB / "sources.json").read_text(encoding="utf-8"))
repo, branch, base = src["repo"], src["branch"], src["base"]
force = "--force" in sys.argv

ok = skip = fail = 0
for p in src.get("pages", []):
    file = p["file"]
    pid = Path(file).stem
    dest = RAW / f"{pid}.md"
    if dest.exists() and not force:
        skip += 1
        continue
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{base}/{p['folder']}/{file}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "claude-code-textbook"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        dest.write_bytes(data)          # 即保存
        ok += 1
        print(f"[ok]   {pid}  ({len(data)} bytes)")
        time.sleep(0.2)                 # GitHub への軽い配慮
    except urllib.error.HTTPError as e:
        fail += 1
        print(f"[FAIL] {pid}  HTTP {e.code}  ({p['folder']}/{file})")
    except Exception as e:
        fail += 1
        print(f"[FAIL] {pid}  {type(e).__name__}: {e}")

print(f"\ndownloaded: {ok}  skipped(existing): {skip}  failed: {fail}")
