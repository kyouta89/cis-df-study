---
chapter: ch4
section: ch4-s1
title: CI Class Manager（クラス定義・設定の中央ハブ）
sources:
  - title: CI Class Manager
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html
  - title: CMDB CI class models
    url: https://www.servicenow.com/docs/r/servicenow-platform/cmdb-ci-class-models/cmdb-ci-class-models.html
related_seqs: []
---

## CI Class Manager とは

**CI Class Manager** は、CMDBクラスに関わる定義・設定を**一元管理する中央ハブ**。
アクセスは **All > Configuration > CI Class Manager**。

ここから扱えるもの（＝この章・他章の設定の入口）：

- **クラス基本**：クラスの作成・閲覧・編集、列(属性)、CIの表示・削除、**Suggested relationship の追加**、Principal Class フィルタ更新。
- **IRE**（第3章）：**識別ルール / 識別 inclusion ルール / 突合ルール / Data refresh ルール / 依存関係ルール（hosting・containment）**。
- **CMDB Health**（第1章）：compliance 監査、certification テンプレート、**orphan / staleness ルール**、
  属性の **mandatory / recommended** 指定、health inclusion ルール。
- **Service Mapping**：エントリポイント種別、Discovery/SM 用のCIタイプ。

> ⚠️ **引っかけ**：CI Class Manager は **非CMDBテーブルを扱えない**。
> また「識別ルール・健全性ルール・依存関係をどこで設定する？」→ **CI Class Manager** が定番の答え。

## クラスモデル（CI Class Models）

ServiceNow は多数の**標準CIクラス**（クラスモデル）を提供し、`cmdb_ci` を頂点とする**テーブル継承階層**を成す。
クラスは拡張でき、識別ルール・突合ルール・健全性設定は**親→子へ継承**される（第3章の継承と同じ考え方）。

> 📌 **要点**：CMDB の「構造（クラス階層・属性・依存）」を司るのが CI Class Manager。
> 第1章(健全性)・第3章(IRE)の各種ルールも、実体はこのハブで設定する。

**主要用語**：class（テーブル）/ 属性(column) / 継承(extension) / Principal Class / Suggested relationship /
hosting・containment ルール。
