# BizSC Architecture

## 1. このドキュメントについて

このドキュメントは、BizSC
の現在のシステム構成・ディレクトリ構成・設計方針を記録するための引継ぎ資料です。

新しいチャットへ移行した際に、実装済みの構成と現在地点を正確に把握できることを目的とします。

**更新時点：2026-08-19 / Phase4 Step9「CRUD / 一覧APIテスト追加」完了 /
Step10「Phase4最終確認」開始前**

> コード確認が必要な場合は、引継ぎ資料だけを前提に推測せず、GitHub
> リポジトリ `eswm223-oss/bizsc` の最新コードを確認すること。

------------------------------------------------------------------------

## 2. プロジェクト概要

### プロジェクト名

BizSC

BizSC は、業務管理機能を段階的に構築しながら、Web
アプリケーション開発の設計・実装・運用を学習するための個人開発プロジェクトです。

重視する項目：

-   可読性
-   保守性
-   拡張性
-   型安全
-   テスタビリティ
-   責務分離
-   理解しながら開発すること

### 開発環境

-   Windows
-   Cursor
-   GitHub
-   GitHub Desktop
-   Docker Desktop
-   Docker Compose
-   TablePlus

### リポジトリ

`https://github.com/eswm223-oss/bizsc`

------------------------------------------------------------------------

## 3. 技術スタック

### Frontend

-   React
-   TypeScript
-   Vite
-   React Router
-   Axios
-   CSS

### Backend

-   Python 3.13
-   FastAPI
-   Uvicorn
-   SQLAlchemy 2.x
-   Pydantic v2
-   Alembic
-   Argon2
-   pytest
-   FastAPI / Starlette TestClient
-   httpx2（TestClient の新しい依存として追加）

### Database

-   PostgreSQL 17

### Infrastructure / Development

-   Docker
-   Docker Compose
-   GitHub
-   GitHub Desktop
-   Cursor
-   TablePlus

------------------------------------------------------------------------

## 4. 全体アーキテクチャ

``` text
Browser
  │
  ▼
React Frontend
  │
  │ Axios / HTTP
  ▼
FastAPI Router
  │
  ▼
Service
  │
  ▼
Repository
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
```

Frontend と Backend は HTTP API を通じて通信します。Frontend から
Database を直接操作しません。

Docker Compose では以下の3サービスを管理します。

``` text
frontend
backend
db
```

主なポート：

``` text
Frontend    5173
Backend     8000
PostgreSQL  5432
```

------------------------------------------------------------------------

## 5. Backend Architecture

Backend は以下の責務分離を基本とします。

``` text
Request
  ↓
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

### Router

-   HTTP リクエスト受付
-   Path / Query / Body の受け取り
-   FastAPI Dependency の利用
-   Service 呼び出し
-   Response の返却

業務ロジックや SQL 処理は原則として持たせません。

### Service

-   業務ロジック
-   入力内容に基づく処理判断
-   Repository の呼び出し・組み合わせ
-   業務上のエラー判定

### Repository

-   Database との直接的なやり取り
-   SQLAlchemy を利用した CRUD
-   Query 条件の組み立て
-   select / insert / update / delete
-   一覧件数の count

業務判断は原則として持たせません。

### Model

SQLAlchemy Model として DB テーブル構造を定義します。

現在の主要 Model：

``` text
User
```

### Schema

Pydantic により API の入出力構造を定義します。

現在の User Schema の主要構成：

``` text
UserCreate
UserUpdate
UserResponse
UserListResponse
```

`UserCreate` で受け取るのは `email` と `password` です。`is_active`
は作成時には指定せず、必要な変更は `UserUpdate` / PATCH で行います。

------------------------------------------------------------------------

## 6. Backend API

### Health

``` text
GET /health
GET /health/db
```

`GET /health/db` の現在のレスポンスは概念上以下です。

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

### User一覧 Query Parameter

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
GET /users?page=1&limit=10
GET /users?search=test&is_active=true&sort_by=email&sort_order=asc&page=2&limit=10
```

役割：

-   `search`：メールアドレスの部分一致検索
-   `is_active`：Active / Inactive の絞り込み
-   `sort_by`：ソート対象
-   `sort_order`：昇順 / 降順
-   `page`：ページ番号
-   `limit`：1ページあたりの取得件数

------------------------------------------------------------------------

## 7. User一覧 Backend Flow

