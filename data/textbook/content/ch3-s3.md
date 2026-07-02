---
chapter: ch3
section: ch3-s3
title: Multisource CMDB / CMDB 360
sources:
  - title: CMDB 360 (Multisource CMDB)
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/multisource-cmdb.html
  - title: Components related to CMDB 360
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/components-multisource-cmdb.html
related_seqs: []
---

## CMDB 360（旧 Multisource CMDB）

複数の discovery source が**同じCI属性**を更新しようとすると、IRE は突合ルールで**1つのソースを選ぶ**。
通常は、選ばれなかった（低優先度）ソースの値は**捨てられ**、後から「この値はどのソース由来か」を追うのが難しい。

**CMDB 360** は、**選ばれた/選ばれなかった全ソースの生データを属性レベルで保持**する。
これにより、ソース別の寄与の可視化・特定ソースの取り消し・ルール変更後の再計算ができる。

- **格納**：CMDB MultiSource Data [`cmdb_multisource_data`] テーブル（ソース×CIの組ごとに1レコード）。
- **できること**：
  - **Dynamic reconciliation rule** の作成（前節）。
  - 属性値のソースを属性レベルで**可視化**。
  - 突合ルールを変更 → CMDBを**再計算(recompute)**。
  - 信頼できないソースの取り込みを**revert（取り消し）**して再計算。
  - 新ソースを既知の正しいソースと**比較して検証**。
- **非CMDBテーブルも対象にできる**（既定はCMDBクラスのみ収集）。

### 有効化

1. **ITOM Discovery License**（`com.snc.itom.discovery.license`）プラグインを有効化。
2. **All > Configuration > CMDB 360 Properties** で `glide.identification_engine.multisource_enabled` を **true**。
3. 任意で特定クラス（と子孫）を CMDB 360 から除外。

> 📌 **要点**：Dynamic reconciliation は CMDB 360 の上に成り立つ。
> 「複数ソースの値を履歴保持して最良値を選ぶ/後から直せる」のが CMDB 360。
> アクセスは **CMDB Workspace の CMDB 360 ビュー** か **Service Graph Workspace の CMDB 360 インサイト**。

**主要テーブル/プロパティ**：`cmdb_multisource_data` / `glide.identification_engine.multisource_enabled` /
`glide.identification_engine.multisource_cmdb_ci_enabled`。
