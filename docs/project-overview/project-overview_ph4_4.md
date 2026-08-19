# BizSC Project Overview

## 1. Project Overview

### Project Name

**BizSC**

BizSC は、業務管理機能を段階的に構築しながら、Web
アプリケーション開発の設計・実装・テスト・運用を学習するための個人開発プロジェクトです。

単に機能を完成させるだけではなく、以下を重視して開発します。

-   可読性
-   保守性
-   拡張性
-   型安全
-   責務分離
-   テスタビリティ
-   実装内容を理解しながら進めること

------------------------------------------------------------------------

## 2. Current Status

**更新日：2026-08-19**

現在は、

**Phase4 Step9「CRUD / 一覧APIテスト追加」まで完了**

しています。

次の作業：

**Phase4 Step10「Phase4最終確認」**

現在の進捗：

``` text
Phase1  環境構築                         完了
Phase2  Backend / User CRUD              完了
Phase3  Frontend CRUD / 共通UI           完了
Phase4  User一覧拡張 / APIテスト         進行中
  ├─ Step5  User検索                     完了
  ├─ Step6  Activeフィルタ               完了
  ├─ Step7  ソート                       完了
  ├─ Step8  ページネーション             完了
  ├─ Step9  CRUD / 一覧APIテスト追加     完了
  └─ Step10 Phase4最終確認               次
```

------------------------------------------------------------------------

## 3. Repository

GitHub Repository：

`https://github.com/eswm223-oss/bizsc`

コードの確認が必要な場合は、このリポジトリの最新コードを確認してください。

引継ぎ資料と GitHub
の実コードに差がある場合は、推測せず最新コードを優先して確認します。

------------------------------------------------------------------------

## 4. Development Environment

``` text
OS             Windows
Editor         Cursor
Git            GitHub / GitHub Desktop
Container      Docker Desktop
Orchestration  Docker Compose
DB Client      TablePlus
```

主なローカル作業ディレクトリ：

``` text
D:\Development\apps\bizsc
```

------------------------------------------------------------------------

## 5. Technology Stack

### Frontend

``` text
React
TypeScript
Vite
React Router
Axios
CSS
```

### Backend

``` text
Python 3.13
FastAPI
Uvicorn
SQLAlchemy 2.x
Pydantic v2
Alembic
Argon2
pytest
FastAPI / Starlette TestClient
httpx2
```

### Database

``` text
PostgreSQL 17
```

### Infrastructure

``` text
Docker
Docker Compose
```

------------------------------------------------------------------------

## 6. Docker Services

Docker Compose では主に以下の3サービスを使用します。

``` text
frontend
backend
db
```

ポート：

``` text
Frontend    http://localhost:5173
Backend     http://localhost:8000
PostgreSQL  localhost:5432
```

Frontend は Vite、Backend は FastAPI / Uvicorn、Database は PostgreSQL
17 で動作します。

------------------------------------------------------------------------

## 7. System Architecture

全体構成：

``` text
Browser
  ↓
React / TypeScript
  ↓
Axios
  ↓
FastAPI
  ↓
Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

Frontend から Database を直接操作せず、FastAPI の API
を通じて処理します。

------------------------------------------------------------------------

## 8. Backend Layer Design

Backend は責務を以下のように分離します。

### Router

担当：

``` text
HTTP Request
Path Parameter
Query Parameter
Request Body
Dependency Injection
Service呼び出し
HTTP Response
```

### Service

担当：

``` text
業務ロジック
処理判断
Repository呼び出し
業務上のエラー判定
```

### Repository

担当：

``` text
SQLAlchemy Query
CRUD
検索
フィルタ
ソート
ページネーション
件数取得
```

### Model

Database Table の構造を SQLAlchemy Model として定義します。

現在の主要Model：

``` text
User
```

### Schema

Pydantic で API 入出力を定義します。

主要Schema：

``` text
UserCreate
UserUpdate
UserResponse
UserListResponse
```

------------------------------------------------------------------------

## 9. User Model / Schema

User の主要データ：

``` text
id
email
password
is_active
created_at
updated_at
```

API Response ではパスワードを返しません。

### UserCreate

作成時に受け取る主要項目：

``` text
email
password
```

`is_active` は `UserCreate` では指定しません。

### UserUpdate

更新対象：

``` text
email
password
is_active
```

少なくとも1項目が必要になるよう Validation を設定しています。

------------------------------------------------------------------------

## 10. Backend API

### Health

``` text
GET /health
GET /health/db
```

`GET /health/db` の現在のレスポンス：

``` json
{
  "status": "ok",
  "db": "connected"
}
```

### User CRUD

``` text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

