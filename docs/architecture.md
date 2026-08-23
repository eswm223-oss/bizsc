# BizSC Architecture

## 1. このドキュメントの目的

このドキュメントは、BizSC の**現在のシステム構成・責務分離・実装ルールを確認するための基準資料**です。

過去にどの Phase で何を実装したかを記録することを目的とはしません。

今後 BizSC に新しい業務機能を追加する際は、この構成を基準として既存設計との整合性を確認します。

---

## 2. プロジェクト概要

**プロジェクト名:** BizSC

BizSC は、今後さまざまな業務機能を段階的に追加できる Web アプリケーション基盤として構成されています。

現時点では、以下の基礎構成が実装されています。

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

今後追加する業務機能については未確定であり、この architecture.md では仕様を固定しません。

---

## 3. 全体アーキテクチャ

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

Docker Compose 上では、以下の 3 Service を利用します。

```text
frontend
backend
db
```

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
| `docs/` | 設計・引継ぎ資料 |
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

BizSC Backend は、責務を分離して実装します。

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
- CRUD 処理の組み立て
- 入力値に応じた判断
- 重複チェック
- Not Found 判定
- Password Hash 化など、Repository より上位の処理

Service は HTTP に依存しすぎないようにします。

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

現在の構成には、主に次のような責務があります。

- Application Settings
- Exception Handler

---

### 7.8 tests

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
Backend は `http://localhost:8000` で動作するため、
Frontend Origin を CORS の許可対象としています。

---

## 9. 現在の User Domain

現在 BizSC で実装されている主要 Domain は `User` です。

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

User を作成します。

成功時:

```text
201 Created
```

---

### List

```http
GET /users
```

現在サポートしている Query Parameter:

```text
search
is_active
sort_by
sort_order
page
limit
```

一覧 API は User 配列に加えて `total` を返します。

Frontend は `total` と `limit` から Pagination を計算します。

---

### Detail

```http
GET /users/{user_id}
```

指定 User の詳細を取得します。

---

### Update

```http
PATCH /users/{user_id}
```

User を更新します。

---

### Delete

```http
DELETE /users/{user_id}
```

User を削除します。

成功時:

```text
204 No Content
```

---

## 11. Frontend 技術構成

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

## 12. Frontend 各 Directory の責務

### 12.1 pages

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

Page では画面単位の State や API 呼び出しを組み立てます。

再利用可能な UI は可能な限り `components/` に分離します。

---

### 12.2 components

複数画面で利用できる共通 UI を配置します。

現在の主な共通 Component:

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

同じ UI を Page ごとに重複実装しない方針とします。

---

### 12.3 api

Backend API との通信処理を配置します。

Axios を利用します。

Page Component 内に Axios の URL や HTTP 処理を直接増やしすぎず、
通信処理は `api/` に集約します。

---

### 12.4 types

Frontend で利用する TypeScript Type を管理します。

Backend の API Response と整合する型を定義します。

---

### 12.5 layouts

複数 Page 共通の画面構造を管理します。

現在は `MainLayout` が以下をまとめています。

```text
Header
  ↓
Sidebar + Main Content
  ↓
Footer
```

Page 本体は React Router の `Outlet` に表示されます。

---

### 12.6 routes

React Router による URL と Page の対応を管理します。

現在の主な Route:

| URL | Page |
|---|---|
| `/` | HomePage |
| `/users` | UserListPage |
| `/users/new` | UserCreatePage |
| `/users/:userId` | UserDetailPage |
| `/users/:userId/edit` | UserEditPage |
| `*` | NotFoundPage |

---

## 13. Frontend Entry Point

Entry Point:

```text
frontend/src/main.tsx
```

主な構成:

```text
React StrictMode
  ↓
BrowserRouter
  ↓
App
  ↓
AppRoutes
```

Bootstrap CSS は `main.tsx` で読み込みます。

```text
bootstrap/dist/css/bootstrap.min.css
```

---

## 14. UI / CSS 方針

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

現在、アプリ全体の独自 CSS は最小限に整理しています。

主な独自 CSS:

```text
frontend/src/index.css
frontend/src/layouts/MainLayout.css
```

Button / Input / Card / Badge / Loading / ErrorMessage / UserForm などは、
Bootstrap Class を共通 Component から利用します。

---

## 15. User Frontend の現在の機能

### User List

```text
/users
```

実装済み:

- User 一覧
- Email Search
- Active / Inactive Filter
- Sort 項目選択
- ASC / DESC
- Pagination
- Empty 表示
- Detail への遷移
- Create への遷移

---

### User Create

```text
/users/new
```

実装済み:

- Email 入力
- Password 入力
- Frontend Validation
- Backend Error 表示
- User 作成
- Cancel

