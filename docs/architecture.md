# BizSC Architecture

更新日: 2026-09-26

## 1. このドキュメントの目的

このドキュメントは、BizSC の現在のシステム構成・責務分離・実装ルールを確認するための基準資料です。

過去の細かな作業履歴ではなく、現在採用している構成と今後の実装判断の基準を記載します。
具体的な進捗・直近の検証結果・次の Step は `handover_phase.md` で管理します。

---

## 2. プロジェクト概要

**Project:** BizSC

BizSC は、日本株を対象とした個人用の株スクリーニング Web Application です。

主な目的:

- 上場銘柄の基礎情報を DB にキャッシュする
- 日足株価を蓄積する
- 財務情報を蓄積する
- 株価・財務データからスクリーニング指標を計算する
- 条件検索・比較・ランキング・可視化へ拡張する

現在の主要データソース方針:

```text
J-Quants API
    ↓
BizSC Backend
    ↓
PostgreSQL Cache
    ↓
Screening / Analysis
```

2026-09-26 から J-Quants を BizSC の主データソースとして採用する。

EDINET はこれまで実装・検証したコードと DB Table は残っているが、今後の主データ取得方式から外し、EDINET ベースの財務データ取得計画は白紙化する。

---

## 3. 技術構成

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL 17
- psycopg
- Alembic
- Pydantic / pydantic-settings
- pytest
- httpx

### Frontend

- React
- TypeScript
- Vite
- React Router
- Axios
- Bootstrap

### Development / Infrastructure

- Windows
- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus

Workspace:

```text
D:\Development\apps\bizsc
```

GitHub:

```text
https://github.com/eswm223-oss/bizsc
```

コード確認が必要な場合は、推測ではなく GitHub の最新状態を確認する。

---

## 4. 全体アーキテクチャ

通常の Web API:

```text
Browser
  ↓
React / TypeScript / Vite
  ↓ Axios
FastAPI
  ↓
API Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy Model
  ↓
PostgreSQL
```

外部データ取得:

```text
J-Quants API
    ↑
    │ HTTP
Client
    ↑
    │
Service
    ├────────→ Repository ─→ Model ─→ PostgreSQL
    └────────→ Business Logic
```

責務:

- **Client**: 外部 API 通信
- **Service**: 業務処理、複数処理の組み立て、Transaction
- **Repository**: PostgreSQL への DB Access
- **Model**: Table 定義
- **API Router**: HTTP Request / Response

Client と Repository を混在させない。

---

## 5. Docker Compose

基本 Service:

```text
frontend
backend
db
```

Ports:

```text
frontend: 5173
backend: 8000
db: 5432
```

PostgreSQL:

```text
Image: postgres:17
Database: bizsc
User: bizsc
```

Windows にインストールした PostgreSQL Service が `5432` を使用すると Docker PostgreSQL と競合するため、BizSC では Docker 側を使用する。

---

## 6. Backend 基本構成

```text
backend/
├─ alembic/
├─ app/
│  ├─ api/
│  ├─ batches/
│  ├─ clients/
│  ├─ core/
│  ├─ db/
│  ├─ models/
│  ├─ repositories/
│  ├─ schemas/
│  ├─ services/
│  └─ main.py
└─ tests/
```

### API Router

URL / HTTP Method / Parameter / Schema / Dependency Injection / Service 呼び出しを担当する。
SQLAlchemy Query や複雑な業務ロジックを直接書かない。

### Client

外部 API の Endpoint、認証、Request Parameter、Timeout、HTTP Error、Response Parsing を担当する。
API Key / Token を Source Code、Log、Error Message に出さない。

### Service

Business Logic、Client 呼び出し、Repository 呼び出し、Transaction を担当する。

### Repository

select / insert / update / delete / pagination / count 等の DB Access を担当する。
Transaction を Service で管理する場合、Repository 内で勝手に `commit()` しない。

### Model

SQLAlchemy Model を定義する。
Schema 変更は Alembic Migration を通す。

### batches

期間指定のデータ取得・DB 更新など、CLI から実行するバッチ処理の入口を置く。
外部 API / DB 処理本体は Client / Service / Repository に委譲する。

---

## 7. J-Quants Domain

2026-09-26 から、J-Quants を BizSC の主データソースとして採用する。

目的:

```text
J-Quants
  ↓
上場銘柄
日足株価
財務 Summary
その他必要データ
  ↓
PostgreSQL
  ↓
BizSC Screening
```

契約プランは現時点では未確定。
Light / Standard 等のプラン差に依存する機能は、契約内容と最新の公式 API 仕様を確認してから実装対象を確定する。

実装をプラン名に密結合させず、「利用可能な Dataset を取得する」構造にする。

---

## 8. J-Quants 取得対象の優先順位

最初に扱うデータ:

```text
1. 上場銘柄情報
2. 日足株価
3. 財務情報 Summary
```

その後、契約プランと BizSC の要件に応じて:

```text
4. 指数データ
5. 決算発表予定
6. 信用取引 / 空売り等
7. その他 Dataset
```

を追加する。

詳細 BS / PL / CF は Premium 前提にしない。
まず Summary で作れるスクリーニングを優先する。

---

## 9. J-Quants DB 設計方針

最初から全 Table を確定しない。
実 API Response を小範囲で確認し、Column と Unique Constraint を決めてから Migration を作る。

想定 Domain:

```text
JQuantsListedIssue
JQuantsDailyQuote
JQuantsFinancialSummary
JQuantsSyncRun
```