``` text
GET /users
    │
    ├─ search
    ├─ is_active
    ├─ sort_by
    ├─ sort_order
    ├─ page
    └─ limit
         ↓
FastAPI Router
         ↓
UserService.get_users()
         ↓
UserRepository
    ├─ get_all()
    └─ count_all()
         ↓
SQLAlchemy
         ↓
PostgreSQL
```

Repository の `get_all()` では、検索・Active
条件・ソート・ページネーションを組み合わせて一覧を取得します。

ページ番号から offset を計算します。

``` python
offset = (page - 1) * limit
```

例：

``` text
page=1, limit=10 → offset=0
page=2, limit=10 → offset=10
page=3, limit=10 → offset=20
```

`count_all()` は `search` / `is_active`
適用後、ページング前の総件数を取得します。

------------------------------------------------------------------------

## 8. ソート設計

Repository の `get_all()` は概念上以下を受け取ります。

``` python
sort_by: str = "id"
sort_order: str = "asc"
```

許可するソート対象：

``` text
id
email
created_at
updated_at
```

文字列をそのまま SQL へ渡さず、許可した SQLAlchemy Column
へ対応付けます。

``` python
sort_columns = {
    "id": User.id,
    "email": User.email,
    "created_at": User.created_at,
    "updated_at": User.updated_at,
}
```

`sort_order`：

``` text
asc  → 昇順
desc → 降順
```

------------------------------------------------------------------------

## 9. ページネーション設計

Phase4 Step8 で `page / limit` 方式を採用しています。

``` python
page: int = 1
limit: int = 10
```

``` python
offset = (page - 1) * limit
statement = statement.offset(offset).limit(limit)
```

一覧 API は以下を返します。

``` text
users
total
```

意味：

``` text
users
→ 現在ページに表示する User 一覧

total
→ search / is_active 適用後、ページング前の全件数
```

Frontend は `total` と `limit` から総ページ数を計算します。

------------------------------------------------------------------------

## 10. Database

Database：

``` text
PostgreSQL 17
```

Docker Compose サービス名：

``` text
db
```

Backend コンテナからは Docker Compose ネットワーク上のサービス名 `db`
をホストとして使用します。

Database schema の変更は Alembic で管理します。

``` text
SQLAlchemy Model
      ↓
Alembic Migration
      ↓
PostgreSQL
```

Phase4 の検索・フィルタ・ソート・ページネーションでは DB
構造変更は行っていないため、Alembic Migration は不要です。

------------------------------------------------------------------------

## 11. Frontend Architecture

Frontend は以下の流れを基本とします。

``` text
Page
  ↓
API Module
  ↓
Axios Client
  ↓
FastAPI
```

Page から Axios を直接呼び出しません。

責務を大きく以下へ分離します。

``` text
Page
Component
API
Type
Layout
Route
```

------------------------------------------------------------------------

## 12. Frontend Directory Structure

主要構成：

``` text
frontend/
└─ src/
   ├─ api/
   │  ├─ client.ts
   │  ├─ health.ts
   │  └─ users.ts
   ├─ components/
   │  ├─ Badge/
   │  ├─ Button/
   │  ├─ Card/
   │  ├─ ErrorMessage/
   │  ├─ Input/
   │  ├─ Loading/
   │  ├─ UserForm/
   │  ├─ Header.tsx
   │  ├─ Sidebar.tsx
   │  └─ Footer.tsx
   ├─ layouts/
   │  └─ MainLayout.tsx
   ├─ pages/
   │  ├─ HomePage.tsx
   │  ├─ UserListPage.tsx
   │  ├─ UserDetailPage.tsx
   │  ├─ UserCreatePage.tsx
   │  ├─ UserEditPage.tsx
   │  └─ NotFoundPage.tsx
   ├─ routes/
   │  └─ AppRoutes.tsx
   └─ types/
      ├─ health.ts
      └─ user.ts
```

------------------------------------------------------------------------

## 13. Frontend Routing

``` text
/
├─ /users
├─ /users/new
├─ /users/:userId
└─ /users/:userId/edit

*
└─ NotFoundPage
```

------------------------------------------------------------------------

## 14. Page と Component の責務

### Page

-   API 通信の呼び出し
-   State 管理
-   React Router
-   submit 処理
-   Axios エラー処理
-   Loading 状態
-   画面固有の Validation
-   画面固有の業務処理

