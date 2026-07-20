# BizSC 引継ぎメモ（Phase1完了）

作成日：2026-07-18

---

# プロジェクト情報

## プロジェクト名

BizSC

## 技術スタック

### Backend

* Python 3.13
* FastAPI
* SQLAlchemy 2.x
* Alembic

### Frontend

* React
* TypeScript
* Vite

### Database

* PostgreSQL 17

### Infrastructure

* Docker
* Docker Compose

---

# 開発方針

* 可読性を最優先
* 保守性・拡張性を重視
* 型安全を意識する
* 実務レベルの設計を学びながら実装する
* 小さな単位でGit Commit
* 区切りでGitHubへPush
* ドキュメントを継続的に更新する

---

# Phase1 完了内容

## Settings管理

実装済み

* pydantic-settings
* app/core/config.py
* .env管理
* Settingsクラス
* database_urlプロパティ
* lru_cacheによる設定キャッシュ

---

## SQLAlchemy

実装済み

* Engine生成
* SessionLocal生成
* create_engine()
* database.py作成

---

## DB Session

実装済み

* get_db()
* Depends(get_db)
* Session自動Close

---

## Alembic

導入済み

実施内容

* alembic init
* env.py設定
* Base.metadata連携
* Settings経由でDB接続
* autogenerate設定

---

## Base

実装済み

```python
class Base(DeclarativeBase):
    pass
```

---

## Userモデル

作成済み

usersテーブル

* id
* email
* hashed_password
* is_active
* created_at
* updated_at

---

## Migration

実施済み

初回Migration生成

```bash
alembic revision --autogenerate
```

適用

```bash
alembic upgrade head
```

---

## 動作確認

確認済み

* Docker Compose起動
* FastAPI起動
* PostgreSQL接続
* Alembic正常動作
* usersテーブル作成
* alembic_version作成

---

## Health Check API

実装済み

```
GET /health/db
```

確認結果

```json
{
  "status": "ok",
  "database": "connected"
}
```

正常動作確認済み

---

# 現在のディレクトリ構成

```text
backend/
│
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   │   ├── base.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic.ini
└── requirements.txt
```

---

# 現在のDB構成

テーブル

* users
* alembic_version

---

# 次回開始予定（Phase2）

以下の順番で進める。

1. Repository層作成
2. Schema(Pydantic)作成
3. Service層作成
4. API Router作成
5. CRUD実装
6. ユーザー登録API
7. ユーザー取得API
8. 更新API
9. 削除API
10. エラーハンドリング
11. バリデーション
12. 共通レスポンス設計

---

# 今後の設計方針

以下を維持する。

* Layered Architecture
* Settingsによる一元管理
* SQLAlchemy 2.xスタイル
* AlembicによるMigration管理
* Docker Composeによる開発
* Repository / Service 分離
* 型安全を維持する

---

# 補足

本プロジェクトは「動けば良い」ではなく、実務レベルの設計を理解しながら開発することを目的としている。

そのため、新しい実装を行う際は以下を重視する。

* なぜその設計なのか
* 他の設計との比較
* 将来的な拡張性
* 保守性
* 実務で一般的な構成
