# BizSC Project Overview

## 1. Project Name

**BizSC**

---

## 2. Project Overview

BizSC は、Web アプリケーション開発を通して Backend / Frontend / Database / Docker / Testing までを一通り実装・学習しながら、段階的に機能を拡張していくプロジェクト。

現在は User 管理機能を中心に基礎アーキテクチャを構築している。

Phase4 完了時点では、User CRUD に加えて一覧画面の検索・フィルタ・ソート・ページネーション、および Backend Test まで実装・動作確認済み。

---

## 3. Development Environment

開発環境:

- Windows
- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus

Repository:

https://github.com/eswm223-oss/bizsc

コードの詳細確認が必要な場合は、ドキュメントの記載だけで推測せず、GitHub Repository の最新コードを確認する。

---

## 4. Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- pytest

### Frontend

- React
- TypeScript
- Vite
- Axios
- React Router
- Bootstrap
- CSS（Bootstrapを基本とし、必要な箇所を自作CSSで調整）

### Database

- PostgreSQL

### Infrastructure / Development

- Docker
- Docker Compose
- GitHub
- GitHub Desktop
- Cursor
- TablePlus

---

## 5. Docker Services

BizSC は Docker Compose を使用して主に以下の3サービスを管理する。

```text
frontend
backend
db
```

開発時の主なURL:

```text
Frontend
http://localhost:5173

Backend
http://localhost:8000

Swagger UI
http://localhost:8000/docs
```

---

## 6. Overall Architecture

基本構成:

```text
Browser
   ↓
React / TypeScript
   ↓
Axios
   ↓
FastAPI
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

Backend では責務を以下のように分離する。

```text
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

### API

HTTP Request / Response を担当する。

### Service

ビジネスロジックを担当する。

### Repository

Database Access を担当する。

---

## 7. Backend Structure

主な Backend 構成:

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
│
├─ alembic/
└─ tests/
```

---

## 8. Frontend Structure

主な Frontend 構成:

```text
frontend/
└─ src/
   ├─ api/
   ├─ components/
   ├─ pages/
   ├─ routes/
   └─ types/
```

Frontend は React State を使用して画面状態を管理し、Axios を通して Backend API と通信する。

---

## 9. User Domain

現在の中心となる Domain は User。

User の主要データ:

```text
id
email
hashed_password
is_active
created_at
updated_at
```

Password は平文では Database に保存せず、Backend で Hash 化して保存する。

---

## 10. User API

現在実装済みの User API:

```text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

対応する主な機能:

```text
Create
Read
Update
Delete
List
Search
Filter
Sort
Pagination
```

---

## 11. User List API

`GET /users` は以下の Query Parameter に対応している。

```text
search
is_active
sort_by
sort_order
page
limit
```

デフォルト:

```text
search      = None
is_active   = None
sort_by     = id
sort_order  = asc
page        = 1
limit       = 10
```

---

## 12. Search

メールアドレスの部分一致検索に対応。

例:

```text
GET /users?search=alice
```

Backend では SQLAlchemy の条件として検索を追加する。

---

## 13. Active Filter

User の Active 状態による絞り込みに対応。

```text
is_active=true
is_active=false
```

`is_active` が指定されない場合は Active / Inactive の両方を対象とする。

---

## 14. Sort

対応する主なソート項目:

```text
id
email
created_at
updated_at
```

ソート順:

```text
asc
desc
```

例:

```text
GET /users?sort_by=email&sort_order=asc
```

---

## 15. Pagination

Query Parameter:

```text
page
limit
```

Backend の offset 計算:

```python
offset = (page - 1) * limit
```

例:

```text
page=1
limit=10
→ offset=0

page=2
limit=10
→ offset=10
```

---

## 16. User List Response

一覧 API は以下の形式で返却する。

```json
{
  "users": [],
  "total": 0
}
```

意味:

```text
users
= 現在のページに表示するUser一覧

total
= 検索・フィルタ条件に一致する全User件数
```

このため Repository では、

```text
get_all()
count_all()
```

