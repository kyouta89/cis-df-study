# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

ExamTopics の ServiceNow **CIS-DF**(Data Foundations / CMDB and CSDM)問題集 192問を、個人学習用に
**日本語化＋AI解説＋スマホ対応HTML化**するパイプライン。成果物は依存・ビルド不要の単一HTML
(`site/index.html`、Vanilla JS + localStorage)。言語は Python(`bs4` のみ依存)。

注意: ExamTopics ToS はスクレイピング禁止・ServiceNow はブレインダンプ使用禁止。本プロジェクトは
**手動保存したHTMLを入力**とし、自動クロールはしない方針(`PLAN.md` 参照)。AI翻訳・解説は API ではなく
Claude Code セッション内でサブエージェントが生成 → ファイル保存する**再開可能**方式。

## 現在の状態(2026-07 時点・重要)

**バッチ工程は全て完了している。着手前に必ず現状を数えること**(下記は実測値):

| 工程 | 状態 |
|---|---|
| 原文パース | 192問(うちドラッグ14問) |
| 翻訳・AI解説 | **192/192 完了**(`translations.json`) |
| 盲検独立検証 | 117問(low中心。全問対象ではない=仕様) |
| 公式docエビデンス査読 | **192/192 完了**(`review_results.json`。confirm 191 / version 1) |
| 教科書本文 | **20/20 節 完了**(`chapters.json` の全節に `content/*.md` あり) |

つまり `split_batches.py` / `split_verify.py` / `review_status.py` は**再開ポイントを出すための道具**で、
今は残件ゼロ。**サブエージェントで翻訳・査読バッチを回し直す必要はない**。日常の再生成は
`py src/merge.py` → `py src/build_site.py`(問題集)、`py src/build_textbook.py`(教科書)だけでよい。
内容を直す時も、バッチを回すのではなく `translations.json` / `review_results.json` /
`content/*.md` を直接編集 → 上記ビルドを流すのが正しい。

## パイプライン(初回構築の全手順)

データは段階的に蓄積され、最終的に `build_site.py` が単一HTMLへ合成する。**この順**(現在は完走済み):

```
raw/cisdf_page1〜4.html (手動保存・50問/頁)
  → python3 src/parse.py            # → data/questions.json(原文192問)
data/parts/out_*.json (翻訳サブエージェント出力)
  → python3 src/merge_parts.py      # → data/translations.json に取込(seqキー・追記=真実源)
data/verify/vout_*.json (盲検検証サブエージェント出力)
  → python3 src/compare_verify.py   # → data/verify_results.json
  → python3 src/merge.py            # questions + translations + verify → data/translated.json
  → python3 src/build_site.py       # → site/index.html
open site/index.html
```

ドラッグ問題14問の翻訳・解説は `py src/add_drag.py` で `translations.json` に追記する。中身は
**`data/drag_answers.json`**(seqキー)にあり、スクリプトはそれを読むだけ(2026-07-29 に方式変更。理由は
下記「公開ポリシー」)。これらは一覧HTMLに正解が無く `raw/cisdf_drag1.html` 等で個別取得している。
`--check` で未対応 seq を確認できる。

## 真実源(source of truth)とデータの流れ

- **`data/questions.json`** — `parse.py` が生成する原文。再生成可能。1問のキー:
  `seq`(通し番号・全体で一意), `topic`+`number`(トピック内番号。番号はトピックごとにリセットするため
  `(topic, number)` で一意), `question`, `options[{label,text}]`, `suggested_answer`(ExamTopics提示正解),
  `community_vote`/`community_answer`/`community_pct`/`vote_total`(コミュニティ投票),
  `confidence`(low/medium/high), `is_drag`(ドラッグ問題=14問), `*_images`, `discussion`。
- **`data/translations.json`** — 翻訳・解説の**蓄積=再開の真実源**。キーは `seq`(文字列)。手で消さない。
  フィールド: `q_ja`/`opts_ja`(綺麗な学習用訳), `q_mt`/`opts_mt`(本番風=機械翻訳調訳), `ai`(AI解説)。
  先頭に `_note`(非数字キー)のメモが1件入っている——`merge_parts.py` が数字キー以外を読み飛ばす仕様に
  乗っているので**消さない・エラーではない**。
- **`data/verify_results.json`** — 盲検独立検証(下記)の突合結果。`merge.py` が `q.verify` として取込。
  ※**現在UIには非表示**(査読の踏み台。下記 review に発展)。
- **`data/review_results.json`** — **公式docエビデンス査読の結果(seqキー・全192問)**。`merge.py` が `q.review_doc` として取込。
  値: `suggested`/`doc_answer`/`verdict`(confirm/version/uncertain)/`confidence`(high/medium)/`evidence`[{point,source,url}]/`note`/`ai_blind`。
  これが**画面に出る唯一の検証**=正解横の小バッジ(✅公式doc / ✅公式doc確度中 / 🕒版依存)＋「出典・補足」折りたたみ(出典URL、version/確度中のみ note も)。
  作り方(既に完走済み): `review_status.py` で優先順の未査読seqを出す→中身を読んで査読→1問ずつ追記(中断耐性)。確度=docがどれだけ直接決着させたか。
