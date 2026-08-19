# BizSC Phase4 Handover

## 1. このドキュメントの目的

このドキュメントは、BizSC の Phase4
作業を別チャットへ引き継ぐための資料です。

次回チャットでは、この資料に加えて以下も読み込んでください。

``` text
project-overview.md
architecture.md
handover_phase.md
```

また、資料だけを前提にコードを推測せず、必要に応じて GitHub
の最新コードを確認してください。

GitHub リポジトリ：

``` text
https://github.com/eswm223-oss/bizsc
```

------------------------------------------------------------------------

# 2. 現在地点

現在は **Phase4 Step8「ページネーション」実装中** です。

進捗：

``` text
Phase4
├─ Step5 User検索                 完了
├─ Step6 Activeフィルタ           完了
├─ Step7 ソート                   完了
├─ Step8 ページネーション
│  ├─ Step8-1                    完了
│  ├─ Step8-2                    完了
│  ├─ Step8-3                    完了
│  ├─ Step8-4                    完了
│  ├─ Step8-5                    完了
│  ├─ Step8-6                    完了
│  ├─ Step8-7                    完了
│  ├─ Step8-8                    完了
│  ├─ Step8-9                    完了
│  ├─ Step8-10                   完了
│  ├─ Step8-11                   完了
│  ├─ Step8-12                   完了
│  └─ Step8-13                   次に実施
├─ Step9 CRUD / 一覧APIテスト追加 未着手
└─ Step10 Phase4最終確認          未着手
```

**次回チャットの開始位置は Step8-13 です。**

------------------------------------------------------------------------

# 3. 重要：次回開始時の確認

今回のチャットでは Step7・Step8 の実装を順番に進めています。

ただし、Step8-12
完了後に「別チャットへ移る」となったため、**今回の最新変更が GitHub に
Push 済みかどうかは、この引継ぎ資料だけでは保証しません。**

次回開始時は、まず GitHub の最新コードを確認してください。

特に確認するファイル：

``` text
backend/app/repositories/user.py
backend/app/services/user.py
backend/app/api/users.py

frontend/src/api/users.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
frontend/src/types/user.ts
```

資料と GitHub のコードに差がある場合は、推測で先へ進まず、ローカル変更の
Commit / Push 状態を確認してください。

------------------------------------------------------------------------

# 4. Phase4 の目的

Phase3 までで User CRUD と Frontend 共通 UI の基本構成は完成しています。

Phase4 では User 一覧画面・一覧 API を拡張し、以下を追加しています。

``` text
User検索
Activeフィルタ
ソート
ページネーション
APIテスト強化
```

一覧 API の最終的なイメージ：

``` text
GET /users
    ?search=test
    &is_active=true
    &sort_by=email
    &sort_order=asc
    &page=1
    &limit=10
```

------------------------------------------------------------------------

# 5. Phase4 Step5 --- User検索

## 状態

**完了**

実装内容：

``` text
Repository検索対応
Service検索条件対応
Router search Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPage検索UI
ブラウザ動作確認
```

検索対象：

``` text
User.email
```

部分一致検索を使用しています。

概念：

``` python
if search:
    statement = statement.where(
        User.email.like(f"%{search}%")
    )
```

------------------------------------------------------------------------

# 6. Phase4 Step6 --- Activeフィルタ

## 状態

**完了**

実装内容：

``` text
Repositoryに is_active 条件追加
Service is_active対応
Router is_active Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPage ActiveフィルタUI
検索＋Activeフィルタのブラウザ確認
```

Frontend UI：

``` text
全て
有効
無効
```

Frontend 内部では文字列 State を使用し、API 呼び出し時に変換しています。

``` text
""      → undefined
"true"  → true
"false" → false
```

------------------------------------------------------------------------

# 7. Phase4 Step7 --- ソート

## 状態

**完了**

実施済み：

