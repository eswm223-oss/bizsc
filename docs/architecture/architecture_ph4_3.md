# BizSC Architecture

## 1. このドキュメントについて

このドキュメントは、BizSC
の現在のシステム構成・ディレクトリ構成・設計方針を記録するための資料です。

新しいチャットや次の作業へ移行した際に、実装済みの構成と現在地点を正確に把握できることを目的とします。

**更新時点：Phase4 Step7 ソート完了 / Step8 ページネーション Step8-12
完了・Step8-13 ブラウザ最終確認前**

> コード確認が必要な場合は、引継ぎ資料だけを前提に推測せず、GitHub
> リポジトリ `eswm223-oss/bizsc` の最新コードを確認すること。
>
> 今回の Step7 / Step8 の変更について、引継ぎ作成時点で GitHub へ Push
> 済みかどうかは本資料だけでは保証しない。次回チャット開始時に最新コードとの差分を確認すること。

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

``` text
https://github.com/eswm223-oss/bizsc
```

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

Frontend と Backend は HTTP API を通じて通信します。

Frontend から Database を直接操作しません。

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

役割：

-   HTTP リクエスト受付
-   Path / Query / Body の受け取り
-   FastAPI Dependency の利用
-   Service 呼び出し
-   Response の返却

業務ロジックや SQL 処理は原則として持たせません。

### Service

役割：

-   業務ロジック
-   入力内容に基づく処理判断
-   Repository の呼び出し・組み合わせ
-   業務上のエラー判定

Router と Repository の間に位置します。

### Repository

役割：

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

User CRUD では、作成・更新・レスポンスなど用途ごとに Schema
を分離します。

------------------------------------------------------------------------

## 6. Backend API

### Health

``` text
GET /health
GET /health/db
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

Phase4 では `GET /users` を一覧画面向けに拡張しています。

現在の構成：

``` text
search
is_active
sort_by
sort_order
page
limit
```

想定例：

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

Phase4 現在の User 一覧処理：

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

Repository では、一覧取得用の1本の SQLAlchemy Query
へ条件を順番に追加します。

``` text
select(User)
  ↓
search 条件
  ↓
is_active 条件
  ↓
sort_by / sort_order
  ↓
order_by
  ↓
offset
  ↓
limit
```

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

------------------------------------------------------------------------

## 8. ソート設計

Repository の `get_all()` は概念上、以下のソート引数を受け取ります。

``` python
sort_by: str = "id"
sort_order: str = "asc"
```

### sort_by

`sort_by` の文字列をそのまま SQL
へ渡さず、許可するカラムを明示的に対応付けます。

現在の対象：

``` text
id
email
created_at
updated_at
```

概念：

``` python
sort_columns = {
    "id": User.id,
    "email": User.email,
    "created_at": User.created_at,
    "updated_at": User.updated_at,
}

sort_column = sort_columns.get(sort_by, User.id)
```

想定外の `sort_by` が指定された場合は `User.id` を使用します。

### sort_order

``` text
asc  → 昇順
desc → 降順
```

概念：

``` python
if sort_order == "desc":
    statement = statement.order_by(sort_column.desc())
else:
    statement = statement.order_by(sort_column.asc())
```

------------------------------------------------------------------------

## 9. ページネーション設計

BizSC では Phase4 Step8 で `page / limit` 方式を採用しています。

Repository の `get_all()` は概念上、以下を受け取ります。

``` python
page: int = 1
limit: int = 10
```

ページング処理：

``` python
offset = (page - 1) * limit
statement = statement.offset(offset).limit(limit)
```

### total

ページネーション後の `len(users)` ではなく、検索・Active
フィルタ適用後の全件数を `total` として返します。

そのため Repository では一覧取得とは別に `count_all()` を使用します。

概念：

``` python
def count_all(
    self,
    db: Session,
    search: str | None = None,
    is_active: bool | None = None,
) -> int:
    ...
```

`count_all()` にはソート条件・ページ番号・limit は不要です。

``` text
search
+
is_active
↓
count
↓
total
```

Service は概念上、

``` python
tuple[list[User], int]
```

を返します。

``` text
users = 現在ページのUser
total = 検索・フィルタ後の全件数
```

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
   │
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
   │
   ├─ layouts/
   │  └─ MainLayout.tsx
   │
   ├─ pages/
   │  ├─ HomePage.tsx
   │  ├─ UserListPage.tsx
   │  ├─ UserDetailPage.tsx
   │  ├─ UserCreatePage.tsx
   │  ├─ UserEditPage.tsx
   │  └─ NotFoundPage.tsx
   │
   ├─ routes/
   │  └─ AppRoutes.tsx
   │
   └─ types/
      ├─ health.ts
      └─ user.ts
```

------------------------------------------------------------------------

## 13. Frontend Routing

React Router を利用します。

