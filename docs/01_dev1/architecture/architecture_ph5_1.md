# BizSC Architecture

## 1. 概要

BizSC は、以下の技術スタックで構成する Web アプリケーション。

- Backend: FastAPI / Python
- Frontend: React / TypeScript / Vite
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migration: Alembic
- HTTP Client: Axios
- UI / CSS: Bootstrap + Custom CSS
- Container: Docker / Docker Compose

開発環境は Windows を前提とし、Cursor、GitHub Desktop、Docker Desktop、Docker Compose、TablePlus を主に使用する。

## 2. 全体構成

```text
Browser
   ↓
React / TypeScript
   ↓ HTTP / Axios
FastAPI
   ↓
API Router
   ↓
Service
   ↓
Repository
   ↓ SQLAlchemy
PostgreSQL
```

Backend 内では API → Service → Repository → Database の責務分離を基本構成とする。

## 3. Docker構成

Docker Compose で frontend / backend / db の3サービスを管理する。

- frontend: React / TypeScript / Vite / Node.js、Port 5173
- backend: FastAPI / Python / SQLAlchemy / Alembic、Port 8000
- db: PostgreSQL、Port 5432

開発時の主なURL:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## 4. Backend Architecture

```text
Request
  ↓
API Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

主な構成:

```text
backend/
├─ app/
│  ├─ api/
│  ├─ core/
│  ├─ db/
│  ├─ models/
│  ├─ repositories/
│  ├─ schemas/
│  ├─ services/
│  └─ main.py
├─ alembic/
└─ tests/
```

## 5. User API

```text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

`GET /users` の Query Parameter:

- search
- is_active
- sort_by（default: id）
- sort_order（default: asc）
- page（default: 1）
- limit（default: 10）

API Layer は DB クエリを直接実行せず、Service を呼び出す。

## 6. Service Layer

UserService の主な処理:

- create_user()
- get_user()
- get_users()
- update_user()
- delete_user()

主な責務は Repository 呼び出し、ユーザー存在確認、メールアドレス重複確認、Password Hash 化、更新データ処理、Domain Error 発生、一覧データと total の組み立て。

一覧取得では Repository.get_all() と Repository.count_all() を呼び出し、users と total を API Layer に返す。

## 7. Repository Layer

UserRepository の主なメソッド:

- get_by_id()
- get_by_email()
- get_all()
- count_all()
- create()
- update()
- delete()

Repository Layer は SQLAlchemy を使用した Database Access を担当する。

## 8. User一覧取得

`GET /users` は以下をサポートする。

- 一覧取得
- メールアドレス部分一致検索
- Active / Inactive フィルタ
- ソート
- ページネーション
- 総件数取得

### Search

`search` が指定された場合、User.email に対して部分一致検索を行う。

### Active Filter

`is_active` は true / false / None を扱い、None の場合は Active / Inactive の両方を対象とする。

### Sort

対応する `sort_by`:

- id
- email
- created_at
- updated_at

`sort_order` は asc / desc。

Repository 内で許可された SQLAlchemy Column に変換してソートする。

### Pagination

```python
offset = (page - 1) * limit
```

`offset()` と `limit()` を使用してページネーションする。

## 9. UserListResponse

User 一覧APIは配列だけではなく総件数も返す。

```json
{
  "users": [],
  "total": 0
}
```

`total` はページネーション後の件数ではなく、検索・フィルタ条件に一致する全件数を表す。そのため get_all() と count_all() を分けて実行する。

## 10. Frontend Architecture

主な構成:

```text
frontend/
└─ src/
   ├─ api/
   ├─ components/
   ├─ pages/
   ├─ routes/
   └─ types/
```

基本的なデータフロー:

```text
User操作
   ↓
React Component
   ↓
API Function
   ↓
Axios
   ↓
FastAPI
   ↓
Response
   ↓
React State 更新
   ↓
再レンダリング
```

## 11. User List Frontend

`/users` の主な機能:

- User 一覧表示
- メール検索
- Active / Inactive フィルタ
- ソート
- ページネーション
- Loading 表示
- Error 表示
- 0件表示
- User 詳細画面への遷移