- **`data/translated.json`** — `merge.py` の出力。`build_site.py` の入力(無ければ `questions.json` で代替)。

`confidence` ルール: high=提示正解とコミュニティ最多投票が一致かつ票が割れない / low=不一致 or 投票なし。

## 翻訳・検証のサブエージェント方式(重要)

API を使わず、Claude Code 内の並列サブエージェントで生成する2つのバッチ工程がある:

1. **翻訳/解説**: `split_batches.py`(未訳の非ドラッグ問題を20問ずつ `data/parts/in_*.json` へ分割)
   → 各バッチをサブエージェントが処理 → `data/parts/out_*.json` に保存 → `merge_parts.py` で取込。
2. **盲検独立検証**: `split_verify.py`(low・非ドラッグ問題を提示正解・投票を**見せずに** `data/verify/vin_*.json` へ分割)
   → サブエージェントが独立解答 → `data/verify/vout_*.json` → `compare_verify.py` で提示正解と突合。
   HTMLに ✅一致/⚠️不一致/🕒バージョン依存 を表示する。ダンプ誤りの早期発見が目的。

`out_*` / `vout_*` のキーは `seq`(文字列)、値は対応するフィールドを持つ dict。`merge_parts.py` /
`compare_verify.py` は数字キー以外・不正JSONをスキップして読む(部分的な再実行に強い)。

## 構成

- `src/` — 全 Python スクリプト(上記)。`ROOT = Path(__file__).resolve().parent.parent` 基準で
  リポジトリ相対にパスを解決するので、どこから実行してもよい。依存は `bs4`(beautifulsoup4)のみ・ビルド無し。
  **このマシン(現行PC)の Python**: `C:\Users\kyout\AppData\Local\Programs\Python\Python312\python.exe`
  (winget で導入)。⚠️ **裸の `python` / `python3` は Windows ストアのスタブに解決され実行できない**
  (`exit 49`)。`py` ランチャ(新シェルで有効)か上記フルパスで呼ぶこと。`bs4` は `pip install beautifulsoup4` 済み。
- `src/sample_translate.py` — **旧プロトタイプ(非推奨・パイプライン外)**。`translated.json` を直接書き、
  しかも本番と別スキーマ(`ja`/`ai_explanation`、現行は `q_ja`/`opts_ja`/`ai`)を使う。現行の正規ルートは
  上記の `merge_parts.py`→`merge.py`→`build_site.py`。混同しないこと(実行すると `merge.py` の出力を上書きする)。
- `raw/` — 手動保存した入力HTML。`samples/` — 構造解析用サンプル。
- `data/` — 上記JSON群。`data/parts/`(翻訳バッチ I/O)・`data/verify/`(検証バッチ I/O)。
- `site/index.html`(生成物・単一ファイル) + `site/images/`(図表33枚・ローカル保存)。
- `PLAN.md` — 当初プラン・リスク認識。ドメイン背景(CSDM 5.0 vs 4.0 等)はメモリ参照。

## 教科書ステージ(本文20節は完成済み・2026-06 開始)

問題集を核に CIS-DF を体系学習できる「教科書」を作る。**成果物は `site/textbook.html`(独立HTML)**で、
`index.html` のヘッダから「📘 教科書」リンクで繋ぐ。当初は index.html 内のタブに合成する案だったが、
**教科書だけを公開できる(=出版安全)よう独立HTMLに分けた**——問題集HTMLはExamTopics由来なので公開不可。
戻して合成しないこと。章＝公式ブループリントの加重ドメイン
(Governance 35% / Insight 20% / Ingestion 19% / Configuration 15% / CSDM 11%)。`data/questions.json`
の `topic`(ExamTopics の便宜的5分割)とは**無関係**——各問はドメインへ内容で分類し直す(`qmap` 予定)。

**出典源は GitHub の公式Markdown(重要)**: ServiceNow は製品docを **LLM最適化Markdown**として
`ServiceNow/ServiceNowDocs`(GitHub)で公開している(`markdown/<product>/<classification>/<file>.md`、
リリース系列ごとのブランチ。最新系列=`australia`、月次更新、画像なし)。各ファイルはフロントマター付き
(`title`/`description`/**`canonical_url`=出典URL**/`release`/`classification`/`topic_type`/`last_updated`)。
→ `raw.githubusercontent.com/ServiceNow/ServiceNowDocs/<branch>/markdown/...` から**直接DLでフル原文取得**。
**`docs.servicenow.com`(→`www.servicenow.com/docs/`)の本体は React SPA + shadow DOM** で WebFetch では本文が
取れない(`EMPTY SHELL`)・ブラウザ描画後抽出も脆い。**SPA を相手にせず GitHub raw を使うのが正解**。

CIS-DF 関連の分類フォルダ(`markdown/servicenow-platform/` 配下、計496 md): `configuration-management-database-cmdb`(407)
/ `common-service-data-model-csdm`(59) / `cmdb-ci-class-models`(21) / `cmdb-integration-commons`(9)。