``` text
/
│
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

Page 側が担当するもの：

-   API 通信の呼び出し
-   State 管理
-   React Router
-   submit 処理
-   Axios エラー処理
-   Loading 状態
-   画面固有の Validation
-   画面固有の業務処理

### Component

Component 側が担当するもの：

-   UI 表示
-   共通レイアウト
-   props による表示制御
-   UI イベントの通知

原則として、共通 Component 自身から API を直接呼び出しません。

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

## 17. UserListPage --- Phase4現在の構成

User 一覧表示：

``` text
ID
メールアドレス
ステータス
操作
```

Phase4 で以下を追加しています。

``` text
メール検索
Activeフィルタ
ソート
ページネーション
```

### 検索 State

``` text
search
```

### Activeフィルタ State

``` text
activeFilter
```

UI：

``` text
全て
有効
無効
```

API へ渡す際：

``` text
""      → undefined
"true"  → true
"false" → false
```

### ソート State

``` text
sortBy
sortOrder
```

ソート対象：

``` text
ID
メールアドレス
作成日時
更新日時
```

並び順：

``` text
昇順
降順
```

### ページネーション State

``` text
page
limit
total
```

現在の基本値：

``` text
page  = 1
limit = 10
```

総ページ数：

``` tsx
const totalPages = Math.max(1, Math.ceil(total / limit));
```

検索を実行した場合は1ページ目へ戻します。

ページ移動時も以下の条件を維持します。

``` text
search
activeFilter
sortBy
sortOrder
page
limit
```

ページネーション UI：

``` text
前へ   現在ページ / 総ページ数   次へ
```

1ページ目では「前へ」を無効化し、最終ページでは「次へ」を無効化します。

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

Phase4 の `getUsers()` は概念上、以下を受け取ります。

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

Backend Query Parameter への対応：

``` text
search     → search
isActive   → is_active
sortBy     → sort_by
sortOrder  → sort_order
page       → page
limit      → limit
```

Frontend 側では camelCase、Backend の Query Parameter では snake_case
を使用します。

------------------------------------------------------------------------

## 19. User CRUD Flow

### User List

``` text
UserListPage
  ↓
getUsers(
  search,
  isActive,
  sortBy,
  sortOrder,
  page,
  limit
)
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
  ↓
User詳細表示
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
  ↓
User詳細へ遷移
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

## 20. UserListResponse

User 一覧 API は概念上、以下を返します。

``` text
users
total
```

ページネーション導入後の意味：

``` text
users
→ 現在ページに表示するUser一覧

total
→ search / is_active 適用後、ページング前の全件数
```

`total` を使って Frontend で総ページ数を計算します。

------------------------------------------------------------------------

## 21. useEffect / 初回データ取得

UserListPage の初回一覧取得は `useEffect` から行います。

Phase4 中に以下の lint 警告へ対応済みです。

``` text
Calling setState synchronously within an effect can trigger cascading renders
```

初回取得用の非同期処理と、ユーザー操作による取得処理を分離しています。

初回取得では cleanup 用フラグを利用し、Unmount 後の State
更新を防止します。

初回取得時は `users` に加えて `total` も保存します。

------------------------------------------------------------------------

## 22. Reactフォームイベント型

フォーム submit 処理では、現在のプロジェクト方針として
`React.SubmitEvent<HTMLFormElement>` を使用します。

``` tsx
function handleSearch(event: React.SubmitEvent<HTMLFormElement>) {
  event.preventDefault();
}
```

------------------------------------------------------------------------

## 23. Validation 方針

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

------------------------------------------------------------------------

## 24. Error Handling 方針

### Field Error

入力欄に関連するエラーは Input 付近に表示します。

### Page / API Error

API 取得失敗・作成失敗・更新失敗・削除失敗などは `ErrorMessage`
を使用します。

検索・フィルタ・ページネーションの結果が0件の場合は API
エラーではなく、一覧の空状態として扱います。

------------------------------------------------------------------------

## 25. Loading State

主な State：

``` text
isLoading
isSubmitting
isDeleting
```

API 通信中は必要に応じて Loading を表示します。

送信・削除処理中は Button の `disabled` を利用し、二重操作を防止します。

検索・フィルタ・ソート・ページ移動時の一覧再取得も Loading
状態へ遷移します。

------------------------------------------------------------------------

## 26. CSS設計方針

### Component CSS

Component 自身の見た目を管理します。

### Page CSS

画面固有の配置を管理します。

``` text
Component = 自分自身の見た目
Page      = 画面内での配置
```

User 一覧の検索・フィルタ・ソート・ページネーション UI の配置は
`UserListPage.css` 側で管理します。

------------------------------------------------------------------------

## 27. 共通化方針

BizSC では過剰な共通化を避けます。

共通化する基準：

-   複数箇所で実際に利用する
-   同じ責務を持っている
-   共通化によってコードが理解しやすくなる

以下だけを理由に共通化しません。

``` text
将来使うかもしれない
なんとなく再利用できそう
コードを短くしたいだけ
```

必要になった段階で共通化します。

------------------------------------------------------------------------

