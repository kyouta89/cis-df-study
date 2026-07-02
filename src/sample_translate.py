#!/usr/bin/env python3
"""
サンプル翻訳・AI解説の投入(セッション内で手動生成した内容を data/translated.json へ反映)。
本番では Claude API バッチで全件生成するが、まずは数問で最終成果物の形を検証する。
seq でひも付け。未翻訳の問題は原文のまま表示される(build_site.py 側で対応)。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
qs = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))

# seq -> {ja:{question, options:[{text}...]}, ai_explanation, needs_review?}
PATCH = {
 1: {
   "ja": {"question":
     "CMDB管理者が、メンバーCIのグループ整合性をより良く維持するため、Dynamic CI Group をベースにした複数の Technology Management Service Offering(Technical Service Offering)を構築しました。\n"
     "Dynamic CI Group とのリレーションを持つオファリングから、CIへ同期されるグループはどれですか?(2つ選択)",
     "options":[{"text":"承認グループ (Approval Group)"},{"text":"管理グループ (Managed by Group)"},
                {"text":"サポートグループ (Support Group)"},{"text":"所有グループ (Owned by Group)"}]},
   "ai_explanation":
     "正解: B・C。Technical Service Offering が Dynamic CI Group とリレーションを持つと、オファリング側で設定した "
     "「Support group(サポートグループ)」と「Managed by group(管理グループ)」がメンバーCIへ同期されます。"
     "Approval Group / Owned by Group は同期対象外です。コミュニティ投票も91%がBCで一致しており、信頼度は高い問題です。"},
 8: {
   "ja": {"question":
     "データセンター管理者が CMDB CI Class Manager と協力し、Application Server とそれがホストする Application のリレーションを定義しています。"
     "同社には、1つ以上の Application をホストする Application Server が複数あります。\n"
     "Application Server テーブル([cmdb_ci_app_server])と Application テーブル([cmdb_ci_appl])のリレーションを最もよく表すのはどれですか?",
     "options":[{"text":"多対一 (Many-to-one)"},{"text":"一対一 (One-to-one)"},
                {"text":"一対多 (One-to-many)"},{"text":"多対多 (Many-to-many)"}]},
   "ai_explanation":
     "正解: D(多対多)。1台の Application Server が複数の Application をホストでき、かつ1つの Application が複数のサーバに分散され得るため、"
     "両テーブルの関係は many-to-many になります。C(一対多)と迷いやすいですが、問題文の「1つ以上の Application をホストする Application Server が複数」"
     "という双方向の多重性が決め手です。コミュニティは62%(Cを支持する票も一定数)とやや割れており、実環境の構成次第で一対多に見えるケースがある点は注意。"},
 14: {
   "ja": {"question":
     "Configuration 管理者が CMDB 内のあるCIクラスを管理しており、識別ルール(identification rule)を更新する必要があります。\n"
     "そのクラスの既存の識別ルールを参照・設定できる場所はどこですか?(2つ選択)",
     "options":[{"text":"CI Identifiers モジュール"},{"text":"API Integrations"},
                {"text":"IRE Application"},{"text":"CI Class Manager"}]},
   "ai_explanation":
     "【AI検証】ExamTopics提示は A・D(コミュニティ投票なしのためAIで検証)。\n"
     "・D: CI Class Manager のクラス詳細(Identification / Reconciliation セクション)から識別ルールを参照・設定できる → ◯\n"
     "・A: CI Identifiers モジュール([cmdb_identifier])でも識別ルールの一覧・設定が可能 → ◯\n"
     "・B(API Integrations)・C(IRE Application)は識別ルールの設定場所ではない。\n"
     "結論: A・D が妥当(確度: 中〜高)。"},
 15: {
   "ja": {"question":
     "CMDB管理者が、管理対象クラスの関連あるCIのみが Incident・Problem・Change レコードに表示されるようにしたいと考えています。\n"
     "CI Class Manager でこの結果を得るために、チェックする必要があるチェックボックスはどれですか?",
     "options":[{"text":"Principal Class"},{"text":"Independent"},
                {"text":"Main Record"},{"text":"Extensible"}]},
   "ai_explanation":
     "【AI検証】ExamTopics提示は A(Principal Class)(コミュニティ投票なし)。\n"
     "Principal Class は、そのクラスをタスク系レコード(Incident/Problem/Change 等)の Configuration item 参照で扱う"
     "「主要クラス」として指定する設定で、表示・選択されるCIを管理対象クラスに絞る役割を持ちます。"
     "Independent(リレーション独立性)・Extensible(クラス拡張可否)は目的が異なります。\n"
     "結論: A が最有力(確度: 中)。用語解釈に幅があるため、実機の CI Class Manager で当該チェックボックスの説明を確認することを推奨。"},
 2: {
   "ja": {"question":
     "【ドラッグ&ドロップ問題】アプリケーションサービスのタイプを、最も適切な説明にドラッグ&ドロップしてください。"},
   "ai_explanation":
     "⚠️ この DRAG DROP 問題は、一覧ページのHTMLにドラッグ項目・対応する説明・正解が含まれていません"
     "(別構造/ポップアップ側)。完全な解説には個別取得が必要です。→ 要・個別対応。",
   "needs_review": True},
}

by_seq = {q["seq"]: q for q in qs}
for seq, patch in PATCH.items():
    q = by_seq.get(seq)
    if not q:
        continue
    q["ja"] = patch.get("ja")
    q["ai_explanation"] = patch.get("ai_explanation")
    if patch.get("needs_review"):
        q["needs_review"] = True

(ROOT / "data" / "translated.json").write_text(
    json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[sample] patched {len(PATCH)} questions -> data/translated.json (total {len(qs)})")
