# BizSC Project Overview

更新日: 2026-09-06

## 1. Project Name

```text
BizSC
```

---

## 2. Project Purpose

BizSC は、企業情報・財務情報・業務データを段階的に取り込み、
Web Application 上で確認・分析できる基盤を作ることを目的とした個人開発 Project です。

現在はまず、

```text
User 管理機能
EDINET データ取得
EDINET 書類棚卸し
```

を中心に基盤を構築しています。

将来的には、取得した企業開示情報や財務データを利用して、
企業比較・分析・検索・可視化などへ拡張することを想定しています。

---

## 3. Development Environment

Main Environment:

```text
OS: Windows
Workspace:
D:\Development\apps\bizsc
```

Tools:

- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus
- ChatGPT

GitHub Repository:

```text
https://github.com/eswm223-oss/bizsc
```

---

## 4. Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- psycopg
- Alembic
- Pydantic
- pydantic-settings
- pytest
- httpx

### Frontend

- React
- TypeScript
- Vite
- React Router
- Axios
- Bootstrap

### Infrastructure / Tooling

- Docker Desktop
- Docker Compose
- GitHub Desktop
- TablePlus
- Cursor

---

## 5. Docker Compose Structure

BizSC は基本的に以下の 3 Service で開発します。

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

Database:

```text
PostgreSQL 17
Database: bizsc
User: bizsc
```

---

## 6. Overall Architecture

Backend の基本構造:

```text
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

外部 API:

```text
Service
   ↓
Client
   ↓
External API
```

重要:

```text
Client
≠
Repository
```

- Client は外部 API 通信
- Repository は DB Access
- Service は Business Logic と Transaction 管理

を担当します。

---

## 7. Current Domains

現在の主要 Domain:

```text
User
EDINET
```

---

## 8. User Domain

User Domain は CRUD まで実装済みです。

Table:

```text
users
```

主な Field:

```text
id
email
hashed_password
is_active
created_at
updated_at
```

API:

```text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

User List では以下に対応済みです。

- Search
- Active / Inactive Filter
- Sort
- Pagination
- Total Count
- Loading
- Error
- Empty State

---

## 9. Frontend Current Status

主な Page:

```text
HomePage
UserListPage
UserCreatePage
UserDetailPage
UserEditPage
NotFoundPage
```

Route:

```text
/
 /users
 /users/new
 /users/:userId
 /users/:userId/edit
 *
```

UI は Bootstrap を基本としています。

---

## 10. EDINET Feature Overview

BizSC では現在、EDINET API から企業開示データを取得する機能を実装しています。

最終的な現在方針:

```text
現在上場している企業
        ×
現在日から過去10年間
        ×
提出日ベース
        ×
csvFlag == "1"
```

に一致する書類を棚卸しし、
BizSC の PostgreSQL に保存する。

---

## 11. EDINET Phase 01

完了済み。

内容:

```text
EDINET API Key 設定
↓
EDINET API v2 接続
↓
指定日の書類一覧取得
```

Client:

```text
backend/app/clients/edinet.py
```

主要関数:

```python
fetch_document_list(target_date: date)
```

---

## 12. Current Listed Company Detection

EDINET Code List から現在上場企業の証券コードを取得します。

主要関数:

```python
fetch_listed_sec_codes() -> set[str]
```

判定:

```text
上場区分 == "上場"
AND
証券コード != 空
```

証券コードは必ず文字列として扱います。

例:

```text
13010
130A0
137A0
```

英字入りコードが存在するため、
数値変換しません。

---

## 13. EDINET Inventory Target

対象書類:

```text
現在上場企業
AND
csvFlag == "1"
```

`docTypeCode` は事前に限定しません。

理由:

```text
まず全対象を棚卸し
↓
docTypeCode 別件数確認
↓
必要な書類種別を後から判断
```

とするためです。

---

## 14. EDINET Database Tables

現在、以下の 2 Table を実装済みです。

```text
edinet_documents
edinet_inventory_runs
```

---

## 15. edinet_documents

目的:

```text
対象となる EDINET Document の保存
```

