---
chapter: ch3
section: ch3-s2
title: 識別ルールと突合ルール（Identification / Reconciliation Rules）
sources:
  - title: Identification rules
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html
  - title: Reconciliation rules
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html
  - title: Create a CI identification rule
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_CreateCIIdentificationRule.html
related_seqs: []
---

## 識別ルール（Identification Rules）

識別ルールは**1つのCIクラスに適用**され、**1つの CI identifier** と、**優先度付きの identifier entry / related entry** から成る。
強い識別子ほど高い優先度を与えるのが定石。

- **Unique attributes（一意属性）**：CIを一意に識別できる criterion 属性の組（同一/派生テーブルから取れる）。
- **Required attributes（必須属性）**：空であってはならない属性。
- **identifier entry の2方式**：
  - *field-based*：CI自身の属性で照合。
  - *lookup-based*：関連リスト（Serial Numbers, Network Adapters 等）で照合。ルックアップ表は `cmdb_ci` への参照フィールドが必要。

### 階層の継承（最頻出）

子クラスに固有の識別ルールが**無ければ親クラスから継承**する。
子に固有ルールを作ると、**継承していた親ルール（related entry 含む）は無効**になる
→ 必要な entry は新ルールに**明示的に再追加**する必要がある。

> ⚠️ **引っかけ**：「子クラスに識別ルールを新規作成」したら、親から継承していた entry は**消える**。
> 同じ related entry が要るなら手動で足し直す。

### independent / dependent 識別ルール

- **independent rule**：CI自身の属性だけで識別（Server など）。
- **dependent rule**：**先に親CIを識別してから**子を識別。dependent CI が持てる**親（dependency）は1つだけ**。
  関係タイプも識別に含まれる。依存連鎖は **dependent relationship** で定義する。

## 突合ルール（Reconciliation Rules）

突合ルールは「**どの discovery source が CI属性を更新できるか**」を決める。無いとソース同士で上書きが起きる。

| 種類 | 仕組み | 格納 | 補足 |
|---|---|---|---|
| **Static** | discovery source に**優先度**を設定。親→子へ継承 | `cmdb_reconciliation_definition` | Attributes 空欄＝全属性対象 |
| **Dynamic** | **CMDB 360** の値ベース（最大値/最多報告値などを選択） | `cmdb_dynamic_reconciliation_definition` | クラス属性あたり**1つだけ**・CMDB 360 有効化が前提 |

> ⚠️ **引っかけ最重要**：同一属性に Static と Dynamic の両方があると、**Dynamic が優先**する。
> また Dynamic は **CMDB 360 を有効化**しないと使えない（次節）。

**主要用語**：CI identifier / identifier entry（優先度）/ related entry / criterion attribute /
discovery source / 継承(derivation) / qualifier chain。
