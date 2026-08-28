# BizSC Handover Phase

## 1. この資料の目的

このファイルは、BizSC の開発作業を別チャットへ引き継ぐための資料。

新しいチャットでは、この資料と `architecture.md`、`project-overview.md` を確認したうえで、現在地点から開発を継続する。

コードの詳細確認が必要な場合は、引継ぎ資料だけで推測せず、GitHub Repository の最新コードを確認する。

Repository:
https://github.com/eswm223-oss/bizsc

---

## 2. 現在地点

**Phase4 完了 / Phase5 方針決定済み**

Phase4 では User 一覧機能を中心に、Backend / Frontend の検索・フィルタ・ソート・ページネーションとテストを実装した。

Phase4 最終確認（Step10）も完了済み。

Phase5 は UI / CSS 調整フェーズとし、**Bootstrap + Custom CSS** を採用する方針を決定済み。実装はこれから開始する。

---

## 3. Phase4 で完了した主な機能

### Backend

User API:

- `POST /users`
- `GET /users`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`

`GET /users` では以下の Query Parameter に対応済み。

- `search`
- `is_active`
- `sort_by`
- `sort_order`
- `page`
- `limit`

一覧レスポンスは以下の形式。

```json
{
  "users": [],
  "total": 0
}
```

Backend の基本構成:

```text
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

UserRepository では以下を実装済み。

- ID検索
- Email検索
- 一覧取得
- 検索
- Active / Inactive フィルタ
- ソート
- ページネーション
- 総件数取得
- Create
- Update
- Delete

---

## 4. Frontend で完了した主な機能

User 一覧画面:

```text
/users
```

以下を実装済み。

- User一覧表示
- メールアドレス検索
- Active / Inactive フィルタ
- IDソート
- メールアドレスソート
- 作成日時ソート
- 更新日時ソート
- 昇順 / 降順切り替え
- ページネーション
- 「前へ」「次へ」
- 検索・フィルタ・ソート条件を維持したページ移動
- 検索条件変更時に1ページ目へ戻る
- Loading表示
- Error表示
- 0件表示
- User詳細画面への遷移

Frontend → Backend は Axios を使用する。

---

## 5. Phase4 Step9：Backend Test

User API の pytest を追加済み。

主なテスト対象:

- Create User
- Get User
- Update User
- Delete User
- Search
- is_active Filter
- Sort
- Pagination
- total

一覧系ではテストデータが既存DBデータと衝突しないよう、検索条件用の固有文字列を利用してテスト対象を限定している。

Phase4 最終確認でも以下を実行済み。

```powershell
docker compose exec backend pytest -v
```

**全テスト PASSED 確認済み。**

---

## 6. Phase4 Step10：最終確認

### Step10-1 GitHub反映確認

完了。

Step9で追加した以下のテストが GitHub Repository に Push されていることを確認済み。

- search
- is_active
- sort
- pagination

### Step10-2 Swagger UI

完了。

```text
http://localhost:8000/docs
```

`GET /users` で以下の Query Parameter を確認済み。

- search
- is_active
- sort_by
- sort_order
- page
- limit

Response が HTTP 200 で、

```json
{
  "users": [],
  "total": 0
}
```

形式になることを確認済み。

### Step10-3 Browser

完了。

```text
http://localhost:5173/users
```

以下を最終確認済み。

- 一覧表示
- メール検索
- Active / Inactive フィルタ
- ソート
- ページ移動
- 条件を維持したページ移動
- 検索条件変更時の page=1
- 0件表示
- User詳細画面への遷移

### Step10-4 Frontend Build

完了。

```powershell
docker compose exec frontend npm run build
```

ビルド成功確認済み。

### Step10-5 pytest

完了。

```powershell
docker compose exec backend pytest -v
```

全テスト PASSED 確認済み。

### Step10-6 Git / Repository

完了。

- 未コミット変更なし
- Push待ちなし
- GitHubへ最新コード反映済み
- 意図しない変更なし

### Step10-7 Documentation

Phase4完了版ドキュメントを作成中。

- `architecture.md`：生成済み
- `handover_phase.md`：このファイル
- `project-overview.md`：次に更新する

---

## 7. 現在の重要な Backend 実装

### UserService.get_users()

概念:

```text
API
 ↓
UserService.get_users()
 ↓
UserRepository.get_all()
UserRepository.count_all()
 ↓
users, total
 ↓
UserListResponse
```

Service は Repository から、

```text
users
total
```

を取得し、API Layer へ返す。

---

## 8. UserRepository.get_all()

一覧取得では以下を処理する。

```text
select(User)
 ↓
sort
 ↓
pagination
 ↓
search
 ↓
is_active
 ↓
DB query
```

現在の実装では SQLAlchemy statement に対して各条件を追加し、最後に DB から一覧を取得する。

