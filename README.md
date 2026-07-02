# CIS-DF 学習パイプライン & 教科書

ServiceNow **CIS-DF**(Certified Implementation Specialist – Data Foundations / CMDB & CSDM)を
個人学習するために自作した、**Python パイプライン**と**教科書(HTML)**です。

> [!IMPORTANT]
> このリポジトリには **ExamTopics 由来の問題文・選択肢・正解・翻訳・査読データは一切含まれていません**。
> ExamTopics の利用規約(スクレイピング禁止)と ServiceNow のポリシー(ブレインダンプ使用禁止)を尊重し、
> 公開しているのは **自分で書いたコードと教科書だけ** です(`.gitignore` で問題データを全除外)。
> したがって、このリポジトリ単体では問題集HTML(`site/index.html`)は再生成できません。

## 含まれるもの

- `src/*.py` — パイプライン全スクリプト(パース／翻訳マージ／査読集計／サイト生成／教科書生成 など)。
  依存は `beautifulsoup4` のみ、教科書ビルド時のみ `markdown`。
- `data/textbook/` — 教科書の骨格と本文(自作)。
  - `chapters.json` — 目次(章＝公式ブループリントの加重ドメイン)。
  - `content/*.md` — 各節の本文(公式Docsを出典に自分で執筆した解説)。
  - `sources.json` / `catalog/file_index.json` — 出典取得キューとファイル索引。
- `site/textbook.html` — 生成済みの教科書(単一HTML・依存なし・帰属/免責付き)。**出版安全**(ExamTopics由来の問題を含まない)。
- `CLAUDE.md` / `PLAN.md` — 設計メモとプラン。

## 含まれないもの(意図的に除外)

`data/*.json`(問題文・翻訳・正解・査読結果)、`data/parts/` `data/verify/`(翻訳・検証バッチ)、
`site/index.html`(問題集)、`site/images/`(試験の図)、`raw/` `samples/`(手動保存した入力HTML)、
`data/textbook/raw/`(DLした公式Docs原文=第三者コンテンツ)。

## 教科書のビルド

```bash
pip install markdown
python src/build_textbook.py     # data/textbook/{chapters.json,content/*.md} -> site/textbook.html
```

公式Docs原文が必要な場合は `data/textbook/sources.json` を元に取得できます(トークン非消費のHTTP DL):

```bash
python src/fetch_docs.py         # -> data/textbook/raw/<id>.md
```

## 出典・免責

- 教科書本文の出典は ServiceNow 公式製品ドキュメント
  ([ServiceNow/ServiceNowDocs](https://github.com/ServiceNow/ServiceNowDocs), Apache-2.0)。各節に出典URLを明記。
- 本リポジトリは **非公式・個人の学習用** であり、ServiceNow, Inc. とは無関係です。
- ServiceNow, CMDB, CSDM, CIS-DF 等は ServiceNow, Inc. の商標です。