- `data/textbook/chapters.json` — 目次(章・節の骨格＝構造の真実源)。
- `data/textbook/catalog/file_index.json` — 上記4フォルダの md ファイル名一覧(選別の土台。DL済=トークン消費なし)。
- `data/textbook/sources.json` — 出典取得キュー。`pages[]` に `{id, section, folder, file}`(raw URLは導出)。
- `data/textbook/raw/<id>.md` — DL した公式Markdown原文。**1ファイルDLごとに即保存**。
- `src/fetch_docs.py` — 出典DL本体。`sources.json` の `pages[]` を読み `raw.githubusercontent.com/<repo>/<branch>/<base>/<folder>/<file>`
  から取得→`raw/<id>.md`(id=ファイル名stem)へ即保存。既存はスキップ(`--force` で再取得)・失敗は記録して次へ(中断耐性)。
- `src/fetch_docs_status.py` — 進捗＝**再開ポイント**表示。`sources.json` と `raw/*.md` を突合し未取得だけ出す。
  現状 `sources.json` のキュー74件に対し `raw/` は92件(キュー外に手で足した分がある)。**差分は不整合ではない**
  ——status はキューを基準に見るので、余分な md は無視される。
- `data/textbook/content/<section>.md` — 生成した教科書本文(中間スタイル=解説＋要点)。フロントマターに
  `sources`(出典=canonical_url)・`related_seqs`(qmap で埋める・現状空)。
- `src/build_textbook.py` — 教科書ジェネレータ。chapters.json＋content/*.md → **`site/textbook.html`**(問題集とは別の
  **出版安全な独立HTML**。ExamTopics由来の問題は含めない・末尾に免責/帰属)。**ビルド時のみ Python-Markdown 依存**
  (`pip install markdown`、出力HTMLは依存なし)。デザインは index.html と同じCSS変数で統一。

**取得は `Invoke-WebRequest`/HTTP DL でトークン非消費**(モデルを使うのは翻訳・解説生成のみ=既に再開可能バッチ)。
よって「使用制限」リスクは取得段では実質ゼロ。出典は各 md の `canonical_url` をそのまま引けばよい。

節本文の `related_seqs`(その節に対応する問題の seq)は**まだ空**。埋める `qmap` は未実装で、
`build_textbook.py` も現状この値を読んでいない(問題集と教科書のリンクは未着手)。

## 公開ポリシー(git で最重要)

**このリポジトリは GitHub で公開されている**が、公開しているのは**自作コードと教科書だけ**。
`.gitignore` が ExamTopics 由来のものを全除外している: `raw/` `samples/` `data/*.json`
`data/parts/` `data/verify/` `site/index.html` `site/images/`、および第三者コンテンツの `data/textbook/raw/`。

- **問題文・選択肢・正解・翻訳・査読結果を commit しない**(ExamTopics ToS / ServiceNow ブレインダンプ禁止)。
  `git add -A` は無害だが、`git add -f` で除外物を足したり `.gitignore` を緩めたりしないこと。
- **鉄則: 問題データは必ず `data/` 配下の JSON に置く。`.py` に書かない。**
  `.gitignore` が守るのは `data/` 系だけで `src/*.py` は公開対象。実際 `add_drag.py` は正解と訳文を
  辞書でハードコードしており、**14問分の正解が公開リポジトリに載っていた**(2026-07-29 発見・是正済み。
  中身は `data/drag_answers.json` へ移動)。**過去のコミット履歴には残っている**(履歴の書き換えは未実施)。
  push前の `git diff --cached --name-only` チェックはファイル名しか見ないので、この型の事故は防げない。
- 結果として**このリポジトリの clone 単体では `site/index.html` は再生成できない**(入力HTMLが無い)。
  これは仕様。教科書側(`build_textbook.py`)だけは clone から再ビルドできる。
- 詳細と免責は `README.md` を参照。

## コマンド(このマシン)

`py` ランチャ推奨(裸の `python`/`python3` はストアのスタブで `exit 49`)。テストもリンタも無し。
**日本語コンソール(cp932)の文字化け・例外に注意**: 日本語や絵文字を print するスクリプトは
`sys.stdout.reconfigure(encoding="utf-8")` を先頭に置く(`review_status.py` が実例)。
その場かぎりの `py -c "..."` で JSON の中身を覗く時は **`py -X utf8 -c "..."`** にしないと
`UnicodeEncodeError` で落ちる。ファイル読み書きは常に `encoding="utf-8"` を明示(既存コードは徹底済み)。

```powershell
py src/parse.py            # raw/*.html      -> data/questions.json
py src/split_batches.py    # 未訳を20問ずつ  -> data/parts/in_*.json
py src/merge_parts.py      # out_*.json 取込 -> data/translations.json
py src/review_status.py    # 査読の未処理seq(優先順)を表示 = 再開ポイント
py src/merge.py            # questions+translations+review -> data/translated.json
py src/build_site.py       # -> site/index.html
py src/fetch_docs_status.py; py src/fetch_docs.py   # 公式doc DL(未取得のみ)
py src/build_textbook.py   # -> site/textbook.html  (要 pip install markdown)
```
