---
chapter: ch2
section: ch2-s3
title: レポート・CMDB Coverage・CIの変化と再分類
sources:
  - title: Exploring CMDB Coverage
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/cmdb-coverage-explore.html
  - title: Configure CI reclassification during IRE processing
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CIReclassification.html
  - title: View CI changes
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_ViewCIChanges.html
related_seqs: []
---

## レポート（データから報告へ）

ダッシュボードに加え、CMDB は**レポート**で洞察を共有できる。
**CMDB Query Builder**（前節）の**クエリ結果からレポートを作成**でき、横断的な問い
（例：あるサービス配下の stale なサーバ一覧）を定型レポート化して関係者と共有する。

## CMDB Coverage（網羅度を測る）

「Discovery を使っているのに、CMDB が**本当に網羅できているか**分からない」という課題に答える機能。
**IPAM（IP アドレス管理）システムの IP と、discover 済みCIを相関**させ、**抜け（カバーされていない範囲）**を可視化する。

- IPAM データと discover 済みCIの**突合・相関**。
- IPアドレスのカバー漏れ＝**未発見の領域**をハイライト。
- 継続的なカバレッジ追跡、**Discovery スケジュールの抜け検出**（IPAM サブネット vs スケジュール済み範囲）。

> 📌 **要点**：CMDB Coverage は「**入っているデータの健全性**(第1章 Health)」ではなく、
> 「**そもそも入っていない領域がないか**(網羅度)」を測る。Health と Coverage は別の問い。
> （Zurich/Australia 以降のアプリ）

## CI の変化（CI Changes / timeline）

CIフォームから **CI Changes（変化の履歴）** を見ると、属性やリレーションが**いつ・どのソースで**変わったかを追える。
監査・トラブルシュート時に「誰が/何が変えたか」を遡れるのが価値。

## CI の再分類（Reclassification）

IRE 処理中、CIが**別の `sys_class_name`（クラス）に変わるべき**と判定されることがある（reclassification）。

- 既定では**自動で再分類**。自動を無効化すると、**reclassification タスク**が生成されレビュー対象になる。
- クラスは **upgrade / downgrade / switch（別ブランチへ）** のいずれかで変わる。
- 関連プロパティ：`glide.class.upgrade.enabled` / `downgrade.enabled` / `switch.enabled`（既定 true）。

> ⚠️ **引っかけ**：**再分類は「識別ルールが同一」のクラス間でしか行えない**。
> 識別ルールが異なるクラスへは再分類できない、という制約が問われやすい。

**主要用語**：クエリ結果レポート / CMDB Coverage（IPAM相関・網羅度）/ CI Changes /
reclassification（upgrade・downgrade・switch、識別ルール同一が条件）。