主な Column:

```text
id
target_date
doc_id
edinet_code
sec_code
filer_name
ordinance_code
form_code
doc_type_code
period_start
period_end
submit_date_time
doc_description
parent_doc_id
withdrawal_status
doc_info_edit_status
disclosure_status
xbrl_flag
pdf_flag
csv_flag
legal_status
created_at
updated_at
```

重要:

```text
doc_id
→ Unique
```

`submit_date_time` は EDINET 元データに timezone がないため、

```python
DateTime(timezone=False)
```

として保存します。

---

## 16. edinet_inventory_runs

目的:

```text
target_date ごとの棚卸し実行状態管理
```

主な Column:

```text
target_date
status
total_count
listed_match_count
csv_flag_count
listed_sec_code_count
error_message
started_at
completed_at
created_at
updated_at
```

Status:

```text
processing
completed
failed
```

`target_date` は Unique。

---

## 17. EDINET Repository

Repository:

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

重要:

```text
Repository 内では commit しない
```

Transaction は Service が管理します。

---

## 18. EDINET Service

Service:

```text
backend/app/services/edinet_inventory.py
```

Class:

```python
EdinetInventoryService
```

現在の主要 Method:

```python
refresh_one_day(
    db: Session,
    target_date: date,
) -> OneDayInventorySummary
```

---

## 19. One Day Refresh Flow

現在の処理:

```text
run取得
↓
processing
↓
commit
↓
現在上場証券コード取得
↓
EDINET書類一覧取得
↓
Response検証
↓
現在上場企業 Filter
↓
csvFlag == "1"
↓
EdinetDocument変換
↓
既存 target_date 削除
↓
新データ追加
↓
run completed
↓
commit
```

---

## 20. Refresh Policy

以下すべて再実行可能です。

```text
completed
failed
processing
```

`completed` だから Skip はしません。

理由:

- 誤った completed を固定化しない
- EDINET 側の後日修正に対応
- 手動 Refresh を可能にする

---

## 21. Transaction Policy

Refresh 本体:

```text
DELETE
↓
INSERT
↓
run completed
↓
commit
```

は 1 Transaction。

途中で失敗:

```text
rollback
↓
以前の正常データを保持
↓
run failed
```

とします。

---

## 22. EDINET Response Safety

以下の場合は Exception:

```text
payload が dict でない
results がない
results が list でない
```

正常な:

```python
"results": []
```

は 0 件として扱います。

これにより、

```text
EDINET異常
↓
0件と誤認
↓
既存データ全削除
```

を防ぎます。

---

## 23. EDINET Tests

主な Test:

```text
backend/tests/test_edinet_client.py
backend/tests/test_edinet_inventory.py
```

現在:

```text
tests/test_edinet_inventory.py
7 passed
```

確認済み:

- 10年前の日付
- 2月29日
- Current Listed Filter
- csvFlag Filter
- completed 再実行
- 英字入り secCode
- naive submitDateTime
- rollback
- failed
- Error re-raise
- Secret 非保存
- Invalid Response Protection

---

## 24. Real Data Verification

実 EDINET Data を使用して確認済み。

確認日:

```text
2026-08-21
```

確認済み:

```text
EDINET API
↓
対象 Filter
↓
edinet_documents 登録
↓
edinet_inventory_runs completed
```

同日再実行も確認済み。

結果:

```text
重複増加なし
1日分 Refresh 成功
run は1行更新
status = completed
error_message = NULL
```

---

## 25. Three Day Inventory Research

実測済み:

```text
2026-08-19
total=203
listed=42
csv=28

2026-08-20
total=313
listed=38
csv=29

2026-08-21
total=226
listed=51
csv=39
```

合計:

```text
days=3
total=742
listed=131
csv=96
```

この確認では 429 / API Error は発生しませんでした。

---

## 26. Current EDINET Progress

現在:

```text
EDINET API接続
↓
完了

Current Listed Company取得
↓
完了

1日棚卸し
↓
完了

DB Table
↓
完了

Migration
↓
完了

Repository
↓
完了

1日Refresh Service
↓
完了

Unit Test
↓
完了

実DB保存
↓
完了

同日再実行
↓
完了
```

