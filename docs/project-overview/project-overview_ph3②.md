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

### API

* [x] Health Check API
* [x] DB接続確認API

### 動作確認

* [x] usersテーブル作成確認
* [x] alembic_version確認
* [x] TablePlus接続確認

---

## Phase 2：ユーザーCRUD実装

### Repository

* [x] UserRepository作成
* [x] get_by_id()
* [x] get_by_email()
* [x] get_all()
* [x] create()
* [x] update()
* [x] delete()

### Schema

* [x] UserCreate
* [x] UserUpdate
* [x] UserResponse
* [x] UserListResponse
* [x] Emailバリデーション
* [x] Passwordバリデーション
* [x] model_validatorによる更新チェック
* [x] パスワード制約の共通化

### Service

* [x] UserService作成
* [x] create_user()
* [x] get_user()
* [x] get_users()
* [x] update_user()
* [x] delete_user()

### Security

* [x] pwdlib(argon2)導入
* [x] パスワードハッシュ化
* [x] パスワード検証関数

### Router

* [x] POST /users
* [x] GET /users
* [x] GET /users/{id}
* [x] PATCH /users/{id}
* [x] DELETE /users/{id}

### Error Handling

* [x] AppError
* [x] UserNotFoundError
* [x] EmailAlreadyRegisteredError
* [x] 共通Exception Handler
* [x] Routerから例外処理を分離

### Validation

* [x] UserCreateバリデーション
* [x] UserUpdateバリデーション
* [x] 空更新防止
* [x] Swaggerによる動作確認

### Test

* [x] pytest導入
* [x] httpx導入
* [x] TestClient導入
* [x] Health APIテスト
* [x] Health DB APIテスト

### 動作確認

* [x] CRUD API確認
* [x] Swagger UI確認
* [x] Exception Handler確認
* [x] Schema Validation確認
* [x] pytest実行確認

---

## Phase 3：フロントエンド基盤

### Routing

* [x] React Router導入
* [x] BrowserRouter設定
* [x] AppRoutes作成
* [x] NotFoundPage作成

### API

* [x] Axios導入
* [x] API Client作成
* [x] 環境変数管理（VITE_API_BASE_URL）
* [x] API Client共通設定
* [x] Health API連携
* [x] Users API連携

### Layout

* [x] MainLayout作成
* [x] Header作成
* [x] Sidebar作成
* [x] Footer作成
* [x] MainLayout.css作成

### Pages

* [x] HomePage作成
* [x] UserListPage作成
* [x] NotFoundPage作成

### Types

* [x] HealthResponse
* [x] User
* [x] UserListResponse

### 動作確認

* [x] React Router動作確認
* [x] Headerリンク遷移確認
* [x] FastAPIとのAPI通信確認
* [x] User一覧取得確認

---

# 現在の構成

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

Docker Compose により

* backend
* frontend
* db

の3コンテナが同時起動する。

---

# 次のマイルストーン

## Phase 3（継続）

* 共通UIコンポーネント（Button / Input / Card）
* レイアウトCSS改善
* User一覧画面改善
* ローディング表示
* エラー表示
* 空データ表示
* User詳細画面
* User作成画面
* User編集画面
* User削除画面

---

---

## Phase 4：ユーザー管理

* ユーザー検索
* ページネーション
* ソート
* フィルタ
* 共通レスポンス設計
* APIレスポンス改善
* OpenAPI改善
* CRUDテスト拡充

---

## Phase 5：BizSC業務機能

* 業務管理機能
* 権限管理
* ダッシュボード
* 各種マスタ管理
* ログ管理

---

# 現在採用している設計

* Layered Architecture
* Repository Pattern
* Service Layer
* SQLAlchemy 2.x
* Alembic Migration
* Pydantic Validation
* FastAPI Dependency Injection
* FastAPI Exception Handler
* React Router
* Axios
* Docker Compose
* 型安全を重視した設計

---

# 開発ルール

* Docker Compose を利用して開発する
* 小さな単位で Git Commit を行う
* 区切りごとに GitHub へ Push する
* 実装前に設計意図を理解する
* 「なぜその実装なのか」を重視する
* ドキュメントを継続的に更新する
* テストを実行してからコミットする

---

# 関連ドキュメント

* README.md
* architecture.md
* handover.md
* decisions/
* docs/

---

# 現在のステータス

**Phase 3（フロントエンド基盤）進行中**

現在は以下が利用可能です。

* React Router
* 共通レイアウト（Header / Sidebar / Footer）
* API Client（Axios）
* Health API通信
* User一覧取得
* ReactとFastAPIのAPI連携

**次回は、共通UIコンポーネントの作成とUser管理画面の改善を進める。**
