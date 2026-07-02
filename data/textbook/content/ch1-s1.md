---
chapter: ch1
section: ch1-s1
title: CMDB Health の3C — Completeness / Correctness / Compliance（＋Relationships）
sources:
  - title: Overview of CMDB Health
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/overview-cmdb-health.html
  - title: CMDB Health KPIs and metrics
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_CMDBHealthMetrics.html
related_seqs: []
---

## CMDB Health の3C

CMDB Health は、CMDB データの健全性を **KPI（Key Performance Indicator）** ごとにスコア化して
ダッシュボードに集約する機能。試験では「3C」として **Completeness / Correctness / Compliance**
が問われるが、公式にはこれに **Relationships（リレーション健全性）** を加えた4本柱で構成される。
各 KPI はさらに複数の**サブメトリクス**に分かれる。

<figure class="diagram">
<svg viewBox="0 0 640 200" role="img" aria-label="CMDB Health の KPI 構成図">
  <rect class="box root" x="240" y="14" width="160" height="36" rx="8"/>
  <text class="tw" x="320" y="37" text-anchor="middle">CMDB Health</text>
  <path class="ln" d="M320 50 V72 M85 72 H555 M85 72 V96 M235 72 V96 M385 72 V96 M535 72 V96"/>
  <rect class="box" x="15" y="96" width="140" height="38" rx="8"/>
  <text class="t" x="85" y="120" text-anchor="middle">Completeness</text>
  <text class="sub" x="85" y="154" text-anchor="middle">Required / Recommended</text>
  <text class="sub" x="85" y="170" text-anchor="middle">（必須・推奨の欠落）</text>
  <rect class="box hlbox" x="165" y="96" width="140" height="38" rx="8"/>
  <text class="t" x="235" y="120" text-anchor="middle">Correctness</text>
  <text class="sub" x="235" y="154" text-anchor="middle">Orphan / Stale /</text>
  <text class="hl" x="235" y="170" text-anchor="middle">Duplicate ← 重複はここ</text>
  <rect class="box" x="315" y="96" width="140" height="38" rx="8"/>
  <text class="t" x="385" y="120" text-anchor="middle">Compliance</text>
  <text class="sub" x="385" y="154" text-anchor="middle">Audit（監査）</text>
  <text class="sub" x="385" y="170" text-anchor="middle">要・監査の有効化</text>
  <rect class="box" x="465" y="96" width="140" height="38" rx="8"/>
  <text class="t" x="535" y="120" text-anchor="middle">Relationships</text>
  <text class="sub" x="535" y="154" text-anchor="middle">dup / orphan / stale</text>
  <text class="sub" x="535" y="170" text-anchor="middle">（設定変更不可）</text>
</svg>
<figcaption>図1: CMDB Health の KPI とサブメトリクス。<b>重複(Duplicate)は Correctness</b> に属する。</figcaption>
</figure>

- **Completeness（完全性）** — 必須・推奨フィールドが未入力でないか。
  - *Required*：辞書(dictionary)で **mandatory** 指定された属性の欠落。
  - *Recommended*：**recommended** 指定属性の欠落（**out-of-box では推奨フィールドは未設定**）。
- **Correctness（正確性）** — データ整合性ルールに対する値の誤り。
  - *Orphan*（孤立）／*Staleness*（陳腐化）／*Duplicate*（重複）。
- **Compliance（準拠性）** — **監査（audit）** の実行結果に基づく。証明書(certificate)への適合。
- **Relationships（リレーション）** — 重複/孤立/陳腐 なリレーション（**設定変更不可**のメトリクス）。

> ⚠️ **引っかけ最重要**：**「重複CI(duplicate)」は Correctness** のサブメトリクス。
> Completeness（欠落）と混同させる選択肢が頻出。欠落＝Completeness、重複/古い/孤立＝Correctness、
> 監査違反＝Compliance、と整理して覚える。

### 集約のされ方

CI を各メトリクスでテスト → 結果を **クラス / ヘルスグループ / サービス / リレーション** の各レベルで
集約 → **CMDB Health ダッシュボード**に表示。多くのメトリクスは**テスト内容自体を設定可能**
（準拠/非準拠の判定基準を組織標準に合わせて調整できる）。

> 📌 **要点**：CMDB Health は **CMDB テーブルのみ対象**（non-CMDB テーブルは非対応）。
> ドメイン分離が有効なら、ログオン中ユーザーのドメインのデータ・ルール・設定に基づき表示され、
> 子ドメインに定義が無ければ親の設定が再帰的に適用される（ドメインアウェア）。

**主要用語**：KPI / メトリクス / inclusion rule（健全性テスト対象の包含） /
集約レベル（class・health group・service・relationship）。

次節では、これらのスコアを見る**ダッシュボードと KPI/メトリクスの設定**を扱う。