### Component

-   UI 表示
-   共通レイアウト
-   props による表示制御
-   UI イベントの通知

共通 Component 自身から API を直接呼び出さないことを基本とします。

------------------------------------------------------------------------

## 15. 共通UI Components

現在実装済み：

``` text
Button
Card
Input
Loading
ErrorMessage
Badge
UserForm
```

Button Variant：

``` text
primary
secondary
danger
```

Badge Variant：

``` text
success
neutral
```

User 状態：

``` text
有効 → success
無効 → neutral
```

Badge 内部には User 固有の業務判断を持たせません。

------------------------------------------------------------------------

## 16. UserForm

UserCreatePage と UserEditPage で共通利用するフォーム UI です。

担当：

``` text
email 入力UI
password 入力UI
Active 入力UI
入力エラー表示
submit ボタン
フォーム内レイアウト
```

担当しないもの：

``` text
API通信
Axiosエラー判定
画面遷移
業務ロジック
Page固有Validation判断
```

これらは Page 側で管理します。

------------------------------------------------------------------------

## 17. UserListPage

User 一覧表示：

``` text
ID
メールアドレス
ステータス
操作
```

Phase4 で以下を追加済みです。

``` text
メール検索
Activeフィルタ
ソート
ページネーション
```

主な State：

``` text
search
activeFilter
sortBy
sortOrder
page
limit
total
```

Activeフィルタ：

``` text
""      → undefined
"true"  → true
"false" → false
```

ソート対象：

``` text
ID
メールアドレス
作成日時
更新日時
```

ページネーション基本値：

``` text
page  = 1
limit = 10
```

総ページ数：

``` tsx
const totalPages = Math.max(1, Math.ceil(total / limit));
```

検索実行時は1ページ目へ戻します。

ページ移動時も以下を維持します。

``` text
search
activeFilter
sortBy
sortOrder
page
limit
```

UI：

``` text
前へ   現在ページ / 総ページ数   次へ
```

1ページ目では「前へ」、最終ページでは「次へ」を無効化します。

------------------------------------------------------------------------

## 18. User API Module

`frontend/src/api/users.ts` に User API 通信を集約します。

主要関数：

``` text
getUsers()
getUser()
createUser()
updateUser()
deleteUser()
```

`getUsers()` は概念上以下を受け取ります。

``` ts
getUsers(
  search?: string,
  isActive?: boolean,
  sortBy?: string,
  sortOrder?: string,
  page?: number,
  limit?: number,
)
```

Frontend 側では camelCase、Backend Query Parameter では snake_case
を使用します。

------------------------------------------------------------------------

## 19. User CRUD Flow

### User List

``` text
UserListPage
  ↓
getUsers(search, isActive, sortBy, sortOrder, page, limit)
  ↓
GET /users
  ↓
検索・フィルタ・ソート・ページネーション
  ↓
UserListResponse
  ├─ users
  └─ total
```

### User Create

``` text
UserCreatePage
  ↓
UserForm
  ↓
createUser()
  ↓
POST /users
  ↓
/users へ遷移
```

### User Detail

``` text
UserDetailPage
  ↓
useParams()
  ↓
getUser()
  ↓
GET /users/{id}
```

### User Edit

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

### User Delete

``` text
UserDetailPage
  ↓
window.confirm()
  ↓
deleteUser()
  ↓
DELETE /users/{id}
  ↓
/users へ遷移
```

------------------------------------------------------------------------

## 20. useEffect / 初回データ取得

UserListPage の初回一覧取得は `useEffect` から行います。

Phase4 中に以下の lint 警告へ対応済みです。

``` text
Calling setState synchronously within an effect can trigger cascading renders
```

初回取得用の非同期処理と、ユーザー操作による取得処理を分離しています。

初回取得では cleanup 用フラグを利用し、Unmount 後の State
更新を防止します。

------------------------------------------------------------------------

## 21. Validation / Error / Loading

Frontend と Backend の両方で Validation を行います。

``` text
Frontend Validation
        ↓
UX向上・早期フィードバック

Backend Validation
        ↓
最終的なデータ保証
```

Backend を最終的な Validation 責任者とします。

API エラーは `ErrorMessage`、通信中は `Loading` や Button の `disabled`
を利用します。

検索・フィルタ・ページネーションの結果が0件の場合は API
エラーではなく一覧の空状態として扱います。

