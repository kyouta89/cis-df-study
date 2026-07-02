---
chapter: ch1
section: ch1-s2
title: Health ダッシュボードと KPI / メトリクスの設定
sources:
  - title: View CMDB Health Dashboard
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_MonitorCMDBHealth.html
  - title: CMDB Health KPIs and metrics
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_CMDBHealthMetrics.html
  - title: Enable and configure a CMDB Health Dashboard job
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_EnableCMDBHealthDashboardJob.html
related_seqs: []
---

## ダッシュボードと設定

### CMDB Health Dashboard のビュー

メインの **CMDB Health Dashboard** には3つのビューがある：

- **Class View** — クラス/CI の健全性をメトリクス・KPI・クラス階層で集約表示。失敗CIの是正タスクへアクセス可。
- **Service View** — サービス単位の健全性。サービスに属するCIごとの詳細。
- **Health Group View** — タイプ **Health** の CMDB グループ単位の健全性。

別途 **Relationship Health Dashboard**（重複/孤立/陳腐なリレーション）や、CIフォーム上の
**CI Health** タイルもある。ダッシュボードは **CMDB Workspace** または **Service Graph Workspace** から開く。

> 📌 **要点（セットアップ）**：健全性データの収集・集約には、初期状態で**無効**の
> **CMDB Health Dashboard ジョブ**を**有効化**する必要がある。あわせて system property と
> KPI/メトリクスのテストルールを組織標準に合わせて構成する。

### KPI / メトリクスの設定どころ

| 場所 | 何を設定するか |
|---|---|
| **CI Class Manager**（Configuration > CI Class Manager） | orphan ルール・audit 証明書・recommended fields ルールなど、**健全性テストに使う規則と定義**を管理 |
| **CMDB Health Preferences**（Configuration > Health Preferences） | system property、ジョブ有効化、KPI/メトリクスの有効・無効、**最大失敗しきい値(threshold)**、失敗CIへのタスク生成 |

ベースシステムでは**全KPI・全メトリクスが対象に含まれる**。どの KPI/メトリクスを評価・ダッシュボードに
含めるかは設定で変更でき、メトリクスには**重み付け**を構成できる。

### 試験で効く具体値

- **Staleness（陳腐化）の既定ルール**：`cmdb_ci` クラスに **Effective Duration = 60日** の既定 staleness ルール。
  全拡張クラスに適用され、クラス固有ルールで上書き可。クラス固有が無ければ既定が使われる。
- **Duplicate メトリクス**：**識別ルール(identification rules)** で検出し、**independent な CI のみ**が重複評価対象。
  1セット内の「重複数」＝セット内CI総数 − 1。
- **Compliance**：**監査(Audit)を有効化**しないと結果が出ない。**scripted audit は Last run date が未設定**のため、
  コンプライアンスKPIに含めるにはスクリプト側で実行時刻を記録する必要がある。

**主要プロパティ**：`glide.cmdb.health.src.cmdb_health_audit_only`（true で CMDB Health 由来の結果のみ集約）。
