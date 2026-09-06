# BizSC Architecture

## 1. このドキュメントの目的

このドキュメントは、BizSC の**現在のシステム構成・責務分離・実装ルールを確認するための基準資料**です。

過去にどの Phase で何を実装したかを詳細に記録することを目的とはしません。

今後 BizSC に新しい業務機能を追加する際は、この構成を基準として既存設計との整合性を確認します。

---

## 2. プロジェクト概要

**プロジェクト名:** BizSC

BizSC は、今後さまざまな業務機能を段階的に追加できる Web アプリケーション基盤として構成されています。

現時点では、主に以下が実装されています。

- Docker Compose による開発環境
- FastAPI Backend
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Migration
- React + TypeScript Frontend
- React Router
- Axios
- Bootstrap
- User CRUD
- User 一覧検索
- Active / Inactive Filter
- Sort
- Pagination
- Loading / Error / Empty 表示
- Backend pytest
- Frontend lint / build
- 外部 API Client 層
- EDINET API Version 2 接続
- EDINET 書類一覧取得 Client

今後追加する業務機能については、必要なものを小さな Phase に分けて設計・実装します。

---

## 3. 全体アーキテクチャ

通常の BizSC Web API 処理は以下の構造です。

```text
Browser
  │
  │  http://localhost:5173
  ▼
React / TypeScript / Vite
  │
  │  Axios
  │  http://localhost:8000
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

外部サービスとの通信は、DB Repository とは分離します。

```text
BizSC Backend
   │
   ▼
Client
   │
   ▼
External API
```

現在の例:

```text
BizSC Backend
   │
   ▼
EDINET Client
   │
   ▼
EDINET API Version 2
```

Docker Compose 上では、以下の 3 Service を利用します。

```text
frontend
backend
db
```

EDINET 用の追加 Docker Service は使用していません。

---

## 4. プロジェクトルート構成

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

主な役割は以下です。

| Path | 役割 |
|---|---|
| `backend/` | FastAPI Backend |
| `frontend/` | React Frontend |
| `docs/` | 設計・引継ぎ・機能指示資料 |
| `compose.yaml` | Docker Compose 構成 |
| `README.md` | Project の基本説明 |

---

## 5. Docker Compose 構成

### backend

```text
Service: backend
Container: bizsc-backend
Port: 8000
Volume: ./backend:/app
```

Backend のソースコードは Volume Mount されています。

通常の Python コード変更だけで毎回 Docker Image を Build する必要はありません。

---

### frontend

```text
Service: frontend
Container: bizsc-frontend
Port: 5173
Volume:
  ./frontend:/app
  /app/node_modules
```

Frontend もソースコードを Volume Mount しています。

`node_modules` は Container 側で管理します。

---

### db

```text
Service: db
Container: bizsc-db
Image: postgres:17
Port: 5432
Database: bizsc
User: bizsc
Volume: postgres-data
```

PostgreSQL のデータは Docker Volume に保持されます。

---

## 6. Backend 技術構成

Backend の主な技術は以下です。

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- psycopg
- Alembic
- Pydantic / pydantic-settings
- email-validator
- pwdlib / Argon2
- pytest
- httpx

Backend の基本構成は次のとおりです。

```text
backend/
├─ Dockerfile
├─ requirements.txt
├─ alembic.ini
├─ alembic/
├─ app/
│  ├─ api/
│  ├─ clients/
│  │  ├─ __init__.py
│  │  └─ edinet.py
│  ├─ core/
│  ├─ db/
│  ├─ models/
│  ├─ repositories/
│  ├─ schemas/
│  ├─ services/
│  └─ main.py
└─ tests/
```

---

## 7. Backend レイヤー構成

BizSC Backend は責務を分離して実装します。

DB を利用する通常の業務処理:

```text
API Router
   ↓
Service
   ↓
Repository
   ↓
Model
   ↓
Database
```

外部 API 通信:

```text
Service または必要な呼び出し元
   ↓
Client
   ↓
