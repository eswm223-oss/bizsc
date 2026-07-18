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
* 理解しながら開発すること

短期的な実装よりも、長期的に保守しやすい設計を採用する。

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
SQLAlchemy
    ▼
PostgreSQL
```

すべて Docker Compose 上で動作する。

---

# 技術スタック

## Backend

* Python 3.13
* FastAPI
* Uvicorn

### 採用理由

* 型安全
* OpenAPI 自動生成
* 高速なAPI開発
* 実務利用実績

---

## Frontend

* React
* TypeScript
* Vite

### 採用理由

* コンポーネント指向
* TypeScript による安全性
* 高速な開発体験

---

## Database

* PostgreSQL

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
* 本番との差異を少なくする

---

# ディレクトリ構成

```text
bizsc/

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

# Docker設計

Compose により以下を管理する。

* backend
* frontend
* db

Frontend は Bind Mount を利用する。

```yaml
./frontend:/app
```

Node.js の依存ライブラリはコンテナ側で保持する。

```yaml
/app/node_modules
```

これにより

* ソースコードはリアルタイム反映
* node_modules は OS に依存しない

という構成を採用する。

---

# Backend設計（実装済み）

```text
app/

├── api/
├── core/
│   └── config.py
├── db/
│   ├── base.py
│   └── database.py
├── models/
│   └── user.py
├── repositories/
├── schemas/
├── services/
└── main.py
```

レイヤードアーキテクチャを採用予定。

---

# Database設計

SQLAlchemy 2.x を採用する。

- DeclarativeBase
- Mapped[]
- mapped_column()

Migrationは Alembic により管理する。

データベース変更は必ず Migration を経由して反映する。

DBアクセスは以下のレイヤーで管理する。

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

責務を分離し、各層が単一責任となる構成を採用する。

---

# Frontend設計（予定）

```text
src/

├── api/
├── components/
├── layouts/
├── pages/
├── routes/
├── hooks/
├── services/
└── types/
```

責務ごとにディレクトリを分離する。

---

# Git運用

* 小さな単位で Commit
* 区切りで Push
* main ブランチを常に動作可能に保つ

---

# ドキュメント運用

README.md

プロジェクトの入口。

---

project-overview.md

現在の進捗を管理する。

---

architecture.md

設計思想を管理する。

---

decisions/

技術選定や設計判断を時系列で記録する。

このドキュメントは基本的に追加運用とし、過去の意思決定を残す。
