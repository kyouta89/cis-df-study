---
chapter: ch4
section: ch4-s3
title: Group Sync（Dynamic CI Group とグループ割当の同期）
sources:
  - title: Matching the usage of dynamic CI groups to service type
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-dynamic-ci-groups-by-service.html
  - title: Synchronizing group assignment attributes
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-data-synchronize.html
  - title: CMDB groups
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/cmdb-groups.html
related_seqs: []
---

## Dynamic CI Group

**Dynamic CI Group** は、**共通の属性・条件（クエリ）で動的に集まるCIの集合**。
Incident / Problem / Change のレコードの **CI フィールドにグループCIとして**使える。

- クエリで定義（共通属性・条件ベース）。
- **グループの中にグループは入れられない**（CIのみ）。
- 1つのCIは複数のクエリに一致しうる → **複数のグループに所属可**（所属数に上限なし）。
- Technology management サービス用途では **最大10,000件**の類似CIをまとめられる。

## Service Classification で用途が変わる

**Service Classification** 属性がサービスの種別を決め、dynamic CI group の使い方が変わる：

- **Technology management service**（旧 Technical service）：個別管理されるCIの集合。互いに関連しないため
  **サービス関連付け不要・インパクト分析は対象外**。例：特定OSのサーバ群、拠点別ネットワーク機器。
- **Service instance**（旧 application service）：1つのCIが影響を受けると**グループ全体が影響**を受けるため、
  **サービス関連付けが必須・インパクト分析が重要**。

## Group Sync（ownership synchronization）

**Technology management offering** または **CI Class Manager** で **group assignment attributes（グループ割当属性）** を設定すると、
**ownership synchronization** が、指定したCIクラス／CI群の**全CIへグループ属性を同期**する。

これにより、あるユーザーグループに「このCI群／クラスの管理権限」を与えられる。
典型的に同期されるのは **Support group** や **Managed by group** などのグループ割当。

> ⚠️ **引っかけ（問題集 #1 と直結）**：Dynamic CI Group とリレーションを持つ **Technical Service Offering** から
> メンバーCIへ同期されるのは **Support group** と **Managed by group**。Approval / Owned by は同期対象外。

> 📌 **要点**：Group Sync ＝「オファリング(またはCI Class Manager)で決めたグループ割当を、配下CIへ一括同期」。
> 同期の入口は **Technology management offering / CI Class Manager**、設定対象は **group assignment attributes**。

**主要用語**：dynamic CI group / Service Classification / Technology management service・offering /
service instance / ownership synchronization / group assignment attributes（Support / Managed by）。