---

### User Detail

```text
/users/:userId
```

実装済み:

- User 情報表示
- Active Badge
- Edit
- Delete
- User List に戻る

---

### User Edit

```text
/users/:userId/edit
```

実装済み:

- Email 編集
- Active / Inactive 編集
- Update
- Validation
- Cancel

---

## 16. Frontend State の基本方針

現時点では React 標準の State 管理を利用します。

主に:

```text
useState
useEffect
```

大規模な Global State Library は導入していません。

新しい State 管理 Library は、
具体的な必要性が発生した場合に検討します。

理由なく Redux 等を追加しません。

---

## 17. Error / Loading 方針

共通 Component:

```text
Loading
ErrorMessage
```

### Loading

Bootstrap Spinner を使用します。

API Request 中の状態をユーザーへ表示します。

### Error

Bootstrap Alert を利用します。

Backend API Error や画面単位の Error を分かりやすく表示します。

### Validation

Input Component では Bootstrap の以下を利用します。

```text
is-invalid
invalid-feedback
```

---

## 18. Frontend と Backend のデータフロー

User 一覧を例にすると、処理は以下の流れです。

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

Response は逆方向に返ります。

```text
PostgreSQL
   ↓
SQLAlchemy Model
   ↓
Service
   ↓
Pydantic Response Schema
   ↓
FastAPI
   ↓
Axios
   ↓
UserListPage
```

---

## 19. Database Migration 方針

Database Schema の変更には Alembic を利用します。

基本的な考え方:

```text
SQLAlchemy Model 変更
       ↓
Alembic Migration 作成
       ↓
Migration 内容確認
       ↓
Database へ適用
```

Model の追加・Column 追加・型変更等を行う際に、
既存 DB を手動変更することを基本方針とはしません。

Migration File を履歴として残します。

---

## 20. 新しい Domain を追加するときの基本構成

例として `Customer` を追加する場合、
既存 User 構成を参考に以下を検討します。

```text
backend/app/models/customer.py
backend/app/schemas/customer.py
backend/app/repositories/customer.py
backend/app/services/customer.py
backend/app/api/customers.py
backend/tests/...
```

Frontend:

```text
frontend/src/types/customer.ts
frontend/src/api/customers.ts
frontend/src/pages/Customer...
frontend/src/components/...
```

ただし、すべての Domain に必ず同じ数の File を作る必要はありません。

責務が必要な場合に追加します。

---

## 21. 新機能追加時の設計原則

新しい機能を実装する際は、既存構造へ無理に処理を追加するのではなく、
まず責務を判断します。

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

## 22. 既存アーキテクチャを変更する場合の注意

次の変更は影響範囲が大きいため、
局所的な変更と同じ感覚で実施しません。

- Backend Layer 構成変更
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

## 23. Build / Test

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

変更内容に応じて必要な確認を行います。

すべての小変更で全コマンドを実行する必要はありませんが、
機能完成・大きな変更・Commit 前などの区切りでは確認します。

---

## 24. Docker の基本コマンド

起動:

```powershell
docker compose up -d
```

状態確認:

```powershell
docker compose ps
```

Frontend 再起動:

```powershell
docker compose restart frontend
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

## 25. Documentation 構成

BizSC の Documentation は `docs/` で管理します。

主な資料:

```text
architecture.md
project-overview.md
handover_phase.md
```

### architecture.md

現在のシステム構成と設計原則。

### project-overview.md

Project 全体の目的・現在地・今後の大きな方向性。

### handover_phase.md

別 Chat へ作業を引き継ぐ際の、
その時点の具体的な進捗と次の作業。

---

## 26. 今後の BizSC

今後追加する具体的な業務仕様は、現時点では architecture として固定しません。

候補として考えられる機能はありますが、
以下はまだ正式仕様ではありません。

- Authentication
- Authorization / Role
- Master Data
- Business Data
- Dashboard
- Audit Log
- 各種業務機能

実装する機能が決まった段階で、

```text
要件
↓
Database
↓
Backend
↓
Frontend
↓
Test
```

の観点から設計します。

---

## 27. Architecture の基本方針まとめ

BizSC の現在の基本方針は以下です。

```text
Docker Compose で開発環境を統一する

Backend は
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

共通 UI は Component 化する

既存動作を壊さず小さな単位で変更する

新しい Library や Architecture は
具体的な必要性が出た場合にのみ導入する
```

---

## 28. Current Architecture Status

この architecture.md 作成時点では、
BizSC の Web Application 基盤と User 管理機能が構築されています。

今後はこの基盤を維持しながら、
実際に BizSC へ追加する業務機能を別途検討し、
必要な Domain を順番に追加していく方針とします。
