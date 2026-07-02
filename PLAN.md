# CIS-DF 学習教材化プロジェクト — プラン

ExamTopics(課金済み・Web閲覧のみ)の ServiceNow CIS-DF 問題集を、個人学習用に
日本語化・AI解説付きのスマホ対応HTMLへ変換する。

## ⚠️ 前提・リスク認識(重要)
- **ExamTopics 利用規約**: 自動アクセス・スクレイピング・再配布を禁止。課金済みでも
  「自動収集・別形式での保存/加工」は閲覧権とは別物として扱われる → アカウント停止リスク。
- **ServiceNow 認定試験ポリシー**: ブレインダンプ(流出問題集)の使用を禁止。発覚時は
  合格取消・受験禁止の対象になりうる。学習リソースとして使うこと自体にこのリスクがある。
- 上記を理解した上で、**個人学習目的**で、検知/BANリスクを抑える方式を採る。

## 確定事項
- 言語: **Python**
- 取得: **Playwright によるブラウザ自動操作(人間ペース・1ページずつ・待機あり)**
  - 自分のログインセッションを使用。全力クロールはしない(低速・低頻度)。
- AI処理: **Claude API(必要になってから)**。少量サンプルはセッション内で先行作成。
  - 翻訳: Haiku 4.5 / 解説: Sonnet 4.6 / Batch API(50%オフ)+ Prompt Caching
- 出力: **ビルド不要の静的HTML**(Vanilla JS + localStorage)、スマホ最適化

## パイプライン
```
①取得 Playwright → raw/        (生HTML or JSON)
②構造化         → data/questions.json
③信頼度判定     → confidence付与(ルールベース・AI不要)
④翻訳+AI解説    → data/translated.json
⑤HTML生成       → site/        (スマホで開くだけ)
```

## データモデル(1問)
- id, number, question, images[], options[{label,text}]
- suggested_answer, community_vote{}, discussion[]
- confidence(low/medium/high), ja{question,options[]}, ai_explanation

## 信頼度ルール
- high: ExamTopics正解 = コミュニティ最多投票 かつ 票が割れていない → 翻訳のみ
- medium: 一致するが票が割れる → 翻訳 + 簡易解説
- low: 正解≠最多投票 / 票が拮抗 → 翻訳 + 詳細解説

## 進行ステップ
1. [現在地] 1ページだけサンプルHTMLを取得し、DOM構造・URL規則を解析  ← samples/
2. 抽出ロジック + Playwright自動操作スクリプトを作成
3. 10問でAI翻訳・解説のサンプル品質確認
4. 問題数確定 → APIコスト試算 → Batch全件処理
5. HTML生成 → スマホ実機確認

## ディレクトリ
- samples/ : 構造解析用のサンプルページ(手動保存)
- raw/     : 取得した生データ
- data/    : 正規化・翻訳済みJSON
- src/     : Pythonスクリプト
- site/    : 生成された学習用HTML(site/images/ に図表)
