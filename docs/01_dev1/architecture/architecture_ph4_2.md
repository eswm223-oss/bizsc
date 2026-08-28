# BizSC Architecture

## 1. このドキュメントについて

このドキュメントは、BizSC
の現在のシステム構成・ディレクトリ構成・設計方針を記録するための資料です。

新しいチャットや次の作業へ移行した際に、実装済みの構成と現在地点を正確に把握できることを目的とします。

**更新時点：Phase4 Step6 完了 / Step7 ソート開始前**

------------------------------------------------------------------------

## 2. プロジェクト概要

### プロジェクト名

BizSC

### 開発環境

-   Windows
-   Cursor
-   GitHub
-   GitHub Desktop
-   Docker Desktop
-   Docker Compose
-   TablePlus

### 基本構成

``` text
Browser
  ↓
React Frontend
  ↓ HTTP / Axios
FastAPI Backend
  ↓ SQLAlchemy
PostgreSQL
```

Docker Compose により以下の3サービスを管理します。

``` text
frontend
backend
db
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
React
  │
  │ Axios
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

-   HTTPリクエスト受付
-   Path / Query / Body の受け取り
-   FastAPI Dependency の利用
-   Service 呼び出し
-   Response の返却

業務ロジックやSQL処理は原則として持たせません。

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
-   SQLAlchemy を利用したCRUD
-   Query条件の組み立て
-   select / insert / update / delete

業務判断は原則として持たせません。

### Model

SQLAlchemy Model としてDBテーブル構造を定義します。

現在の主要Model：

``` text
User
```

### Schema

Pydantic によりAPIの入出力構造を定義します。

User CRUDでは、作成・更新・レスポンスなど用途ごとにSchemaを分離します。

------------------------------------------------------------------------

## 6. Backend API

### Health

``` text
GET /health
GET /health/db
```

用途：

-   Backend稼働確認
-   Database接続確認

### User CRUD

``` text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

Phase3までにFrontendから一連のUser CRUD操作が可能になっています。

### User一覧 Query Parameter

Phase4で `GET /users` を拡張しています。

現在実装済み：

``` text
GET /users?search=test
GET /users?is_active=true
GET /users?is_active=false
GET /users?search=test&is_active=true
```

Query Parameter：

``` text
search
is_active
```

役割：

-   `search`：メールアドレスの部分一致検索
-   `is_active`：Active / Inactive の絞り込み
-   両方を同時指定可能

Phase4 Step7以降で追加予定：

``` text
sort_by
sort_order
```

その後、ページネーションを追加予定です。

------------------------------------------------------------------------

## 7. User一覧 Backend Flow

Phase4時点のUser一覧処理：

``` text
GET /users
    │
    ├─ search
    └─ is_active
         ↓
FastAPI Router
         ↓
UserService.get_users()
         ↓
UserRepository.get_all()
         ↓
SQLAlchemy Query
         ↓
PostgreSQL
```

Repositoryでは、1本のSQLAlchemy
Queryへ必要な条件を順番に追加する方針です。

想定構造：

``` python
statement = select(User)

if search:
    statement = statement.where(...)

if is_active is not None:
    statement = statement.where(...)

statement = statement.order_by(...)
```

この形を維持し、今後のソート・ページネーションも同じQueryへ追加します。

検索は大文字・小文字を区別しない部分一致検索として `ilike()`
を利用する方針です。

------------------------------------------------------------------------

## 8. Database

Database：

``` text
PostgreSQL 17
```

Docker Compose のサービス名：

``` text
db
```

Backendコンテナから接続する際は、Docker
Composeネットワーク上のサービス名 `db` をホストとして使用します。

Database schema の変更は Alembic で管理します。

``` text
SQLAlchemy Model
      ↓
Alembic Migration
      ↓
PostgreSQL
```

テーブル構造を変更するときは、Model変更だけで完了とはせず、Migrationを作成・適用します。

Phase4の検索・フィルタ機能ではDB構造変更は不要です。

------------------------------------------------------------------------

## 9. Frontend Architecture

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

責務を大きく以下に分離します。

``` text
Page
Component
API
Type
Layout
Route
```

PageからAxiosを直接呼び出しません。

------------------------------------------------------------------------

## 10. Frontend Directory Structure

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

CSSは必要に応じて各Component / Page / Layoutに配置します。

------------------------------------------------------------------------

## 11. Frontend Routing

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

役割：

``` text
/                     Home
/users                User一覧
/users/new            User新規作成
/users/:userId        User詳細
/users/:userId/edit   User編集
*                     404
```

------------------------------------------------------------------------

## 12. Page と Component の責務

### Page

Page側が担当するもの：

