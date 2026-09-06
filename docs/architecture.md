# BizSC Architecture

更新日: 2026-09-06

## 1. このドキュメントの目的

このドキュメントは、BizSC の**現在のシステム構成・責務分離・実装ルールを確認するための基準資料**です。

過去の各 Phase / Step の詳細な作業履歴ではなく、現在の構成と今後の実装判断の基準を記載します。

具体的な進捗・次の作業・直前の検証結果は `handover_phase.md` 側で管理します。

---

## 2. プロジェクト概要

**Project:** BizSC

BizSC は、業務機能を段階的に追加していく Web Application です。

現在の主要技術構成:

- Docker Desktop
- Docker Compose
- FastAPI
- Python
- SQLAlchemy
- PostgreSQL 17
- Alembic
- Pydantic / pydantic-settings
- pytest
- httpx
- React
- TypeScript
- Vite
- React Router
- Axios
- Bootstrap
- Cursor
- GitHub Desktop
- TablePlus

現在の主要 Domain:

- User
- EDINET Document Inventory

---

## 3. 全体アーキテクチャ

通常の BizSC Web API は以下のレイヤーで構成します。

```text
Browser
  │
  │ http://localhost:5173
  ▼
React / TypeScript / Vite
  │
  │ Axios
  ▼
FastAPI
  │
  ▼
API Router
  │
  ▼
Service
  │
  ▼
Repository
  │
  ▼
SQLAlchemy Model
  │
  ▼
PostgreSQL
```

外部 API を利用する処理では Client を分離します。

```text
External API
    ▲
    │ HTTP
    │
Client
    ▲
    │
Service
    │
    ├────────► Repository ──► Model ──► PostgreSQL
    │
    ▼
Business Logic
```

EDINET の現在の構成:

```text
EDINET API / EDINET Code List
        │
        ▼
backend/app/clients/edinet.py
        │
        ▼
EdinetInventoryService
        │
        ▼
EdinetInventoryRepository
        │
        ▼
EdinetDocument / EdinetInventoryRun
        │
        ▼
PostgreSQL
```

Client と Repository は別責務です。

- **Client**: 外部サービスとの通信
- **Repository**: PostgreSQL への DB Access
- **Service**: Client と Repository を組み合わせた業務処理
- **Model**: DB Table 定義
- **API Router**: HTTP Request / Response

---

## 4. 開発環境

主な開発環境:

```text
OS: Windows
Workspace:
D:\Development\apps\bizsc
```

主な Tool:

- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus

GitHub Repository:

```text
https://github.com/eswm223-oss/bizsc
```

コード内容を確認する必要がある場合は、推測ではなく GitHub の最新コードを確認します。

---

## 5. Project Root

```text
bizsc/
├─ .cursor/
├─ backend/
├─ frontend/
├─ docs/
├─ compose.yaml
├─ README.md
├─ .editorconfig
└─ .gitignore
```

| Path | 役割 |
|---|---|
| `backend/` | FastAPI Backend |
| `frontend/` | React Frontend |
| `docs/` | Architecture / Handover / Project Overview 等 |
| `compose.yaml` | Docker Compose |
| `README.md` | Project の基本説明 |

---

## 6. Docker Compose

BizSC は基本的に以下の 3 Service で開発します。

```text
frontend
backend
db
```

### backend

```text
Container: bizsc-backend
Port: 8000
Volume: ./backend:/app
```

Backend Source は Volume Mount されています。

通常の Python Source 修正だけなら、毎回 Image Build は不要です。

### frontend

```text
Container: bizsc-frontend
Port: 5173
Volume:
  ./frontend:/app
  /app/node_modules
```

Frontend Source も Volume Mount されています。

### db

```text
Container: bizsc-db
Image: postgres:17
Port: 5432
Database: bizsc
User: bizsc
Volume: postgres-data
```

PostgreSQL Data は Docker Volume に保存します。

