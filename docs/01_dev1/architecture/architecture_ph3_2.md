# BizSC Architecture

## 目的

本ドキュメントは BizSC の設計思想を記録する。

コードだけでは伝わらない「なぜこの設計にしたのか」を残し、将来の保守性・拡張性を高めることを目的とする。

---

# 基本設計方針

本プロジェクトでは以下を最優先とする。

* 可読性
* 保守性
* 拡張性
* 型安全
* テスタビリティ
* 理解しながら開発すること

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
Axios
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

* Python 3.13
* FastAPI
* Uvicorn
* SQLAlchemy 2.x
* Pydantic v2
* Alembic
* pwdlib（Argon2）

### 採用理由

* 型安全
* OpenAPI 自動生成
* 高速なAPI開発
* 実務利用実績
* 保守しやすいレイヤー構成

---

## Frontend

* React
* TypeScript
* Vite
* React Router
* Axios

### 採用理由

* コンポーネント指向
* TypeScriptによる型安全
* SPA構成
* API通信の共通化
* 高速な開発体験

---

## Database

* PostgreSQL 17

### 採用理由

* 実務採用率が高い
* 高い信頼性
* 将来的な拡張性

---

## Infrastructure

* Docker
* Docker Compose

### 採用理由

* 開発環境の統一
* OS差異の吸収
* 本番との差異を最小化

---

# ディレクトリ構成

```text
bizsc/
│
├── backend/
├── frontend/
├── docs/
├── docker/
├── compose.yaml
├── README.md
├── .gitignore
└── .editorconfig
```

---

# Backend構成

```text
backend/
│
├── alembic/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
├── alembic.ini
└── requirements.txt
```

---

# Frontend構成

```text
frontend/
└── src/
    ├── api/
    │   ├── client.ts
    │   ├── health.ts
    │   └── users.ts
    │
    ├── components/
    │   ├── Header.tsx
    │   ├── Sidebar.tsx
    │   └── Footer.tsx
    │
    ├── layouts/
    │   ├── MainLayout.tsx
    │   └── MainLayout.css
    │
    ├── pages/
    │   ├── HomePage.tsx
    │   ├── UserListPage.tsx
    │   └── NotFoundPage.tsx
    │
    ├── routes/
    │   └── AppRoutes.tsx
    │
    ├── types/
    │   ├── health.ts
    │   └── user.ts
    │
    └── utils/
```

---

# フロントエンド設計

## pages

画面単位のコンポーネントを配置する。

Routerから直接表示される画面は pages 配下で管理する。

---

## components

再利用可能なUIコンポーネントを配置する。

例

* Header
* Sidebar
* Footer
* Button（予定）
* Input（予定）

---

## layouts

画面共通レイアウトを管理する。

共通レイアウトは MainLayout に集約する。

```text
MainLayout
├── Header
├── Sidebar
├── Outlet
└── Footer
```

Outlet に各ページが表示される。

---

## routes

URLとページの対応を管理する。

AppRoutes はルーティングのみを責務とし、画面の実装は持たない。

---

## api

API通信を集約する。

画面からAxiosを直接呼び出さず、必ず api 配下を経由する。

例

```text
health.ts
users.ts
```

---

## types

TypeScriptの型定義を管理する。

画面ごとに型を定義せず、共通利用する。

---

# API通信設計

API通信は以下の流れとする。

```text
Page
   │
   ▼
API Module
   │
   ▼
Axios Client
   │
HTTP
   ▼
FastAPI
```

責務

* Page：画面表示・状態管理
* API Module：API呼び出し
* Axios Client：共通設定
* FastAPI：API提供

API URLやHeader設定は client.ts に集約する。

---

# アーキテクチャ

Layered Architecture を採用する。

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

各レイヤーは単一責任となるよう設計する。

---

## Router

責務

* HTTPリクエスト受付
* Request Schema受け取り
* Service呼び出し
* Response Schema返却

ビジネスロジックは実装しない。

---

## Service

責務

* ビジネスロジック
* Repository呼び出し
* ドメインルール管理

DB操作を直接行わない。

---

## Repository

責務

* SQLAlchemy操作
* CRUD処理
* ORM管理

ビジネスロジックを持たない。

---

## Schema（Pydantic）

責務

* 入力チェック
* レスポンス整形
* 型保証

採用機能

* EmailStr
* Field
* ConfigDict
* model_validator

---

## Model（SQLAlchemy）

責務

* テーブル定義
* ORMマッピング

データ構造のみを保持する。

---

# Database設計

* SQLAlchemy 2.x
* DeclarativeBase
* Mapped[]
* mapped_column()

Migrationは Alembic により管理する。

DB変更は必ず Migration を経由する。

---

# 例外設計

```text
AppError
│
├── UserNotFoundError
└── EmailAlreadyRegisteredError
```

Service層で例外を送出し、FastAPIの共通Exception HandlerでHTTPレスポンスへ変換する。

---

# バリデーション設計

入力値検証はPydanticで実施する。

* Field
* model_validator

ビジネスロジックに到達する前に入力値を保証する。

---

# セキュリティ設計

パスワードは平文保存しない。

採用

* pwdlib
* Argon2

認証機能はPhase4で実装予定。

---

# API設計

現在実装済み

```text
GET    /health
GET    /health/db

POST   /users
GET    /users
GET    /users/{id}
PATCH  /users/{id}
DELETE /users/{id}
```

---

# テスト設計

現在

* pytest
* FastAPI TestClient
* httpx

実装済み

* Health API
* Health DB API

今後

* User CRUD API
* Repositoryテスト
* Serviceテスト
* Frontendコンポーネントテスト

---

# Git運用

* 小さな単位でCommit
* フェーズ単位でPush
* mainブランチを常に動作可能に保つ
* テスト成功後にCommitする

---

# ドキュメント運用

* README.md：プロジェクト概要
* project-overview.md：進捗管理
* architecture.md：設計思想
* handover.md：フェーズ引き継ぎ
* decisions/：設計判断の記録

---

# 今後の設計方針

Phase3以降も以下を維持する。

* Layered Architecture
* Repository Pattern
* Service Layer
* React Router
* Axios
* SQLAlchemy 2.x
* Alembic Migration
* Pydantic Validation
* FastAPI Dependency Injection
* FastAPI Exception Handler
* Docker Compose
* 型安全を重視した設計
* 保守性・拡張性を優先する
