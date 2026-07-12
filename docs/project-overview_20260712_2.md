# BizSC Project Overview

## プロジェクト概要

BizSC は、FastAPI・React・PostgreSQL を用いた Web アプリケーションです。
開発環境は Docker Compose により統一し、バックエンド・フロントエンド・データベースをコンテナで管理します。

---

# 技術スタック

## Backend

* Python 3.13
* FastAPI
* Uvicorn

## Frontend

* React 19
* TypeScript
* Vite 8

## Database

* PostgreSQL 17

## Infrastructure

* Docker
* Docker Compose

## Development

* Git
* GitHub
* Cursor

---

# 現在の進捗

## 開発環境

* [x] プロジェクトディレクトリ作成
* [x] backend / frontend / docs ディレクトリ作成
* [x] README.md 作成
* [x] .gitignore 作成
* [x] .editorconfig 作成

## Docker

* [x] backend Dockerfile 作成
* [x] frontend Dockerfile 作成
* [x] compose.yaml 作成
* [x] Docker Compose 起動確認
* [x] Volume（Bind Mount / Named Volume）の設定
* [x] Backend・Frontend・PostgreSQL の同時起動確認

## Backend

* [x] FastAPI 初期構築
* [x] Hello API 作成
* [x] Swagger UI 動作確認

## Frontend

* [x] React (Vite + TypeScript) 初期構築
* [x] Docker 上で Vite 起動確認

## Database

* [x] PostgreSQL コンテナ起動
* [ ] FastAPI との接続
* [ ] ORM 導入（SQLAlchemy）
* [ ] マイグレーション導入（Alembic）

---

# 次のマイルストーン

## Phase 1：バックエンド基盤

* PostgreSQL 接続
* SQLAlchemy 導入
* Alembic 導入
* 設定ファイル整理

## Phase 2：API 基盤

* API ディレクトリ構成
* Router 整理
* Pydantic Schema 作成
* 共通レスポンス設計

## Phase 3：フロントエンド基盤

* React ディレクトリ整理
* API 通信（Fetch / Axios）
* 共通レイアウト
* 画面ルーティング

## Phase 4：BizSC 機能開発

* 認証機能
* ユーザー管理
* 業務機能
* 権限管理

---

# 開発ルール

* Docker Compose を使用して開発する
* 機能単位で Git Commit を行う
* 区切りごとに GitHub へ Push する
* 理解を優先し、手順だけを追わない
* エラーは原因を切り分けながら解決する