### Windows 版 PostgreSQL との競合

Windows にインストールされた PostgreSQL Service が `5432` を使用すると、
Docker の PostgreSQL と接続先が混在することがあります。

BizSC では Docker PostgreSQL を利用するため、不要な Windows PostgreSQL Service は停止した状態を基本とします。

---

## 7. Backend 基本構成

```text
backend/
├─ Dockerfile
├─ requirements.txt
├─ alembic.ini
├─ alembic/
│  └─ versions/
├─ app/
│  ├─ api/
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

主な Backend 技術:

- FastAPI
- SQLAlchemy
- PostgreSQL
- psycopg
- Alembic
- Pydantic
- pydantic-settings
- pytest
- httpx

---

## 8. Backend Layer の責務

### 8.1 API Router

配置:

```text
backend/app/api/
```

責務:

- URL
- HTTP Method
- Path Parameter
- Query Parameter
- Request Schema
- Response Schema
- Dependency Injection
- Service 呼び出し

API Router に複雑な Business Logic や SQLAlchemy Query を直接書かない方針です。

### 8.2 Service

配置:

```text
backend/app/services/
```

責務:

- Business Logic
- Client 呼び出し
- Repository 呼び出し
- 複数処理の組み立て
- Transaction の境界
- Error 時の rollback / status 更新

EDINET のように「外部 API 取得 → Filter → DB刷新」を行う処理は Service が中心になります。

### 8.3 Repository

配置:

```text
backend/app/repositories/
```

責務:

- select
- insert
- update
- delete
- filter
- sort
- pagination
- count
- SQLAlchemy Session を利用した DB Access

Transaction 全体を Service で制御する必要がある処理では、
Repository 内で勝手に `commit()` しない設計を採用します。

### 8.4 Model

配置:

```text
backend/app/models/
```

SQLAlchemy Model を定義します。
DB Schema 変更は Alembic Migration を通します。

### 8.5 Schema

配置:

```text
backend/app/schemas/
```

主な用途:

- API Request
- API Response
- Validation
- Create / Update Schema
- List Response

### 8.6 Client

配置:

```text
backend/app/clients/
```

外部 Service との通信を担当します。

責務:

- Endpoint
- Request Parameter
- Header / API Key
- HTTP
- Timeout
- HTTP Error
- Response 取得
- 外部データ形式の Parsing
- 秘密情報を漏らさない Error Handling

### 8.7 db

```text
backend/app/db/
├─ base.py
└─ database.py
```

`database.py` では `engine` と `SessionLocal` を生成します。

### 8.8 core

Application 全体の共通設定です。

EDINET API Key:

```python
edinet_api_key: Optional[str] = None
```

Environment Variable:

```text
EDINET_API_KEY
```

API Key は Source Code に直接記載しません。

---

## 9. Database Migration 方針

DB Schema は Alembic で管理します。

```text
SQLAlchemy Model変更
        ↓
alembic revision --autogenerate
        ↓
Migration内容を確認
        ↓
alembic upgrade head
        ↓
DB/TablePlusで確認
```

EDINET 用 DB Table は Alembic で追加済みです。

主な Migration:

```text
2290170f9497
add EDINET inventory tables

6fb348a0c9e4
change EDINET submit datetime timezone
```

`submit_date_time` は EDINET の元データに合わせ、
`timestamp without time zone` としています。

---

## 10. User Domain

既存の User Domain:

```text
API Router
   ↓
UserService
   ↓
UserRepository
   ↓
User
   ↓
users
```

### users

```text
users
├─ id
├─ email
├─ hashed_password
├─ is_active
├─ created_at
└─ updated_at
```

Password 平文は DB に保存しません。

---

## 11. User API

Base Path:

```text
/users
```

主な Endpoint:

```text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

一覧では search / is_active filter / sort / pagination / total count に対応済みです。

---

## 12. EDINET Domain の目的

