---
chapter: ch2
section: ch2-s2
title: サービス視点・リレーション活用とベンチマーク
sources:
  - title: CMDB 360 view in CMDB Workspace
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/cmdb-workspace-cmdb360-view.html
  - title: View CMDB benchmarks
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/view-cmdb-benchmarks.html
  - title: CMDB Query Builder
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/cmdb-query-builder-landing-page.html
related_seqs: []
---

## サービス視点でCMDBを読む

CMDBの価値は、CIを**サービスやリレーションの文脈**で見たときに出る。

- **サービスマップ / Application service map**：サービスを構成するCIとその依存を図で表示。1つのCIの障害が
  サービス全体へどう波及するか（インパクト分析）を理解できる。
- **CMDB 360 ビュー**（CMDB Workspace）：属性値が**どの discovery source 由来か**を属性レベルで可視化し、
  ソースの比較・取り消し・再計算を行う（第3章の CMDB 360 のUI入口）。
- **Dependency Views / Unified Map**：CI間の関係をたどって影響範囲を把握。

## CMDB Query Builder

**CMDB Query Builder** は、複数クラス・複数リレーションにまたがる**横断クエリ**をGUIで組み立てるツール。
「あるサービスに属し、かつ stale なサーバ」のような**関係をまたぐ問い**に答え、データから洞察を引き出す。

## ベンチマーク（自組織を客観視する）

**Benchmarks ダッシュボード**は、CMDB Health メトリクスを基に**月次平均・トレンド・同業他社/グローバル比較**を示す。

- 指標：**% 非準拠CI / % 重複CI / % stale CI**。
- 前提：**CMDB Health Dashboard ジョブが有効**で健全性データが収集されていること。

> 📌 **要点**：Insight の出口は「**サービス文脈の可視化（マップ/360/クエリ）**」と「**ベンチマークで他社比較**」。
> 健全性スコア（第1章）が、Insightでは"見える化"され、改善アクションに繋がる。

> ⚠️ **引っかけ**：ベンチマークの3指標は **非準拠・重複・stale** の割合（月次平均）。
> これらは第1章の Correctness/Compliance メトリクスと対応している。

**主要用語**：application service map / CMDB 360 ビュー / Dependency Views・Unified Map /
CMDB Query Builder / Benchmarks（非準拠・重複・stale の月次平均）。
