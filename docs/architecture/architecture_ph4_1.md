# BizSC Architecture

## 1. このドキュメントについて

このドキュメントは、BizSC の現在のシステム構成・ディレクトリ構成・設計方針を記録するための資料です。

新しいチャットや次フェーズへ移行した際に、実装済みの構成を正確に把握できることを目的とします。

**更新時点：Phase3 完了**

---

# 2. プロジェクト概要

## プロジェクト名

BizSC

## 開発環境

* Windows
* Cursor
* GitHub
* GitHub Desktop
* Docker Desktop
* Docker Compose
* TablePlus

## 基本構成

```text
Browser
  ↓
React Frontend
  ↓ HTTP / Axios
FastAPI Backend
  ↓ SQLAlchemy
PostgreSQL
```

Docker Compose により、以下の3サービスを管理します。

```text
frontend
backend
db
```

---

# 3. 技術スタック

## Frontend

* React
* TypeScript
* Vite
* React Router
* Axios
* CSS

## Backend

* Python 3.13
* FastAPI
* Uvicorn
* SQLAlchemy 2.x
* Pydantic v2
* Alembic

## Database

* PostgreSQL 17

## Infrastructure / Development

* Docker
* Docker Compose
* GitHub
* GitHub Desktop
* Cursor
* TablePlus

---

# 4. 全体アーキテクチャ

```text
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

---

# 5. Backend Architecture

Backend は以下の責務分離を基本とします。

```text
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

## Router

役割：

* HTTPリクエスト受付
* Path / Query / Body の受け取り
* FastAPI Dependency の利用
* Service 呼び出し
* Response の返却

業務ロジックやSQL処理は原則として持たせません。

---

## Service

役割：

* 業務ロジック
* 入力内容に基づく処理判断
* Repository の組み合わせ
* 業務上のエラー判定

Router と Repository の間に位置します。

---

## Repository

役割：

* Database との直接的なやり取り
* SQLAlchemy を利用したCRUD
* select / insert / update / delete

業務判断は原則として持たせません。

---

## Model

SQLAlchemy Model としてDBテーブル構造を定義します。

現在の主要Model：

```text
User
```

---

## Schema

Pydantic によりAPIの入出力構造を定義します。

User CRUDでは、作成・更新・レスポンスなど用途ごとにSchemaを分離します。

---

# 6. Backend API

現在実装済みの主要APIです。

## Health

```text
GET /health
GET /health/db
```

用途：

* Backend稼働確認
* Database接続確認

---

## User

```text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

Phase3完了時点で、Frontendから一連のUser CRUD操作が可能です。

---

# 7. Database

Database：

```text
PostgreSQL 17
```

Docker Compose のサービス名：

```text
db
```

Backendコンテナから接続する際は、Docker Composeネットワーク上のサービス名 `db` をホストとして使用します。

Database schema の変更は Alembic で管理します。

```text
SQLAlchemy Model
      ↓
Alembic Migration
      ↓
PostgreSQL
```

テーブル構造を変更するときは、Modelを変更しただけで完了とはせず、Migrationを作成・適用します。

---

# 8. Frontend Architecture

Frontend は以下の流れを基本とします。

```text
Page
  ↓
API Module
  ↓
Axios Client
  ↓
FastAPI
```

責務を大きく以下に分離します。

```text
Page
Component
API
Type
Layout
Route
```

---

# 9. Frontend Directory Structure

Phase3完了時点の主要構成：

```text
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

---

# 10. Frontend Routing

React Router を利用します。

現在の主要ルート：

```text
/
│
├─ /users
│
├─ /users/new
│
├─ /users/:userId
│
└─ /users/:userId/edit

*
└─ NotFoundPage
```

役割：

```text
/                     Home
/users                User一覧
/users/new            User新規作成
/users/:userId        User詳細
/users/:userId/edit   User編集
*                     404
```

---

# 11. Page と Component の責務

BizSCでは、PageとComponentを明確に分離します。

## Page

Page側が担当するもの：

* API通信
* state管理
* React Router
* useNavigate
* useParams
* submit処理
* Axiosエラー処理
* 画面固有のバリデーション
* 画面固有の業務処理

例：

```text
UserCreatePage
UserEditPage
UserDetailPage
UserListPage
```

---

## Component

Component側が担当するもの：

* UI表示
* 共通レイアウト
* propsによる表示制御
* UIイベントの通知

原則として、共通Component自身からAPIを直接呼び出しません。

---

# 12. 共通UI Components

Phase3完了時点で以下を実装済みです。

## Button

用途：

* 共通ボタンUI

Variant：

```text
primary
secondary
danger
```

HTML標準のbutton属性を利用可能とします。

---

## Card

用途：

* コンテンツ領域
* タイトル
* 枠
* 内部余白

画面固有の処理は持ちません。

---

## Input

用途：

* label
* input
* 入力単位のerror表示

Input自身が他のInputとの配置を管理するのではなく、フォーム側で配置を管理します。

---

## Loading

用途：

* API通信中などの読み込み状態表示

任意のメッセージを指定可能です。

---

## ErrorMessage

用途：

* 画面レベルのエラー表示