EDINET 機能の現在方針:

```text
現在上場している企業
        ×
現在日から過去10年間の提出日
        ×
csvFlag == "1"
```

に該当する EDINET 書類を棚卸しし、BizSC の PostgreSQL に Cache します。

重要:

- `docTypeCode` を事前に限定しない
- `csvFlag == "1"` を対象にする
- まず書類一覧を棚卸しする
- CSV ZIP 本体取得は別 Phase
- いきなり10年分を実行しない
- 小期間で検証してから対象期間を拡大する

---

## 13. EDINET Client

実装:

```text
backend/app/clients/edinet.py
```

### 13.1 書類一覧

```python
fetch_document_list(target_date: date)
```

Endpoint:

```text
GET https://api.edinet-fsa.go.jp/api/v2/documents.json
```

Parameter:

```text
date=YYYY-MM-DD
type=2
Subscription-Key=<EDINET_API_KEY>
```

Timeout:

```text
30 seconds
```

自動 Retry は現時点では実装していません。

### 13.2 EDINET Code List

```python
fetch_listed_sec_codes() -> set[str]
```

現在上場企業判定:

```text
上場区分 == "上場"
AND
証券コード != 空
```

証券コードは必ず `str` として扱います。

例:

```text
13010
130A0
137A0
```

英字を含むため数値変換は禁止します。

---

## 14. EDINET Client Error 方針

主な Error:

```text
EdinetClientError
EdinetApiKeyNotConfiguredError
EdinetHttpError
EdinetTimeoutError
EdinetInvalidJsonError
```

基本方針:

- API Key 未設定を明示
- HTTP Error を区別
- Timeout を区別
- Invalid JSON を区別
- Request URL 全体を Error Message に出さない
- Subscription-Key を Error Message / Log に出さない
- 429 を無限 Retry しない

---

## 15. EDINET Database Domain

EDINET は DB Domain まで実装済みです。

```text
EDINET Client
      ↓
EdinetInventoryService
      ↓
EdinetInventoryRepository
      ↓
┌────────────────────────┐
│ edinet_documents       │
│ edinet_inventory_runs  │
└────────────────────────┘
```

---

## 16. edinet_documents

Model:

```text
backend/app/models/edinet_document.py
```

主な目的:

> 指定提出日の「現在上場企業 × csvFlag=1」に一致する EDINET Document を保存する。

| Column | 概要 |
|---|---|
| `id` | Primary Key |
| `target_date` | EDINET 書類一覧を取得した対象日 |
| `doc_id` | EDINET docID / Unique |
| `edinet_code` | EDINET Code |
| `sec_code` | 証券コード |
| `filer_name` | 提出者名 |
| `ordinance_code` | 府令コード |
| `form_code` | 様式コード |
| `doc_type_code` | 書類種別コード |
| `period_start` | 期間開始日 |
| `period_end` | 期間終了日 |
| `submit_date_time` | 提出日時 |
| `doc_description` | 書類説明 |
| `parent_doc_id` | 親書類ID |
| `withdrawal_status` | 取下げ状態 |
| `doc_info_edit_status` | 書類情報修正状態 |
| `disclosure_status` | 開示状態 |
| `xbrl_flag` | XBRL flag |
| `pdf_flag` | PDF flag |
| `csv_flag` | CSV flag |
| `legal_status` | Legal status |
| `created_at` | BizSC 作成日時 |
| `updated_at` | BizSC 更新日時 |

主な Index / Constraint:

- `doc_id`: Unique + Index
- `target_date`: Index
- `sec_code`: Index
- `doc_type_code`: Index
- `submit_date_time`: Index

`submit_date_time` は:

```python
DateTime(timezone=False)
```

として保存します。

---

## 17. edinet_inventory_runs

Model:

```text
backend/app/models/edinet_inventory_run.py
```

目的:

> 各 target_date の最新棚卸し実行状態・件数・Error を管理する。

