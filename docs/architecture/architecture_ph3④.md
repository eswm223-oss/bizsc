# BizSC Architecture

## 目的

本ドキュメントは BizSC の設計思想を記録する。

コードだけでは伝わらない「なぜこの設計にしたのか」を残し、将来の保守性・拡張性を高めることを目的とする。

---

# 基本設計方針

本プロジェクトでは以下を最優先とする。

- 可読性
- 保守性
- 拡張性
- 型安全
- テスタビリティ
- 理解しながら開発すること

短期的な実装速度よりも、長期的に保守しやすい設計を採用する。

---

# システム構成

```text
Browser
    │
    ▼
React (Vite)
    │
React Router
    │
API Module
    │
Axios Client
    │
HTTP
    ▼
FastAPI
    │
Router
    │
Service
    │
Repository
    │
SQLAlchemy
    │
PostgreSQL
```

すべて Docker Compose 上で動作する。

---

# 技術スタック

## Backend

- Python 3.13
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Pydantic v2
- Alembic
- pwdlib（Argon2）

---

## Frontend

- React 19
- TypeScript
- Vite
- React Router
- Axios

---

## Database

- PostgreSQL 17

---

## Infrastructure

- Docker
- Docker Compose

---

# ディレクトリ構成

```text
frontend/src/

├── api/
│   ├── client.ts
│   ├── health.ts
│   └── users.ts

├── components/
│   ├── Button/
│   ├── Card/
│   ├── ErrorMessage/
│   ├── Input/
│   ├── Loading/

├── layouts/

├── pages/
│   ├── HomePage.tsx
│   ├── UserListPage.tsx
│   ├── UserDetailPage.tsx
│   ├── UserCreatePage.tsx
│   └── NotFoundPage.tsx

├── routes/
│   └── AppRoutes.tsx

├── types/
│   ├── health.ts
│   └── user.ts
```

---

# Frontend設計

## Pages

画面単位の責務を持つ。

現在実装済み

- HomePage
- UserListPage
- UserDetailPage
- UserCreatePage
- NotFoundPage

---

## Components

再利用可能なUIコンポーネントのみ配置する。

現在

- Button
- Input
- Card
- Loading
- ErrorMessage

---

## Layout

MainLayoutへ集約。

```text
MainLayout
├── Header
├── Sidebar
├── Outlet
└── Footer
```

---

## API Module

画面からAxiosを直接利用しない。

```text
Page
    ↓
API Module
    ↓
Axios Client
    ↓
FastAPI
```

現在

users.ts

- getUsers()
- getUser()
- createUser()

---

## Types

画面単位ではなく共通型として管理。

現在

- User
- UserListResponse
- UserCreate

---

# UI設計

一覧画面

- Card
- Table
- Loading
- ErrorMessage
- Empty表示

作成画面

- Card
- Input
- Button
- ErrorMessage

---

# Routing

現在

```text
/

/users

/users/new

/users/:userId
```

React RouterによりSPA遷移を行う。

---

# アーキテクチャ

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

各レイヤーは単一責任とする。

---

# API設計

現在

```text
GET     /health
GET     /health/db

POST    /users
GET     /users
GET     /users/{id}
PATCH   /users/{id}
DELETE  /users/{id}
```

Frontendで利用済み

- GET /users
- GET /users/{id}
- POST /users

---

# バリデーション

Frontend

- 必須チェック
- パスワード8文字以上

Backend

- Pydantic Validation
- EmailStr
- Field
- model_validator

---

# エラーハンドリング

Backend

Exception Handler

- UserNotFoundError
- EmailAlreadyRegisteredError

Frontend

Axios Error Handling

- 409
    - メールアドレス重複
- 422
    - 入力エラー
- その他
    - 共通エラー表示

---

# 共通UI設計

画面から直接HTMLを増やさず、共通Componentを利用する。

現在

- Button
- Input
- Card
- Loading
- ErrorMessage

---

# 今後の実装予定

Phase3

- UserEditPage
- UserDelete導線
- 共通Formコンポーネント化

Phase4

- 検索
- ページネーション
- ソート
- フィルタ

---

# Git運用

- 小さな単位でCommit
- フェーズ単位でPush
- テスト成功後にCommit

---

# ドキュメント運用

- README.md
- project-overview.md
- architecture.md
- handover_phase.md
- decisions/

---

# 設計原則

BizSCでは以下を徹底する。

- Layered Architecture
- Repository Pattern
- Service Layer
- React Router
- Axios経由のAPI通信
- 共通UIコンポーネントの再利用
- 型安全
- 保守性・拡張性を優先