External API
```

Client は Repository の代替ではありません。

- Repository: PostgreSQL / SQLAlchemy を使う DB Access
- Client: EDINET など外部サービスとの通信

として責務を明確に分離します。

### 7.1 api

HTTP Request / Response を担当します。

主な責務:

- URL 定義
- HTTP Method 定義
- Query Parameter
- Path Parameter
- Request Schema
- Response Schema
- Dependency Injection
- Service 呼び出し

API 層に DB 操作や複雑な業務ロジックを直接書かない方針とします。

---

### 7.2 services

Application / Business Logic を担当します。

主な責務:

- Repository の呼び出し
- Client の呼び出しが必要な業務処理の組み立て
- CRUD 処理の組み立て
- 入力値に応じた判断
- 重複チェック
- Not Found 判定
- Password Hash 化など、Repository より上位の処理

Service は HTTP や具体的な DB 実装へ依存しすぎないようにします。

---

### 7.3 repositories

Database Access を担当します。

主な責務:

- `select`
- `insert`
- `update`
- `delete`
- filter
- sort
- pagination
- count

SQLAlchemy を使用した DB 操作を Repository に集約します。

外部 HTTP API との通信は Repository に置きません。

---

### 7.4 models

SQLAlchemy Model を定義します。

DB Table の構造を表します。

Model を変更しただけでは、既存 Database の Schema は自動的には変更しません。

DB Schema の変更には Alembic Migration を利用します。

---

### 7.5 schemas

Pydantic Schema を管理します。

主な用途:

- API Request
- API Response
- Validation
- Create 用 Schema
- Update 用 Schema
- List Response

DB Model と API Schema は別の責務として扱います。

外部 API のレスポンスを必ず即座に Pydantic 化する必要はありません。
実データ構造を確認してから必要性を判断します。

---

### 7.6 db

Database 接続関連を管理します。

主な対象:

- SQLAlchemy Base
- Engine
- Session
- `get_db`

FastAPI の Dependency Injection を利用して DB Session を API に渡します。

---

### 7.7 core

Application 全体で利用する共通設定を管理します。

現在の構成には、主に次の責務があります。

- Application Settings
- Database Settings
- External API Settings
- Exception Handler
- Security

EDINET API Key は `Settings` で管理します。

```python
edinet_api_key: Optional[str] = None
```

環境変数名:

```text
EDINET_API_KEY
```

API Key をソースコードへ直接記述しません。

`.env` および `.env.*` は Git 管理対象外です。

---

### 7.8 clients

外部サービスとの HTTP 通信を担当します。

現在:

```text
backend/app/clients/
├─ __init__.py
└─ edinet.py
```

Client の基本責務:

- 外部 API Endpoint 管理
- Request Parameter / Header 等の構築
- HTTP 通信
- Timeout
- 外部 API の HTTP Error 処理
- 外部 API Response の取得
- 秘密情報を漏らさない例外処理

Client に以下を混在させません。

- PostgreSQL 保存
- SQLAlchemy Query
- Alembic Migration
- UI 処理
- 複雑な Business Logic

---

### 7.9 tests

pytest による Backend Test を配置します。

機能追加時は、必要に応じて以下を確認します。

- 正常系
- Validation
- Not Found
- Conflict
- Filter
- Sort
- Pagination
- CRUD
- 外部 API Request Parameter
- 外部 API Error
- API Key 等の秘密情報漏えい防止

外部 API Client の単体テストでは、
可能な限り実 API へアクセスせずモックを利用します。

---

## 8. FastAPI Entry Point

Backend の Entry Point は以下です。

```text
backend/app/main.py
```

主な役割:

- `FastAPI()` の生成
- CORS Middleware
- Exception Handler 登録
- Router 登録
- Root Endpoint
- Health Check

Frontend は `http://localhost:5173`、
Backend は `http://localhost:8000` で動作します。

---

## 9. 現在の User Domain

現在 BizSC で実装されている主要 DB Domain は `User` です。

### users Table

```text
users
├─ id
├─ email
├─ hashed_password
├─ is_active
├─ created_at
└─ updated_at
```

### Column 概要

