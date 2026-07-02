#!/usr/bin/env python3
"""
ExamTopics CIS-DF パーサー
保存したページHTML(1問〜50問/ページ)から問題・選択肢・正解・投票分布・
Discussion(インライン分)を抽出し、data/questions.json を生成する。

使い方:
    python3 src/parse.py samples/sample1.html
    python3 src/parse.py raw/*.html
    python3 src/parse.py            # 引数なし → raw/*.html を対象
"""
import sys, re, json, glob, html
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent


def text_of(el):
    return el.get_text(" ", strip=True) if el else ""


def parse_question(card, seq):
    q = {}

    body = card.select_one(".question-body")
    q["data_id"] = body.get("data-id") if body else None

    # 問題番号/トピック: カードヘッダー "Question #1 Topic 1" から拾う
    hdr = text_of(card.select_one(".card-header"))
    mnum = re.search(r"Question\s*#?\s*(\d+)", hdr, re.I)
    mtop = re.search(r"Topic\s*(\d+)", hdr, re.I)
    # フォールバック: 単独ページの data-title="... question N ..."
    if not mnum:
        dt = card.find(attrs={"data-title": re.compile(r"question", re.I)})
        if dt:
            mnum = re.search(r"question\s+(\d+)", dt["data-title"], re.I)
    q["number"] = int(mnum.group(1)) if mnum else seq
    q["topic"] = f"Topic {mtop.group(1)}" if mtop else text_of(card.select_one(".question-title-topic"))

    # 問題文: question-answer クラスでない card-text
    qtext = ""
    for ct in (body.select(".card-text") if body else []):
        if "question-answer" not in (ct.get("class") or []):
            qtext = ct.get_text("\n", strip=True)
            break
    q["question"] = qtext

    # 画像(ローカルパスへ書換え: images/imageN.png)
    def localize(src):
        m = re.search(r"(image\d+\.(?:png|jpg|jpeg|gif|webp))(?:\?|$)", src or "", re.I)
        return f"images/{m.group(1)}" if m else None
    ans_imgs = [localize(i.get("src")) for i in card.select(".correct-answer img")]
    q["answer_images"] = [x for x in ans_imgs if x]
    qimgs = []
    if body:
        for img in body.select("img"):
            if img.find_parent(class_="correct-answer") or img.find_parent(class_="question-answer"):
                continue
            l = localize(img.get("src"))
            if l:
                qimgs.append(l)
    q["question_images"] = qimgs
    q["is_drag"] = bool(re.search(r"drag\s*and\s*drop|drag drop", q["question"], re.I))

    # 選択肢
    choices = []
    for li in card.select(".question-choices-container li.multi-choice-item"):
        letter_el = li.select_one(".multi-choice-letter")
        letter = (letter_el.get("data-choice-letter") or text_of(letter_el).strip(". ")) if letter_el else ""
        # 選択肢テキスト = li 全体から letter span と badge を除去
        clone = BeautifulSoup(str(li), "html.parser")
        for rm in clone.select(".multi-choice-letter, .most-voted-answer-badge"):
            rm.decompose()
        choices.append({"label": letter, "text": clone.get_text(" ", strip=True),
                        "community_most_voted": bool(li.select_one(".most-voted-answer-badge"))})
    q["options"] = choices

    # 正解 (ExamTopics提示)
    q["suggested_answer"] = text_of(card.select_one(".correct-answer"))

    # 投票分布 (埋め込みJSON)
    votes = []
    tally = card.select_one(".voted-answers-tally script[type='application/json']")
    if tally and tally.string:
        try:
            votes = json.loads(tally.string)
        except Exception:
            votes = []
    q["community_vote"] = votes
    total = sum(v.get("vote_count", 0) for v in votes) or 0
    q["vote_total"] = total
    most = next((v for v in votes if v.get("is_most_voted")), None)
    q["community_answer"] = most.get("voted_answers") if most else ""
    q["community_pct"] = round(100 * most.get("vote_count", 0) / total) if (most and total) else None

    # Discussion(インライン分)
    comments = []
    for c in card.select(".comment-container"):
        # ネストした返信も拾うが、まずはフラットに
        comments.append({
            "comment_id": c.get("data-comment-id"),
            "author": text_of(c.select_one(".comment-head h5")),
            "date": text_of(c.select_one(".comment-date")),
            "selected_answer": text_of(c.select_one(".comment-selected-answers")),
            "content": text_of(c.select_one(".comment-content")),
            "upvotes": text_of(c.select_one(".upvote-count")),
            "is_most_voted_comment": "most-voted" in " ".join(c.get("class") or []),
        })
    q["discussion"] = comments

    # 信頼度スコア(ルールベース)
    q["confidence"] = score_confidence(q)
    return q


def score_confidence(q):
    sa = (q.get("suggested_answer") or "").replace(" ", "")
    ca = (q.get("community_answer") or "").replace(" ", "")
    pct = q.get("community_pct")
    if not ca or not sa:
        return "low"
    if sa != ca:
        return "low"               # 提示正解とコミュニティ最多が不一致
    if pct is None:
        return "medium"
    if pct >= 80:
        return "high"
    if pct >= 55:
        return "medium"
    return "low"


def parse_file(path):
    soup = BeautifulSoup(Path(path).read_text(encoding="utf-8", errors="replace"), "html.parser")
    cards = soup.select(".exam-question-card")
    out = []
    for i, card in enumerate(cards, 1):
        out.append(parse_question(card, i))
    return out


def main():
    args = sys.argv[1:]
    files = []
    for a in args:
        files.extend(sorted(glob.glob(a)))
    if not files:
        files = sorted(glob.glob(str(ROOT / "raw" / "*.html")))
    if not files:
        print("対象HTMLが見つかりません。引数でファイルを指定してください。")
        sys.exit(1)

    all_q = []
    for f in files:
        qs = parse_file(f)
        print(f"[parse] {f}: {len(qs)} questions")
        all_q.extend(qs)

    # data_id で重複排除(複数ページ間の重なり対策)
    seen, dedup = set(), []
    for q in all_q:
        key = q.get("data_id") or f"seq-{q.get('number')}"
        if key in seen:
            continue
        seen.add(key)
        dedup.append(q)

    def topic_num(q):
        m = re.search(r"(\d+)", q.get("topic") or "")
        return int(m.group(1)) if m else 0
    dedup.sort(key=lambda q: (topic_num(q), q.get("number") or 0))
    for i, q in enumerate(dedup, 1):
        q["seq"] = i  # 全体通し番号(表示・ID用)

    out_path = ROOT / "data" / "questions.json"
    out_path.write_text(json.dumps(dedup, ensure_ascii=False, indent=2), encoding="utf-8")

    # サマリー(本文は出さず統計のみ)
    from collections import Counter
    conf = Counter(q["confidence"] for q in dedup)
    print(f"\n[done] {len(dedup)} questions -> {out_path}")
    print(f"  confidence: high={conf['high']} medium={conf['medium']} low={conf['low']}")


if __name__ == "__main__":
    main()