------------------------------------------------------------------------

## 11. User List API

`GET /users` は以下の Query Parameter に対応済みです。

``` text
search
is_active
sort_by
sort_order
page
limit
```

例：

``` text
GET /users?search=test
GET /users?is_active=true
GET /users?sort_by=email&sort_order=asc
GET /users?page=2&limit=10
```

組み合わせも可能です。

``` text
GET /users?search=test&is_active=true&sort_by=email&sort_order=asc&page=2&limit=10
```

------------------------------------------------------------------------

## 12. Search

User のメールアドレスを検索できます。

``` text
search
```

Backend Repository では SQL `LIKE` を利用しています。

注意：

SQL LIKE では、

``` text
_
%
```

がワイルドカードとして扱われます。

特に自動テスト用の検索文字列では、意図しない一致を避けるため、固有な英数字を利用しています。

------------------------------------------------------------------------

## 13. Active Filter

``` text
is_active=true
is_active=false
```

で User を絞り込めます。

Frontend：

``` text
""      → undefined
"true"  → true
"false" → false
```

として Backend に渡します。

------------------------------------------------------------------------

## 14. Sorting

対応 Query Parameter：

``` text
sort_by
sort_order
```

主な `sort_by`：

``` text
id
email
created_at
updated_at
```

`sort_order`：

``` text
asc
desc
```

Repository では文字列を直接 SQL へ渡さず、許可した SQLAlchemy Column
へ対応付ける設計です。

------------------------------------------------------------------------

## 15. Pagination

採用方式：

``` text
page / limit
```

基本値：

``` text
page  = 1
limit = 10
```

offset：

``` python
offset = (page - 1) * limit
```

例：

``` text
page=1 → offset=0
page=2 → offset=10
page=3 → offset=20
```

一覧 API Response：

``` text
users
total
```

`total` は検索・Activeフィルタ適用後、ページング前の総件数です。

------------------------------------------------------------------------

## 16. Frontend Structure

主要ディレクトリ：

``` text
frontend/
└─ src/
   ├─ api/
   ├─ components/
   ├─ layouts/
   ├─ pages/
   ├─ routes/
   └─ types/
```

主要Page：

``` text
HomePage
UserListPage
UserDetailPage
UserCreatePage
UserEditPage
NotFoundPage
```

------------------------------------------------------------------------

## 17. Frontend Routing

``` text
/
├─ /users
├─ /users/new
├─ /users/:userId
└─ /users/:userId/edit

*
└─ NotFoundPage
```

React Router を使用しています。

------------------------------------------------------------------------

## 18. Frontend Responsibility

### Page

Page 側で担当：

``` text
API通信
State
画面遷移
submit処理
Loading
Error
Validation
画面固有処理
```

### Component

Component 側で担当：

``` text
UI
表示
props
イベント通知
共通レイアウト
```

Component から API を直接呼び出さないことを基本方針とします。

------------------------------------------------------------------------

## 19. Shared UI Components

現在の主な共通Component：

``` text
Button
Card
Input
Loading
ErrorMessage
Badge
UserForm
```

### Button

Variant：

``` text
primary
secondary
danger
```

### Badge

Variant：

``` text
success
neutral
```

User状態：

``` text
有効 → success
無効 → neutral
```

Badge 自体は User 固有の業務ロジックを持ちません。

------------------------------------------------------------------------

## 20. UserForm

UserCreatePage / UserEditPage で共通利用しています。

担当：

``` text
email入力UI
password入力UI
Active入力UI
入力エラー表示
submitボタン
フォームレイアウト
```

担当しないもの：

``` text
API通信
Axiosエラー処理
画面遷移
業務ロジック
Page固有Validation判断
```

------------------------------------------------------------------------

## 21. UserListPage

現在の UserListPage では以下を実装済みです。

``` text
User一覧
メール検索
Activeフィルタ
ソート
ページネーション
Loading
Error
0件表示
詳細画面遷移
```

