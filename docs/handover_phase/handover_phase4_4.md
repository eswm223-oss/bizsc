# BizSC Phase Handover

## 1. 引継ぎ概要

このドキュメントは、BizSC
の開発作業を別チャットへ引き継ぐための資料です。

**引継ぎ時点：2026-08-19**

現在は **Phase4 Step9「CRUD / 一覧APIテスト追加」まで完了**しています。

次のチャットでは、

**Phase4 Step10「Phase4最終確認」**

から開始してください。

コード確認が必要な場合は、以下の GitHub
リポジトリの最新コードを確認してください。

`https://github.com/eswm223-oss/bizsc`

引継ぎ資料の記載と GitHub
の実コードに差がある場合は、推測で補完せず、最新コードを確認して判断してください。

------------------------------------------------------------------------

## 2. 現在地点

Phase4 は User 一覧機能の拡張と Backend API テスト強化を進めています。

現在の進捗：

``` text
Phase4
├─ Step5  User検索                  完了
├─ Step6  Activeフィルタ            完了
├─ Step7  ソート                    完了
├─ Step8  ページネーション          完了
├─ Step9  CRUD / 一覧APIテスト追加  完了
└─ Step10 Phase4最終確認            次
```

したがって、新しいチャットでは Step5～9
を再実装せず、**Step10から開始**してください。

------------------------------------------------------------------------

## 3. Phase4 Step5 - User検索

完了済みです。

実装内容：

``` text
Backend
├─ Repository検索対応
├─ Service検索条件対応
└─ Router search Query Parameter対応

Frontend
├─ getUsers() search対応
├─ UserListPage検索State
├─ 検索UI
└─ 検索実行処理
```

Swagger UI / Browser の動作確認も完了しています。

------------------------------------------------------------------------

## 4. Phase4 Step6 - Activeフィルタ

完了済みです。

実装内容：

``` text
Backend
├─ Repository is_active対応
├─ Service is_active対応
└─ Router is_active Query Parameter対応

Frontend
├─ API Module isActive対応
├─ activeFilter State
├─ ActiveフィルタUI
└─ 検索 + Active条件連携
```

Frontend 内部では以下のように扱います。

``` text
""      → undefined
"true"  → true
"false" → false
```

Swagger UI / Browser の動作確認も完了しています。

------------------------------------------------------------------------

## 5. Phase4 Step7 - ソート

完了済みです。

Backend：

``` text
sort_by
sort_order
```

を追加済みです。

主なソート対象：

``` text
id
email
created_at
updated_at
```

Frontend には、

``` text
ソート対象
並び順
```

のUIを追加済みです。

検索・Activeフィルタ・ソートを組み合わせても正常に動作することを Browser
で確認済みです。

------------------------------------------------------------------------

## 6. Phase4 Step8 - ページネーション

完了済みです。

採用方式：

``` text
page / limit
```

Backend の基本値：

``` text
page  = 1
limit = 10
```

offset：

``` python
offset = (page - 1) * limit
```

一覧 API は以下を返します。

``` text
users
total
```

`total` は `search / is_active` 適用後、ページング前の総件数です。

Frontend では、

``` tsx
const totalPages = Math.max(1, Math.ceil(total / limit));
```

で総ページ数を計算します。

UI：

``` text
前へ   現在ページ / 総ページ数   次へ
```

------------------------------------------------------------------------

## 7. Step8 最終ブラウザ確認

Step8-13 の確認項目はすべて完了しています。

確認済み：

``` text
Step8-13-1
1ページ目で「前へ」が無効

Step8-13-2
「次へ」で2ページ目へ移動

Step8-13-3
2ページ目で表示内容が切り替わる

Step8-13-4
「前へ」で1ページ目へ戻る

Step8-13-5
最終ページで「次へ」が無効

Step8-13-6
検索条件ありでもページ移動可能

Step8-13-7
Activeフィルタ + ページネーション

Step8-13-8
ソート + ページネーション

Step8-13-9
検索条件変更時に1ページ目へ戻る

Step8-13-10
検索結果0件でもエラーにならない
```

これにより **Phase4 Step8 完了**としています。

------------------------------------------------------------------------

## 8. Phase4 Step9 - CRUD / 一覧APIテスト追加

Step9 は Backend API の自動テストを整備するフェーズです。

目的：

``` text
これまで手動確認していたAPI動作
        ↓
pytestで継続的に自動確認可能にする
```

Step9 はすべて完了しています。

``` text
Step9-1  テストDB方針決定              完了
Step9-2  テスト共通設定                完了
Step9-3  User作成テスト                完了
Step9-4  User詳細取得テスト            完了
Step9-5  User更新テスト                完了
Step9-6  User削除テスト                完了
Step9-7  User一覧 + searchテスト       完了
Step9-8  is_activeフィルタテスト       完了
Step9-9  ソートテスト                  完了
Step9-10 pagination / totalテスト      完了
Step9-11 全pytest実行                  完了
```

