#!/usr/bin/env python3
"""ドラッグ問題13問の翻訳・解説を translations.json に追記する。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "data" / "translations.json"
tr = json.loads(p.read_text(encoding="utf-8"))

D = {
"2": {
 "q_ja":"アプリケーションサービスを作成・populate する方法を、最も適切な説明にドラッグ&ドロップしてください。(一部は使用しない場合があります)",
 "q_mt":"アプリケーションサービスを設定する方法を、最も適切な説明にドラッグアンドドロップしてください。",
 "ai":"【正解(正解画像で確認)】\n・Service Mapping (Top-down) ← ミッションクリティカルなアプリサービス向け。パターンを用いた精密な手法\n・Service Mapping (Connection Suggestion) ← カスタムビルドのアプリ向け。application fingerprinting で迅速にサービスマップ生成\n・Tag-Based ← クラウドネイティブ/コンテナ/VM環境のマッピングに最適\n・Dynamic CI Group ← 小規模アプリサービス向け。フィルタとCMDBクエリで容易にグループ化"},
"50": {
 "q_ja":"ServiceNow は、CI とリレーションを効果的に取り込み・管理・維持するための CMDB 管理ツール群を提供しています。\n設計アーキテクチャを、対応する管理ツールにドラッグ&ドロップしてください。(一部は使用しない場合があります)",
 "q_mt":"ServiceNowは、CIとリレーションシップを効果的に取り込み、管理し、維持するために設計されたCMDB管理ツールのスイートを提供します。\nデザインアーキテクチャを、その管理ツールにドラッグアンドドロップしてください。\nいくつかのオプションは適用されない場合があります。",
 "ai":"【正解(画像の対応)】\n・Agent Client Collector ← エージェント型で、パターンを実行する自動化ソリューション\n・Import Sets ← トランスフォームマップを用いた自組織構築のソリューション\n・Service Graph Connector ← ストア提供の事前構築済み統合(最小限のカスタマイズで利用)\n・ServiceNow Discovery ← エージェントレスで、パターンを実行する自動化ソリューション\n(未使用: 他ベンダーからのサードパーティ統合)"},
"55": {
 "q_ja":"製品(プロダクト)を、その説明にドラッグ&ドロップしてください。",
 "q_mt":"プロダクトを、その説明にドラッグアンドドロップしてください。",
 "ai":"【正解(画像の対応)】\n・ServiceNow Discovery ← ネットワーク上のデバイスとアプリを自動的に識別し、正確で最新の情報でCMDBを更新\n・Service Graph Connectors ← ServiceNowと外部システム間の統合を促進し、データをインポート・同期\n・Service Mapping ← サービスの完全なトポロジーを示し、下位のインフラ/アプリにどう支えられているかを表す\n・Agent Client Collector(ACC)← エンドポイント構成へのリアルタイムな可視性を提供し、CMDBを更新"},
"71": {
 "q_ja":"CMDB Health Dashboard の指標(メトリック)を、説明にドラッグ&ドロップしてください。",
 "q_mt":"CMDBヘルスダッシュボードのメトリックを、説明にドラッグアンドドロップしてください。",
 "ai":"【正解(正解画像を参照。以下は読み取り・確度中)】\n・Audits ← 実際の値を期待値と比較する\n・Duplicate CIs ← 識別と突合(IRE)で検出され、base system の修復ツールを持つ\n・Orphan CIs ← 使用(数)は最小化すべき\n・Required fields ← 一部の属性値が未設定/リレーションが欠落\n・Recommended fields ← 設定されているのが望ましく、トラブルシュートに役立つ\n・Stale CIs ← 更新されておらず古い可能性がある\n※一部の対応は解釈に幅があるため、上の正解画像で確認してください。"},
"87": {
 "q_ja":"新規 ServiceNow 顧客が、CMDB を支える構成管理チームを編成しています。\n各ロールを、対応する職務記述にドラッグしてください。",
 "q_mt":"新しいServiceNowの顧客が、彼らのCMDBをサポートするためのコンフィギュレーション管理チームを編成しています。\n各ロールを、それに対応するジョブの説明にドラッグしてください。",
 "ai":"【正解(画像の対応)】\n・CI Analyst ← CMDBデータおよびレポート/ダッシュボード等の基本UIに読み取り専用でアクセス\n・CMDB Process Owner ← ポートフォリオを構成する全要素を、そのライフサイクル全体にわたり管理する責任を持つ\n・Service or Product Owner ← 割り当てられたCIテーブルを管理し、レコードを最新に保ち、CMDB関連タスクを解決\n・Configuration Manager/CMDB Admin ← CMDB権限の最上位ロールを持つ"},
"88": {
 "q_ja":"CMDB管理者が、重複CIの予防・対処・修復に使えるツールを把握しようとしています。\n各機能を、対応する成果(アウトカム)にドラッグ&ドロップしてください。(一部は使用しない場合があります)",
 "q_mt":"あるCMDBアドミニストレーターが、重複したCIを防止、対処、および修復するための利用可能なツールを理解しようとしています。\n各機能を、対応するアウトカムとともにドラッグアンドドロップしてください。\nいくつかのオプションは適用されない場合があります。",
 "ai":"【正解(画像の対応)】\n・De-Duplication Tasks ← 重複CI解決のためグループに割り当て可能\n・CMDB Health Dashboard Correctness Scorecard ← CMDB内の重複CIに関する洞察を提供\n・De-Duplication Templates ← 重複解決タスクを一括(bulk)で解決する手段\n・Duplicate CI Remediator ← 重複解決タスクを個別に解決するウィザードを提供\n(未使用: Certification Tasks)"},
"101": {
 "q_ja":"CMDB Health Dashboard の指標(メトリック)を、説明にドラッグ&ドロップしてください。",
 "q_mt":"CMDBヘルスダッシュボードのメトリックを、説明にドラッグアンドドロップしてください。",
 "ai":"【正解(画像の対応)】\n・Duplicate ← 同一の物理/論理資産を複数回表すCMDBレコード\n・Required ← CIレコードの作成/更新に必要なフィールド\n・Orphan ← 他CIとの論理/物理リレーションを維持していないCMDBレコード\n・Stale ← もはや更新されないがDBに残るCMDBレコード\n・Recommended ← CIレコードの正確性・完全性・使いやすさを支えるフィールド\n・Audit ← 指定フィールドの実際値を、テンプレートで定義した期待値と比較"},
"102": {
 "q_ja":"CMDB Health Dashboard は3つの KPI(Correctness/Compliance/Completeness)に基づきます。各 KPI には複数のサブメトリックがあります。\nサブメトリックを KPI にドラッグしてください。(一部は使用しない場合があります)",
 "q_mt":"CMDBヘルスダッシュボードは、3つの主要業績評価指標(KPI)、すなわち正確性(Correctness)、コンプライアンス(Compliance)、完全性(Completeness)に基づいています。各KPIはいくつかのサブメトリックを含みます。\nサブメトリックをKPIにドラッグしてください。\nいくつかのオプションは適用されない場合があります。",
 "ai":"【正解(正解画像＋公式docで確定)】\nサブメトリック→KPI の対応:\n・Completeness(完全性)← Required(必須フィールド)\n・Compliance(コンプライアンス)← Audit(実際値と期待値の比較)\n・Correctness(正確性)← Orphan(孤立CI)\n(未使用: Stability / Certify / Suggested)\n※公式メトリクス定義: Completeness=Required/Recommended, Correctness=Orphan/Stale/Duplicate, Compliance=Audit。"},
"128": {
 "q_ja":"ある製造業組織が ServiceNow で Incident Management を導入し、機能強化のため追加製品の統合を検討しています。\n各 ServiceNow 製品を、Incident Management 支援においてもたらす価値にドラッグしてください。",
 "q_mt":"ある製造組織がServiceNowでインシデント管理を実装しており、その機能を強化するために追加の製品を統合したいと考えています。\n各ServiceNow製品を、インシデント管理のサポートにもたらす価値にドラッグしてください。",
 "ai":"【正解(画像の対応)】\n・Hardware Asset Management ← インシデント時の資産管理・維持のための資産アクションとイベントを提供\n・Risk Management ← 重要なIT/財務リスクデータを提供し、インシデントの業務への広範な影響を評価可能にする\n・Discovery ← ハードウェアやアプリの詳細な運用レベルデータを提供し、インシデント解決を改善\n・Service Portfolio Management ← サービスのライフサイクル情報を提供し、インシデントをサービスの状態・履歴に整合させる"},
"157": {
 "q_ja":"CMDB で異なるステータス属性を使う方式から、ライフサイクルオブジェクトへ移行するための手順があります。\n目的/属性を、説明にドラッグ&ドロップしてください。",
 "q_mt":"CMDBで異なるステータス属性を使用することから、ライフサイクルオブジェクトへ移行するために、いくつかのステップが取られる必要があります。\nオブジェクティブ/属性を、説明にドラッグアンドドロップしてください。",
 "ai":"【正解(画像の対応)】\n・life_cycle_mapping ← レガシーのステータス値を、最適なCSDMライフサイクル値ペアにマッピングする事前投入済みテーブル\n・life_cycle_stage ← レコードのライフサイクルのメタレベル状態を表すレコード属性\n・life_cycle_stage_status ← レコードのライフサイクルのサブレベル状態を表すレコード属性\n・life_cycle_object ← CIのタイプ(ハードウェア/ドキュメント/論理など)に基づき、利用可能なサブレベルのライフサイクル状態値を決めるテーブル"},
"168": {
 "q_ja":"CMDB オーナーが CSDM の取り組みを開始し、CSDM ドメインを理解する必要があります。\nCMDB オブジェクトを、正しい CSDM ドメインにドラッグしてください。",
 "q_mt":"あるCMDBオーナーがCSDMの旅を開始し、CSDMドメインに慣れる必要があります。\nCMDBオブジェクトを、正しいCSDMドメインにドラッグしてください。",
 "ai":"【正解(画像の対応)】\n・Business Application ← Design and Planning(設計・計画)ドメイン\n・Business Process ← Foundation(基盤)ドメイン\n・Application Service ← Service Delivery(サービス提供)ドメイン\n・Business Service ← Sell / Consume(販売・消費)ドメイン"},
"174": {
 "q_ja":"プラットフォーム上のサービスタイプの一覧があります。適切なサービスを、その定義にドラッグしてください。",
 "q_mt":"プラットフォーム内のサービスタイプのリストが与えられています。適切なサービスを、その定義にドラッグしてください。",
 "ai":"【正解(画像の対応)】\n・Application Service ← デプロイされたシステム/アプリケーションスタックの論理的表現\n・Technology Management Service(Technical Service)← サービスオーナー向けに公開され、1つ以上のビジネス/アプリケーションサービスを支える\n・Business Service ← ビジネスユーザー向けに公開され、1つ以上のビジネスケイパビリティを支える"},
"175": {
 "q_ja":"プラットフォームオーナーが CSDM を支えるガバナンスチームを編成しています。\nドメインを、ガバナンスチームを構成するロールにドラッグしてください。",
 "q_mt":"あるプラットフォームオーナーが、CSDMをサポートするためのガバナンスチームを構築しています。\nドメインを、ガバナンスチームを構成するロールにドラッグしてください。",
 "ai":"【正解(画像の対応)】各CSDMドメインとガバナンスロール:\n・Design Domain ← Enterprise Architect(s), Platform Owner\n・Foundation Domain ← Enterprise Architect(s), Data Steward(s), Process Owner(s), Platform Owner\n・Portfolio Domain ← Service Owner(s), Platform Owner\n・Technical Domain ← Technology Service Owner(s), Application Service Owner(s), Platform Owner"},
"176": {
 "q_ja":"エンタープライズアーキテクトが、CMDB オーナーに CSDM の利点を理解してもらう必要があります。\nCSDM ドメインを、それぞれの利点にドラッグしてください。",
 "q_mt":"あるエンタープライズアーキテクトが、CMDBオーナーにCSDMの利点を理解する手助けをする必要があります。\nCSDMドメインを、それぞれの利点(ベネフィット)にドラッグしてください。",
 "ai":"【正解(画像の対応)】\n・Design and Planning ← ビジネスアプリと関連ケイパビリティのCIを把握し、重複の特定・コスト監視・ロードマップ投資判断に活用\n・Service Delivery ← テクニカルサービス/サービスオファリング/サービスサポートと、下位の技術CIへの全リレーションを把握\n・Service Consumption ← ビジネスサービスと、その所有・コスト・提供範囲を把握し、アクセス要求を行う\n・Foundation ← CSDM実装時にベースシステムのテーブルを使い、ServiceNow製品とNow Platformから最大の価値を引き出す"},
}

for seq, v in D.items():
    v["opts_ja"] = []
    v["opts_mt"] = []
    tr[seq] = v

p.write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[add_drag] {len(D)} drag questions added. translations total: {sum(1 for k in tr if k.isdigit())}")