主要State：

``` text
search
activeFilter
sortBy
sortOrder
page
limit
total
```

総ページ数：

``` tsx
const totalPages = Math.max(1, Math.ceil(total / limit));
```

ページネーションUI：

``` text
前へ   現在ページ / 総ページ数   次へ
```

検索条件を変更して検索した場合は1ページ目へ戻します。

ページ移動時には、

``` text
search
activeFilter
sortBy
sortOrder
```

を維持します。

------------------------------------------------------------------------

## 22. User API Module

Frontend の User API 通信は、

``` text
frontend/src/api/users.ts
```

へ集約しています。

主要関数：

``` text
getUsers()
getUser()
createUser()
updateUser()
deleteUser()
```

Page から Axios を直接利用するのではなく、API Module を経由します。

------------------------------------------------------------------------

## 23. Frontend User CRUD

### Create

``` text
UserCreatePage
↓
UserForm
↓
createUser()
↓
POST /users
↓
/users
```

### Detail

``` text
UserDetailPage
↓
useParams()
↓
getUser()
↓
GET /users/{id}
```

### Update

``` text
UserEditPage
↓
getUser()
↓
UserForm
↓
updateUser()
↓
PATCH /users/{id}
```

### Delete

``` text
UserDetailPage
↓
確認
↓
deleteUser()
↓
DELETE /users/{id}
↓
/users
```

------------------------------------------------------------------------

## 24. Validation

Frontend と Backend の両方で Validation を行います。

``` text
Frontend
↓
ユーザーへの早いフィードバック

Backend
↓
最終的なデータ保証
```

Backend を最終的な Validation の責任者とします。

------------------------------------------------------------------------

## 25. Database / Alembic

Database：

``` text
PostgreSQL 17
```

DB Schema の変更は Alembic で管理します。

``` text
SQLAlchemy Model
↓
Alembic Migration
↓
PostgreSQL
```

Phase4 の、

``` text
検索
Activeフィルタ
ソート
ページネーション
テスト追加
```

では Database Schema を変更していないため、新規 Migration は不要でした。

------------------------------------------------------------------------

## 26. Testing

Backend の自動テストには pytest を使用します。

現在の主要テスト構成：

``` text
backend/tests/
├─ conftest.py
├─ test_health.py
└─ test_users.py
```

------------------------------------------------------------------------

## 27. Test Database Strategy

Phase4 Step9 で API テスト用の共通設定を追加しました。

`conftest.py` で FastAPI の `get_db` を pytest 実行中だけ差し替えます。

概念：

``` text
pytest
↓
connection.begin()
↓
テスト用Session
↓
dependency_overrides[get_db]
↓
TestClient
↓
API実行
↓
rollback
```

主要構成：

``` python
connection = engine.connect()
transaction = connection.begin()

db = Session(
    bind=connection,
    join_transaction_mode="create_savepoint",
)
```

テスト終了後に外側 transaction を rollback します。

------------------------------------------------------------------------

## 28. Test Database Important Note

現在は完全なテスト専用DBではありません。

``` text
通常のPostgreSQL DB
↓
既存データはテストから見える
↓
テスト中の変更はrollback
```

したがって一覧テストでは、既存Userが `total` へ混ざらないよう、固有の
`search` 条件を使用します。

将来的にテスト規模が大きくなった場合は、独立したテスト専用DBを検討できます。

------------------------------------------------------------------------

## 29. Current Automated Tests

Phase4 Step9 で以下を自動テスト化しました。

``` text
Health
User作成
User詳細取得
User更新
User削除
User一覧
search
is_active
sort_by
sort_order
page
limit
total
```

User削除テストでは、

``` text
DELETE
↓
204
↓
再GET
↓
404
```

まで確認しています。

------------------------------------------------------------------------

## 30. is_active Test Note

`UserCreate` では `is_active` を受け取りません。

Inactive User をテストで準備するときは、

``` text
POST /users
↓
is_active=True
↓
PATCH /users/{id}
↓
is_active=False
```

とします。

この仕様は Step9-8 で確認済みです。

------------------------------------------------------------------------

## 31. Pagination Test

ページネーションテストでは、テスト用 User を12件作成しました。

条件：