| Column | 概要 |
|---|---|
| `id` | Primary Key |
| `target_date` | 対象日 / Unique |
| `status` | processing / completed / failed |
| `total_count` | EDINET 書類一覧件数 |
| `listed_match_count` | 現在上場企業に一致した件数 |
| `csv_flag_count` | csvFlag=1 件数 |
| `listed_sec_code_count` | 使用した現在上場証券コード数 |
| `error_message` | 安全化した Error Message |
| `started_at` | 実行開始日時 |
| `completed_at` | 完了 / 失敗日時 |
| `created_at` | Record 作成日時 |
| `updated_at` | Record 更新日時 |

`target_date` は Unique です。

同じ日を再実行した場合、新しい run 行を増やさず同じ Record を更新します。

---

## 18. EDINET Repository

実装:

```text
backend/app/repositories/edinet_inventory.py
```

Class:

```python
EdinetInventoryRepository
```

主な Method:

```text
get_documents_by_target_date
delete_documents_by_target_date
add_documents
get_run_by_target_date
add_run
```

Repository では `commit()` を行わず `flush()` までとし、
Transaction は Service が管理します。

Repository は `completed なら skip` のような Business Logic を持ちません。

---

## 19. EDINET 1日刷新 Service

実装:

```text
backend/app/services/edinet_inventory.py
```

Class:

```python
EdinetInventoryService
```

公開 Method:

```python
refresh_one_day(
    db: Session,
    target_date: date,
) -> OneDayInventorySummary
```

基本フロー:

```text
target_date の run 取得
        ↓
processing に更新
        ↓
commit
        ↓
最新の上場証券コード取得
        ↓
EDINET 書類一覧取得
        ↓
Response 検証
        ↓
現在上場企業で Filter
        ↓
csvFlag == "1" で Filter
        ↓
EdinetDocument へ変換
        ↓
指定 target_date の既存 documents 削除
        ↓
新しい documents 追加
        ↓
run を completed に更新
        ↓
commit
```

---

## 20. 再実行 / Refresh 方針

```text
completed でも再実行可能
failed でも再実行可能
processing でも再実行可能
```

`completed` を Skip Gate にはしません。

同日再実行時:

```text
既存 target_date documents
        ↓ DELETE
新しい対象 documents
        ↓ INSERT
```

とし、日単位で置き換えます。

---

## 21. Transaction 方針

### processing 保存

外部 HTTP 通信前に `processing` として一度 `commit()` します。

### Refresh 本体

以下は同じ Transaction:

```text
既存 documents DELETE
        ↓
新 documents INSERT
        ↓
run completed UPDATE
        ↓
commit
```

DELETE 後に途中 `commit()` はしません。

### 失敗時

```text
Exception
   ↓
rollback
   ↓
run 再取得
   ↓
status = failed
   ↓
安全な error_message
   ↓
commit
   ↓
元 Exception を re-raise
```

刷新途中で失敗した場合、以前の正常な Document を残せる構成です。

---

## 22. EDINET Response Safety

Document List Response は `results` が正常な `list` の場合だけ Refresh を続行します。

正常:

```python
{"results": [...]}
```

異常:

```text
payload が dict ではない
results key がない
results が list ではない
```

正常な `"results": []` は 0 件の日として扱います。

目的は、API異常を空配列と誤認して既存データを削除することを防ぐためです。

---

## 23. EDINET Document 変換

主な Mapping:

```text
docID              -> doc_id
edinetCode         -> edinet_code
secCode            -> sec_code
filerName          -> filer_name
ordinanceCode      -> ordinance_code
formCode           -> form_code
docTypeCode        -> doc_type_code
periodStart        -> period_start
periodEnd          -> period_end
submitDateTime     -> submit_date_time
docDescription     -> doc_description
parentDocID        -> parent_doc_id
withdrawalStatus   -> withdrawal_status
docInfoEditStatus  -> doc_info_edit_status
disclosureStatus   -> disclosure_status
xbrlFlag           -> xbrl_flag
pdfFlag            -> pdf_flag
csvFlag            -> csv_flag
legalStatus        -> legal_status
```

