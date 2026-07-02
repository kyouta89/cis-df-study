---
chapter: ch5
section: ch5-s3
title: 実装ステージ（Crawl→Fly）と CSDM の有効化・移行
sources:
  - title: Implementing the CSDM framework in stages
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-implementation-stages.html
  - title: Foundation domain in the CSDM model
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/foundation-domain.html
  - title: Map legacy status values to CSDM life-cycle values
    url: https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-life-cycle-standard-values.html
related_seqs: []
---

## 段階的実装：Foundation → Crawl → Walk → Run → Fly

CSDM は**一度に全部ではなく段階導入**する。人の成長になぞらえた5段階で、各段階は前段階の上に積み上がる。

<figure class="diagram">
<svg viewBox="0 0 640 195" role="img" aria-label="CSDM実装ステージのはしご図">
  <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" class="ahfill"/></marker></defs>
  <rect class="box hlbox" x="8" y="150" width="115" height="30" rx="6"/><text class="t" x="65" y="170" text-anchor="middle">Foundation</text>
  <rect class="box" x="133" y="120" width="115" height="30" rx="6"/><text class="t" x="190" y="140" text-anchor="middle">Crawl</text>
  <rect class="box" x="258" y="90" width="115" height="30" rx="6"/><text class="t" x="315" y="110" text-anchor="middle">Walk</text>
  <rect class="box" x="383" y="60" width="115" height="30" rx="6"/><text class="t" x="440" y="80" text-anchor="middle">Run</text>
  <rect class="box" x="508" y="30" width="120" height="30" rx="6"/><text class="t" x="568" y="50" text-anchor="middle">Fly</text>
  <path class="arrow" d="M123 156 L133 144"/>
  <path class="arrow" d="M248 126 L258 114"/>
  <path class="arrow" d="M373 96 L383 84"/>
  <path class="arrow" d="M498 66 L508 54"/>
</svg>
<figcaption>図: 段階導入 <b>Foundation → Crawl → Walk → Run → Fly</b>。各段は前段の上に積む（Foundation が必須の土台）。</figcaption>
</figure>

| ステージ | 主に扱うデータ | ねらい |
|---|---|---|
| **Foundation** | 参照用の**基礎データ**（拠点・会社・グループ・モデル等） | 正確なレポートの土台。**最初に必須** |
| **Crawl** | **ITSM** 関連のベースCMDBテーブル | ITSM が回る最低限のCMDB |
| **Walk** | ネットワークインフラCI・技術チームが支えるアプリ | 技術サービスの可視化 |
| **Run** | 技術と、それを**売る/消費するビジネス**の関係 | ビジネスサービスとの接続 |
| **Fly** | 情報ポートフォリオ等の高度な対象 | 戦略・全社最適 |

> ⚠️ **引っかけ**：順序は **Foundation → Crawl → Walk → Run → Fly**。Foundation を飛ばして Crawl はできない
> （基礎データが他ドメインから参照されるため）。「最初にやるべきは？」→ **Foundation**。

> 📌 **要点**：各ステージは**段階的に価値を出す**。Crawl=ITSM、Walk=インフラ/アプリ、Run=ビジネスとの関係、
> という"何を載せるか"の順番で覚える。

## CSDM の有効化と移行

1. **CSDM プラグインを有効化**。
2. **ライフサイクル同期を有効化**：一度きりの処理でレガシー状態値（asset/CI）を CSDM value pair へ変換。
   以後は business rule が IBI / asset / CI のライフサイクル値を**定期的に揃える**。
3. **既存データを移行・同期**して、正しいCMDBテーブルへ載せ替える。

### Lifecycle Mapping フォーム

`life_cycle_mapping`（前節）の各マッピングルールは **Lifecycle Mapping フォーム**で確認・設定する。
レガシー値 → CSDM value pair の対応を、テーブル単位・優先度付きで定義する。

## 第5章まとめ（CSDM）

1. CSDM＝CMDBの**使い方の標準**。データを正しいテーブル/ドメインへ（[§1](#ch5-s1)）。
2. 状態は **stage＋status の value pair**。Asset/CI/IBI は **product instance** で整合（[§2](#ch5-s2)）。
3. 導入は **Foundation→Crawl→Walk→Run→Fly** の段階式。有効化＝プラグイン＋ライフサイクル同期＋移行（本節）。

**主要用語**：foundation/crawl/walk/run/fly / CSDM プラグイン / ライフサイクル同期 / `life_cycle_mapping` /
Information Object [`cmdb_ci_information_object`]。