Table 名・Column は Phase 01 で実レスポンス確認後に確定する。

重要方針:

- 証券コードは文字列として扱う
- API の生 Response をそのまま巨大 JSON として保存することを目的にしない
- Screening に必要な項目を正規化して保存する
- 元データとの追跡に必要な識別子・日付は保持する
- Decimal が必要な数値で安易に `float` を使わない
- 欠損値と 0 を区別する
- 株価と財務は別 Domain / Table とする
- 再取得時に重複しない Unique Key を設計する

---

## 10. Screening 指標

### 株価系

- 最新株価
- 1か月 / 3か月 / 6か月 / 1年騰落率
- 52週高値
- 52週安値
- 52週高値からの下落率
- 出来高
- 時価総額

### 財務系

- 売上高
- 営業利益
- 経常利益
- 純利益
- EPS
- BPS
- 総資産
- 純資産
- 自己資本比率
- 営業 CF
- 投資 CF
- 財務 CF
- FCF
- ROE
- ROA
- 営業利益率
- 売上 / 利益成長率
- PER
- PBR

「API から直接取得する値」と「BizSC で計算する指標」を分離する。

---

## 11. データ履歴方針

過去データは DB に Cache し、毎回すべてを外部 API から再取得しない。

過去10年を目標としてきたが、J-Quants の利用可能期間は契約プランに依存するため、最終的な履歴年数はプラン確定後に決める。

基本方針:

```text
初期投入
→ 取得可能な過去履歴を範囲指定で Cache

通常運用
→ 最新分を定期追加

必要時
→ 指定期間を Refresh
```

一度に長期間を処理することを前提にせず、小範囲で検証してから期間を広げる。

---

## 12. J-Quants Error / Transaction 方針

外部 API では以下を区別できる構造にする。

- 認証設定不足
- HTTP Error
- Rate Limit
- Timeout
- Invalid Response
- Validation Error

DB Refresh では:

```text
外部 API 取得
↓
Response Validation
↓
DB 更新
↓
commit
```

を基本とし、不正 Response を「0件」と誤認して正常データを削除しない。

複数日処理の場合、必要に応じて日単位 / Dataset 単位で Transaction を分離する。

---

## 13. J-Quants 認証情報

認証方式・Environment Variable 名は、実装開始時に最新の J-Quants 公式 API 仕様を確認して確定する。

原則:

```text
Secret
→ .env / Environment Variable

Source Code
→ Secret を直接記述しない
```

認証情報を Git / Log / Error Message に出さない。

---

## 14. EDINET Legacy Status

EDINET は 2026-09-26 で主データソースから外す。

既存実装は Repository に残っている。

主な Legacy File:

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

既存 Table:

```text
edinet_documents
edinet_inventory_runs
```

確認済み実績:

- 日単位 Refresh
- 範囲指定 Refresh
- CLI Batch
- `docInfoEditStatus == "1"` 除外
- 2026-07-01 ～ 2026-07-31 の31日処理
- `run_days = 31`
- `completed_days = 31`
- `failed_days = 0`
- `document_count = 1848`

今後:

```text
EDINET CSV ZIP 取得
XBRL / CSV 財務解析
EDINET ベースの Screening
```

は進めない。

既存 EDINET Table / Migration / Code を今すぐ削除する必要はない。
J-Quants 移行が安定してから、削除するか Legacy として残すかを別途判断する。

---

## 15. User Domain

既存 User CRUD は維持する。

```text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

Frontend の User UI も既存機能として維持する。

---

## 16. Frontend 方針

React + TypeScript + Vite + Bootstrap を継続する。

今後の主要画面候補:

```text
銘柄一覧
Screening 条件設定
Screening 結果
銘柄詳細
株価 Chart
財務推移
比較画面
```

J-Quants のデータ取得基盤が完成するまでは、Frontend の Screening UI を先行しすぎない。

---

## 17. Migration / Test 方針

Migration:

```text
SQLAlchemy Model変更
↓
alembic revision --autogenerate
↓
Migration確認
↓
alembic upgrade head
↓
TablePlus確認
```

J-Quants Table は、API Response を確認してから作る。

Test:

- Client は HTTP を mock
- Service は Mapping / Refresh / Transaction / rollback / 重複防止を確認
- Batch は CLI / Service 呼び出し / Session close を確認
- 実 API 接続は Unit Test と分け、小件数で確認する

---

## 18. 開発進行ルール

```text
Step
↓
実装
↓
Unit Test
↓
小範囲の実 API 確認
↓
DB 確認
↓
次 Step
```

- 1 Step ずつ進める
- 既存コードを GitHub で確認してから変更
- 不要な Library / Infrastructure を追加しない
- 外部 API を大量に叩く前に小範囲で検証
- Error 原因を推測で確定しない
- Secret を出さない
- Commit / Push は区切りの良い地点
- 正確性を優先する

---

## 19. 次の Architecture Step

```text
J-Quants Phase 01

Step JQ-1
契約プラン / 利用可能 Dataset / 認証方式 / 取得可能期間を確認

Step JQ-2
backend/app/clients/jquants.py を追加
最小の実 API 接続を確認

Step JQ-3
上場銘柄情報を取得し、DB Model / Repository / Service を設計

Step JQ-4
日足株価 DB Cache

Step JQ-5
財務 Summary DB Cache

Step JQ-6
Screening 指標計算
```

まず Client と上場銘柄 Master から開始する。

以上。