``` text
Step7-1 Repositoryソート対応
Step7-2 Service sort_by / sort_order対応
Step7-3 Router Query Parameter対応
Step7-4 Swagger UI確認
Step7-5 Frontend API Module対応
Step7-6 UserListPageソートUI追加
Step7-7 ブラウザ動作確認
```

## Backend

Repository の `get_all()` に以下を追加しました。

``` python
sort_by: str = "id"
sort_order: str = "asc"
```

ソート対象：

``` text
id
email
created_at
updated_at
```

安全のため、受け取った文字列をそのまま SQL
へ渡さず、カラムを明示的に対応付けます。

概念：

``` python
sort_columns = {
    "id": User.id,
    "email": User.email,
    "created_at": User.created_at,
    "updated_at": User.updated_at,
}

sort_column = sort_columns.get(sort_by, User.id)
```

並び順：

``` python
if sort_order == "desc":
    statement = statement.order_by(sort_column.desc())
else:
    statement = statement.order_by(sort_column.asc())
```

## Frontend

`getUsers()` に以下を追加しました。

``` text
sortBy
sortOrder
```

Backend へ送信する際：

``` text
sortBy    → sort_by
sortOrder → sort_order
```

UserListPage にソート用 State を追加：

``` text
sortBy
sortOrder
```

UI：

``` text
ソート対象
├─ ID
├─ メールアドレス
├─ 作成日時
└─ 更新日時

並び順
├─ 昇順
└─ 降順
```

------------------------------------------------------------------------

# 8. Phase4 Step8 --- ページネーション

## 状態

**Step8-12まで完了。Step8-13が次。**

BizSC では `page / limit` 方式を採用しました。

API例：

``` text
GET /users?page=1&limit=10
GET /users?page=2&limit=10
```

検索等との組み合わせ：

``` text
GET /users?search=test&is_active=true&sort_by=email&sort_order=asc&page=2&limit=10
```

------------------------------------------------------------------------

# 9. Step8-1 --- Repository引数

**完了**

Repository の `get_all()` に以下を追加しました。

``` python
page: int = 1
limit: int = 10
```

------------------------------------------------------------------------

# 10. Step8-2 --- offset / limit

**完了**

ページ番号から offset を計算します。

``` python
offset = (page - 1) * limit
```

Query：

``` python
statement = statement.offset(offset).limit(limit)
```

例：

``` text
page=1, limit=10 → offset=0
page=2, limit=10 → offset=10
page=3, limit=10 → offset=20
```

Query の基本的な組み立て順：

``` text
select(User)
↓
search
↓
is_active
↓
sort_by / sort_order
↓
order_by
↓
offset
↓
limit
```

------------------------------------------------------------------------

# 11. Step8-3 --- Service

**完了**

`UserService.get_users()` に、

``` text
page
limit
```

を追加し、Repositoryへ渡すようにしました。

------------------------------------------------------------------------

# 12. Step8-4 --- Router

**完了**

`GET /users` の Query Parameter に、

``` text
page
limit
```

を追加しました。

基本値：

``` text
page=1
limit=10
```

------------------------------------------------------------------------

# 13. Step8-5 --- count_all()

**完了**

ページネーション導入後、従来の

``` python
total = len(users)
```

では、現在ページの件数しか取得できません。

そのため Repository に `count_all()` を追加しました。

概念：

``` python
def count_all(
    self,
    db: Session,
    search: str | None = None,
    is_active: bool | None = None,
) -> int:
    statement = select(func.count(User.id))

    if search:
        statement = statement.where(
            User.email.like(f"%{search}%")
        )

    if is_active is not None:
        statement = statement.where(
            User.is_active == is_active
        )

    return db.scalar(statement) or 0
```

`count_all()` では、

``` text
search
is_active
```

のみを条件に使用します。

以下は件数取得には不要です。

``` text
sort_by
sort_order
page
limit
```

------------------------------------------------------------------------

# 14. Step8-6 --- Serviceで users / total取得

**完了**

Service の返り値を概念上、