------------------------------------------------------------------------

## 22. CSS設計方針

``` text
Component = 自分自身の見た目
Page      = 画面内での配置
```

User 一覧の検索・フィルタ・ソート・ページネーション UI の配置は
`UserListPage.css` 側で管理します。

------------------------------------------------------------------------

## 23. 共通化 / TypeScript 方針

過剰な共通化を避けます。

共通化する基準：

-   複数箇所で実際に利用する
-   同じ責務を持っている
-   共通化によってコードが理解しやすくなる

TypeScript では型安全性を優先します。

-   `any` を安易に使用しない
-   API Response は型を定義する
-   catch した error は安全に型判定する
-   Component Props を明示する
-   optional 値を明確に扱う

------------------------------------------------------------------------

## 24. Backend Test Architecture

Phase4 Step9 で User API の自動テスト基盤を追加しました。

主要構成：

``` text
backend/
└─ tests/
   ├─ conftest.py
   ├─ test_health.py
   └─ test_users.py
```

### conftest.py

pytest fixture `client` を定義し、FastAPI の `get_db` Dependency
をテスト用 Session に差し替えます。

概念：

``` text
pytest
  ↓
connection.begin()
  ↓
テスト用 SQLAlchemy Session
  ↓
app.dependency_overrides[get_db]
  ↓
FastAPI TestClient
  ↓
テスト終了
  ↓
rollback
```

現在の基本構成：

``` python
connection = engine.connect()
transaction = connection.begin()

db = Session(
    bind=connection,
    join_transaction_mode="create_savepoint",
)
```

アプリ側の Repository は `db.commit()` を行いますが、テストでは外側の
transaction を保持し、テスト終了後に rollback します。

### 重要な性質

現在の方式は **既存 PostgreSQL DB を参照しつつ、テスト中の変更を
rollback する方式**です。

そのため：

``` text
既存DBデータ
→ テストから見える

テスト中に追加・更新・削除した変更
→ テスト終了時に rollback
```

既存データを空にして完全分離するテスト専用DB方式ではありません。

したがって一覧テストでは、既存データに結果が左右されないように固有の
`search` 条件を組み合わせています。

------------------------------------------------------------------------

## 25. Phase4 Step9 で追加したテスト

`test_users.py` では以下を確認済みです。

``` text
User作成
User詳細取得
User更新
User削除
User一覧 + search
is_active フィルタ
sort_by / sort_order
page / limit
total
```

### CRUD

``` text
POST /users
GET /users/{id}
PATCH /users/{id}
DELETE /users/{id}
```

削除テストでは DELETE 後に同じ ID を GET し、404
になることまで確認します。

### search

テスト専用メールアドレスを作成し、`search` に一致する User
のみ取得されることを確認します。

### is_active

`UserCreate` には `is_active` がないため、Inactive User
の作成は次の流れで行います。

``` text
POST /users
  ↓
初期状態 Active=True
  ↓
PATCH /users/{id}
  ↓
is_active=False
```

その後 `search + is_active=true` で Active User
のみ返ることを確認します。

### sort

固有の検索条件と `sort_by=email&sort_order=asc`
を組み合わせ、期待するメールアドレス順になることを確認します。

### pagination / total

テスト用 User を12件作成し、概念上以下を確認します。

``` text
page=2
limit=5
total=12
users=5件
```

ソートも組み合わせ、2ページ目の内容が期待どおりであることを確認します。

------------------------------------------------------------------------

## 26. テスト依存ライブラリ

Step9 中、FastAPI / Starlette TestClient 実行時に以下の Warning
が発生しました。

``` text
StarletteDeprecationWarning:
Using `httpx` with `starlette.testclient` is deprecated;
install `httpx2` instead.
```

対応として Backend の依存関係に `httpx2` を追加し、Backend
イメージを再ビルドしました。

再ビルド後、Warning が解消し、User API
テストも正常に実行できることを確認済みです。

------------------------------------------------------------------------

## 27. Phase進捗

### Phase1

環境構築。

**完了。**

### Phase2

Backend / User CRUD。

**完了。**

### Phase3

Frontend CRUD / 共通 UI。

**完了。**

### Phase4

User 一覧機能拡張・テスト強化。

``` text
Step5  User検索                  完了
Step6  Activeフィルタ            完了
Step7  ソート                    完了
Step8  ページネーション          完了
Step9  CRUD / 一覧APIテスト追加  完了
Step10 Phase4最終確認            次
```

