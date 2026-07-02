#!/usr/bin/env python3
"""盲検結果(vout_*.json)と ExamTopics提示正解を突き合わせ、verify_results.json を作る。"""
import json, glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
qs = {q["seq"]: q for q in json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))}

def norm(ans):
    return "".join(sorted(re.findall(r"[A-Z]", (ans or "").upper())))

res = {}
for f in sorted(glob.glob(str(ROOT / "data" / "verify" / "vout_*.json"))):
    try:
        d = json.loads(Path(f).read_text(encoding="utf-8"))
    except Exception as e:
        print("parse error", f, e); continue
    for seq, v in d.items():
        if not str(seq).isdigit():
            continue
        sq = qs.get(int(seq))
        if not sq:
            continue
        ai = norm(v.get("ai_answer"))
        sug = norm(sq.get("suggested_answer"))
        res[str(seq)] = {
            "ai_answer": v.get("ai_answer", ""),
            "suggested": sq.get("suggested_answer", ""),
            "match": (ai == sug and ai != ""),
            "ai_confidence": v.get("ai_confidence", ""),
            "reasoning": v.get("reasoning", ""),
            "version_flag": bool(v.get("version_flag")),
            "version_note": v.get("version_note", ""),
        }

(ROOT / "data" / "verify_results.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

match = [s for s, v in res.items() if v["match"]]
mism = [s for s, v in res.items() if not v["match"]]
vflag = [s for s, v in res.items() if v["version_flag"]]
print(f"検証済み: {len(res)}問")
print(f"  ✅ 一致(提示正解とAI独立解答が同じ): {len(match)}")
print(f"  ⚠️ 不一致(要確認): {len(mism)}")
print(f"  🕒 バージョン依存フラグ: {len(vflag)}")
print("\n=== 不一致リスト(seq / トピックQ / 提示 → AI独立 / AI確度) ===")
for s in sorted(mism, key=lambda x: int(x)):
    v = res[s]; q = qs[int(s)]
    print(f"  {s:>3}問目 ({q['topic']} Q{q['number']}): 提示 {v['suggested'] or '(なし)'} → AI {v['ai_answer']}  [AI確度:{v['ai_confidence']}]")
