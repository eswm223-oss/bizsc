# BizSC Project Overview

## プロジェクト概要

BizSC は、FastAPI・React・PostgreSQL を利用した Web アプリケーションです。

本プロジェクトは単に動作するシステムを作ることを目的とせず、設計意図を理解しながら、保守性・拡張性を重視した実務レベルの開発を目指します。

---

# 現在の進捗

## Phase0：開発環境構築

### プロジェクト

- [x] GitHub リポジトリ作成
- [x] Cursor 開発環境構築
- [x] ディレクトリ構成作成
- [x] README.md 作成
- [x] .gitignore 作成
- [x] .editorconfig 作成

### Docker

- [x] backend Dockerfile
- [x] frontend Dockerfile
- [x] compose.yaml
- [x] Docker Compose起動
- [x] Bind Mount
- [x] node_modules Volume

### Backend

- [x] FastAPI構築
- [x] Swagger UI
- [x] Health API

### Frontend

- [x] React
- [x] TypeScript
- [x] Vite

### Database

- [x] PostgreSQL

---

## Phase1：バックエンド基盤

### Settings

- [x] Settings
- [x] .env
- [x] Pydantic Settings

### Database

- [x] SQLAlchemy
- [x] Engine
- [x] Session
- [x] get_db

### Migration

- [x] Alembic
- [x] Migration
- [x] usersテーブル作成

### API

- [x] Health
- [x] Health DB

---

## Phase2：User CRUD API

### Repository

- [x] get_by_id
- [x] get_by_email
- [x] get_all
- [x] create
- [x] update
- [x] delete

### Service

- [x] create_user
- [x] get_user
- [x] get_users
- [x] update_user
- [x] delete_user

### Router

- [x] POST /users
- [x] GET /users
- [x] GET /users/{id}
- [x] PATCH /users/{id}
- [x] DELETE /users/{id}

### Validation

- [x] Email
- [x] Password
- [x] model_validator

### Error

- [x] AppError
- [x] UserNotFoundError
- [x] EmailAlreadyRegisteredError
- [x] Exception Handler

### Test

- [x] pytest
- [x] Health API
- [x] CRUD確認

---

## Phase3：フロントエンド基盤

### Routing

- [x] React Router
- [x] BrowserRouter
- [x] MainLayout
- [x] NotFoundPage

### API

- [x] Axios
- [x] API Client
- [x] getUsers
- [x] getUser
- [x] createUser

### Layout

- [x] Header
- [x] Sidebar
- [x] Footer
- [x] MainLayout

### 共通UI

- [x] Button
- [x] Input
- [x] Card
- [x] Loading
- [x] ErrorMessage

### Pages

- [x] HomePage
- [x] UserListPage
- [x] UserDetailPage
- [x] UserCreatePage
- [x] NotFoundPage

### User一覧画面

- [x] Card化
- [x] Loading
- [x] Error表示
- [x] Empty表示
- [x] Table表示
- [x] 詳細リンク
- [x] 新規作成リンク

### User詳細画面

- [x] GET /users/{id}
- [x] 詳細表示
- [x] 一覧へ戻る

### User新規作成

- [x] Email入力
- [x] Password入力
- [x] POST /users
- [x] バリデーション
- [x] APIエラー表示
- [x] Email重複表示
- [x] 作成成功後一覧へ戻る

### 動作確認

- [x] User一覧取得
- [x] User詳細取得
- [x] User作成
- [x] Email重複確認
- [x] Loading確認
- [x] Error確認

---

# 現在の構成

```text
Browser
    │
React
    │
React Router
    │
API Module
    │
Axios Client
    │
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

- backend
- frontend
- db

の3コンテナが同時起動する。

---

# 次のマイルストーン

## Phase3（継続）

### User編集

- [ ] UserUpdate型
- [ ] updateUser()
- [ ] UserEditPage
- [ ] PATCH連携
- [ ] 編集成功後詳細へ戻る

### User削除

- [ ] 削除ボタン
- [ ] DELETE API
- [ ] 削除確認
- [ ] 一覧へ戻る

### UI改善

- [ ] Form共通化
- [ ] Button配置調整
- [ ] ステータス表示改善

---

## Phase4

- [ ] ユーザー検索
- [ ] ページネーション
- [ ] ソート
- [ ] フィルタ
- [ ] CRUDテスト拡充

---

## Phase5

- [ ] 業務管理
- [ ] 権限管理
- [ ] ダッシュボード
- [ ] マスタ管理
- [ ] ログ管理

---

# 現在採用している設計

- Layered Architecture
- Repository Pattern
- Service Layer
- SQLAlchemy 2.x
- Alembic
- Pydantic Validation
- FastAPI Dependency Injection
- FastAPI Exception Handler
- React Router
- Axios
- Docker Compose
- 型安全
- 共通UIコンポーネント
- API Module分離

---

# 開発ルール

- Docker Composeで開発する
- 小さな単位でCommit
- フェーズ単位でPush
- 実装理由を理解して進める
- テスト実施後にCommit
- ドキュメントを継続的に更新する

---

# 関連ドキュメント

- README.md
- architecture.md
- handover_phase.md
- decisions/

---

# 現在のステータス

**Phase3後半進行中**

現在利用可能

- User一覧
- User詳細
- User新規作成
- 共通レイアウト
- 共通UIコンポーネント
- API Client
- React Router
- FastAPI連携

**次回は UserEditPage の実装から開始する。**