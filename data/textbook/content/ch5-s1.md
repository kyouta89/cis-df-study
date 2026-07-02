---
chapter: ch5
section: ch5-s1
title: CSDM フレームワーク概要とデータドメイン（v5）
sources:
  - title: CSDM data domains
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-conceptual-model.html
  - title: CSDM term definitions
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-term-definitions.html
related_seqs: []
---

## CSDM とは

**CSDM（Common Service Data Model）** は、管理者が ServiceNow 製品をセットアップする際に**従うべきデータモデルの標準**。
CIとリレーションを**適切なCMDBテーブルに配置**するルールを定め、プラットフォーム全体で一貫した
レポート・分析を可能にする。CSDM は新しいテーブルではなく、**既存CMDBの上の"使い方の標準"**。

## データドメイン（CSDM v5）

CSDM の概念モデルは複数の**ドメイン（責務の層）**で構成される。各ボックスはCIを保持するCMDBテーブル群、
線はクラス間リレーションを表す。

| ドメイン | 役割 |
|---|---|
| **Foundation** | 他ドメインから参照される**基礎データ**。製品利用前に**最初に投入**が必要 |
| **Ideation & Strategy** | サービスの着想・戦略（SPM 領域） |
| **Design & Planning** | 買う/作るデジタル製品の設計・計画 |
| **Build & Integration** | 開発中の論理的成果（**運用CIではない**） |
| **Service Delivery** | インフラ〜運用までのエンドツーエンド提供系 |
| **Service Consumption** | カタログ経由でビジネスサービスを要求・消費 |
| **Manage Portfolio** | 他ドメインを横断する管理層（service owner） |

<figure class="diagram">
<svg viewBox="0 0 640 208" role="img" aria-label="CSDMドメインの層構造の図">
  <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" class="ahfill"/></marker></defs>
  <rect class="box" x="12" y="12" width="616" height="30" rx="6"/><text class="t" x="320" y="32" text-anchor="middle">Manage Portfolio（全ドメイン横断）</text>
  <rect class="box" x="12" y="92" width="116" height="46" rx="6"/><text class="t" x="70" y="112" text-anchor="middle">Ideation</text><text class="sub" x="70" y="128" text-anchor="middle">&amp; Strategy</text>
  <rect class="box" x="136" y="92" width="116" height="46" rx="6"/><text class="t" x="194" y="112" text-anchor="middle">Design</text><text class="sub" x="194" y="128" text-anchor="middle">&amp; Planning</text>
  <rect class="box" x="260" y="92" width="116" height="46" rx="6"/><text class="t" x="318" y="112" text-anchor="middle">Build</text><text class="sub" x="318" y="128" text-anchor="middle">&amp; Integration</text>
  <rect class="box" x="384" y="92" width="116" height="46" rx="6"/><text class="t" x="442" y="112" text-anchor="middle">Service</text><text class="sub" x="442" y="128" text-anchor="middle">Delivery</text>
  <rect class="box" x="508" y="92" width="116" height="46" rx="6"/><text class="t" x="566" y="112" text-anchor="middle">Service</text><text class="sub" x="566" y="128" text-anchor="middle">Consumption</text>
  <path class="arrow" d="M129 115 H135"/><path class="arrow" d="M253 115 H259"/><path class="arrow" d="M377 115 H383"/><path class="arrow" d="M501 115 H507"/>
  <rect class="box hlbox" x="12" y="168" width="616" height="30" rx="6"/><text class="t" x="320" y="188" text-anchor="middle">Foundation（基礎データ・最初に投入）</text>
</svg>
<figcaption>図: CSDM のドメイン層。<b>Foundation</b> を土台に価値連鎖（Ideation→…→Consumption）、上に <b>Manage Portfolio</b> が横断。</figcaption>
</figure>

## サービス種別（最重要）

- **Technology management service** [`cmdb_ci_service_technical`]（**旧 Technical service**）
  - **運用CI**。**1階層のみ**（Technology management service の階層は作らない）。
  - **Incident / Problem / Change のインパクト**に使い、**Change の承認**にも使う。
  - provider 視点（提供する技術）。
- **Business service / Service instance（旧 application service）** … 消費者視点・サービス単位。

> ⚠️ **引っかけ**：CSDM v5 で **「Technical service」→「Technology management service」** に改称。
> Technology management service は **operational CI かつ 1レベル**（階層化しない）。

> 📌 **v4 → v5 の主な差**：用語刷新（Technology management service 等）、**ライフサイクル value pair**
> (stage＋status, 次節)、**Asset/CI/IBI を product instance として整合**（IBI 概念の前面化）。

**主要テーブル/用語**：`cmdb_ci_service_technical` / business service / service instance /
Foundation domain / Manage Portfolio / service の3要素（interaction・offering・service system）。
