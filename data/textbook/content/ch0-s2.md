---
chapter: ch0
section: ch0-s2
title: データの流れ：どこから来て、どう入るか（→ IRE → CMDB）
sources:
  - title: Identification and Reconciliation Engine (IRE)
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html
related_seqs: []
---

> 🧭 前提の地ならし（任意）。「CMDBにデータがどう入るのか」を俯瞰し、第3章(Ingestion)の前提を作る。

## データの入り口（ソース）

CMDB のデータは、いくつかの**データソース**から入ってくる。CIS-DF では「**入った後の処理**」が主役だが、
"どこから来るか"を知っておくと理解が早い。

- **Discovery** … エージェントレスでインフラを探索し、サーバ・ネットワーク等を自動登録。
- **Service Mapping** … アプリケーションサービスを上位からたどって構成（CIとリレーション）を地図化。
- **Import Set** … 外部データ（CSV/他システム）を取り込む仕組み。
- **Service Graph Connector（SGC）/ IntegrationHub ETL** … サードパーティ製品との標準統合。
- **手動入力** … フォームからの手作業。

## すべては IRE を通る（ゲートキーパー）

どのソースから来ても、データは **IRE（Identification and Reconciliation Engine）** を通って CMDB に入る。
IRE は2つの仕事をする：

1. **識別（Identification）**：既存CIと同じか判定し、**重複CIの作成を防ぐ**。
2. **突合（Reconciliation）**：**権威あるソースの値だけ**を書き込み、ソース同士の上書きを防ぐ。

<figure class="diagram">
<svg viewBox="0 0 640 210" role="img" aria-label="データソースからIREを通ってCMDBへ入る流れの図">
  <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" class="ahfill"/></marker></defs>
  <rect class="box" x="10" y="20" width="150" height="26" rx="6"/><text class="t" x="85" y="38" text-anchor="middle">Discovery</text>
  <rect class="box" x="10" y="56" width="150" height="26" rx="6"/><text class="t" x="85" y="74" text-anchor="middle">Service Mapping</text>
  <rect class="box" x="10" y="92" width="150" height="26" rx="6"/><text class="t" x="85" y="110" text-anchor="middle">Import Set</text>
  <rect class="box" x="10" y="128" width="150" height="26" rx="6"/><text class="t" x="85" y="146" text-anchor="middle">SGC / ETL</text>
  <rect class="box" x="10" y="164" width="150" height="26" rx="6"/><text class="t" x="85" y="182" text-anchor="middle">手動入力</text>
  <path class="arrow" d="M166 105 H250"/>
  <rect class="box root" x="250" y="76" width="150" height="58" rx="8"/>
  <text class="tw" x="325" y="100" text-anchor="middle">IRE</text>
  <text class="tw" x="325" y="120" text-anchor="middle">識別＋突合</text>
  <path class="arrow" d="M400 105 H486"/>
  <rect class="box" x="486" y="76" width="140" height="58" rx="8"/>
  <text class="t" x="556" y="100" text-anchor="middle">CMDB</text>
  <text class="sub" x="556" y="120" text-anchor="middle">cmdb_ci ほか</text>
  <text class="sub" x="325" y="156" text-anchor="middle">重複防止 / 権威ソース選択</text>
</svg>
<figcaption>図: データソース → <b>IRE（ゲートキーパー）</b> → CMDB。入口が何であっても IRE を通る。</figcaption>
</figure>

> 📌 **要点**：「CMDBが汚れる」主因は、重複と、信頼できないソースの上書き。だから入口に IRE を置く。
> 第3章ではこの IRE（識別ルール・突合ルール・CMDB 360）を詳しく扱う。

> 🧩 第1章（健全性）とのつながり：IRE で防ぎきれない劣化（古いCI・欠落・監査違反）を、
> 後追いで測って直すのが CMDB Health。**入口=IRE、健診=CMDB Health** と対にして覚えると整理できる。
