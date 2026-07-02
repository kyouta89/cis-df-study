---
chapter: ch3
section: ch3-s1
title: IRE（識別・突合エンジン）とゲートキーパー
sources:
  - title: Identification and Reconciliation Engine (IRE)
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html
  - title: CMDB Identify and Reconcile
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CMDBIdentifyandReconcile.html
related_seqs: []
---

## IRE とは

**IRE（Identification and Reconciliation Engine）** は、さまざまなデータソースからの入力を
**CMDBに書き込む前に処理する中央フレームワーク**。CMDBの**ゲートキーパー**であり、データ整合性を保つ。

- **Identification（識別）**：CIを一意に識別して **重複CIの作成を防ぐ**。
- **Reconciliation（突合）**：**権威あるデータソースだけに属性の書き込みを許可**し、ソース同士の上書き合戦を防ぐ。

IRE は **識別ルール / 突合ルール / IRE データソースルール** を使って、入力(payload)を処理する。
Service Mapping・horizontal/pattern discovery は API 経由で IRE を通す。Import Set のデータにも適用でき、
サードパーティは REST / スクリプタブル IRE API（`createOrUpdateCI()` など）で識別・突合を実行する。

> 📌 **要点**：CMDBへ入るデータは基本すべて IRE を通る。「重複を防ぐ＝識別」「正しいソースの値だけ通す＝突合」
> という2役を1つのエンジンが担う、と押さえる。

## 識別の流れ（payload）

IRE は入力 payload の各項目に**識別子キー**を生成して照合する。識別子キーは次のいずれかに基づく：

- **`source_name` ＋ `source_native_key`**（`sys_object_source_info`）による高速識別。
  Source [`sys_object_source`] テーブルで一意識別できれば、識別ルールの照合アルゴリズム（低速）を省ける。
- **識別ルールの criterion 属性**による識別。

<figure class="diagram">
<svg viewBox="0 0 640 150" role="img" aria-label="IREの識別→突合→CMDBの流れ">
  <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" class="ahfill"/></marker></defs>
  <rect class="box" x="8" y="48" width="104" height="44" rx="8"/><text class="t" x="60" y="74" text-anchor="middle">payload</text>
  <path class="arrow" d="M114 70 H150"/>
  <rect class="box root" x="152" y="48" width="140" height="44" rx="8"/><text class="tw" x="222" y="67" text-anchor="middle">① 識別</text><text class="tw" x="222" y="83" text-anchor="middle">Identification</text>
  <text class="sub" x="222" y="112" text-anchor="middle">一致=更新 / 不一致=新規(重複防止)</text>
  <path class="arrow" d="M294 70 H330"/>
  <rect class="box root" x="332" y="48" width="140" height="44" rx="8"/><text class="tw" x="402" y="67" text-anchor="middle">② 突合</text><text class="tw" x="402" y="83" text-anchor="middle">Reconciliation</text>
  <text class="sub" x="402" y="112" text-anchor="middle">権威ソースのみ書込</text>
  <path class="arrow" d="M474 70 H510"/>
  <rect class="box" x="512" y="48" width="118" height="44" rx="8"/><text class="t" x="571" y="74" text-anchor="middle">CMDB</text>
</svg>
<figcaption>図: IRE は <b>①識別（重複防止）→ ②突合（権威ソース選択）</b> の順で処理して CMDB に書く。</figcaption>
</figure>

> ⚠️ **引っかけ**：`source_name`/`source_native_key` があれば識別ルールより**先に**使われる（高速経路）。
> ただし `glide.identification_engine.skip_sys_object_source_matching` で識別ルール優先に変更できる。

## 依存CIは「文脈」で識別する

識別は **CIの依存分類（independent / dependent）** に依存する。dependent CI は単独では一意識別できないため、
**まず親（host）を識別し、その文脈で**子を識別する。

例：Windows Server（independent）上で動く Tomcat（dependent）は、`config file path` だけでは
複数マシンで同一になり得て一意にできない。**先に Windows Server を識別 → その上で Tomcat を識別**する。

<details markdown="1">
<summary>🔧 深掘り：タイムスタンプによる新旧判定（last_discovered / first_discovered）</summary>

IRE は競合する属性値の解決にタイムスタンプを使い、現行より古いレコードは無視する。

- **`last_discovered`** … 最後に discover された時刻。IRE は payload 処理のたびに（他属性が変わらなくても）この値と `discovery_source` を更新する。payload に値があれば、それが CMDB より**新しいときだけ**採用（無ければ現在時刻）。
- **`first_discovered`** … 最初に作成された時刻。新規作成時は payload 値（無ければ現在時刻）。以降の更新では payload に値があれば更新、無ければ据え置き。

この仕組みで「古いソースの値で新しい値を上書きする」事故を防ぐ。挙動は `glide.identification_engine.skip_updating_source_last_discovered_if_older` 等のプロパティで変更可能。
</details>

**主要テーブル/用語**：payload / `createOrUpdateCI()` / `sys_object_source` /
`cmdb_ire_partial_payloads_index` / `last_discovered`・`first_discovered`（タイムスタンプで新旧判定）。