---

## 27. Next Step

次は:

```text
Step 7-1
refresh_date_range
```

を実装する。

予定 Method:

```python
refresh_date_range(
    db: Session,
    start_date: date,
    end_date: date,
) -> list[tuple[date, OneDayInventorySummary]]
```

---

## 28. refresh_date_range Planned Design

予定:

```text
start_date
↓
1日ずつ順番
↓
end_date
```

Current Listed Code List:

```text
1回の範囲処理につき1回だけ取得
```

各日:

```text
processing
↓
document list
↓
filter
↓
refresh
↓
completed
↓
commit
```

各日は独立して commit。

---

## 29. Initial Range Test Plan

いきなり10年分は実行しません。

まず:

```text
2026-08-19
2026-08-20
2026-08-21
```

の 3日で実 DB 確認予定。

確認項目:

- 3日分保存
- 各 run completed
- Documents 重複なし
- 日別件数
- Error 無し

---

## 30. Future 10-Year Scan

3日確認後に、10年実行向けの設計を行います。

検討項目:

```text
Retry
Rate Limit
Sleep
失敗日の継続
途中再開
Progress
長時間実行
実行単位
```

ただし、

```text
completed なら永久に Skip
```

という設計には現時点ではしません。

---

## 31. Future EDINET Phases

今後候補:

```text
複数日棚卸し
10年棚卸し
CSV ZIP Download
ZIP展開
CSV解析
財務数値抽出
XBRL解析
企業別財務データCache
企業検索
企業比較
チャート表示
分析画面
```

---

## 32. Currently Not Implemented

```text
refresh_date_range
10年全量走査
Retry
Rate Limit 制御
失敗継続
Scheduler
Celery
Redis
EDINET Router
EDINET Frontend
CSV ZIP Download
CSV Parse
XBRL Parse
Financial Analysis
決算短信取得
TDnet連携
```

---

## 33. Development Policy

BizSC では以下を基本とします。

```text
小さい Step
↓
実装
↓
Test
↓
確認
↓
次へ
```

重要:

- 既存コードを確認してから変更
- 不要な Library を追加しない
- Error 原因を推測で確定しない
- 外部 API は小期間から検証
- DB Migration は内容確認後に適用
- Client / Service / Repository の責務を分離
- API Key を Git / Log / Error へ出さない
- Commit / Push は区切りの良い地点
- 新 Chat 移行時は handover を更新

---

## 34. Documentation

主な資料:

```text
architecture.md
handover_phase.md
project-overview.md
```

役割:

### architecture.md

```text
現在の構成
責務分離
設計原則
```

### handover_phase.md

```text
具体的な進捗
直近の作業
次 Step
```

### project-overview.md

```text
Project 全体像
目的
現在の到達地点
今後の方向
```

---

## 35. Current Project Status Summary

2026-09-06 時点:

```text
BizSC
│
├─ Web Application 基盤
│  └─ 完了
│
├─ User CRUD
│  └─ 完了
│
├─ Frontend User UI
│  └─ 完了
│
└─ EDINET
   ├─ API Client
   │  └─ 完了
   │
   ├─ Current Listed Company 判定
   │  └─ 完了
   │
   ├─ 1日棚卸し
   │  └─ 完了
   │
   ├─ DB Model / Migration
   │  └─ 完了
   │
   ├─ Repository
   │  └─ 完了
   │
   ├─ 1日 Refresh Service
   │  └─ 完了
   │
   ├─ 実 DB 保存
   │  └─ 完了
   │
   ├─ 同日再実行確認
   │  └─ 完了
   │
   └─ 複数日 Refresh
      └─ 次 Step
```

---

## 36. Next Chat Starting Point

次 Chat では、

```text
architecture.md
handover_phase.md
project-overview.md
```

を基準にする。

作業再開地点:

```text
EDINET Phase 02
Step 7-1
refresh_date_range
```

Step 6-6 までは完了済みなので、
1日 Refresh 設計からやり直さない。

以上。
