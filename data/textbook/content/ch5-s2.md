---
chapter: ch5
section: ch5-s2
title: ライフサイクル（Stage / Status）と Asset・CI・IBI
sources:
  - title: CSDM life-cycle terms
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-life-cyle-terms.html
  - title: Map legacy status values to CSDM life-cycle values
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-life-cycle-standard-values.html
related_seqs: []
---

## ライフサイクル value pair

CSDM はCIの状態を **life-cycle value pair = 「life cycle stage」＋「life cycle stage status」** で表す。
この2値の組で、製品インスタンスのライフサイクル状態を**完全に記述**する。

<figure class="diagram">
<svg viewBox="0 0 640 116" role="img" aria-label="ライフサイクル value pair の図">
  <rect class="box" x="14" y="30" width="180" height="50" rx="8"/><text class="t" x="104" y="52" text-anchor="middle">life cycle stage</text><text class="sub" x="104" y="70" text-anchor="middle">大段階 例: Operational</text>
  <text class="t" x="208" y="61" text-anchor="middle">＋</text>
  <rect class="box" x="224" y="30" width="180" height="50" rx="8"/><text class="t" x="314" y="52" text-anchor="middle">stage status</text><text class="sub" x="314" y="70" text-anchor="middle">細状態 例: In Use</text>
  <text class="t" x="418" y="61" text-anchor="middle">＝</text>
  <rect class="box root" x="434" y="30" width="192" height="50" rx="8"/><text class="tw" x="530" y="52" text-anchor="middle">value pair</text><text class="tw" x="530" y="70" text-anchor="middle">状態を完全記述</text>
</svg>
<figcaption>図: <b>life cycle stage ＋ stage status ＝ value pair</b>。2値の組で1つの状態を完全に表す。</figcaption>
</figure>

- **life cycle stage**：CIが通る**大きな段階**（例：調達 → 運用 → 廃止）。
- **life cycle stage status**：現ステージ内の**細かい状態**。
  例：tangible/physical CI が **Operational** ステージで `In Use → In Maintenance → End of Support` と推移
  （`In Maintenance` を経ず `In Use → End of Support` もあり得る）。

> ⚠️ **引っかけ**：「stage」と「status」は別物。stage＝大段階、status＝その中の状態。**ペアで1つの状態**を表す。

### レガシー値（旧来の状態）

value pair 導入前は次の値で状態管理していた（v4以前〜互換）：
**install status / operational status / hardware status / hardware substatus**。

## Asset・CI・IBI と Product Instance

| 用語 | テーブル | 説明 |
|---|---|---|
| **CI** | `cmdb_ci` | 構成アイテム |
| **asset** | `alm_asset` | 本番資産 |
| **IBI（Install Base Item）** | `sn_install_base_item` | サービス提供/販売する対象として追跡する項目 |
| **Product Instance (PI)** | — | **Asset＋CI＋IBI** の論理グループ（Asset+CI や Asset+IBI の形もあり） |

Model category テーブルが、同一アイテムの Asset / CI / IBI を関連付ける。

## life_cycle_mapping（レガシー → CSDM）

ベースシステムの **life cycle mapping [`life_cycle_mapping`]** テーブルは、よく使われる**レガシー状態値**を
等価な **CSDM value pair** に対応づける**マッピングルール**を持つ（プリセット済み）。

- クラスごとに複数ルールがあり、**優先度**付き。複数該当時は**最優先ルール**が使われる。
- Asset / CI / IBI のライフサイクル値は、business rule で**相互に同期**される。

> 📌 **要点（継承の罠）**：ライフサイクル定義(`life_cycle_control`)は **aggregation ベースの継承**
> ＝子クラスは親の定義を**上書きせず結合（拡張）**する。だから Business Application に
> ハード向けの stage（Deploy/Inventory 等）が混じって見えることがある（仕様）。
> 一方 **`sys_choice` の継承は子が親を上書き**する——この違いが問われやすい。

**主要テーブル**：`life_cycle_mapping` / `life_cycle_control` / `alm_asset` / `sn_install_base_item` / Model category。
