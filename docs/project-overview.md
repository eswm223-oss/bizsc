# BizSC Project Overview

## プロジェクト概要

BizSC は、FastAPI・React・PostgreSQL を利用した Web アプリケーションです。

本プロジェクトは単に動作するシステムを作ることを目的とせず、設計意図を理解しながら、保守性・拡張性を重視した実務レベルの開発を目指します。

---

# 現在の進捗

## Phase 0：開発環境構築

### プロジェクト

* [x] GitHub リポジトリ作成
* [x] Cursor 開発環境構築
* [x] ディレクトリ構成作成
* [x] README.md 作成
* [x] .gitignore 作成
* [x] .editorconfig 作成

### Docker

* [x] backend Dockerfile 作成
* [x] frontend Dockerfile 作成
* [x] compose.yaml 作成
* [x] Docker Compose 起動確認
* [x] Bind Mount 設定
* [x] node_modules Volume 設定

### Backend

* [x] FastAPI 初期構築
* [x] Uvicorn 起動確認
* [x] Hello API 作成
* [x] Swagger UI 動作確認

### Frontend

* [x] React 作成
* [x] TypeScript 導入
* [x] Vite 導入
* [x] Docker 上で起動確認

### Database

* [x] PostgreSQL コンテナ作成
* [x] PostgreSQL 起動確認

---

## Phase 1：バックエンド基盤

### Settings

* [x] Settings管理
* [x] .env管理
* [x] Pydantic Settings導入

### Database

* [x] PostgreSQL接続
* [x] SQLAlchemy導入
* [x] Engine作成
* [x] SessionLocal作成
* [x] DBセッション管理（get_db）

### Migration

* [x] Alembic導入
* [x] Base作成
* [x] 初回Migration生成
* [x] Migration適用

### Model

* [x] Userモデル作成

### 動作確認

* [x] DB接続確認API
* [x] usersテーブル作成確認
* [x] alembic_version確認

---

# 現在の構成

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
    │
PostgreSQL
```

Docker Compose により

* backend
* frontend
* db

の3コンテナが同時起動する。

---

# 次のマイルストーン

## Phase 2：ユーザー機能（CRUD）

* User Schema 作成
* User Repository 作成
* User Service 作成
* User Router 作成
* ユーザー登録API
* ユーザー一覧API
* ユーザー詳細API
* ユーザー更新API
* ユーザー削除API
* バリデーション
* エラーハンドリング

---

## Phase 3：フロントエンド基盤

* React Router
* API Client
* 共通レイアウト
* ページ構成
* バックエンド連携

---

## Phase 4：BizSC 機能実装

* 認証
* ユーザー管理
* 業務機能
* 権限管理

---

# 開発ルール

* Docker Compose を利用して開発する
* 小さな単位で Git Commit を行う
* 区切りごとに GitHub へ Push する
* 理由を理解しながら実装する
* ドキュメントを継続的に更新する

---

# 関連ドキュメント

* README.md
* architecture.md
* decisions/
