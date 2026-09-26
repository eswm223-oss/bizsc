# BizSC Handover Phase

更新日: 2026-09-26

## 1. この資料の目的

この資料は、BizSC の現在の進捗を別 Chat へ引き継ぎ、そのまま開発を再開するための資料です。

2026-09-26 に大きな方針変更を行った。

```text
旧:
EDINET を主データソースとして財務データを抽出

新:
J-Quants API を主データソースとして
株価・財務データを PostgreSQL に Cache
↓
BizSC の株スクリーニングへ利用
```

EDINET の既存実装は残すが、以降の主開発対象から外す。

---

## 2. Project

```text
Project: BizSC
Workspace: D:\Development\apps\bizsc
GitHub: https://github.com/eswm223-oss/bizsc
```

BizSC は日本株向けの個人用株スクリーニング Web Application。

主 Stack:

- FastAPI
- Python 3.12
- SQLAlchemy
- PostgreSQL 17
- Alembic
- pytest
- httpx
- React
- TypeScript
- Vite
- Bootstrap
- Docker Compose

---

## 3. 開発ルール

```text
Phase
↓
Step
↓
実装
↓
Test
↓
小範囲の実データ確認
↓
DB確認
↓
次 Step
```

重要:

- 1 Step ずつ進める
- 完了済み Step を繰り返さない
- コードは必要に応じて GitHub の最新状態を確認
- 推測で現在コードを決めつけない
- API は小件数で確認してから拡大
- Client / Service / Repository の責務を分離
- Repository で勝手に Transaction を確定しない
- API Key / Token を Log / Error / Git に出さない
- 新しい Library は必要性を確認してから追加
- 正確性優先

---

## 4. 2026-09-26 方針変更

### 採用

```text
J-Quants API
```

を BizSC の主データソースにする。

目的:

```text
上場銘柄
日足株価
財務情報
必要な市場データ
↓
PostgreSQL
↓
Screening
```

### 白紙化

EDINET を使った:

```text
CSV ZIP Download
CSV / XBRL 財務解析
全上場企業の財務項目正規化
EDINET ベース Screening
```

は進めない。

EDINET は会計基準・Taxonomy・Context・提出者拡張の正規化コストが高く、株スクリーニング用途では J-Quants の整形済みデータを中心にする方針へ変更した。

---

## 5. J-Quants の現在の決定事項

確定:

- J-Quants を主データソースにする
- J-Quants API 取得データを PostgreSQL に Cache する
- 株価と財務は別 Domain / Table にする
- Screening 用の派生指標は BizSC 側で計算する
- EDINET は主処理から外す

未確定:

- 契約プラン
- 保存する全 Dataset
- 最終的な履歴年数
- J-Quants Table の Column / Unique Constraint
- Scheduler / 自動定期取得方式

Light / Standard 等の利用可能 Dataset は契約プランで変わるため、実装前に最新の公式仕様と契約内容を確認する。

---

## 6. 最初に取得する予定の Dataset

優先順位:

```text
1. 上場銘柄情報
2. 日足株価
3. 財務情報 Summary
```

その後の候補:

```text
指数
決算発表予定
信用関連
空売り関連
その他 Screening に必要な Dataset
```

Premium の詳細 BS / PL / CF を前提にしない。

---

## 7. DB の初期方針

まだ Table Schema は確定しない。

想定:

```text
jq_listed_issues
jq_daily_quotes
jq_financial_summaries
jq_sync_runs
```

名称を含め、実 API Response を確認してから確定する。

保存方針:

- Screening に必要な値を正規化
- 証券コードは文字列
- 欠損と 0 を区別
- 金額 / 比率は型を慎重に決める
- 取得元の日付・識別子を保持
- 再取得で重複しない Unique Key を設計
- 生 JSON をそのまま唯一の保存形式にしない

---

## 8. BizSC で作る主な Screening 指標

株価:

```text
最新株価
1M / 3M / 6M / 1Y 騰落率
52週高値 / 安値
52週高値からの下落率
出来高
時価総額
```

財務:

```text
売上高
営業利益
経常利益
純利益
EPS
BPS
総資産
純資産
自己資本比率
営業CF
投資CF
財務CF
```

派生:

```text
売上成長率
利益成長率
営業利益率
ROE
ROA
FCF
PER
PBR
```

API から直接取得する値と BizSC 計算値を区別する。