-   API通信の呼び出し
-   state管理
-   React Router
-   submit処理
-   Axiosエラー処理
-   Loading状態
-   画面固有のバリデーション
-   画面固有の業務処理

### Component

Component側が担当するもの：

-   UI表示
-   共通レイアウト
-   propsによる表示制御
-   UIイベントの通知

原則として、共通Component自身からAPIを直接呼び出しません。

------------------------------------------------------------------------

## 13. 共通UI Components

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

### Card

コンテンツ領域・タイトル・枠・内部余白を担当します。

### Input

label / input / 入力単位のerror表示を担当します。

### Loading

API通信中などの読み込み状態を表示します。

### ErrorMessage

画面・APIレベルのエラーを表示します。

### Badge

現在のVariant：

``` text
success
neutral
```

User状態：

``` text
有効 → success
無効 → neutral
```

Badge内部にはUser固有の業務判断を持たせません。

------------------------------------------------------------------------

## 14. UserForm

UserCreatePage と UserEditPage で共通利用するフォームUIです。

担当：

``` text
email入力UI
password入力UI
Active入力UI
入力エラー表示
submitボタン
フォーム内レイアウト
```

担当しないもの：

``` text
API通信
Axiosエラー判定
画面遷移
業務ロジック
Page固有バリデーション判断
```

これらはPage側で管理します。

------------------------------------------------------------------------

## 15. User CRUD Flow

### User List

Phase4で検索・フィルタが追加されています。

``` text
UserListPage
  ↓
getUsers(search?, isActive?)
  ↓
GET /users
  ↓
search / is_active
  ↓
User一覧表示
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

## 16. UserListPage --- Phase4現在の構成

User一覧表示：

``` text
ID
メールアドレス
ステータス
操作
```

ステータスはBadgeで表示します。

Phase4で以下を追加済みです。

### メール検索

検索用State：

``` text
search
```

検索フォームから `getUsers()` へ検索文字列を渡します。

処理：

``` text
検索欄
  ↓
submit
  ↓
handleSearch()
  ↓
fetchUsers()
  ↓
getUsers(search, ...)
  ↓
GET /users?search=...
```

### Activeフィルタ

フィルタ用State：

``` text
activeFilter
```

UIでは3状態を扱います。

``` text
すべて
有効
無効
```

APIへ渡す際には以下へ変換します。

``` text
すべて → undefined
有効   → true
無効   → false
```

検索とActiveフィルタは組み合わせ可能です。

``` text
検索 + すべて
検索 + 有効
検索 + 無効
```

### Submitイベント型

Reactのフォームsubmit処理では、現在のプロジェクト方針として
`SubmitEvent<HTMLFormElement>` を使用します。

``` tsx
function handleSearch(event: SubmitEvent<HTMLFormElement>) {
  event.preventDefault();
  ...
}
```

`FormEvent` / `FormEventHandler` は使用しない方針です。

### 初回データ取得

初回一覧取得は `useEffect` から行います。

Effect内で同期的なState更新につながる関数呼び出しに対するlint警告へ対応するため、初回取得用の非同期処理と検索時の取得処理を分離しています。

初回取得ではcleanup用のフラグを利用し、Unmount後のState更新を防止する構成とします。

------------------------------------------------------------------------

## 17. User API Module

`frontend/src/api/users.ts` にUser API通信を集約します。

主要関数：

``` text
getUsers()
getUser()
createUser()
updateUser()
deleteUser()
```

Phase4の `getUsers()` は検索・Activeフィルタ条件を受け取ります。

概念：

``` ts
getUsers(
  search?: string,
  isActive?: boolean,
)
```

Axios Query Parameter：

``` text
search    → search
isActive  → is_active
```

Page側ではBackendのsnake_caseを直接意識しすぎない構成とします。

------------------------------------------------------------------------

## 18. Validation 方針

FrontendとBackendの両方でValidationを行います。

``` text
Frontend Validation
        ↓
UX向上・早期フィードバック

Backend Validation
        ↓