------------------------------------------------------------------------

## 9. Step9 テスト基盤

新規追加：

``` text
backend/tests/conftest.py
backend/tests/test_users.py
```

既存：

``` text
backend/tests/test_health.py
```

`conftest.py` では pytest fixture として FastAPI `TestClient`
を準備しています。

概念：

``` text
pytest
  ↓
DB connection
  ↓
外側transaction開始
  ↓
テスト用Session
  ↓
FastAPI get_dbをoverride
  ↓
TestClient
  ↓
APIテスト
  ↓
テスト終了
  ↓
rollback
```

主要部分：

``` python
connection = engine.connect()
transaction = connection.begin()

db = Session(
    bind=connection,
    join_transaction_mode="create_savepoint",
)
```

`app.dependency_overrides[get_db]` を使って、pytest 実行中だけ API
がテスト用 Session を使用するようにしています。

------------------------------------------------------------------------

## 10. テストDB方式の重要事項

現在は **専用の空DBを作る方式ではありません**。

既存の PostgreSQL DB を使用し、

``` text
テスト開始
↓
既存DBデータは見える
↓
テスト用データを追加・更新・削除
↓
テスト終了
↓
テスト中の変更をrollback
```

という方式です。

したがって一覧系テストでは、

``` text
total == テストで作った件数
```

と単純に確認すると、既存データが混ざる可能性があります。

そのため、固有のメールアドレスと `search`
条件を利用して、テスト対象データだけに絞っています。

この点は Step10 や今後テストを追加する際にも注意してください。

------------------------------------------------------------------------

## 11. Step9-3 - User作成テスト

確認内容：

``` text
POST /users
↓
201 Created
↓
email確認
is_active=True確認
idが存在することを確認
```

完了済みです。

------------------------------------------------------------------------

## 12. Step9-4 - User詳細取得テスト

流れ：

``` text
POST /users
↓
作成Userのid取得
↓
GET /users/{id}
↓
200 OK
↓
id / email / is_active確認
```

完了済みです。

------------------------------------------------------------------------

## 13. Step9-5 - User更新テスト

流れ：

``` text
POST /users
↓
PATCH /users/{id}
↓
email更新
is_active=False
↓
200 OK
↓
更新内容確認
```

完了済みです。

------------------------------------------------------------------------

## 14. Step9-6 - User削除テスト

流れ：

``` text
POST /users
↓
DELETE /users/{id}
↓
204 No Content
↓
GET /users/{id}
↓
404 Not Found
```

完了済みです。

------------------------------------------------------------------------

## 15. Step9-7 - User一覧 + searchテスト

テスト専用Userを作成し、

``` text
GET /users?search=...
```

によって対象Userだけが返ることを確認しています。

確認：

``` text
status_code
total
users件数
email
```

完了済みです。

------------------------------------------------------------------------

## 16. Step9-8 - is_activeフィルタテスト

このStepでは重要な仕様確認がありました。

現在の `UserCreate` は、

``` text
email
password
```

のみを受け取ります。

**`is_active` は UserCreate では指定できません。**

したがって、以下のように POST
時に指定してもテスト意図どおりにはなりません。

``` python
{
    "email": "...",
    "password": "...",
    "is_active": False,
}
```

Inactive User を準備するときは、

``` text
POST /users
↓
初期状態 is_active=True
↓
PATCH /users/{id}
↓
is_active=False
```

とします。

その後、

``` text
search
+
is_active=true
```

を指定し、Active User のみ返ることを確認しました。

Step9-8 は完了済みです。

------------------------------------------------------------------------

## 17. search と SQL LIKE の注意

Step9-8 の途中で、検索用文字列として `_` を含む値を使用しました。

Repository の検索は SQL `LIKE` を利用しています。

SQL LIKE では、

``` text
_
```

は通常のアンダースコアではなく、**任意の1文字に一致するワイルドカード**です。

そのため、テスト専用の検索文字列では `_` や `%`
を避け、十分に固有な英数字を使用する方針にしています。

------------------------------------------------------------------------

## 18. Step9-9 - ソートテスト

テスト専用Userを2件作成し、

``` text
search=固有文字列
sort_by=email
sort_order=asc
```

を指定します。

期待：

``` text
bizscsorta@example.com
bizscsortb@example.com
```

の順番になることを確認済みです。

Step9-9 完了済みです。

------------------------------------------------------------------------

## 19. Step9-10 - pagination / totalテスト

テスト専用Userを12件作成しています。

条件：

``` text
search=bizscpage
sort_by=email
sort_order=asc
page=2
limit=5
```

期待：

``` text
total = 12
users = 5件
```

さらに2ページ目の内容として概念上、

``` text
bizscpage05@example.com
～
bizscpage09@example.com
```

になることを確認しています。

Step9-10 完了済みです。

------------------------------------------------------------------------

## 20. Step9-11 - 全pytest

以下を実行済みです。

``` powershell
docker compose exec backend pytest -v
```