入力項目単位のエラーはInput側、画面・APIレベルのエラーはErrorMessage側という形で分離します。

---

## Badge

用途：

* 状態表示

現在のVariant：

```text
success
neutral
```

UserのActive状態では、

```text
有効 → success
無効 → neutral
```

として使用します。

---

# 13. UserForm

UserCreatePage と UserEditPage で共通利用するフォームUIです。

UserFormの責務：

```text
email入力UI
password入力UI
Active入力UI
入力エラー表示
submitボタン
フォーム内レイアウト
```

UserFormが担当しないもの：

```text
API通信
Axiosエラー判定
画面遷移
業務ロジック
Page固有バリデーション判断
```

これらはPage側で管理します。

---

# 14. User CRUD Flow

## User List

```text
UserListPage
  ↓
getUsers()
  ↓
GET /users
  ↓
User一覧表示
```

ステータス表示にはBadgeを使用します。

---

## User Create

```text
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

---

## User Detail

```text
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

---

## User Edit

```text
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

---

## User Delete

```text
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

---

# 15. Validation 方針

FrontendとBackendの両方でValidationを行います。

```text
Frontend Validation
        ↓
UX向上・早期フィードバック

Backend Validation
        ↓
最終的なデータ保証
```

Backendを最終的なValidation責任者とします。

FrontendのValidationだけを信用してDatabaseへ保存する設計にはしません。

---

# 16. Error Handling 方針

Frontendではエラーを大きく2種類に分けます。

## Field Error

例：

```text
メールアドレス未入力
パスワード文字数不足
メールアドレス重複
```

入力欄に関連するエラーはInput付近に表示します。

---

## Page / API Error

例：

```text
ユーザー情報取得失敗
ユーザー作成失敗
ユーザー更新失敗
ユーザー削除失敗
```

ErrorMessageを使用して表示します。

---

# 17. Loading State

API通信中は必要に応じてLoadingを表示します。

また、送信・削除処理中はButtonの `disabled` を利用し、二重操作を防止します。

例：

```text
作成中...
更新中...
削除中...
```

---

# 18. CSS設計方針

CSSは以下の責務を意識します。

## Component CSS

Component自身の見た目を管理します。

例：

```text
Button.css
Card.css
Input.css
Badge.css
Loading.css
ErrorMessage.css
UserForm.css
```

---

## Page CSS

画面固有の配置を管理します。

例：

```text
UserListPage.css
UserDetailPage.css
```

原則として、

```text
Component = 自分自身の見た目
Page = 画面内での配置
```

とします。

---

# 19. 共通化方針

BizSCでは、過剰な共通化を避けます。

共通化する基準：

* 複数箇所で実際に利用する
* 同じ責務を持っている
* 共通化によってコードが理解しやすくなる

以下の理由だけでは共通化しません。

```text
将来使うかもしれない
なんとなく再利用できそう
コードを短くしたいだけ
```

必要になった段階で共通化します。

---

# 20. TypeScript 方針

TypeScriptの型安全性を優先します。

原則：

* `any` を安易に使用しない
* API Responseは型を定義する
* catchしたerrorは安全に型判定する
* Component Propsを明示する
* optional値を明確に扱う

FrontendとBackendのデータ構造のずれを早期に発見できる構成を目指します。

---

# 21. Phase3 完了状態

Phase3ではFrontend CRUD UIを構築しました。

完了済み：

```text
User一覧
User詳細
User新規作成
User編集
User削除

React Router
Axios API通信

Loading表示
Error表示
Active / Inactive表示

Button
Card
Input
Loading
ErrorMessage
Badge
UserForm

共通UI見直し
User画面表示確認
CRUD一連のブラウザ動作確認
Frontend build確認
```

Phase3完了後、変更内容はGitHubへPush済みです。

---

# 22. 開発時の基本方針

BizSCでは以下を基本とします。

1. 小さい単位で実装する
2. 実装後にブラウザで確認する
3. 必要に応じてDockerログを確認する
4. APIはSwagger UIでも確認する
5. DatabaseはTablePlusでも確認する
6. Backendの責務をRouter / Service / Repositoryに分離する
7. Frontendの責務をPage / Component / APIに分離する
8. TypeScriptの型安全性を優先する
9. 過剰な共通化を避ける
10. 動作確認後にCommitする
11. Phaseなど大きな区切りでPushする

---

# 23. Documentation

BizSCでは以下のドキュメントを管理します。

```text
README.md
docs/
├─ project-overview.md
├─ architecture.md
├─ handover_phase.md
└─ decisions/
```

## README.md

プロジェクト全体の入口。

---

## project-overview.md

現在の進捗・完了Phase・次の作業を管理します。

---

## architecture.md

現在のシステム構成・設計・責務分離を管理します。

---

## handover_phase.md

別チャット・次Phaseへの引継ぎ資料です。

「次に何をするか」をarchitecture.mdより詳細に記録します。

---

## decisions/

重要な設計判断を記録します。

---

# 24. 現在地点

```text
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
完了・GitHub Push済み

Phase4
次フェーズ
  ↓
次チャットから開始
```

Phase4の具体的な実装内容・手順については、`handover_phase.md` および `project-overview.md` を基準として開始します。