------------------------------------------------------------------------

## 28. Phase4 Step5 - User検索

完了済み：

``` text
Repository検索対応
Service検索条件対応
Router search Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPage検索UI
ブラウザ動作確認
```

------------------------------------------------------------------------

## 29. Phase4 Step6 - Activeフィルタ

完了済み：

``` text
Repository検索 + Active条件対応
Service is_active対応
Router is_active Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPage ActiveフィルタUI
検索 + Activeフィルタのブラウザ動作確認
```

------------------------------------------------------------------------

## 30. Phase4 Step7 - ソート

完了済み：

``` text
Repositoryソート対応
Service sort_by / sort_order対応
Router Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPageソートUI追加
ブラウザ動作確認
```

------------------------------------------------------------------------

## 31. Phase4 Step8 - ページネーション

完了済み：

``` text
Repository page / limit対応
offset / limit適用
Service page / limit対応
Router page / limit対応
Repository count_all()追加
Service users / total対応
Router total対応
Swagger UI確認
Frontend API Module対応
UserListPage page / limit / total State対応
総ページ数・前へ/次へ処理
ページネーションUI
ブラウザ最終動作確認
```

Step8-13 のブラウザ確認も完了済みです。

確認済み：

``` text
1ページ目で「前へ」が無効
次へで2ページ目へ移動
表示内容の切替
前へで1ページ目へ戻る
最終ページで「次へ」が無効
検索 + ページ移動
Activeフィルタ + ページ移動
ソート + ページ移動
検索条件変更時に1ページ目へ戻る
0件でもエラーにならない
```

------------------------------------------------------------------------

## 32. Phase4 Step9 - CRUD / 一覧APIテスト追加

**完了済み。**

実施内容：

``` text
Step9-1  テストDB方針決定
Step9-2  conftest.py / 共通TestClient fixture
Step9-3  User作成テスト
Step9-4  User詳細取得テスト
Step9-5  User更新テスト
Step9-6  User削除テスト
Step9-7  User一覧 + searchテスト
Step9-8  is_activeフィルタテスト
Step9-9  ソートテスト
Step9-10 pagination / totalテスト
Step9-11 全pytest実行
```

Step9-11 で以下を実行し、全テスト成功を確認済みです。

``` powershell
docker compose exec backend pytest -v
```

### Step9中に修正した既存Healthテスト

`GET /health/db` の実レスポンスが、

``` json
{
  "status": "ok",
  "db": "connected"
}
```

であるため、既存 `test_health.py` の期待値を `"database"` から `"db"`
に合わせました。

------------------------------------------------------------------------

## 33. 次の作業 - Phase4 Step10

次回チャットは **Phase4 Step10「Phase4最終確認」** から開始します。

引継ぎ時点で想定している確認項目：

``` text
Swagger UI
Browser
Frontend build
pytest
Git状態 / 最新コード確認
ドキュメント更新
```

Step10 の詳細な分割は、新しいチャットで GitHub
の最新コードを確認したうえで決定します。

------------------------------------------------------------------------

## 34. Git / コード確認ルール

対象リポジトリ：

`https://github.com/eswm223-oss/bizsc`

新しいチャット開始時は、引継ぎ資料を読んだ後、GitHub
上の最新コードを確認します。

特に確認候補：

``` text
backend/app/api/users.py
backend/app/services/user.py
backend/app/repositories/user.py
backend/app/schemas/user.py
backend/tests/conftest.py
backend/tests/test_health.py
backend/tests/test_users.py
backend/requirements.txt

frontend/src/api/users.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
frontend/src/types/user.ts
```

引継ぎ資料と GitHub
のコードに差がある場合は、推測で進めず、最新コードを優先して差分を確認します。

------------------------------------------------------------------------

## 35. 開発方針

今後も以下を維持します。

-   一度に大きく変更しない
-   1ステップずつ進める
-   なぜ変更するのか理解してから実装する
-   GitHub の実コードを確認してから変更案を出す
-   UI と業務処理を分離する
-   Page と Component の責務を分離する
-   Backend を最終 Validation 保証とする
-   型安全を維持する
-   不要な共通化を避ける
-   動作確認してから次へ進む
-   区切りの良いタイミングで Commit / Push する
-   フェーズやチャットの区切りでドキュメントを更新する
