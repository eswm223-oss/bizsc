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
Pages
    │
    ▼
API Module
    │
    ▼
Axios Client
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

すべて Docker Compose 上で動作する。

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
- SQLAlchemy 2.x
- Pydantic v2
- Alembic
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

## Development

- Cursor
- Docker Desktop
- GitHub Desktop
- TablePlus

---

# ディレクトリ構成

## Frontend

```text
frontend/src/

api/
components/
    Button/
    Card/
    ErrorMessage/
    Input/
    Loading/
    UserForm/
layouts/
pages/
routes/
types/
```

## Backend

```text
backend/app/

api/
core/
db/
models/
repositories/
schemas/
services/
main.py
```

責務ごとのレイヤー分離を維持する。

---

# Frontend設計

## Pages

Pagesは画面単位の責務を持つ。

現在実装済み

- HomePage
- UserListPage
- UserDetailPage
- UserCreatePage
- UserEditPage
- NotFoundPage

担当する責務

- URL取得
- API呼び出し
- State管理
- Loading表示
- Error表示
- 画面遷移

---

## Components

共通UI

- Button
- Card
- ErrorMessage
- Input
- Loading
- UserForm

複数画面で利用できるUIのみ配置する。

---

## UserForm

Phase3で追加した共通フォーム。

目的

- Create/Edit画面の重複削減
- UI統一
- 保守性向上

担当

- Email入力
- Password入力（Createのみ）
- Active入力（Editのみ）
- Submitボタン
- Submit状態表示

担当しないもの

- API通信
- バリデーション
- 画面遷移
- Axiosエラー処理

これらはPage側で管理する。

---

## API Module

画面からAxiosを直接利用しない。

```text
Page
    │
    ▼
API Module
    │
    ▼
Axios Client
```

現在

users.ts

- getUsers()
- getUser()
- createUser()
- updateUser()
- deleteUser()

---

## Types

共通型は

src/types

へ集約する。

User関連

- User
- UserListResponse
- UserCreate
- UserUpdate

---

# Routing

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

React Router により SPA遷移を行う。

---

# Backendアーキテクチャ

Layered Architecture

```text
Request
    │
Router
    │
Service
    │
Repository
    │
Database
```

## Router

担当

- URL定義
- Request受け取り
- Service呼び出し
- Response返却

## Service

担当

- 業務ロジック
- Password Hash
- Validation
- 独自例外送出

## Repository

担当

- CRUD
- SQLAlchemy操作

---

# API

現在利用

```text
GET     /health
GET     /health/db

POST    /users
GET     /users
GET     /users/{id}
PATCH   /users/{id}
DELETE  /users/{id}
```

FrontendはUser CRUDをすべて利用している。

---

# バリデーション

Frontend

- 必須
- Password8文字以上

Backend

- EmailStr
- model_validator
- Request Schema

Backendを最終保証とする。

---

# エラーハンドリング

Backend

- AppError
- UserNotFoundError
- EmailAlreadyRegisteredError

Frontend

- Axios
- Email重複
- Validation Error
- 共通Error表示

---

# Loading設計

State

- isLoading
- isSubmitting
- isDeleting

処理中

- Loading表示
- ボタン無効
- 二重送信防止

---

# 共通化方針

現在共通化済み

- Button
- Card
- ErrorMessage
- Input
- Loading
- UserForm

処理の共通化ではなく

**UIの共通化**

を優先する。

---

# 今後の予定

## Phase3

- Button配置調整
- Status表示改善
- UI調整

## Phase4

- User検索
- ページネーション
- ソート
- フィルタ
- CRUDテスト追加

## Phase5

- 業務管理
- 権限管理
- ダッシュボード
- マスタ管理
- ログ管理

---

# Git運用

- 小さい単位でCommit
- フェーズ単位でPush
- 動作確認後Commit
- ドキュメント更新

---

# ドキュメント

継続更新

- README.md
- project-overview.md
- architecture.md
- handover_phase.md
- decisions/

---

# 設計原則

継続する方針

- Layered Architecture
- Repository Pattern
- Service Layer
- SQLAlchemy2
- Pydantic
- Dependency Injection
- Exception Handler
- React Router
- Axios
- API Module
- UserFormによるUI共通化
- 型安全
- 保守性・拡張性優先

---

# 現在の到達点

Phase3終盤まで完了。

現在利用可能

- User一覧
- User詳細
- User新規作成
- User編集
- User削除
- 共通レイアウト
- 共通UI
- UserForm共通化

次回は

- UI改善
- Button配置調整
- Status表示改善

から開始する。