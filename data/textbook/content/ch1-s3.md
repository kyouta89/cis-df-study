---
chapter: ch1
section: ch1-s3
title: 重複CIの検出と是正（De-duplication）
sources:
  - title: Duplicate CIs remediation
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/de-duplication-tasks.html
  - title: Properties related to remediation of duplicate CIs
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/properties-duplicate-ci.html
related_seqs: []
---

## 重複CIの是正

重複CIは CMDB の整合性・信頼性を損なうため、検出と是正を定期的に行う。

### 検出 → タスク化

**IRE（Identification and Reconciliation Engine）** が重複を検出すると、重複CIの各セットを
**de-duplication タスク**にまとめる。タスクには重複と判定した根拠データと、セット内の全重複CIが含まれる。

> 📌 一部のケースでは IRE が自動でタスクを生成しない。その場合は **手動で de-duplication タスクを作成**して是正する。

### Main CI と `duplicate_of`（最頻出概念）

是正は、重複CIのセットを**1つのCIに統合**して重複を解消する操作。

<figure class="diagram">
<svg viewBox="0 0 640 190" role="img" aria-label="重複是正でMain CIへ統合する流れの図">
  <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" class="ahfill"/></marker></defs>
  <text class="sub" x="95" y="22" text-anchor="middle">重複セット（互いに重複）</text>
  <rect class="box" x="20" y="30" width="150" height="140" rx="8"/>
  <rect class="box" x="40" y="44" width="110" height="30" rx="6"/><text class="t" x="95" y="64" text-anchor="middle">CI-A</text>
  <rect class="box hlbox" x="40" y="84" width="110" height="30" rx="6"/><text class="t" x="95" y="104" text-anchor="middle">CI-B</text>
  <rect class="box" x="40" y="124" width="110" height="30" rx="6"/><text class="t" x="95" y="144" text-anchor="middle">CI-C</text>
  <path class="arrow" d="M176 100 H248"/>
  <text class="sub" x="212" y="90" text-anchor="middle">Main選択</text>
  <text class="sub" x="212" y="118" text-anchor="middle">＋統合</text>
  <rect class="box hlbox" x="300" y="38" width="322" height="34" rx="6"/><text class="t" x="461" y="59" text-anchor="middle">Main = CI-B（duplicate_of = 空）</text>
  <rect class="box" x="300" y="84" width="322" height="30" rx="6"/><text class="t" x="461" y="104" text-anchor="middle">CI-A → duplicate_of = B</text>
  <rect class="box" x="300" y="124" width="322" height="30" rx="6"/><text class="t" x="461" y="144" text-anchor="middle">CI-C → duplicate_of = B</text>
</svg>
<figcaption>図: 重複セットから <b>Main CI</b> を選び統合。残りは <code>duplicate_of</code> が Main を指す。</figcaption>
</figure>

- **Main CI** … セットの中で**残す（active のままにする）CI**。是正の最初の手順で選ぶ。
  残りのCIから、どの属性値・リレーション・関連項目を Main CI に取り込むかを選択して統合する。
- **`duplicate_of` 属性** … 重複CIが Main CI を参照するためのフィールド。
  - 是正後：Main CI の `duplicate_of` は**空**。他の重複CIの `duplicate_of` は **Main CI を参照**。
  - New York 以降にアップグレードしたインスタンスで Main CI 不明の重複は、`duplicate_of` が **'Unknown'**。
  - IRE が内部利用するため**手動更新は制限**（自分自身を Main にできない／別ドメインの Main 不可／重複の連鎖不可）。

### 是正の2経路

- **一括（bulk）** … **De-duplication Dashboard** と **De-duplication Template Library**。
  クラスごとの是正設定を**テンプレート**化し、複数タスクへ一貫適用。
- **単一** … **Duplicate CI Remediator**（ウィザード）で1タスクずつ。属性・リレーション・関連項目の統合オプションを設定。
  Now Assist for CMDB 3.0+ があれば AI 支援の解決スキルも利用可。

### 試験で効く具体値・挙動

- **大量重複のしきい値**：`glide.duplicate_ci_remediator.max.cis` 既定 **1,000**（上げても**上限5,000**）。
  超過時はウィザードのオプションが制限（Recommended な Main CI のみ等）。
- **関連テーブルへの影響**：`glide.duplicate_ci_remediator.merge_related_items_enhanced = true` と
  設定テーブル登録で、是正中に関連テーブルのワークフロー/ビジネスルールを無効化して完走させられる
  （既定で **Change [change_request]** と **Task CI [task_ci]** はワークフロー無効化＋エラー無視で構成済み）。
- 変更要求の状態が **New 以外**ならCI削除時に当該CIは change から除去、**New** なら Main CI に更新される
  （ビジネスルール *Read only CI when not New* が保護）。

**主要テーブル/用語**：de-duplication task / Main CI / `duplicate_of` / Duplicate CI Remediator / テンプレート。