| Column | 概要 |
|---|---|
| `id` | Primary Key |
| `email` | Unique / Index |
| `hashed_password` | Hash 化した Password |
| `is_active` | User の有効 / 無効 |
| `created_at` | 作成日時 |
| `updated_at` | 更新日時 |

Password の平文を DB に保存しません。

---

## 10. 現在の User API

Base Path:

```text
/users
```

### Create

```http
POST /users
```

成功時:

```text
201 Created
```

### List

```http
GET /users
```

Query Parameter:

```text
search
is_active
sort_by
sort_order
page
limit
```

一覧 API は User 配列に加えて `total` を返します。

### Detail

```http
GET /users/{user_id}
```

### Update

```http
PATCH /users/{user_id}
```

### Delete

```http
DELETE /users/{user_id}
```

成功時:

```text
204 No Content
```

---

## 11. EDINET External Data Domain

BizSC では現在、外部データ取得機能として EDINET 対応を開始しています。

EDINET は現時点では DB Domain ではありません。

つまり現在は、

```text
EDINET API
   ↓
EDINET Client
   ↓
JSON取得
```

までであり、

```text
EDINET Model
EDINET Repository
EDINET DB Table
Frontend EDINET画面
```

はまだ実装していません。

---

## 12. EDINET API Client

実装ファイル:

```text
backend/app/clients/edinet.py
```

公開:

```text
backend/app/clients/__init__.py
```

現在の主要関数:

```python
fetch_document_list(target_date: date)
```

目的:

> 指定日の EDINET 提出書類一覧及びメタデータを取得する。

使用 API:

```text
EDINET API Version 2
GET https://api.edinet-fsa.go.jp/api/v2/documents.json
```

Request:

```text
date=<YYYY-MM-DD>
type=2
Subscription-Key=<EDINET_API_KEY>
```

HTTP Client:

```text
httpx
```

Timeout:

```text
30秒
```

現在は自動リトライを実装していません。

---

## 13. EDINET Client Error 方針

現在、EDINET Client では主に以下の Error を分離しています。

```text
EdinetClientError
EdinetApiKeyNotConfiguredError
EdinetHttpError
EdinetTimeoutError
EdinetInvalidJsonError
```

主な考え方:

- API Key 未設定を明確にする
- HTTP Status を呼び出し元で確認可能にする
- Timeout を区別する
- JSON でない Response を区別する
- httpx の Request URL をそのまま Error Message に出さない
- `Subscription-Key` を含む URL をログへ出さない

EDINET API Key は Query Parameter に含まれるため、
例外・ログに Request URL をそのまま表示しないことを特に重視します。

---

## 14. EDINET Client Test

現在:

```text
backend/tests/test_edinet_client.py
```

を配置しています。

実 API へアクセスしないテストで、主に以下を確認します。

- 指定日が `YYYY-MM-DD` で送信される
- `type=2`
- `Subscription-Key`
- API Key 未設定
- HTTP Error
- 429 時に自動リトライしない
- Timeout
- Invalid JSON
- API Key を例外 Message に含めない

EDINET の実 API 接続確認は単体テストとは分離して行います。

---

## 15. EDINET 現在の実装範囲

現在完了している範囲:

```text
EDINET API Key 設定
        ↓
EDINET Client
        ↓
書類一覧API
        ↓
指定日のJSON取得
```

実接続確認では、指定日の書類一覧取得が成功しています。

現在まだ実装していないもの:

```text
現在上場企業の棚卸し
過去10年分の書類一覧走査
CSV ZIPダウンロード
ZIP展開
CSV解析
XBRL解析
財務数値抽出
DBキャッシュ
SQLAlchemy Model
Alembic Migration
EDINET Repository
EDINET Service
EDINET Router
Frontend
定期取得
```

これらは必要な Phase ごとに順番に設計します。

---

## 16. EDINET 今後の設計方針

現在確定している対象方針:

```text
対象企業:
現在上場している企業

上場判定:
現在時点の証券コードを基準

対象期間:
実行日の現在日から過去10年間
提出日ベース

書類対象:
docTypeCode を事前限定しない

CSV対象:
csvFlag == "1"
```

まず CSV 本体を大量取得せず、