を分けて実行する。

---

## 17. User Repository

主なメソッド:

```text
get_by_id()
get_by_email()
get_all()
count_all()
create()
update()
delete()
```

`get_all()` では主に、

```text
Search
Active Filter
Sort
Pagination
```

を処理する。

`count_all()` では、

```text
Search
Active Filter
```

を適用して総件数を取得する。

---

## 18. User Service

主なメソッド:

```text
create_user()
get_user()
get_users()
update_user()
delete_user()
```

Service の主な責務:

- Repository 呼び出し
- User存在確認
- Email重複確認
- Password Hash化
- User更新処理
- Domain Error
- 一覧データと total の取得

一覧取得:

```text
UserService.get_users()
       ↓
UserRepository.get_all()
UserRepository.count_all()
       ↓
users, total
```

---

## 19. Error Handling

Backend では Domain Error と HTTP Response を分離する。

代表例:

```text
UserNotFoundError
EmailAlreadyRegisteredError
```

基本フロー:

```text
Service
 ↓
Domain Error
 ↓
Exception Handler
 ↓
HTTP Response
```

Service Layer を HTTP 固有処理へ直接依存させない構成とする。

---

## 20. User List Frontend

User 一覧画面:

```text
/users
```

Phase4 完了時点で以下を実装済み。

- User一覧表示
- メール検索
- Active / Inactive フィルタ
- ソート
- ページネーション
- Loading表示
- Error表示
- 0件表示
- User詳細画面への遷移

---

## 21. Frontend State

User一覧画面で扱う主な State:

```text
users
total
searchInput
search
isActive
sortBy
sortOrder
page
limit
isLoading
error
```

検索フォームでは入力中の値と確定した検索条件を分離する。

```text
searchInput
 ↓
検索
 ↓
search
 ↓
API Request
```

検索・フィルタ条件変更時には `page=1` に戻す。

ページ移動時には検索・フィルタ・ソート条件を維持する。

---

## 22. Testing

Backend Test には pytest を使用する。

Phase4 完了時点の主な User API テスト:

- Create User
- Get User
- Update User
- Delete User
- Search
- Active Filter
- Sort
- Pagination
- total

最終確認コマンド:

```powershell
docker compose exec backend pytest -v
```

Phase4 最終確認で全テスト PASSED を確認済み。

---

## 23. Frontend Build

Phase4 最終確認で以下を実行済み。

```powershell
docker compose exec frontend npm run build
```

Build 成功確認済み。

---

## 24. Swagger UI

Swagger UI:

```text
http://localhost:8000/docs
```

Phase4 最終確認では `GET /users` の以下の Query Parameter が表示されることを確認済み。

```text
search
is_active
sort_by
sort_order
page
limit
```

HTTP 200 と `users` / `total` を含む Response も確認済み。

---

## 25. Browser Verification

以下で User 一覧画面を確認済み。

```text
http://localhost:5173/users
```

確認済み項目:

- 一覧表示
- メール検索
- Active / Inactive フィルタ
- ID / Email / Created At / Updated At のソート
- 前へ / 次へ
- 条件を維持したページ移動
- 検索条件変更時の1ページ目への移動
- 0件表示
- User詳細画面への遷移

---

## 26. Database / Migration

Database:

```text
PostgreSQL
```

ORM:

```text
SQLAlchemy
```

Migration:

```text
Alembic
```

Database Schema の変更は Alembic Migration を使用して管理する。

基本:

```text
Model変更
 ↓
Migration作成
 ↓
Migration確認
 ↓
Alembic Upgrade
 ↓
Database反映
```

---

## 27. Development Commands

よく使用するコマンド:

### Docker起動

```powershell
docker compose up -d
```

### Container確認

```powershell
docker compose ps
```

### Backend Test

```powershell
docker compose exec backend pytest -v
```

### Frontend Build

```powershell
docker compose exec frontend npm run build
```

---

## 28. Development Policy

開発は大きな変更を一度に行わず、Step 単位で進める。

基本フロー:

```text
Step提示
 ↓
実装
 ↓
動作確認
 ↓
必要ならGitHubコード確認
 ↓
Step完了
 ↓
次のStep
```

Commit / Push は細かい変更のたびではなく、区切りのよいタイミングで行う。

ドキュメント更新もフェーズ完了など、区切りのよいタイミングで行う。

---

## 29. Documentation

引継ぎで使用する主要ドキュメント:

### project-overview.md

プロジェクト全体の目的・技術構成・現在の実装状況を把握するための資料。

### architecture.md

現在のシステム構成・Backend / Frontend の責務やデータフローを把握するための資料。

### handover_phase.md

直近フェーズの作業内容・完了状況・次チャットの開始地点を把握するための資料。

新しいチャットでは原則として、この3資料を確認してから作業を開始する。

---

# 30. Development Progress

## Initial Setup

完了。

主な内容:

- Docker Compose
- Backend
- Frontend
- PostgreSQL
- FastAPI
- React / TypeScript / Vite
- Database Connection
- Alembic
- GitHub

## User CRUD

完了。

```text
Create
Read
Update
Delete
```

## Frontend User Management

完了。

User一覧・詳細など、User管理の基本画面を構築。

## Phase4

**完了。**

主な内容:

```text
User List
Search
Active Filter
Sort
Pagination
total
Frontend UI
Backend Test
Final Verification
```

---

# 31. Phase4 Final Status

```text
Phase4
├─ User CRUD                     DONE
├─ User List                     DONE
├─ Search                        DONE
├─ Active Filter                 DONE
├─ Sort                          DONE
├─ Pagination                    DONE
├─ total                         DONE
├─ Frontend UI                   DONE
├─ Backend Tests                 DONE
├─ Swagger Final Check           DONE
├─ Browser Final Check           DONE
├─ Frontend Build                DONE
├─ pytest Final Check            DONE
├─ Git / GitHub Check            DONE
└─ Documentation                DONE
```

**Phase4 完了。**

次の開発は次フェーズとして開始する。

---

---

# 32. Phase5 - UI / CSS

Phase5 では、Phase4 までに実装した機能を維持したまま、Frontend の見た目を最低限の Web アプリケーションらしい UI に整える。

## Phase5 方針

```text
Bootstrap
   ↓
基本的なUI・レイアウトを構築
   ↓
必要な箇所のみ自作CSS
   ↓
BizSC向けに微調整
```

Bootstrap が提供する既存のスタイルやクラスを積極的に利用し、CSSを一から大量に実装することは避ける。

余白・幅・配置・角丸など、Bootstrapだけでは調整しにくい部分については自作CSSを追加する。

Phase5では高度なデザインや独自デザインシステムの構築は目的とせず、既存画面を「最低限それらしい業務Webアプリケーション」に整えることを優先する。

## Phase5 で想定する対象

- アプリ全体のレイアウト
- ページ見出し
- ボタン
- 入力フォーム
- User一覧テーブル
- 検索 / Active Filter
- Pagination
- User作成画面
- User詳細 / 編集画面
- Loading / Error / 0件表示
- 余白・幅・配置などの微調整

## Phase5 の進め方

一度に全画面を変更せず、これまでと同様に Step 単位で進める。

```text
Step1
Bootstrap 導入
 ↓
Step2以降
画面・部品ごとにUI調整
 ↓
必要な箇所のみ自作CSS
 ↓
Browser確認
 ↓
Frontend Build確認
```

Phase4までに完成している検索・フィルタ・ソート・ページネーション等の機能ロジックは原則変更せず、Phase5ではUI / CSSの変更を中心とする。

Phase5 の最初の作業は **Bootstrap の導入** とする。

---

# 33. Handover

新しいチャットでは、

```text
architecture.md
handover_phase.md
project-overview.md
```

を引継ぎ資料として使用する。

コードの詳細や資料との差分を確認する必要がある場合は、以下の Repository の最新コードを参照する。

https://github.com/eswm223-oss/bizsc
