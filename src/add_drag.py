#!/usr/bin/env python3
"""
ドラッグ&ドロップ問題(14問)の翻訳・解説を translations.json に取り込む。

⚠️ 2026-07-29 に方式変更(重要):
  以前はこのファイルの中に辞書 `D` として**訳文と正解をハードコード**していた。
  `.gitignore` が守っているのは `data/` 配下だけで `src/*.py` は公開対象なので、
  これは ExamTopics 由来の正解を公開リポジトリに載せてしまう状態だった。
  現在は中身を **data/drag_answers.json(= /data/*.json で除外済み)** に置き、
  コードはそれを読むだけにしてある。「コードは公開・データは非公開」を崩さないこと。

drag_answers.json の形(キー=seq の文字列。translations.json と同じフィールド):
  {
    "2": {"q_ja": "...", "q_mt": "...", "ai": "【正解(正解画像で確認)】\\n・A ← ..."},
    ...
  }
ドラッグ問題は一覧HTMLに正解が無いため、個別ページ(raw/cisdf_drag1.html 等)を保存し、
正解画像(site/images/*.png)を読んで対応関係を起こしている。opts_ja/opts_mt は空でよい。

  py src/add_drag.py            # 取り込み
  py src/add_drag.py --check    # 取り込まず、対象seqと不足を確認するだけ
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
qs_path = ROOT / "data" / "questions.json"
tr_path = ROOT / "data" / "translations.json"
d_path = ROOT / "data" / "drag_answers.json"

if not d_path.exists():
    print(f"[add_drag] {d_path} が無い。")
    print("  ドラッグ問題の訳・解説は seq をキーにこのファイルへ書く(形式は docstring 参照)。")
    print("  .gitignore 済みなので公開されない。")
    sys.exit(0)

D = json.loads(d_path.read_text(encoding="utf-8"))
D = {k: v for k, v in D.items() if k.isdigit()}     # _note 等のメモキーは無視

# questions.json 側が認識しているドラッグ問題と突き合わせる(取りこぼし検出)
drag_seqs = set()
if qs_path.exists():
    for q in json.loads(qs_path.read_text(encoding="utf-8")):
        if q.get("is_drag"):
            drag_seqs.add(str(q["seq"]))

missing = sorted(drag_seqs - set(D), key=int)
extra = sorted(set(D) - drag_seqs, key=int)
print(f"[add_drag] ドラッグ問題 {len(drag_seqs)}問 / 用意済み {len(D)}件")
if missing:
    print(f"  未対応 seq ({len(missing)}件): {', '.join(missing)}")
if extra:
    print(f"  questions.json が is_drag と判定していない seq: {', '.join(extra)}")

if "--check" in sys.argv:
    sys.exit(0)

tr = json.loads(tr_path.read_text(encoding="utf-8")) if tr_path.exists() else {}
for seq, v in D.items():
    v.setdefault("opts_ja", [])
    v.setdefault("opts_mt", [])
    tr[seq] = v

tr_path.write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[add_drag] {len(D)} 件を取り込み。translations 合計: {sum(1 for k in tr if k.isdigit())}")