`periodStart` / `periodEnd` は `date` に変換します。

`submitDateTime` は timezone を付加せず naive `datetime` として扱います。

---

## 24. EDINET Inventory Summary

```python
OneDayInventorySummary
```

Field:

```text
total_count
listed_match_count
csv_flag_count
doc_type_counts
```

集計順序:

```text
全 results
    ↓
現在上場 secCode と一致
    ↓
csvFlag == "1"
    ↓
docTypeCode 集計
```

---

## 25. 10年間の対象期間

対象期間は、実行日時点から過去10年間の**提出日ベース**です。

開始日計算:

```python
inventory_start_date(end_date)
```

2月29日は存在しない年を考慮し 2月28日に補正します。

---

## 26. 複数日 / 10年走査の設計方針

現在の `refresh_one_day()` を基本単位とします。

次の実装予定:

```python
refresh_date_range(
    db: Session,
    start_date: date,
    end_date: date,
)
```

方針:

- まだ未実装
- いきなり10年走査しない
- まず3日程度で確認
- 並列化しない
- 1日単位 commit を維持
- Current Listed Code List は範囲処理ごとに1回取得する方向
- Retry / Rate Limit / 失敗継続は次段階で設計

---

## 27. EDINET Test

主な Test:

```text
backend/tests/test_edinet_client.py
backend/tests/test_edinet_inventory.py
```

`tests/test_edinet_inventory.py` は現在 7 tests pass を確認済みです。

主な確認内容:

- 10年前の日付
- 2月29日
- 上場企業 Filter
- csvFlag Filter
- completed 済みでも再実行
- 英字入り証券コード `130A0`
- `submitDateTime` が naive datetime
- rollback / failed / re-raise
- 秘密情報を error_message に保存しない
- 不正な `results` Response を拒否
- 不正 Response で既存 Documents を削除しない

---

## 28. EDINET 実データ確認

対象確認日:

```text
2026-08-21
```

1日分の実 DB 保存まで確認済みです。

同じ `target_date` を再実行し、

- `edinet_documents` が2倍に増えない
- 1日分が削除 → 再登録で刷新される
- `edinet_inventory_runs` が同日で増殖せず1行を更新
- `status = completed`
- `error_message = NULL`

を確認済みです。

---

## 29. EDINET 現在未実装

```text
複数日 refresh_date_range
10年一括走査
失敗日を飛ばして継続
Retry
Rate Limit 制御 / Sleep
Scheduler
Celery
Redis
EDINET API Router
EDINET Frontend
CSV ZIP 本体取得
CSV ZIP 展開
CSV解析
XBRL解析
財務数値抽出
決算短信取得
TDnet連携
```

必要性が明確になる前に新しい Infrastructure を追加しません。

---

## 30. Frontend 技術構成

```text
frontend/
├─ Dockerfile
├─ package.json
└─ src/
   ├─ api/
   ├─ components/
   ├─ layouts/
   ├─ pages/
   ├─ routes/
   ├─ types/
   ├─ App.tsx
   ├─ main.tsx
   └─ index.css
```

主な技術:

- React
- TypeScript
- Vite
- React Router
- Axios
- Bootstrap

EDINET Frontend はまだ実装していません。

---

## 31. Frontend Route

| URL | Page |
|---|---|
| `/` | HomePage |
| `/users` | UserListPage |
| `/users/new` | UserCreatePage |
| `/users/:userId` | UserDetailPage |
| `/users/:userId/edit` | UserEditPage |
| `*` | NotFoundPage |

---

## 32. UI / CSS 方針

Bootstrap を基本とします。

