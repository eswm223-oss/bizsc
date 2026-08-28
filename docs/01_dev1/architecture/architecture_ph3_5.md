# BizSC Architecture

## 目的

本ドキュメントは、BizSC の設計思想と現在のシステム構成を記録する。

コードだけでは伝わりにくい「なぜこの設計にしたのか」を残し、将来の保守性・拡張性を高めることを目的とする。

---

# 基本設計方針

本プロジェクトでは、以下を優先する。

- 可読性
- 保守性
- 拡張性
- 型安全
- テスタビリティ
- 理解しながら開発すること

短期的な実装速度だけを優先せず、長期的に保守しやすい構成を採用する。

---

# システム構成

```text
Browser
    │
    ▼
React（Vite）
    │
    ▼
React Router
    │
    ▼
API Module
    │
    ▼
Axios Client
    │
    ▼
HTTP
    │
    ▼
FastAPI
    │
    ▼
Router
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

すべてのサービスは Docker Compose 上で動作する。

```text
Docker Compose
├── frontend
├── backend
└── db
```

---

# 技術スタック

## Backend

- Python 3.13
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Pydantic v2
- Alembic
- pwdlib
- Argon2
- pytest

## Frontend

- React 19
- TypeScript
- Vite
- React Router
- Axios

## Database

- PostgreSQL 17

## Infrastructure

- Docker
- Docker Compose

## Development Tools

- Cursor
- GitHub Desktop
- Docker Desktop
- TablePlus

---

# ディレクトリ構成

## Frontend

```text
frontend/src/

├── api/
│   ├── client.ts
│   ├── health.ts
│   └── users.ts
│
├── components/
│   ├── Button/
│   ├── Card/
│   ├── ErrorMessage/
│   ├── Input/
│   └── Loading/
│
├── layouts/
│   └── MainLayout.tsx
│
├── pages/
│   ├── HomePage.tsx
│   ├── UserListPage.tsx
│   ├── UserDetailPage.tsx
│   ├── UserCreatePage.tsx
│   ├── UserEditPage.tsx
│   └── NotFoundPage.tsx
│
├── routes/
│   └── AppRoutes.tsx
│
└── types/
    ├── health.ts
    └── user.ts
```

## Backend

バックエンドは、責務ごとにレイヤーを分離する。

```text
backend/app/

├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/
└── main.py
```

実際のディレクトリ名は現在の実装を基準とし、役割の分離を維持する。

---

# Frontend設計

## Pages

`pages` には、画面単位の責務を持つコンポーネントを配置する。

現在の画面は以下のとおり。

- HomePage
- UserListPage
- UserDetailPage
- UserCreatePage
- UserEditPage
- NotFoundPage

画面コンポーネントでは、以下を担当する。

- URLパラメータの取得
- APIの呼び出し
- 画面固有のState管理
- Loading表示
- エラー表示
- 画面遷移
- 共通UIコンポーネントの組み合わせ

---

## Components

`components` には、複数画面で再利用可能なUIコンポーネントを配置する。

現在の共通UIは以下のとおり。

- Button
- Input
- Card
- Loading
- ErrorMessage

画面固有の処理を共通コンポーネントへ持たせすぎず、UIとして再利用できる責務に限定する。

---

## Layout

共通レイアウトは `MainLayout` に集約する。

```text
MainLayout
├── Header
├── Sidebar
├── Outlet
└── Footer
```

各ページは React Router の `Outlet` を通して表示する。

---

## API Module

画面から Axios を直接利用しない。

```text
Page
    │
    ▼
API Module
    │
    ▼
Axios Client
    │
    ▼