``` python
tuple[list[User], int]
```

に変更しました。

``` text
users = 現在ページのUser一覧
total = 検索・Activeフィルタ後の全件数
```

概念：

``` python
users = self.repository.get_all(...)
total = self.repository.count_all(...)

return users, total
```

------------------------------------------------------------------------

# 15. Step8-7 --- Routerのtotal修正

**完了**

Router では、

``` python
users, total = user_service.get_users(...)
```

として受け取ります。

Response：

``` python
return UserListResponse(
    users=[
        UserResponse.model_validate(user)
        for user in users
    ],
    total=total,
)
```

これにより、例えば全体25件で `page=2, limit=10` の場合、

``` text
users → 10件
total → 25
```

となります。

------------------------------------------------------------------------

# 16. Step8-8 --- Swagger UI確認

**完了**

以下を確認済みです。

``` text
page=1, limit=10
page=2, limit=10
page=1, limit=5

search + page + limit
is_active + page + limit
search + is_active + sort_by + sort_order + page + limit
```

ページを変更しても `total`
が現在ページ件数ではなく、検索・フィルタ後の全件数になることを確認しています。

------------------------------------------------------------------------

# 17. Step8-9 --- Frontend API Module

**完了**

`frontend/src/api/users.ts` の `getUsers()` に以下を追加しました。

``` ts
page?: number
limit?: number
```

Backend Query Parameter：

``` text
page  → page
limit → limit
```

現在の概念：

``` ts
getUsers(
  search?,
  isActive?,
  sortBy?,
  sortOrder?,
  page?,
  limit?,
)
```

------------------------------------------------------------------------

# 18. Step8-10 --- UserListPage State

**完了**

UserListPage にページネーション用 State を追加しました。

``` tsx
const [page, setPage] = useState(1);
const [limit] = useState(10);
const [total, setTotal] = useState(0);
```

`fetchUsers()` に、

``` text
pageValue
limitValue
```

を追加しました。

API Response 取得後：

``` tsx
setUsers(response.users);
setTotal(response.total);
```

初回取得用 `loadUsers()` でも `total` を保存します。

検索実行時には、

``` tsx
setPage(1);
```

として1ページ目へ戻す構成です。

------------------------------------------------------------------------

# 19. Step8-11 --- ページ移動処理

**完了**

総ページ数：

``` tsx
const totalPages = Math.ceil(total / limit);
```

その後、0件時の表示を考慮して以下を推奨・採用する流れで進めています。

``` tsx
const totalPages = Math.max(1, Math.ceil(total / limit));
```

ページ移動関数：

``` text
handlePreviousPage()
handleNextPage()
```

ページ移動時にも現在の以下の条件を維持します。

``` text
search
activeFilter
sortBy
sortOrder
page
limit
```

------------------------------------------------------------------------

# 20. Step8-12 --- ページネーションUI

**完了**

一覧テーブル下部に以下のUIを追加しました。

``` text
前へ   1 / 3   次へ
```

概念：

``` tsx
<div className="user-pagination">
  <button
    type="button"
    onClick={handlePreviousPage}
    disabled={page <= 1}
  >
    前へ
  </button>

  <span>
    {page} / {totalPages}
  </span>

  <button
    type="button"
    onClick={handleNextPage}
    disabled={page >= totalPages}
  >
    次へ
  </button>
</div>
```

1ページ目：

``` text
前へ → disabled
```

最終ページ：

``` text
次へ → disabled
```

------------------------------------------------------------------------

# 21. 次に行う Step8-13

## ブラウザ最終動作確認

次回チャットでは、まず GitHub /
ローカルの最新状態を確認したうえで、この確認から再開してください。

確認項目：

