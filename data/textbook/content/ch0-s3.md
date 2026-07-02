---
chapter: ch0
section: ch0-s3
title: サービスの基礎（service / offering / business service）
sources:
  - title: CSDM data domains
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-conceptual-model.html
related_seqs: []
---

> 🧭 前提の地ならし（任意）。第4章(Group Sync)・第5章(CSDM)の前提になる「サービス」の語彙を整理する。

## 「サービス」とは

ServiceNow（と ITIL）でいう **service** は、「**コストやリスクを自分で抱えずに、望む成果を得られるようにするもの**」。
サービスは典型的に3要素を持つ：**interaction（やり取り）/ offering（提供形態）/ service system（提供を支える仕組み）**。

CMDB/CSDM では、似た言葉が複数出てくるので、最初に区別しておくと混乱しない。

| 用語 | ざっくり | 視点 |
|---|---|---|
| **Business service** | ビジネスから見たサービス（例：メール、給与計算） | 消費者・ビジネス |
| **Technology management service**（旧 Technical service） | それを支える技術的なサービス（運用CI・1階層） | 提供者・技術 |
| **Service offering** | サービスの**具体的な提供形態/コミットメント**（例：Gold/Silver、地域別） | 契約・SLA |
| **Service instance**（旧 application service） | 実際に動いている1つのサービスの実体（構成CIの集合） | 運用実体 |

> 📌 **要点**：**service（種類）** と **offering（その具体的な提供形態）** は別物。
> offering は SLA や対象範囲を伴う「売り物/約束」の単位。第4章の Group Sync は、この
> **offering を起点にグループ割当をCIへ同期**する話。

> 🧩 第5章（CSDM）への布石：CSDM は、これらサービスやCIを**正しいテーブル/ドメインに置く**ための標準。
> 「business service は誰が消費し、technology management service が何を提供し…」という関係を
> 整理するのが CSDM の目的、と捉えておくと第5章が読みやすい。

これで前提は十分。次は **第1章 Governance / CMDB Health（配点35%）** から本編に入る。