FastAPI
```

API通信は `src/api` を経由する。

現在の `users.ts` の主な関数は以下のとおり。

- `getUsers()`
- `getUser()`
- `createUser()`
- `updateUser()`
- `deleteUser()`

API処理を画面から分離することで、以下を実現する。

- 通信処理の再利用
- URL定義の集約
- 型の統一
- 画面コンポーネントの責務軽減
- 将来のAPI仕様変更への対応

---

## Types

共通で利用する型は `src/types` に集約する。

現在のUser関連型は以下のとおり。

- `User`
- `UserListResponse`
- `UserCreate`
- `UserUpdate`

`UserCreate` は新規作成時の入力値を表し、必要な項目を必須とする。

`UserUpdate` はPATCHによる部分更新に利用するため、更新可能な各項目を省略可能とする。

```ts
export type UserUpdate = {
  email?: string;
  password?: string;
  is_active?: boolean;
};
```

---

# Routing

現在のルーティングは以下のとおり。

```text
/
    HomePage

/users
    UserListPage

/users/new
    UserCreatePage

/users/:userId
    UserDetailPage

/users/:userId/edit
    UserEditPage

*
    NotFoundPage
```

React RouterによりSPA遷移を行う。

`userId` は `useParams()` で取得し、API呼び出し時に数値へ変換する。

---

# User画面設計

## User一覧画面

主な機能は以下のとおり。

- User一覧取得
- Card表示
- Table表示
- Loading表示
- Error表示
- Empty表示
- 詳細画面への導線
- 新規作成画面への導線

---

## User詳細画面

主な表示内容は以下のとおり。

- ID
- Email
- Active
- created_at
- updated_at

主な導線は以下のとおり。

- 編集画面へ移動
- User削除
- 一覧画面へ戻る

削除時は確認ダイアログを表示し、承認された場合のみDELETE APIを呼び出す。

削除成功後はUser一覧画面へ遷移する。

---

## User新規作成画面

入力項目は以下のとおり。

- Email
- Password

主な機能は以下のとおり。

- 必須チェック
- Password 8文字以上
- User作成API呼び出し
- 送信中のボタン無効化
- Loading表示
- APIエラー表示
- Email重複エラー表示
- 作成成功後に一覧画面へ遷移

---

## User編集画面

入力項目は以下のとおり。

- Email
- Active

現在のUser情報を `getUser()` で取得し、フォームの初期値として設定する。

更新時は `updateUser()` からPATCH APIを呼び出す。

主な機能は以下のとおり。

- URLからUser IDを取得
- 編集対象Userの取得
- フォーム初期値の設定
- Email必須チェック
- PATCH API呼び出し
- 更新中のボタン無効化
- Email重複エラー表示
- 入力エラー表示
- 更新成功後に詳細画面へ遷移

---

# Backendアーキテクチャ

BizSCのバックエンドでは、Layered Architectureを採用する。

```text
Request
    │
    ▼
Router
    │
    ▼
Service
    │
    ▼
Repository
    │
    ▼
Database
```

## Router

RouterはHTTPリクエストとレスポンスを担当する。

主な責務は以下のとおり。

- URL定義
- HTTPメソッド定義
- Request Schemaの受け取り
- Serviceの呼び出し
- Response Modelの指定
- HTTPステータスコードの指定

## Service

Serviceは業務処理を担当する。

主な責務は以下のとおり。

- Repositoryの呼び出し
- User存在確認
- Email重複確認
- Password Hash
- 例外の送出
- 更新可能項目の制御

## Repository

Repositoryはデータベースアクセスを担当する。

主な責務は以下のとおり。

- SELECT
- INSERT
- UPDATE
- DELETE
- SQLAlchemy Modelの操作

## Database

SQLAlchemyを通してPostgreSQLへアクセスする。

`get_db` によるDependency Injectionを利用し、API処理ごとにDB Sessionを受け渡す。

---

# API設計

現在の主なAPIは以下のとおり。

```text
GET     /health
GET     /health/db