``` text
① 1ページ目で「前へ」が無効

② 「次へ」で2ページ目へ移動

③ 2ページ目で表示内容が切り替わる

④ 「前へ」で1ページ目へ戻る

⑤ 最終ページで「次へ」が無効

⑥ 検索条件を入れてもページ移動できる

⑦ Activeフィルタを入れてもページ移動できる

⑧ ソート条件を入れてもページ移動できる

⑨ 検索条件を変更したら1ページ目へ戻る

⑩ 0件でもエラーにならない
```

特に重要なのは、

``` text
検索
+
Activeフィルタ
+
ソート
+
ページネーション
```

が同時に機能することです。

Step8-13 に問題がなければ、

> **Phase4 Step8「ページネーション」完了**

とします。

------------------------------------------------------------------------

# 22. Step8完了後

次は、

> **Phase4 Step9：CRUD / 一覧APIテスト追加**

へ進みます。

想定する対象：

``` text
User CRUD
User一覧
search
is_active
sort_by
sort_order
page
limit
total
```

ただし、テスト内容・既存テスト構成は次回開始時に GitHub
の最新コードを確認してから決定してください。

既存コードを確認せず、テストファイル名やfixture構成を推測して進めないこと。

------------------------------------------------------------------------

# 23. Step10

Step9 完了後は Phase4 の最終確認です。

想定：

``` text
Swagger UI確認
Browser確認
Frontend build
pytest
Git状態確認
ドキュメント更新
```

詳細は Step9 完了後に決定します。

------------------------------------------------------------------------

# 24. Backendで次回確認するポイント

``` text
backend/app/repositories/user.py
backend/app/services/user.py
backend/app/api/users.py
```

確認したい内容：

``` text
get_all(
    search,
    is_active,
    sort_by,
    sort_order,
    page,
    limit,
)

count_all(
    search,
    is_active,
)

Service:
    users, total

Router:
    total=total
```

Repository のQuery順：

``` text
select(User)
↓
search
↓
is_active
↓
sort
↓
offset
↓
limit
```

------------------------------------------------------------------------

# 25. Frontendで次回確認するポイント

``` text
frontend/src/api/users.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
```

`getUsers()`：

``` text
search
isActive
sortBy
sortOrder
page
limit
```

UserListPage State：

``` text
users
isLoading
error

search
activeFilter

sortBy
sortOrder

page
limit
total
```

ページ移動時：

``` text
現在の検索条件
現在のActive条件
現在のソート条件
現在のページ番号
```

を API に渡していることを確認します。

------------------------------------------------------------------------

# 26. Phase4で維持する責務分離

Backend：

``` text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

Frontend：

``` text
Page
  ↓
API Module
  ↓
Axios
  ↓
Backend
```

Repository が DB Query を担当し、Service が処理の組み合わせ、Router が
HTTP 入出力を担当します。

Frontend では Page が State と画面固有処理を持ち、API Module に HTTP
通信を集約します。

------------------------------------------------------------------------

# 27. 開発ルール

次回も以下の進め方を維持してください。

``` text
1ステップずつ進める
↓
ユーザーが実装
↓
動作確認
↓
「StepX完了」
↓
次のステップ
```

一度に大量の変更を提示しないこと。

コード確認が必要な場合は GitHub の最新コードを確認すること。

不明な点を推測で埋めないこと。

エラーが出た場合は、エラー全文と実コードを確認して原因を切り分けること。

Commit / Push やドキュメント更新は区切りの良いタイミングで案内すること。

------------------------------------------------------------------------

# 28. 次回チャットへの開始指示

次回チャットでは以下の順番で進めることを推奨します。

``` text
1. architecture.md を確認
2. handover_phase.md を確認
3. project-overview.md を確認
4. GitHub eswm223-oss/bizsc の最新コードを確認
5. Step8の変更がPush済みか確認
6. 必要なら差分確認
7. Phase4 Step8-13 ブラウザ最終確認
8. Step8完了判定
9. Phase4 Step9へ進む
```

**開始地点：Phase4 Step8-13**

Step8-13 完了後は、Phase4 Step9「CRUD /
一覧APIテスト追加」へ進んでください。
