# BizSC Project Overview

## プロジェクト概要

BizSC は、FastAPI・React・PostgreSQL を利用した Web
アプリケーションです。

本プロジェクトは単に動作するシステムを作ることを目的とせず、設計意図を理解しながら、保守性・拡張性を重視した実務レベルの開発を目指します。

------------------------------------------------------------------------

# 現在の進捗

## Phase0：開発環境構築

### プロジェクト

-   [x] GitHub リポジトリ作成
-   [x] Cursor 開発環境構築
-   [x] ディレクトリ構成作成
-   [x] README.md 作成
-   [x] .gitignore 作成
-   [x] .editorconfig 作成

### Docker

-   [x] backend Dockerfile
-   [x] frontend Dockerfile
-   [x] compose.yaml
-   [x] Docker Compose起動
-   [x] Bind Mount
-   [x] node_modules Volume

### Backend

-   [x] FastAPI構築
-   [x] Swagger UI
-   [x] Health API

### Frontend

-   [x] React
-   [x] TypeScript
-   [x] Vite

### Database

-   [x] PostgreSQL

------------------------------------------------------------------------

## Phase1：バックエンド基盤

-   [x] Settings
-   [x] Database
-   [x] SQLAlchemy
-   [x] Alembic
-   [x] Health API

------------------------------------------------------------------------

## Phase2：User CRUD API

-   [x] Repository
-   [x] Service
-   [x] Router
-   [x] Validation
-   [x] Exception Handler
-   [x] pytest
-   [x] User CRUD API完成

------------------------------------------------------------------------

## Phase3：フロントエンド

### Routing

-   [x] React Router
-   [x] MainLayout
-   [x] NotFoundPage

### API

-   [x] Axios
-   [x] API Client
-   [x] getUsers
-   [x] getUser
-   [x] createUser
-   [x] updateUser
-   [x] deleteUser

### 共通UI

-   [x] Button
-   [x] Input
-   [x] Card
-   [x] Loading
-   [x] ErrorMessage

### Pages

-   [x] HomePage
-   [x] UserListPage
-   [x] UserDetailPage
-   [x] UserCreatePage
-   [x] UserEditPage
-   [x] NotFoundPage

### User機能

-   [x] 一覧
-   [x] 詳細
-   [x] 新規作成
-   [x] 編集
-   [x] 削除

### 動作確認

-   [x] User一覧取得
-   [x] User詳細取得
-   [x] User作成
-   [x] User編集
-   [x] User削除
-   [x] Email重複確認
-   [x] Loading確認
-   [x] Error確認

------------------------------------------------------------------------

# 現在の構成

``` text
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

Docker Compose により backend / frontend / db の3コンテナで動作する。

------------------------------------------------------------------------

# 次のマイルストーン

## Phase3（継続）

-   [ ] UserCreatePage と UserEditPage のForm共通化
-   [ ] Button配置調整
-   [ ] ステータス表示改善
-   [ ] UI調整

## Phase4

-   [ ] ユーザー検索
-   [ ] ページネーション
-   [ ] ソート
-   [ ] フィルタ
-   [ ] CRUDテスト拡充

## Phase5

-   [ ] 業務管理
-   [ ] 権限管理
-   [ ] ダッシュボード
-   [ ] マスタ管理
-   [ ] ログ管理

------------------------------------------------------------------------

# 現在採用している設計

-   Layered Architecture
-   Repository Pattern
-   Service Layer
-   SQLAlchemy 2.x
-   Alembic
-   Pydantic Validation
-   FastAPI Dependency Injection
-   FastAPI Exception Handler
-   React Router
-   Axios
-   Docker Compose
-   型安全
-   共通UIコンポーネント
-   API Module分離

------------------------------------------------------------------------

# 開発ルール

-   Docker Composeで開発する
-   小さな単位でCommit
-   フェーズ単位でPush
-   実装理由を理解して進める
-   テスト実施後にCommit
-   ドキュメントを継続的に更新する

------------------------------------------------------------------------

# 関連ドキュメント

-   README.md
-   architecture.md
-   handover_phase.md
-   decisions/

------------------------------------------------------------------------

# 現在のステータス

**Phase3後半完了**

現在利用可能

-   User一覧
-   User詳細
-   User新規作成
-   User編集
-   User削除
-   共通レイアウト
-   共通UIコンポーネント
-   API Client
-   React Router
-   FastAPI連携

**次回は Form共通化（UserCreatePage / UserEditPage）から開始する。**
