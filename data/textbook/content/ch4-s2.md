---
chapter: ch4
section: ch4-s2
title: CI リレーションと依存関係（Dependent / Suggested）
sources:
  - title: CI relationships in the CMDB
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CIRelationships.html
  - title: Create a dependent relationship
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-dependent-relationship.html
  - title: Suggested relationship model
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_SuggestedRelationshipModel.html
related_seqs: []
---

## リレーションの構造

CMDB はCIだけでなく**CI間のリレーション**を追跡する。リレーションは必ず3要素：
**Parent CI ＋ Child CI ＋ Relationship type**。

例：`[Server1] [Managed by] [Server2]` は **Server1=child / Server2=parent / 「Managed by」=type**。

<figure class="diagram">
<svg viewBox="0 0 600 110" role="img" aria-label="リレーションのparent/child方向の図">
  <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" class="ahfill"/></marker></defs>
  <rect class="box" x="20" y="34" width="200" height="44" rx="8"/><text class="t" x="120" y="54" text-anchor="middle">Server1</text><text class="sub" x="120" y="71" text-anchor="middle">child（子）</text>
  <path class="arrow" d="M222 56 H376"/>
  <text class="sub" x="300" y="46" text-anchor="middle">Managed by（type）</text>
  <rect class="box" x="380" y="34" width="200" height="44" rx="8"/><text class="t" x="480" y="54" text-anchor="middle">Server2</text><text class="sub" x="480" y="71" text-anchor="middle">parent（親）</text>
</svg>
<figcaption>図: <code>[Server1][Managed by][Server2]</code> → Server1=<b>child</b>・Server2=<b>parent</b>。読み方は「child–type–parent」。</figcaption>
</figure>

> ⚠️ **引っかけ**：parent/child は直感と逆になりやすい。リレーション文の読み方
> 「**child – type – parent**」を、上の Managed by の例で固定しておく。

リレーションは Discovery で自動作成されるほか、CIフォームの **CI relationship editor** や
**Unified Map**（CMDB Workspace）で手動作成・編集できる。実体は CI Relationship [`cmdb_rel_ci`] テーブル。

## Dependent と Non-dependent

| 種別 | 用途 | 削除 | 備考 |
|---|---|---|---|
| **Dependent**（例: Tomcat *RunsOn* Hardware） | **IRE の識別に使う**（依存CIを文脈で一意化） | **直接削除しない**（追跡されない） | hosting / containment ルール |
| **Non-dependent** | 単なる関連の記録 | 不要になれば削除可 | ソースは `sys_rel_source` に記録 |

- **Non-dependent** のソース履歴 Relationship Sources [`sys_rel_source`] は、IRE負荷軽減のため**既定で自動格納しない**
  （`glide.identification_engine.populate_sys_rel_source` で有効化可）。`cmdb_rel_ci` の非依存リレーション削除時は
  対応する `sys_rel_source` レコードもカスケード削除。

> 📌 **要点**：依存関係＝**IREの識別材料**だから安易に消さない。非依存＝表示・管理用で消してよい、と覚える。

## Suggested Relationships

**Suggested relationship** は「このクラス間にはこの型のリレーションが**あるべき**」というモデル定義。
CI Class Manager で追加し、**CMDB Health のリレーション健全性**（第1章）で「suggested に準拠していない」関係を検出できる。
hosting / containment ルールも、あるべき構造を表す。

**主要テーブル/用語**：`cmdb_rel_ci` / `sys_rel_source` / relationship type / dependent relationship /
suggested relationship / hosting・containment / CI relationship editor・Unified Map。