ソート対象:

- `id`
- `email`
- `created_at`
- `updated_at`

ページネーション:

```python
offset = (page - 1) * limit
```

---

## 9. UserRepository.count_all()

`total` を取得するための処理。

概念:

```python
select(func.count(User.id))
```

検索条件:

- search
- is_active

を適用する。

ページネーションは適用しない。

そのため、

```text
users = 現在のページに表示するデータ
total = 条件に一致する全件数
```

となる。

---

## 10. Frontend の一覧状態管理

User一覧画面では主に以下の State を管理する。

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

重要な考え方:

```text
State変更
 ↓
Component再レンダリング
```

検索フォームでは、入力値と確定した検索条件を分離している。

```text
searchInput
 ↓
検索操作
 ↓
search
 ↓
API Request
```

---

## 11. ページネーション

Backend:

```text
page
limit
 ↓
offset = (page - 1) * limit
 ↓
offset()
limit()
```

Frontend:

```text
total
limit
 ↓
Math.ceil(total / limit)
 ↓
総ページ数
```

検索・フィルタ条件変更時は1ページ目へ戻す。

---

## 12. 開発環境

主な開発環境:

- Windows
- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus

Technology Stack:

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

### Database

- PostgreSQL

---

## 13. Docker

主なサービス:

```text
frontend
backend
db
```

主なURL:

```text
Frontend
http://localhost:5173

Backend
http://localhost:8000

Swagger UI
http://localhost:8000/docs
```

よく使用するコマンド:

```powershell
docker compose up -d

docker compose ps

docker compose exec backend pytest -v

docker compose exec frontend npm run build
```

---

## 14. Phase5 方針：UI / CSS

Phase5 では、既存の React / TypeScript の機能を維持しながら、Frontend の見た目を最低限の業務アプリ風に整える。

採用方針:

- Bootstrap を使用する
- Bootstrap の既存クラスを優先して利用する
- 足りない部分だけ Custom CSS で微調整する
- CSS を全面的に自作しない
- 過度に凝ったデザインは目標にしない
- CSS 初学者でも追いやすい Step 単位で進める

主な調整対象:

- 全体レイアウト
- 見出し
- ボタン
- 入力フォーム
- 検索 / フィルタ
- User 一覧テーブル
- Active / Inactive 表示
- ページネーション
- User 作成画面
- User 詳細 / 編集画面
- Loading / Error / 0件表示

Phase5 のゴール:

```text
既存機能を維持
  ↓
Bootstrap で基本デザインを適用
  ↓
必要箇所のみ Custom CSS
  ↓
最低限それらしい業務アプリ UI
```

Phase5 の開始候補:

```text
Step1 Bootstrap 導入
Step2 全体レイアウト調整
Step3 共通 UI 調整
Step4 User 一覧画面
Step5 User 作成画面
Step6 User 詳細 / 編集画面
Step7 Loading / Error / 0件表示
Step8 全体確認・微調整
```

---

## 15. 次のチャットでの開始位置

**Phase4 は完了済み。Phase5 の UI / CSS 方針も決定済み。**

次のチャットでは Phase4 の実装をやり直さず、**Phase5 Step1：Bootstrap 導入** から開始する。

開始時には、

1. `architecture.md`
2. `handover_phase.md`
3. `project-overview.md`

を確認する。

必要に応じて GitHub Repository の最新コードを確認する。

Repository:
https://github.com/eswm223-oss/bizsc

---

## 16. 次チャットへの依頼方針

新しいチャットでは、ユーザーを一度に大量の作業へ誘導せず、これまでと同様に Step 単位で進める。

基本:

```text
Step N
 ↓
ユーザーが実装
 ↓
必要ならGitHubの最新コードを確認
 ↓
問題なければ完了
 ↓
次のStep
```

コード確認が必要な場合は、推測で現在のコードを補完せず GitHub Repository を確認する。

大きな区切りでのみ Commit / Push やドキュメント更新を案内する。

---

# Phase4 / Phase5 Status

```text
Phase4
├─ User CRUD                     DONE
├─ Search                        DONE
├─ Active Filter                 DONE
├─ Sort                          DONE
├─ Pagination                    DONE
├─ total                         DONE
├─ Frontend User List            DONE
├─ Backend Tests                 DONE
├─ Swagger Final Check           DONE
├─ Browser Final Check           DONE
├─ Frontend Build                DONE
├─ pytest Final Check            DONE
├─ GitHub Push                   DONE
└─ Documentation                DONE
```

Phase4 の実装・動作確認は完了。

```text
Phase5
├─ UI / CSS方針                 DECIDED
├─ Bootstrap採用                DECIDED
├─ Custom CSS併用               DECIDED
└─ 実装                         NOT STARTED
```

次は **Phase5 Step1：Bootstrap 導入** から開始する。
