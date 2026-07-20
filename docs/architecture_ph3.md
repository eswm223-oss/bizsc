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
- pwdlib (Argon2)

### 採用理由

- 型安全
- OpenAPI 自動生成
- 高速なAPI開発
- 実務利用実績
- 保守しやすいレイヤー構成

---

## Frontend

- React
- TypeScript
- Vite

### 採用理由

- コンポーネント指向
- TypeScript による型安全
- 高速な開発体験

---

## Database

- PostgreSQL 17

### 採用理由

- 実務採用率が高い
- 高い信頼性
- 将来的な拡張性

---

## Infrastructure

- Docker
- Docker Compose

### 採用理由

- 開発環境の統一
- OS差異の吸収
- 本番との差異を最小化

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
│   │   └── users.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   └── exception_handlers.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   │
│   └── main.py
│
├── tests/
│   └── test_health.py
│
├── alembic.ini
└── requirements.txt
```

---

# アーキテクチャ

本プロジェクトでは Layered Architecture を採用する。

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

- HTTPリクエスト受付
- Request Schema受け取り
- Service呼び出し
- Response Schema返却

Routerではビジネスロジックを実装しない。

---

## Service

責務

- ビジネスロジック
- 入力値判定
- Repository呼び出し
- ドメインルール管理

ServiceはDB操作を直接行わない。

---

## Repository

責務

- SQLAlchemy操作
- CRUD処理
- ORM管理

Repositoryはビジネスロジックを持たない。

---

## Schema（Pydantic）

責務

- 入力チェック
- レスポンス整形
- 型保証

採用している機能

- EmailStr
- Field
- ConfigDict
- model_validator

---

## Model（SQLAlchemy）

責務

- テーブル定義
- ORMマッピング

モデルはデータ構造のみを保持し、業務ロジックは持たない。

---

# Database設計

SQLAlchemy 2.x を採用する。

採用している書き方

- DeclarativeBase
- Mapped[]
- mapped_column()

Migrationは Alembic により管理する。

データベース変更は必ず Migration を経由して反映する。

---

# 例外設計

ビジネス例外は独自例外として管理する。

```text
AppError
│
├── UserNotFoundError
└── EmailAlreadyRegisteredError
```

Service層で例外を送出し、Routerでは捕捉しない。

FastAPIの共通Exception HandlerでHTTPレスポンスへ変換する。

```text
Service
    │
raise AppError
    │
FastAPI Exception Handler
    │
HTTP Response
```

これにより例外処理を一元管理できる。

---

# バリデーション設計

入力値検証はPydanticで実施する。

単項目

```python
Field(...)
```

複数項目

```python
@model_validator(mode="after")
```

ビジネスロジックに到達する前に入力値を保証する。

---

# セキュリティ設計

パスワードは平文で保存しない。

採用ライブラリ

- pwdlib
- Argon2

```text
Password
    │
Hash
    │
Database
```

認証機能はPhase4で実装予定。

---

# API設計

REST APIを採用する。

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

レスポンスはFastAPI標準のレスポンス設計を採用する。

---

# テスト設計

テストフレームワーク

- pytest
- FastAPI TestClient
- httpx

現在実装済み

- Health API
- Health DB API

今後追加予定

- User CRUD API
- Repositoryテスト
- Serviceテスト

---

# Frontend設計（Phase3予定）

```text
src/
│
├── api/
├── components/
├── hooks/
├── layouts/
├── pages/
├── routes/
├── services/
├── types/
└── utils/
```

責務ごとにディレクトリを分離する。

---

# Git運用

- 小さな単位でCommit
- フェーズ単位でPush
- mainブランチを常に動作可能に保つ
- テスト成功後にCommitする

---

# ドキュメント運用

README.md

プロジェクトの入口。

---

project-overview.md

進捗管理。

---

architecture.md

設計思想・採用理由・アーキテクチャを管理する。

---

handover_phase2.md

フェーズ終了時点の実装内容と次フェーズへの引継ぎを管理する。

---

decisions/

設計判断や技術選定を時系列で記録する。

---

# 今後の設計方針

Phase3以降も以下を維持する。

- Layered Architecture
- Repository Pattern
- Service Layer
- SQLAlchemy 2.x
- Alembic Migration
- Pydantic Validation
- FastAPI Dependency Injection
- FastAPI Exception Handler
- Docker Compose
- 型安全を重視した設計
- 実務で保守しやすい構成を優先する