---
chapter: ch1
section: ch1-s4
title: Data Manager とポリシー、データ認証（Compliance）
sources:
  - title: Components related to CMDB Data Manager
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/components-cmdb-data-manager.html
  - title: Data Certification
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_DataCertification.html
  - title: CMDB Health KPIs and metrics（Compliance / Audit）
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_CMDBHealthMetrics.html
related_seqs: []
---

## CMDB Data Manager

**CMDB Data Manager** は、CIの**ライフサイクル（保持・退役・削除/アーカイブ・認証/証明）**を
**ポリシー**で管理するガバナンスツール。CMDB Workspace の **Management**、または
Service Graph Workspace の **Governance** ビューから開く。

- **ロール**：**`data_manager_admin`**（Data Manager Administrator）でプロパティ・ポリシーを管理。
- **ライフサイクルポリシー**：フィルタ条件に合うCIへ、退役/削除/アーカイブ等のアクションを適用。
- **Retirement definitions（退役定義）**：ポリシーで使う退役の定義（どう退役させるか）。
- **スケジュール実行**：ポリシーのジョブは指定ユーザーで実行（既定 **DataManager Job Runner**、
  グループ *Data Manager Scheduled Job Users*）。
- **バッチサイズ**：`glide.cmdb.data.manager.delete.batch.size` 既定 **1000**（削除/アーカイブの性能最適化）。

> 📌 **要点**：Data Manager は「重複の是正」ではなく、**CIのライフサイクル統制**（古い/不要なCIを
> ポリシーで退役・削除し、健全性を維持する）担当。de-duplication（前節）とは役割が別。

### ポリシーの型

- **Retirement / retention（退役・保持）**：条件に合うCIを退役・削除・アーカイブ。
- **Certification / Attestation（認証・証明）**：CIデータの正しさを担当者にレビュー・証明させる
  （review task / attestation task が生成される）。下書きポリシーは**publish**して有効化する。

## データ認証と Compliance KPI

**Data Certification** は、CMDBの値が期待どおりかを**監査(audit)**で検証する仕組み。
これが CMDB Health の **Compliance KPI** に直結する。

- **テンプレート監査**と**スクリプト監査(scripted audit)** がある。
- CIが Compliance テストに合格するには、そのCIに対する**全ての監査に準拠**している必要がある。
- **監査の有効化が必須**（無効だと Compliance KPI に結果が出ない）。
- スクリプト監査は **Last run date が未設定**のため、KPIに含めるにはスクリプトで実行時刻を記録する。

> ⚠️ **引っかけ**：Compliance＝**監査(audit/certification)結果**。Completeness（必須フィールド欠落）や
> Correctness（重複・stale）とは別軸。「監査」「証明書」「attestation」が出たら Compliance を想起。

**主要用語**：Data Manager / lifecycle policy / retirement definition / `data_manager_admin` /
certification・attestation / template audit・scripted audit。