```text
現在上場企業
        ↓
過去10年のEDINET書類一覧
        ↓
csvFlag = 1
        ↓
docTypeCode別に棚卸し
```

を行います。

棚卸し完了後に CSV ダウンロード Phase を別途設計します。

---

## 17. EDINET データ取得時のアクセス方針

長期間の EDINET API 走査では API への負荷を抑えます。

基本方針:

- いきなり10年間を一括実行しない
- 小期間で先に動作確認する
- 大量並列アクセスを行わない
- 429 Too Many Requests を無限リトライしない
- API Key をログへ出さない
- 長時間処理では途中再開方法を先に設計する
- CSV取得前に対象件数を棚卸しする

外部 API の利用規約・仕様に合わせ、
アクセス方法は必要に応じて見直します。

---

## 18. Frontend 技術構成

Frontend の主な技術は以下です。

- React
- TypeScript
- Vite
- React Router
- Axios
- Bootstrap

基本構成:

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

---

## 19. Frontend 各 Directory の責務

### pages

URL 単位の Page Component を配置します。

現在の主要 Page:

```text
HomePage
UserListPage
UserCreatePage
UserDetailPage
UserEditPage
NotFoundPage
```

### components

複数画面で利用できる共通 UI を配置します。

主な共通 Component:

```text
Button
Input
Card
Badge
Loading
ErrorMessage
UserForm
Header
Sidebar
Footer
```

### api

Backend API との通信処理を配置します。

Axios を利用します。

### types

Frontend で利用する TypeScript Type を管理します。

### layouts

複数 Page 共通の画面構造を管理します。

### routes

React Router による URL と Page の対応を管理します。

---

## 20. Frontend Route

現在の主な Route:

| URL | Page |
|---|---|
| `/` | HomePage |
| `/users` | UserListPage |
| `/users/new` | UserCreatePage |
| `/users/:userId` | UserDetailPage |
| `/users/:userId/edit` | UserEditPage |
| `*` | NotFoundPage |

EDINET 用 Frontend Route は現在ありません。

---

## 21. UI / CSS 方針

BizSC の UI は Bootstrap を基本とします。

優先順位:

```text
1. Bootstrap 標準 Component / Class
2. Bootstrap Grid
3. Bootstrap Utility
4. 共通 React Component
5. 必要な場合のみ独自 CSS
```

独自 CSS を大量に作ることは避けます。

---

## 22. Frontend State の基本方針

現時点では React 標準の State 管理を利用します。

主に:

```text
useState
useEffect
```

大規模な Global State Library は導入していません。

理由なく Redux 等を追加しません。

---

## 23. Frontend と Backend のデータフロー

User 一覧を例にすると、

```text
UserListPage
   ↓
frontend/src/api
   ↓ Axios
GET /users
   ↓
FastAPI Router
   ↓
UserService
   ↓
UserRepository
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

EDINET は現時点でこの API / Frontend Flow には接続していません。

現在:

```text
Backend
   ↓
EDINET Client
   ↓
EDINET API
```

までです。

---

## 24. Database Migration 方針

Database Schema の変更には Alembic を利用します。

基本:

```text
SQLAlchemy Model 変更
       ↓
Alembic Migration 作成
       ↓
Migration 内容確認
       ↓
