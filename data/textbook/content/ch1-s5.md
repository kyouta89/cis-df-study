---
chapter: ch1
section: ch1-s5
title: Remediation（是正）— CMDB Remediation Rule とワークフロー
sources:
  - title: Create a CMDB remediation rule
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_CreateCMDBRemediationRule.html
  - title: Apply CMDB remediation
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_ApplyCMDBRemediation.html
related_seqs: []
---

## CI Remediation（是正の仕組み）

CMDB Health は、健全性テストに**失敗したCI**へ修正アクションを、管理された標準的なやり方で
適用する**是正(remediation)フレームワーク**を提供する。失敗したCIには**タスク**が作られ、
そこに **CMDB Remediation Rule** を紐づけてワークフローを実行する（例：stale/orphan なCIを削除）。

### 事前準備：是正ワークフロー

- 先に**是正ワークフローを作成して publish**（**Workflow [wf_workflow]** テーブル）。Classic でも Orchestration でも可。
- ワークフローの**テーブルは是正ルールの Task type と一致**させる。
- ワークフロー側の **If condition matches を `None`** にして条件を持たせない
  → **是正ルール側のフィルタ**が効くようにする。
- **必要ロール**：`sn_cmdb_admin` または `itil_admin`（`sn_cmdb_editor` / `itil` の上に付与）。

### CMDB Remediation Rule の主なフィールド

| フィールド | 説明 |
|---|---|
| **Task type** | 是正対象の CMDB ヘルス関連タスクの種類 |
| **Task filter** | 対象タスクの絞り込み（CIフィールドへの **dot-walking** 可） |
| **Execution** | **Manual**＝手動適用 ／ **Automatic**＝条件一致タスクの**作成時に一度**自動適用 |
| **Active** | ワークフロー実行の許可 |
| **Workflow** | 実行する是正ワークフロー |

> 📌 **要点**：
> - **Automatic** … ビジネスルール ***Run remediations for CMDBHealth task*** が、Task filter に一致するCIへ
>   ワークフローを適用（タスク作成時に1回）。
> - **Manual** … ルールに定義したワークフローを**手動で**適用（**Apply CMDB remediation**）。

### 章のまとめ（Governance / CMDB Health）

1. 健全性は **Completeness / Correctness / Compliance（＋Relationships）** で測る（[§1](#ch1-s1)）。
2. **ダッシュボード**で可視化、**ジョブ有効化**と**KPI/メトリクス設定**で運用に合わせる（[§2](#ch1-s2)）。
3. **重複**は IRE がタスク化 → **Main CI / `duplicate_of`** で統合（単一ウィザード or 一括テンプレート）（[§3](#ch1-s3)）。
4. **Data Manager** でライフサイクル統制、**監査/認証**が **Compliance** を支える（[§4](#ch1-s4)）。
5. 失敗CIは **Remediation Rule＋ワークフロー**で標準的に是正（本節）。

**ナビ重要**：是正の起点は常に「**健全性テスト失敗 → タスク → ルール → ワークフロー**」という流れ。