POST    /users
GET     /users
GET     /users/{id}
PATCH   /users/{id}
DELETE  /users/{id}
```

Frontendでは、User CRUD APIをすべて利用している。

- `GET /users`
- `GET /users/{id}`
- `POST /users`
- `PATCH /users/{id}`
- `DELETE /users/{id}`

---

# バリデーション

## Frontend

現在の主な入力チェックは以下のとおり。

- 必須チェック
- Email入力
- Password 8文字以上

Frontendのバリデーションは、利用者へ早く入力エラーを知らせる目的で行う。

## Backend

BackendではPydanticによるバリデーションを行う。

主な仕組みは以下のとおり。

- `EmailStr`
- `Field`
- `model_validator`
- Request Schema

Backendのバリデーションを最終的な入力保証とする。

Frontendのチェックだけに依存しない。

---

# エラーハンドリング

## Backend

共通Exception Handlerを利用する。

主な独自例外は以下のとおり。

- `UserNotFoundError`
- `EmailAlreadyRegisteredError`
- `AppError`

Serviceで独自例外を送出し、Exception HandlerでHTTPレスポンスへ変換する。

## Frontend

Axios Error Handlingを利用する。

主な扱いは以下のとおり。

```text
409
└── Email重複エラー

422
└── 入力内容エラー

その他
└── 共通エラー表示
```

エラー内容に応じて、入力欄単位のエラーまたは画面全体のエラーとして表示する。

---

# Loading・送信状態

API通信中はStateで処理状態を管理する。

主なStateは以下のとおり。

- `isLoading`
- `isSubmitting`
- `isDeleting`

処理中は、以下を行う。

- Loadingコンポーネントを表示する
- 送信ボタンを無効化する
- ボタン表示を「作成中」「更新中」「削除中」へ変更する
- 二重送信を防止する

---

# 削除設計

User削除は詳細画面から実行する。

処理の流れは以下のとおり。

```text
削除ボタン押下
    │
    ▼
確認ダイアログ表示
    │
    ├── キャンセル
    │      └── 処理終了
    │
    └── OK
           │
           ▼
    DELETE /users/{id}
           │
           ▼
    User一覧画面へ遷移
```

削除前に確認処理を入れることで、利用者の誤操作を防ぐ。

---

# 共通UI設計

画面ごとに同じHTMLやスタイルを繰り返さず、共通コンポーネントを利用する。

現在の共通UIは以下のとおり。

- Button
- Input
- Card
- Loading
- ErrorMessage

ただし、共通化を目的に責務を過剰にまとめない。

複数画面で同じ構造や処理が確認できた段階で、共通化を検討する。

---

# 今後の実装予定

## Phase3 継続

- UserCreatePageとUserEditPageのフォーム共通化検討
- Button配置調整
- ステータス表示改善
- UI全体の調整

## Phase4

- User検索
- ページネーション
- ソート
- フィルタ
- CRUDテスト拡充

## Phase5

- 業務管理
- 権限管理
- ダッシュボード
- マスタ管理
- ログ管理

---

# Git運用

- 小さな単位でCommitする
- フェーズ単位でPushする
- 動作確認とテスト成功後にCommitする
- 実装理由が分かるCommit単位を意識する

User編集・削除機能の区切りでは、以下のCommitメッセージを利用できる。

```text
feat: implement user edit and delete features
```

---

# ドキュメント運用

以下のドキュメントを継続的に更新する。

- README.md
- project-overview.md
- architecture.md
- handover_phase.md
- decisions/

役割は以下のとおり。

- `project-overview.md`
  - プロジェクト全体の進捗とマイルストーン
- `architecture.md`
  - 現在の設計思想と技術構成
- `handover_phase.md`
  - 次のチャットや開発作業への引き継ぎ
- `decisions/`
  - 個別の設計判断と採用理由

---

# 設計原則

BizSCでは、以下を継続する。

- Layered Architecture
- Repository Pattern
- Service Layer
- SQLAlchemy 2.x
- Alembic
- Pydantic Validation
- FastAPI Dependency Injection
- FastAPI Exception Handler
- React Router
- Axios経由のAPI通信
- API Module分離
- 共通UIコンポーネントの再利用
- 型安全
- SPA遷移
- 保守性・拡張性の優先
- 実装理由を理解しながら進める

---

# 現在の到達点

Phase3後半まで完了している。

現在利用可能なUser機能は以下のとおり。

- 一覧
- 詳細
- 新規作成
- 編集
- 削除

User CRUDのFrontend連携は一通り完了した。

次の作業では、Phase3の残作業としてフォーム共通化やUI改善を検討する。
