---
chapter: ch2
section: ch2-s1
title: CMDB データの可視化 — Workspace と Insights ダッシュボード
sources:
  - title: CMDB Workspace store app
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/cmdb-workspace.html
  - title: Insights view in Service Graph Workspace
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/sg-workspace-insights-view.html
  - title: CMDB Data Foundations dashboard
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/cmdb-data-foundations-dashboard.html
related_seqs: []
---

## Insight ＝ ガバナンスされたデータから価値を引き出す

第1章で「健全化」し第3章で「正しく取り込んだ」CMDBデータを、**可視化して意思決定に使う**のが Insight 領域。
中心は2つのワークスペースと、その **Insights（インサイト）ダッシュボード**群。

### CMDB Workspace / Service Graph Workspace

- **CMDB Workspace**：CMDBの検索・探索、健全性や最近のアクティビティの確認、各ダッシュボード/ツール
  （**CMDB Health・Data Manager・CMDB 360**）への入口。ビューは Home / Insights / Management / Governance など。
- **Service Graph Workspace**：データオーナー視点。**Insights / Ingestion / Governance** などのビューを持つ。

### Insights ダッシュボード（Service Graph Workspace）

ナビゲーションの **Insights アイコン**から、集計・状態・健全性を示すダッシュボードを見る。
**必要ロール：`sn_cmdb_user` 系**（`sn_cmdb_user` / `sn_cmdb_editor` / `sn_cmdb_admin`）。アクセス権のあるものだけ表示。

| ダッシュボード | 見えるもの |
|---|---|
| **CMDB Health** | 健全性スコア（3C＋Relationships） |
| **CMDB Data Foundation** / **CSDM Data Foundation** | データ基盤の成熟度（getwell） |
| **Service instances** | サービスインスタンスの状態 |
| **CMDB 360** | 属性のソース別履歴（第3章） |
| **CMDB success advisor** / **Feature adoption** / **Performance insights** | 改善提案・機能採用・性能 |

> 📌 **要点**：「健全性・データ基盤・サービス・360・採用度」を**ダッシュボードで俯瞰**するのが Insight。
> アクセスは Workspace の **Insights ビュー**、最低限 `sn_cmdb_user` ロールが要る。

## Data Foundations ダッシュボード

CMDB/CSDM の**データ基盤がどれだけ整っているか**を段階的に示すダッシュボード。
CSDM 側は **crawl / walk / run / fly** の成熟ステージ（第5章）に対応するタブで進捗を可視化する。

**主要用語**：CMDB Workspace / Service Graph Workspace / Insights ビュー / Data Foundation(getwell) /
`sn_cmdb_user`・`sn_cmdb_editor`・`sn_cmdb_admin`。