``` text
search=bizscpage
sort_by=email
sort_order=asc
page=2
limit=5
```

確認：

``` text
total = 12
users = 5件
```

2ページ目に期待した User が表示されることも確認しています。

------------------------------------------------------------------------

## 32. pytest Status

Phase4 Step9-11 で以下を実行済みです。

``` powershell
docker compose exec backend pytest -v
```

**全テスト PASSED を確認済みです。**

------------------------------------------------------------------------

## 33. Health Test Adjustment

既存 Health Test で API Response と期待値に差がありました。

現在の `/health/db`：

``` json
{
  "status": "ok",
  "db": "connected"
}
```

テスト側を現在の API 仕様へ合わせ、

``` text
"database"
↓
"db"
```

へ修正済みです。

------------------------------------------------------------------------

## 34. TestClient Dependency Warning

Step9 中に以下の Warning が発生しました。

``` text
StarletteDeprecationWarning:
Using `httpx` with `starlette.testclient` is deprecated;
install `httpx2` instead.
```

Backend へ `httpx2` を追加し、Docker Backend Image を再ビルドしました。

対応後：

``` text
Warning解消
pytest成功
```

を確認済みです。

------------------------------------------------------------------------

## 35. Phase History

### Phase1 - Environment

実施：

``` text
Docker Compose
Backend
Frontend
PostgreSQL
Cursor
GitHub
TablePlus
```

**完了。**

### Phase2 - Backend / CRUD

実施：

``` text
User Model
Alembic
Schema
Repository
Service
Router
CRUD API
Validation
Exception Handler
Health API
```

**完了。**

### Phase3 - Frontend CRUD / Shared UI

実施：

``` text
React Router
API Module
User List
User Detail
User Create
User Edit
User Delete
Button
Card
Input
Loading
ErrorMessage
Badge
UserForm
Layout
```

**完了。**

### Phase4 - User List Enhancement / Testing

実施済み：

``` text
User検索
Activeフィルタ
ソート
ページネーション
CRUD / 一覧API自動テスト
```

現在：

``` text
Step9完了
Step10開始前
```

------------------------------------------------------------------------

## 36. Next Step

次の作業は、

# Phase4 Step10 - Phase4最終確認

です。

現時点で想定している確認：

``` text
Swagger UI
Browser
Frontend build
pytest
Git / Repository状態
ドキュメント
```

ただし、新しいチャットでは最初に GitHub の最新コードを確認し、Step10
の詳細な小Stepを確定してください。

------------------------------------------------------------------------

## 37. Files to Check at Next Chat

Backend：

``` text
backend/app/api/users.py
backend/app/services/user.py
backend/app/repositories/user.py
backend/app/schemas/user.py
backend/app/db/database.py
backend/tests/conftest.py
backend/tests/test_health.py
backend/tests/test_users.py
backend/requirements.txt
```

Frontend：

``` text
frontend/src/api/users.ts
frontend/src/types/user.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
```

必要に応じてその他の関連ファイルも確認します。

------------------------------------------------------------------------

## 38. Development Principles

今後も以下を維持します。

``` text
小さなStepで進める
実装理由を理解する
GitHub最新コードを確認する
推測でコードを決めない
Page / Component責務を分離する
Router / Service / Repository責務を分離する
型安全を維持する
Backendを最終Validation責任者とする
不要な共通化を避ける
実装後に動作確認する
```

Commit / Push やドキュメント更新は、区切りの良いタイミングで行います。

------------------------------------------------------------------------

## 39. Handover Documents

新しいチャットへ移る際は、以下3資料を使用します。

``` text
architecture_ph4_4.md
handover_phase4_4.md
project-overview_ph4_4.md
```

推奨確認順：

``` text
1. architecture
2. handover_phase
3. project-overview
4. GitHub最新コード
5. Phase4 Step10開始
```

------------------------------------------------------------------------

## 40. Current Final State

引継ぎ時点の最重要情報：

``` text
Project: BizSC

Phase1: 完了
Phase2: 完了
Phase3: 完了

Phase4:
  Step5  完了
  Step6  完了
  Step7  完了
  Step8  完了
  Step9  完了
  Step10 次

Backend pytest:
  全テスト PASSED

次の開始地点:
  Phase4 Step10「Phase4最終確認」
```