```text
1. Bootstrap Component
2. Bootstrap Grid
3. Bootstrap Utility
4. 共通 React Component
5. 必要な場合のみ独自 CSS
```

---

## 33. Build / Test

Backend 全体:

```powershell
docker compose run --rm backend pytest -v
```

EDINET Client:

```powershell
docker compose run --rm backend pytest -v tests/test_edinet_client.py
```

EDINET Inventory:

```powershell
docker compose run --rm backend pytest -v tests/test_edinet_inventory.py
```

Frontend lint:

```powershell
docker compose exec frontend npm run lint
```

Frontend build:

```powershell
docker compose exec frontend npm run build
```

---

## 34. TablePlus

Docker PostgreSQL の確認には TablePlus を利用します。

```text
Host: 127.0.0.1
Port: 5432
Database: bizsc
User: bizsc
```

接続不良時は Windows 側 PostgreSQL Service が `5432` に混在していないかも確認します。

---

## 35. Documentation

主な Document:

```text
architecture.md
handover_phase.md
project-overview.md
development-guidelines.md
EDINET Phase Documents
```

`architecture.md` は現在構成と設計原則、
`handover_phase.md` は具体的進捗と次の作業を担当します。

---

## 36. Git / GitHub 方針

Repository:

```text
https://github.com/eswm223-oss/bizsc
```

基本方針:

- 現在コードを推測しない
- 必要時は GitHub 最新状態を確認
- 小さな変更ごとに Commit / Push を強制しない
- 機能単位・区切りの良い地点で Commit
- `.env` / API Key は Commit しない
- Migration は Git 管理する

---

## 37. 開発進行ルール

```text
大きな機能
↓
Phase
↓
Step
↓
実装
↓
Test
↓
確認
↓
次Step
```

重要:

- 1 Step を小さくする
- 既存 Code を確認してから変更
- 必要性がない Library を追加しない
- Error 原因を推測だけで確定しない
- 実データは小範囲で確認してから拡大
- 外部 API 負荷を意識
- Migration は内容確認後に適用
- Repository / Service / Client の責務を混在させない
- 新 Chat 移行時は Handover Document を作成

---

## 38. Current Architecture Status

2026-09-06 時点:

```text
Base Web Application
        ↓
User CRUD
        ↓
EDINET API Client
        ↓
EDINET Code List
        ↓
現在上場企業判定
        ↓
1日棚卸し
        ↓
EDINET DB Models
        ↓
Alembic Migration
        ↓
EDINET Repository
        ↓
EdinetInventoryService.refresh_one_day
        ↓
実DB保存
        ↓
同日再実行 / Refresh確認
        ↓
完了
```

EDINET Phase 02 は、**1日単位の安全な棚卸し・DB Refresh まで完了**しています。

次の予定は:

```text
refresh_date_range
```

による複数日順次処理です。

Step 7-1 の実装指示は整理済みですが、
この architecture.md 作成時点では未実装です。

---

## 39. Architecture 基本原則まとめ

```text
Docker Compose を開発環境の基準にする

Backend:
API
↓
Service
↓
Repository
↓
Model
↓
PostgreSQL

External API:
Service
↓
Client
↓
External Service

Client と Repository を混在させない

Business Logic は Service に置く

Transaction 境界は Service で管理する

DB Schema は Alembic で管理する

API Key 等の秘密情報を Source / Log / Error に出さない

証券コードは str として扱う

EDINET submitDateTime に存在しない timezone を推測しない

completed でも EDINET 1日棚卸しを再実行可能にする

日単位 Refresh は
DELETE + INSERT + completed
を1 Transaction とする

外部 API 異常を「0件」と誤認して既存データを削除しない

大量処理はいきなり全量実行しない

まず小期間で実データ検証し、
安全性を確認してから10年へ拡大する

必要性が明確になるまで
Scheduler / Celery / Redis / 新しい Framework を導入しない

既存動作を壊さず、小さな Step で進める
```

以上。