Database へ適用
```

EDINET データを将来 DB キャッシュする場合も、
Table 構造を設計した後に Alembic Migration を作成します。

EDINET Client を追加しただけでは DB Schema を変更しません。

---

## 25. 新しい Domain を追加するときの基本構成

例として `Customer` を追加する場合:

```text
backend/app/models/customer.py
backend/app/schemas/customer.py
backend/app/repositories/customer.py
backend/app/services/customer.py
backend/app/api/customers.py
backend/tests/...
```

外部サービス通信が必要な場合は、必要に応じて:

```text
backend/app/clients/<external_service>.py
```

を検討します。

ただし、すべての Domain に必ず同じ数の File を作る必要はありません。

---

## 26. 新機能追加時の設計原則

### 外部 API と通信するか

必要な場合:

- Client

を検討します。

### DB に保存するデータか

保存する場合:

- Model
- Migration

を検討します。

### API Request / Response が必要か

必要な場合:

- Schema
- API Router

を検討します。

### DB Access が必要か

必要な場合:

- Repository

へ配置します。

### 業務判断が必要か

必要な場合:

- Service

へ配置します。

### URL 単位の画面か

必要な場合:

- Page
- Route

を検討します。

### 複数画面で再利用する UI か

該当する場合:

- Component

へ分離します。

---

## 27. 既存アーキテクチャを変更する場合の注意

次の変更は影響範囲が大きいため、
局所的な変更と同じ感覚で実施しません。

- Backend Layer 構成変更
- Client 層の責務変更
- API Base Path 変更
- DB Connection 方針変更
- ORM 変更
- Authentication 基盤導入
- Global State Library 導入
- React Router 構成変更
- Bootstrap 以外の UI Framework 導入
- Docker Service 構成変更

必要性と影響範囲を整理してから変更します。

---

## 28. Build / Test

### Frontend lint

```powershell
docker compose exec frontend npm run lint
```

### Frontend build

```powershell
docker compose exec frontend npm run build
```

### Backend test

```powershell
docker compose run --rm backend pytest -v
```

### EDINET Client test

```powershell
docker compose run --rm backend pytest -v tests/test_edinet_client.py
```

変更内容に応じて必要な確認を行います。

---

## 29. Docker の基本コマンド

起動:

```powershell
docker compose up -d
```

状態確認:

```powershell
docker compose ps
```

Backend Container で Command 実行:

```powershell
docker compose exec backend <command>
```

Frontend Container で Command 実行:

```powershell
docker compose exec frontend <command>
```

Dependency や Dockerfile を変更していない通常の Source Code 修正では、
原則として毎回 `docker compose build` は行いません。

---

## 30. Documentation 構成

BizSC の Documentation は `docs/` で管理します。

主な資料:

```text
architecture.md
development-guidelines.md
project-overview/
handover_phase/
```

EDINET 機能では Phase ごとの指示書も利用します。

例:

```text
01-edinet-api-fetch.md
02-edinet-document-inventory.md
handover_edinet_phase.md
```

### architecture.md

現在のシステム構成と設計原則。

### development-guidelines.md

開発を進める際の共通ルール。

### handover 系資料

別 Chat へ作業を引き継ぐ際の、
その時点の具体的な進捗と次の作業。

### 機能 Phase md

特定機能を小さな Step に分けて実装するための指示書。

---

## 31. Git / GitHub 方針

コード確認が必要な場合は、
現在のコードを推測せず最新状態を確認します。

Repository:

```text
https://github.com/eswm223-oss/bizsc
```

Commit / Push は、小さな変更のたびではなく、
機能単位または区切りのよい地点で行います。

API Key や `.env` を Git へ Commit しません。

---

## 32. Current Architecture Status

この architecture.md 作成時点では、

```text
Web Application 基盤
User 管理機能
External API Client 層
EDINET API Client
EDINET 書類一覧取得
```

まで構築されています。

EDINET については現在、

```text
Phase 01:
EDINET API 接続・書類一覧取得
→ 完了

Phase 02:
現在上場企業 × 過去10年 × csvFlag=1
書類棚卸し
→ 次に実施
```

の状態です。

まだ EDINET データを PostgreSQL へ保存する設計には進んでいません。

---

## 33. Architecture の基本方針まとめ

BizSC の基本方針:

```text
Docker Compose で開発環境を統一する

Backend のDB処理は
API
↓
Service
↓
Repository
↓
Model
↓
PostgreSQL
で責務を分離する

外部APIとの通信は
Client
に分離する

Repository に外部HTTP通信を混在させない

Database Schema は Alembic で管理する

Frontend は
pages
components
api
types
layouts
routes
に責務を分離する

API 通信は Axios に集約する

UI は Bootstrap を基本とする

秘密情報は .env で管理する

既存動作を壊さず小さな単位で変更する

新しい Library や Architecture は
具体的な必要性が出た場合にのみ導入する

大量データ・外部API処理は
いきなり全量実行せず
小さい範囲で検証してから拡大する
```

以上。