## 28. TypeScript 方針

TypeScript の型安全性を優先します。

原則：

-   `any` を安易に使用しない
-   API Response は型を定義する
-   catch した error は安全に型判定する
-   Component Props を明示する
-   optional 値を明確に扱う
-   React の現在の型定義に合わせたイベント型を使用する

------------------------------------------------------------------------

## 29. Phase進捗

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
Step5  User検索
Step6  Activeフィルタ
Step7  ソート
Step8  ページネーション
Step9  CRUD / 一覧APIテスト追加
Step10 Phase4最終確認
```

現在：

``` text
Step5 User検索
  ↓
完了

Step6 Activeフィルタ
  ↓
完了

Step7 ソート
  ↓
完了

Step8 ページネーション
  ↓
Step8-12まで完了
  ↓
Step8-13 ブラウザ最終動作確認が次
```

------------------------------------------------------------------------

## 30. Phase4 Step5 --- User検索

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

## 31. Phase4 Step6 --- Activeフィルタ

完了済み：

``` text
Repository検索＋Active条件対応
Service is_active対応
Router is_active Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPage ActiveフィルタUI
検索＋Activeフィルタのブラウザ動作確認
```

------------------------------------------------------------------------

## 32. Phase4 Step7 --- ソート

完了済み：

``` text
Step7-1 Repositoryソート対応
Step7-2 Service sort_by / sort_order対応
Step7-3 Router Query Parameter対応
Step7-4 Swagger UI確認
Step7-5 Frontend API Module対応
Step7-6 UserListPageソートUI追加
Step7-7 ブラウザ動作確認
```

確認対象：

``` text
ID 昇順 / 降順
メールアドレス 昇順 / 降順
作成日時
更新日時
検索 + Activeフィルタ + ソート
```

------------------------------------------------------------------------

## 33. Phase4 Step8 --- ページネーション

### 完了済み

``` text
Step8-1  Repositoryに page / limit 引数追加
Step8-2  offset計算・offset/limit適用
Step8-3  Service page / limit対応
Step8-4  Router page / limit Query Parameter対応
Step8-5  Repository count_all()追加
Step8-6  Serviceで users / total取得
Step8-7  Routerで正しい total を返却
Step8-8  Swagger UI確認
Step8-9  Frontend API Module page / limit対応
Step8-10 UserListPage page / limit / total State対応
Step8-11 総ページ数・前へ/次へ処理追加
Step8-12 ページネーションUI追加
```

### 次に確認すること

**Step8-13：ブラウザ最終動作確認**

確認項目：

``` text
1. 1ページ目で「前へ」が無効
2. 「次へ」で2ページ目へ移動
3. 2ページ目で表示内容が切り替わる
4. 「前へ」で1ページ目へ戻る
5. 最終ページで「次へ」が無効
6. 検索条件を入れてもページ移動できる
7. Activeフィルタを入れてもページ移動できる
8. ソート条件を入れてもページ移動できる
9. 検索条件を変更したら1ページ目へ戻る
10. 0件でもエラーにならない
```

Step8-13 が問題なければ Phase4 Step8 を完了とします。

------------------------------------------------------------------------

## 34. Phase4 Step9以降

### Step9 CRUD / 一覧APIテスト追加

Step8 完了後に開始します。

対象候補：

``` text
User CRUD
User検索
Activeフィルタ
ソート
ページネーション
total
```

詳細なテスト設計は Step9 開始時に最新コードを確認して決定します。

### Step10 Phase4最終確認

想定：

``` text
Swagger UI
Browser
Frontend build
pytest
Git状態
ドキュメント更新
```

------------------------------------------------------------------------

## 35. Git / コード確認ルール

対象リポジトリ：

``` text
eswm223-oss/bizsc
```

次回チャット開始時は、引継ぎ資料を読んだ後、GitHub
上の最新コードを確認します。

特に確認するファイル：

``` text
backend/app/api/users.py
backend/app/services/user.py
backend/app/repositories/user.py

frontend/src/api/users.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
frontend/src/types/user.ts
```

引継ぎ資料と GitHub
のコードに差がある場合は、推測で進めず差分の理由を確認します。

------------------------------------------------------------------------

## 36. 開発方針

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
-   区切りの良いタイミングで Commit する
-   フェーズやチャットの区切りでドキュメントを更新する

------------------------------------------------------------------------

## 37. 次回開始位置

次回チャットでは、以下の引継ぎ資料を読み込みます。

``` text
project-overview.md
architecture.md
handover_phase.md
```

その後、GitHub リポジトリ `eswm223-oss/bizsc` の最新コードを確認します。

現在の作業上の開始位置：

> **Phase4 Step8-13：ブラウザでページネーション最終動作確認**

Step8-13 完了後：

``` text
Phase4 Step8 ページネーション完了
  ↓
Phase4 Step9 CRUD / 一覧APIテスト追加
```

これまでと同様、一度に大きく進めず、1ステップずつ確認しながら進めます。
