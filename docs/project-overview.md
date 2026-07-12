# BizSC プロジェクト概要

## プロジェクトの目的

BizSC は、学習用ではなく実際に運用することを前提としたWebアプリケーションとして開発する。

開発では以下を重視する。

* 保守性
* 拡張性
* 可読性
* AIとの協調開発
* Dockerによる環境統一
* 実務レベルの構成

---

# 技術スタック

## IDE

* Cursor

## AI

* Codex

## バージョン管理

* Git
* GitHub
* GitHub Desktop

## コンテナ

* Docker Desktop
* Docker Compose

## バックエンド

* Python
* FastAPI

## フロントエンド

* React
* TypeScript
* Vite

## データベース

* PostgreSQL

## ORM

* SQLAlchemy 2.x

## マイグレーション

* Alembic

---

# 開発環境

## OS

Windows

## 開発ディレクトリ

```text
D:\Development
```

## プロジェクト

```text
D:\Development\apps\bizsc
```

---

# GitHub

Repository

```text
bizsc
```

Visibility

Private

GitHub Desktop を利用して管理する。

---

# Docker

導入済み

```text
Docker version 29.5.2
Docker Compose version v5.1.4
```

Docker Compose により

* React
* FastAPI
* PostgreSQL

を起動する。

---

# プロジェクト構成

```text
bizsc/

├── .github/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── docker/
│
├── docs/
│
├── compose.yaml
├── .gitignore
├── .editorconfig
├── README.md
```

---

# Docker構成

```text
React (Vite)
        │
        ▼
FastAPI
        │
        ▼
PostgreSQL
```

Docker Compose によって各コンテナを管理する。

---

# 開発ルール

* `main` ブランチには常に動作するコードを保持する。
* 機能開発は `feature/<機能名>` ブランチで行う。
* AIが生成したコードはレビューしてから採用する。
* Docker環境を前提として開発する。
* GitHub Desktopを基本操作とする。
* README や docs を後回しにしない。
* 各ステップで動作確認を行う。

---

# AIとの開発方針

* 手順を中心に進める。
* 必要な理由のみ簡潔に説明する。
* AI（Cursor・Codex）の説明は補足程度に留める。
* 実務で一般的な構成を採用する。
* 機能追加は小さな単位で実施し、その都度動作確認を行う。

---

# 現在の進捗

* GitHub アカウント作成
* Git インストール
* Cursor インストール
* Docker Desktop インストール
* GitHub Desktop インストール
* Private Repository `bizsc` 作成
* ローカルへクローン完了

---

# 次回の作業

1. backend / frontend ディレクトリ作成
2. `.gitignore`
3. `.editorconfig`
4. `README.md`
5. Dockerfile（backend）
6. Dockerfile（frontend）
7. `compose.yaml`
8. FastAPI 初期構築
9. React（Vite + TypeScript）初期構築
10. PostgreSQL 接続
11. Docker 起動確認
12. 初回コミット