**全テスト PASSED を確認済みです。**

これにより Phase4 Step9 完了としています。

------------------------------------------------------------------------

## 21. Step9中に修正したHealthテスト

既存 `test_health.py` で期待値の不一致がありました。

実際の `/health/db`：

``` json
{
  "status": "ok",
  "db": "connected"
}
```

既存テスト側では以前、

``` json
{
  "status": "ok",
  "database": "connected"
}
```

を期待していました。

現在の API 仕様に合わせてテスト側を、

``` text
database
↓
db
```

へ修正済みです。

修正後、テスト成功を確認しています。

------------------------------------------------------------------------

## 22. httpx / httpx2 Warning対応

Step9 中、pytest 実行時に以下の Warning が発生しました。

``` text
StarletteDeprecationWarning:
Using `httpx` with `starlette.testclient` is deprecated;
install `httpx2` instead.
```

Backend の依存関係へ `httpx2` を追加し、Backend
イメージを再ビルドしています。

実施：

``` powershell
docker compose build backend
docker compose up -d backend
docker compose exec backend pytest tests/test_users.py -v
```

対応後：

``` text
Warning解消
User APIテスト成功
```

を確認済みです。

------------------------------------------------------------------------

## 23. 現在の Backend API

主要 API：

``` text
GET    /health
GET    /health/db

POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

User一覧 Query Parameter：

``` text
search
is_active
sort_by
sort_order
page
limit
```

一覧Response：

``` text
users
total
```

------------------------------------------------------------------------

## 24. 現在の Frontend User一覧

UserListPage では以下を実装済みです。

``` text
User一覧表示
メール検索
Activeフィルタ
ソート
ページネーション
Loading
Error表示
0件表示
詳細画面への遷移
```

ページネーションでは、

``` text
page
limit
total
```

を State として扱います。

検索条件変更時には1ページ目へ戻ります。

ページ移動時には、

``` text
search
activeFilter
sortBy
sortOrder
```

を維持した状態で再取得します。

------------------------------------------------------------------------

## 25. 次の作業 - Phase4 Step10

新しいチャットでは、まず資料を読み、その後 GitHub
の最新コードを確認してください。

次に、

**Phase4 Step10「Phase4最終確認」**

を開始します。

現時点で想定している確認内容：

``` text
Step10
├─ Swagger UI 最終確認
├─ Browser 最終確認
├─ Frontend build確認
├─ pytest最終確認
├─ Git / Repository状態確認
└─ Phase4ドキュメント更新
```

ただし、**Step10 の具体的な小Stepは GitHub
の最新状態を確認してから決定**してください。

古い引継ぎ資料だけを根拠にコード変更を指示しないでください。

------------------------------------------------------------------------

## 26. Step10開始時に確認するGitHubファイル

Backend：

``` text
backend/app/api/users.py
backend/app/services/user.py
backend/app/repositories/user.py
backend/app/schemas/user.py
backend/app/db/database.py

backend/tests/conftest.py
backend/tests/test_health.py
backend/tests/test_users.py

backend/requirements.txt
```

Frontend：

``` text
frontend/src/api/users.ts
frontend/src/types/user.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
```

必要に応じて関連ファイルも確認してください。

------------------------------------------------------------------------

## 27. 開発環境

``` text
OS             Windows
Editor         Cursor
Repository     GitHub
Git GUI        GitHub Desktop
Containers     Docker Desktop / Docker Compose
Backend        FastAPI / Python
Frontend       React / TypeScript / Vite
Database       PostgreSQL 17
DB Client      TablePlus
```

主な作業ディレクトリ：

``` text
D:\Development\apps\bizsc
```

------------------------------------------------------------------------

## 28. 開発時の進め方

ユーザーは1ステップずつ確認しながら進める方式を希望しています。

基本：

``` text
Assistant
↓
小さなStepを提示

User
↓
実装・確認

User
↓
「Step○完了」

Assistant
↓
次のStep
```

一度に大量のコード変更を指示しないこと。

ただし、単純なブラウザ確認などは、ユーザーから希望があれば複数項目をまとめても構いません。

コード変更前には、可能な限り GitHub の最新コードを確認してください。

------------------------------------------------------------------------

## 29. 回答方針

以下を維持してください。

-   正確性を優先する
-   推測を事実として扱わない
-   不明点は不明と明示する
-   GitHubで確認できる内容は最新コードを確認する
-   エラー発生時は原因を切り分けてから修正する
-   なぜその変更が必要なのか簡潔に説明する
-   一度に大きく変更しない
-   ユーザーが理解しながら進められる粒度にする

------------------------------------------------------------------------

## 30. 新チャット開始時の推奨手順

``` text
1. architecture.md を読む
2. handover_phase.md を読む
3. project-overview.md を読む
4. GitHub最新コードを確認
5. Phase4 Step10 の詳細を決める
6. Step10-1から開始
```

開始地点を間違えないこと。

**次の作業は Phase4 Step10 です。**