---

## 9. EDINET Legacy 実装

既存コードは GitHub に残っている。

```text
backend/app/clients/edinet.py
backend/app/services/edinet_inventory.py
backend/app/repositories/edinet_inventory.py
backend/app/models/edinet_document.py
backend/app/models/edinet_inventory_run.py
backend/app/batches/edinet_inventory.py

backend/tests/test_edinet_client.py
backend/tests/test_edinet_inventory.py
backend/tests/test_edinet_inventory_batch.py
```

DB:

```text
edinet_documents
edinet_inventory_runs
```

---

## 10. EDINET 最終確認地点

EDINET 側で完了していた内容:

```text
EDINET API Client
現在上場企業判定
1日 Refresh
複数日 refresh_date_range
CLI Batch
Unit Test
実 DB 保存
再実行 Refresh
docInfoEditStatus 修正レコード対応
```

実運用テスト:

```text
2026-07-01 ～ 2026-07-31

run_days       = 31
completed_days = 31
failed_days    = 0
document_count = 1848
```

2026-07-13 に同一 `docID` が2件返る実データを確認し、`docInfoEditStatus == "1"` を保存対象から除外して解消した。

この EDINET 実装は今後の J-Quants 実装の Transaction / Batch 設計の参考にはできるが、EDINET の続きを実装しない。

---

## 11. EDINET Code / Table の扱い

現時点では削除しない。

```text
J-Quants 基盤完成
↓
BizSC Screening で利用可能確認
↓
EDINET Legacy を削除するか判断
```

J-Quants の実装中に EDINET Table を再利用しない。
J-Quants は新しい Domain / Table として作る。

---

## 12. J-Quants Phase 01 の再開地点

次の作業は EDINET Step 7-3 ではない。

新しい開始地点:

```text
J-Quants Phase 01
Step JQ-1
```

### Step JQ-1

最新の公式仕様を確認して以下を確定する。

```text
契約プラン
利用可能 Dataset
認証方式
Base URL
Rate Limit / Request 制約
取得可能期間
```

Secrets は `.env` / Environment Variable で管理する。

### Step JQ-2

J-Quants Client の最小実装。

候補:

```text
backend/app/clients/jquants.py
backend/tests/test_jquants_client.py
```

まず1 Datasetだけ実接続確認する。

### Step JQ-3

上場銘柄情報を対象に:

```text
Model
Migration
Repository
Service
Unit Test
実 DB 保存
```

を順に作る。

その後:

```text
日足株価
↓
財務 Summary
↓
Screening 指標
```

へ進む。

---

## 13. J-Quants Client 実装時の原則

- 認証方式を最新公式仕様で確認
- API Token / Key をコードに直書きしない
- Timeout を設定
- HTTP Error を分類
- Rate Limit を考慮
- Invalid Response を正常データとして扱わない
- Secret を Log に出さない
- Unit Test では HTTP を mock
- 実接続では全銘柄・長期間をいきなり取得しない

---

## 14. J-Quants DB Refresh 原則

EDINET で確認した良い設計を継承する。

```text
取得
↓
Validation
↓
DB更新
↓
commit
```

失敗:

```text
rollback
↓
安全な実行状態保存
↓
Exception re-raise
```

ただし J-Quants の Dataset ごとに最適な Upsert / Refresh 単位を決める。
EDINET の「日単位 DELETE → INSERT」をそのままコピーしない。

---

## 15. 既存 Web App 状態

User Domain:

- CRUD 実装済み
- Search
- Active Filter
- Sort
- Pagination
- React UI

基本 Layer:

```text
Router
↓
Service
↓
Repository
↓
Model
↓
PostgreSQL
```

外部 API:

```text
Client
↑
Service
```

この構成は J-Quants でも維持する。

---

## 16. 新 Chat で最初に読む資料

```text
docs/architecture.md
docs/handover_phase.md
docs/project-overview.md
```

必要に応じて GitHub 最新コードを確認する。

---

## 17. 再開時の最重要事項

```text
EDINET の続きから始めない。
```

開始地点:

```text
J-Quants Phase 01
Step JQ-1
J-Quants の契約プラン・認証・利用 Dataset の確認
```

その後:

```text
Client
↓
Listed Issues DB Cache
↓
Daily Quotes DB Cache
↓
Financial Summary DB Cache
↓
Screening
```

以上。
