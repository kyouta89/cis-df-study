---
chapter: ch0
section: ch0-s1
title: CMDB と CI とクラス階層（まず全体像）
sources:
  - title: CI relationships in the CMDB
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CIRelationships.html
  - title: CI Class Manager
    url: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html
related_seqs: []
---

> 🧭 **この章は前提知識の地ならしです（任意）**。CMDB/CSDM をすでに触っている人はスキップしてOK。
> CSA（プラットフォーム基礎）は分かるが CMDB は初めて、という読者向けに最短の全体像を置きます。

## CMDB とは

**CMDB（Configuration Management Database）** は、IT環境の構成要素と**その関係**を記録するデータベース。
単なる資産一覧（静的なリスト）と違い、「何があるか」だけでなく「**何が何に繋がっているか**」を持つのが本質。

- **CI（Configuration Item）** … 構成アイテム。実体は **CI [`cmdb_ci`] テーブルのレコード**。
  サーバ・DB・アプリ・ネットワーク機器などが CI。
- **リレーション** … CI 間の関係（例：アプリ→DB→サーバ）。第4章で詳説。

> 📌 CSAの知識で言い換えると：CMDB は `cmdb_ci` を基底とする**テーブル群**で、各CIはそのレコード。
> 普段のテーブル/フォーム/参照の知識がそのまま効く。違うのは「**関係**」と「**識別の厳密さ**」（後述）。

## クラス階層（テーブル継承）

CMDB は `cmdb_ci` を頂点に、**クラス（＝テーブル）が継承で枝分かれ**する構造。
例：`cmdb_ci` → `cmdb_ci_hardware` → `cmdb_ci_computer` → `cmdb_ci_server` … と具体化していく。

<figure class="diagram">
<svg viewBox="0 0 640 188" role="img" aria-label="CMDBクラス継承階層の図">
  <rect class="box root" x="20" y="12" width="230" height="32" rx="6"/><text class="tw" x="35" y="33">cmdb_ci（基底）</text>
  <path class="ln" d="M40 44 V73 H70"/>
  <rect class="box" x="70" y="58" width="250" height="30" rx="6"/><text class="t" x="85" y="78">cmdb_ci_hardware</text>
  <path class="ln" d="M90 88 V119 H120"/>
  <rect class="box" x="120" y="104" width="250" height="30" rx="6"/><text class="t" x="135" y="124">cmdb_ci_computer</text>
  <path class="ln" d="M140 134 V165 H170"/>
  <rect class="box" x="170" y="150" width="250" height="30" rx="6"/><text class="t" x="185" y="170">cmdb_ci_server</text>
  <text class="sub" x="450" y="112">子は親の属性・</text>
  <text class="sub" x="450" y="130">ルールを継承 ↓</text>
</svg>
<figcaption>図: クラス継承。<code>cmdb_ci</code> を頂点に具体化し、子は親の属性・識別/突合/健全性ルールを継承する。</figcaption>
</figure>

- 子クラスは親の**属性を継承**し、独自属性を足す。
- 識別ルール・突合ルール・健全性設定なども**親→子へ継承**される（第1・3章で再登場）。
- これらクラスの定義・設定を一元管理するのが **CI Class Manager**（第4章）。

> 🧩 **independent / dependent**（第3・4章への布石）：単独で存在できるCI（Server等）は **independent**、
> 他のCIに依存しないと意味を成さないCI（Network Adapter, Application等）は **dependent**。
> この区別が「識別の仕方」を左右する。

**この先の地図**：構造（本節）→ **データの入り方**（次節）→ **サービスの考え方**（第3節）と進むと、
第1章以降（健全性・取り込み・構成・CSDM）が読みやすくなる。