最終的なデータ保証
```

Backendを最終的なValidation責任者とします。

------------------------------------------------------------------------

## 19. Error Handling 方針

### Field Error

入力欄に関連するエラーはInput付近に表示します。

### Page / API Error

API取得失敗・作成失敗・更新失敗・削除失敗などは `ErrorMessage`
を使用します。

検索・フィルタによる0件はAPIエラーではなく、一覧の空状態として扱います。

------------------------------------------------------------------------

## 20. Loading State

主なState：

``` text
isLoading
isSubmitting
isDeleting
```

API通信中は必要に応じてLoadingを表示します。

送信・削除処理中はButtonの `disabled` を利用し、二重操作を防止します。

検索実行時も一覧取得中はLoading状態へ遷移します。

------------------------------------------------------------------------

## 21. CSS設計方針

### Component CSS

Component自身の見た目を管理します。

### Page CSS

画面固有の配置を管理します。

原則：

``` text
Component = 自分自身の見た目
Page      = 画面内での配置
```

User一覧の検索・フィルタUIの配置は `UserListPage.css` 側で管理します。

------------------------------------------------------------------------

## 22. 共通化方針

BizSCでは、過剰な共通化を避けます。

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

## 23. TypeScript 方針

TypeScriptの型安全性を優先します。

原則：

-   `any` を安易に使用しない
-   API Responseは型を定義する
-   catchしたerrorは安全に型判定する
-   Component Propsを明示する
-   optional値を明確に扱う
-   Reactの現在の型定義に合わせたイベント型を使用する

FrontendとBackendのデータ構造のずれを早期に発見できる構成を目指します。

------------------------------------------------------------------------

## 24. Phase進捗

### Phase1

環境構築。

**完了。**

### Phase2

Backend / User CRUD。

**完了。**

### Phase3

Frontend CRUD / 共通UI。

**完了・GitHub Push済み。**

### Phase4

一覧機能拡張・テスト強化。

実装順：

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
次に開始
```

------------------------------------------------------------------------

## 25. Phase4で完了した内容

### Step5 User検索

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

検索なしの場合は従来どおり全件取得します。

### Step6 Activeフィルタ

完了済み：

``` text
Repositoryを検索＋Active条件の組み合わせへ整理
Service is_active対応
Router is_active Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPage ActiveフィルタUI
検索＋Activeフィルタのブラウザ動作確認
```

検索とActive条件を同時利用できる構成です。

------------------------------------------------------------------------

## 26. 次の実装：Step7 ソート

次はUser一覧のソートを追加します。

想定Query Parameter：

``` text
sort_by
sort_order
```

想定例：

``` text
GET /users?sort_by=email&sort_order=asc
GET /users?sort_by=created_at&sort_order=desc
GET /users?search=test&is_active=true&sort_by=email&sort_order=asc
```

進め方：

``` text
Step7-1 Repositoryにソート条件を追加
Step7-2 Service対応
Step7-3 Router対応
Step7-4 Swagger UI確認
Step7-5 Frontend API Module対応
Step7-6 UserListPageにソートUI追加
Step7-7 ブラウザ動作確認
```

`sort_by`
をそのままSQLへ渡すのではなく、許可するカラムを明示して安全に扱う方針とします。

------------------------------------------------------------------------

## 27. 開発時の基本方針

BizSCでは以下を基本とします。

1.  小さい単位で実装する
2.  実コードを確認してから変更案を出す
3.  実装後にブラウザで確認する
4.  APIはSwagger UIでも確認する
5.  必要に応じてDockerログを確認する
6.  DatabaseはTablePlusでも確認する
7.  Backendの責務をRouter / Service / Repositoryに分離する
8.  Frontendの責務をPage / Component / APIに分離する
9.  TypeScriptの型安全性を優先する
10. 過剰な共通化を避ける
11. 動作確認後にCommitする
12. 区切りの良いタイミングでPush・ドキュメント更新する

------------------------------------------------------------------------

## 28. Documentation

BizSCでは以下のドキュメントを管理します。

``` text
README.md
docs/
├─ project-overview.md
├─ architecture.md
├─ handover_phase.md
└─ decisions/
```

### project-overview.md

プロジェクト全体の現在地・進捗・次の作業を管理します。

### architecture.md

現在のシステム構成・設計・責務分離を管理します。

### handover_phase.md

別チャットへの引継ぎ資料です。

「次に何をするか」をarchitecture.mdより詳細に記録します。

### decisions/

重要な設計判断を記録します。

------------------------------------------------------------------------

## 29. GitHub確認時の注意

対象リポジトリ：

``` text
eswm223-oss/bizsc
```

新しいチャットでは、引継ぎ資料だけを前提にコードを推測せず、変更前にGitHub上の最新コードを確認します。

今回の引継ぎ作成時点では、Phase4
Step6までの作業はこのチャット上で完了しています。GitHub上のコードがローカルの最新変更より遅れている可能性があるため、次チャット開始時に最新Push状態を確認してください。

------------------------------------------------------------------------

## 30. 現在地点

``` text
Phase1
環境構築
  ↓
完了

Phase2
Backend / User CRUD
  ↓
完了

Phase3
Frontend CRUD UI
  ↓
完了

Phase4
一覧機能拡張
  ↓
User検索 完了
  ↓
Activeフィルタ 完了
  ↓
Step7 ソート ← 次回ここから
```

次チャットでは
`project-overview.md`、`architecture.md`、`handover_phase.md`
を読み込み、GitHubの最新コードを確認したうえで、**Phase4
Step7「ソート」** から再開します。