検索フォームの入力値と実際の検索条件を分離し、検索実行時に条件を反映する。

ソートでは同じカラムをクリックすると asc / desc を切り替え、別カラムでは asc を基本とする。

ページ移動時も search / is_active / sort_by / sort_order を維持し、検索・フィルタ条件変更時は page=1 に戻す。

## 12. State Management

現在は React の `useState` を中心に画面状態を管理する。

代表的な State:

- users
- total
- searchInput
- search
- isActive
- sortBy
- sortOrder
- page
- limit
- isLoading
- error

## 13. Error Handling

Backend では Domain Error と HTTP Response の責務を分離する。

例:

- UserNotFoundError
- EmailAlreadyRegisteredError

Service Layer で Domain Error を発生させ、Exception Handler で HTTP Response に変換する。

Frontend では API Request 失敗時に Error State を設定して画面表示する。

## 14. Database / Migration

Database は PostgreSQL、ORM は SQLAlchemy、Migration は Alembic を使用する。

主要テーブルは users。

User Model の主要項目:

- id
- email
- hashed_password
- is_active
- created_at
- updated_at

Password は平文保存せず、Backend で Hash 化して保存する。

Database Schema の変更は Alembic Migration を介して管理する。

## 15. Testing Architecture

Backend のテストには pytest を使用する。

主なテスト対象:

- Health API
- User CRUD
- User Search
- User Active Filter
- User Sort
- User Pagination
- total

Phase4 最終確認では以下を実行し、全テスト PASSED を確認済み。

```powershell
docker compose exec backend pytest -v
```

## 16. Phase4 完了時点の確認状況

Phase4 の最終確認として以下を実施済み。

### Backend / Swagger

`GET /users` について search / is_active / sort_by / sort_order / page / limit が Swagger UI に表示され、API Response が正常であることを確認。

### Frontend / Browser

`/users` について以下を確認。

- 一覧表示
- 検索
- Active / Inactive フィルタ
- ソート
- ページネーション
- 条件維持
- 検索条件変更時の page=1
- 0件表示
- User詳細画面遷移

### Frontend Build

```powershell
docker compose exec frontend npm run build
```

成功確認済み。

### Backend Test

```powershell
docker compose exec backend pytest -v
```

全テスト PASSED 確認済み。

### Git / GitHub

Phase4 の変更を Commit / Push し、GitHub Repository へ反映済み。

## 17. Phase4 完了

Phase4 では User 一覧機能を中心に CRUD、検索、Active Filter、Sort、Pagination、total、Frontend UI、Backend Test まで実装・確認した。

さらに Swagger UI、Browser、Frontend Build、pytest、Git / GitHub の最終確認を完了。

これにより **Phase4 完了** とする。

## 18. Phase5 UI / CSS 方針

Phase5 では、既存機能のロジックを大きく変更せず、Frontend の見た目を最低限の業務アプリ風に整える。

UI / CSS の基本方針:

- Bootstrap を導入する
- Bootstrap が提供する既存の CSS クラスや UI スタイルを優先して使用する
- Bootstrap だけでは調整しにくい箇所のみ Custom CSS を追加する
- CSS を最初から全面的に自作しない
- 過度に凝ったデザインやアニメーションは対象外とする
- 既存の React / TypeScript の機能・状態管理・API 通信は可能な限り維持する

Phase5 で主に整える対象:

- アプリ全体の余白・横幅・基本レイアウト
- 見出し
- ボタン
- フォーム
- User 一覧テーブル
- Active / Inactive 表示
- 検索・フィルタ UI
- ページネーション
- User 作成画面
- User 詳細 / 編集画面
- Loading / Error / 0件表示

学習方針としては、Bootstrap を使って大部分の見た目を整えながら、必要になった CSS の基本（margin、padding、display、gap、width など）を都度確認する。

Phase5 のゴールは、BizSC の各画面を「最低限それらしい Web / 業務アプリの見た目」に統一すること。

## 19. Repository

BizSC Repository:

https://github.com/eswm223-oss/bizsc

コードの詳細確認が必要な場合は、引継ぎ資料だけで判断せず、GitHub Repository の最新コードを確認する。
