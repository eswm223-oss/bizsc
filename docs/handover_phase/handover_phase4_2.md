# BizSC Handover — Phase4 継続

## 1. このドキュメントの目的

本ドキュメントは、BizSC の現在の開発状況を次のチャットへ引き継ぐための資料です。

次回は以下の3資料を基準として開発を再開します。

```text
project-overview.md
architecture.md
handover_phase.md
```

コード変更時は、引継ぎ資料だけを前提に推測せず、GitHub上の最新コードも確認します。

対象リポジトリ：

```text
eswm223-oss/bizsc
```

---

## 2. 現在の開発状況

現在は **Phase4 継続中** です。

Phase1〜Phase3は完了済みです。

```text
Phase1
環境構築
  ↓
完了

Phase2
Backend / User CRUD
  ↓
完了

Phase3
Frontend CRUD / 共通UI
  ↓
完了
```

Phase4ではUser一覧機能の拡張を進めています。

現在の到達点：

```text
Step5 User検索
  ↓
完了

Step6 Activeフィルタ
  ↓
完了

Step7 ソート
  ↓
次に開始
```

---

## 3. Phase4の実装順

Phase4は以下の順番で進める方針です。

```text
Step5  User検索
Step6  Activeフィルタ
Step7  ソート
Step8  ページネーション
Step9  CRUD / 一覧APIテスト追加
Step10 Phase4最終確認
```

一度にすべて実装せず、1機能ずつ小さく進めます。

---

## 4. 現在利用可能なUser機能

Frontendから以下のUser CRUDを利用できます。

```text
POST    /users
GET     /users
GET     /users/{id}
PATCH   /users/{id}
DELETE  /users/{id}
```

Frontend画面：

```text
/users
/users/new
/users/:userId
/users/:userId/edit
```

React RouterによるSPA遷移を行います。

---

## 5. Phase4で追加したUser一覧機能

### User検索

メールアドレスの部分一致検索を追加済みです。

想定API：

```text
GET /users?search=test
```

BackendではQuery Parameter `search` を受け取ります。

検索なしの場合は従来どおり全件取得します。

検索は大文字・小文字を区別しない部分一致検索として `ilike()` を利用する方針です。

---

### Activeフィルタ

Active / Inactive の絞り込みを追加済みです。

想定API：

```text
GET /users?is_active=true
GET /users?is_active=false
```

検索との併用も可能です。

```text
GET /users?search=test&is_active=true
```

条件の意味：

```text
is_active未指定
→ Active条件なし

is_active=true
→ 有効ユーザーのみ

is_active=false
→ 無効ユーザーのみ
```

---

## 6. Backendの現在の方針

Backendの基本構成：

```text
Request
  ↓
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

### Router

担当：

- Query Parameterの受け取り
- Service呼び出し
- Response返却

### Service

担当：

- 入力値をRepositoryへ渡す
- 業務ロジック
- 業務上のエラー判断

### Repository

担当：

- SQLAlchemy Queryの組み立て
- Database操作

Phase4ではUser一覧の検索・フィルタ条件を、Repositoryの1本のQueryへ順番に追加する方針です。

概念：

```python
statement = select(User)

if search:
    statement = statement.where(...)

if is_active is not None:
    statement = statement.where(...)

statement = statement.order_by(...)
```

Step7以降のソート・ページネーションも、このQueryへ追加していきます。

---

## 7. User一覧 Backend Flow

現在の一覧取得処理：

```text
GET /users
    │
    ├─ search
    └─ is_active
         ↓
Router
         ↓
UserService.get_users()
         ↓
UserRepository.get_all()
         ↓
SQLAlchemy
         ↓
PostgreSQL
```

検索・フィルタの組み合わせをService側で細かく分岐せず、Repository側でQuery条件を積み上げます。

---

## 8. Frontendの現在の方針

基本構成：

```text
Page
  ↓
API Module
  ↓
Axios Client
  ↓
FastAPI
```

PageからAxiosを直接呼び出しません。

### UserListPage

現在以下を担当します。

```text
一覧表示
検索State
ActiveフィルタState
Loading
Error
submit処理
API Module呼び出し
```

### API Module

`frontend/src/api/users.ts` に通信処理を集約します。

Phase4の `getUsers()` は概念上以下の引数を受け取ります。

```ts
getUsers(
  search?: string,
  isActive?: boolean,
)
```

Backendへは以下として渡します。

```text
search
is_active
```

---

## 9. UserListPage 検索UI

検索欄からメールアドレスの部分一致検索を行います。

処理：

```text
検索欄
  ↓
submit
  ↓
handleSearch()
  ↓
fetchUsers()
  ↓
getUsers()
  ↓
GET /users?search=...
```

検索結果が0件の場合はAPIエラーではなく、一覧の空状態として扱います。

---

## 10. UserListPage ActiveフィルタUI

Activeフィルタは3状態です。

```text
すべて
有効
無効
```

Frontend上では文字列Stateとして管理し、API呼び出し時に以下へ変換します。

```text
""      → undefined
"true"  → true
"false" → false
```

検索との組み合わせも確認済みです。

---

## 11. Reactフォームイベント型

Reactのフォームsubmit処理では、現在のプロジェクト方針として `SubmitEvent<HTMLFormElement>` を使用します。

例：

```tsx
function handleSearch(event: SubmitEvent<HTMLFormElement>) {
  event.preventDefault();
  ...
}
```

`FormEvent` / `FormEventHandler` は使用しない方針です。

---

## 12. useEffect / 初回データ取得

UserListPageの初回一覧取得は `useEffect` から行います。

Phase4中に以下のlint警告へ対応しました。

```text
Calling setState synchronously within an effect can trigger cascading renders
```

初回取得とユーザー操作による検索処理を分離しています。

### 初回取得

Effect内に非同期処理を定義し、cleanup用フラグを使用します。

概念：

```tsx
useEffect(() => {
  let ignore = false;

  async function loadUsers() {
    ...
  }

  loadUsers();

  return () => {
    ignore = true;
  };
}, []);
```

### 検索時取得

ユーザー操作から呼ばれる `fetchUsers()` 側では、

```text
setIsLoading(true)
setError(null)
API呼び出し
setUsers(...)
setIsLoading(false)
```

を行います。

---

## 13. Step5 User検索 — 完了内容

実施済み：

```text
Step5-1 Repository検索対応
Step5-2 Service検索条件対応
Step5-3 Router search Query Parameter対応
Step5-4 Swagger UI確認
Step5-5 Frontend API Module対応
Step5-6 UserListPage検索UI追加
Step5-7 ブラウザ動作確認
```

確認済み：

```text
検索なし → 全件表示
検索あり → 該当Userのみ
該当なし → 0件表示
空検索 → 全件表示
```

---

## 14. Step6 Activeフィルタ — 完了内容

実施済み：

```text
Step6-1 Repository検索＋Active条件対応
Step6-2 Service is_active対応
Step6-3 Router is_active Query Parameter対応
Step6-4 Swagger UI確認
Step6-5 Frontend API Module対応
Step6-6 UserListPage ActiveフィルタUI追加
Step6-7 ブラウザ動作確認
```

確認済み：

```text
検索なし + すべて
検索なし + 有効
検索なし + 無効
検索あり + すべて
検索あり + 有効
検索あり + 無効
該当なし
```

---

## 15. 次回開始位置

次回は **Phase4 Step7：ソート** から開始します。

想定Query Parameter：

```text
sort_by
sort_order
```

想定API：

```text
GET /users?sort_by=email&sort_order=asc

GET /users?sort_by=created_at&sort_order=desc

GET /users?search=test&is_active=true&sort_by=email&sort_order=asc
```

---

## 16. Step7の予定

以下の順番で進めます。

```text
Step7-1
Repositoryにソート条件を追加

Step7-2
Serviceでsort_by / sort_orderを受け取る

Step7-3
RouterでQuery Parameterを受け取る

Step7-4
Swagger UIで確認

Step7-5
Frontend API Module対応

Step7-6
UserListPageにソートUI追加

Step7-7
ブラウザで検索＋フィルタ＋ソート確認
```

---

## 17. Step7-1で意識すること

RepositoryのQueryへソート条件を追加します。

現在の流れ：

```text
select(User)
  ↓
search条件
  ↓
is_active条件
  ↓
order_by
```

これを以下へ拡張します。

```text
select(User)
  ↓
search条件
  ↓
is_active条件
  ↓
sort_by
  ↓
sort_order
```

`sort_by` の値をそのままSQLへ渡さず、許可するカラムを明示的に対応付ける方針です。

例：

```text
id
email
created_at
updated_at
```

実装時に最新コードを確認して、対象カラムを確定します。

---

## 18. Step8以降

### Step8 ページネーション

検索・フィルタ・ソート後のQueryへページネーションを追加します。

想定候補：

```text
page
limit
```

または、

```text
offset
limit
```

詳細はStep8開始時に決定します。

### Step9 テスト追加

対象候補：

```text
User CRUD
User検索
Activeフィルタ
ソート
ページネーション
```

### Step10 Phase4最終確認

```text
Swagger UI
Browser
Frontend build
pytest
Git状態
ドキュメント更新
```

---

## 19. 共通UI方針

現在共通化済み：

```text
Badge
Button
Card
ErrorMessage
Input
Loading
UserForm
```

共通化の基本：

```text
Component
→ UI・見た目

Page
→ API・State・業務処理・画面固有処理
```

不要な共通化は行いません。

---

## 20. Validation方針

FrontendとBackendの両方でValidationを行います。

```text
Frontend
→ UX向上

Backend
→ 最終的なデータ保証
```

Backendを最終Validation責任者とします。

---

## 21. Error Handling方針

入力項目単位：

```text
Input error
```

画面・API単位：

```text
ErrorMessage
```

検索・フィルタ結果が0件の場合はエラーではありません。

---

## 22. CSS方針

基本：

```text
Component CSS
→ Component自身の見た目

Page CSS
→ 画面固有の配置・レイアウト
```

User一覧の検索・フィルタ・今後追加するソートUIの配置は `UserListPage.css` 側で管理します。

---

## 23. TypeScript方針

今後も以下を維持します。

- `any` を安易に使用しない
- API Responseに型を定義する
- optional値を明確に扱う
- Component Propsを明示する
- catchしたerrorを安全に型判定する
- Reactの現在の型定義に合わせる

---

## 24. Backend変更時の注意

Phase4では既存Backendを不用意にリファクタリングしません。

変更前に責務を確認します。

```text
Router
Service
Repository
Schema
Model
Migration
```

検索・フィルタ・ソート・ページネーションは基本的に既存User一覧APIの拡張として実装します。

DB構造変更が不要であればAlembicは使用しません。

---

## 25. Frontend変更時の注意

PageからAxiosを直接利用しません。

```text
Page
  ↓
API Module
  ↓
Axios Client
```

共通型は `types/` で管理します。

UIだけを理由に過剰なComponent追加を行いません。

---

## 26. Git / コード確認時の注意

対象リポジトリ：

```text
eswm223-oss/bizsc
```

次チャット開始時は、まずGitHub上の最新コードを確認します。

特に確認するファイル：

```text
backend/app/api/users.py
backend/app/services/user.py
backend/app/repositories/user.py

frontend/src/api/users.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
frontend/src/types/user.ts
```

今回の引継ぎ作成時点では、このチャット上ではStep6まで完了しています。

GitHub上のコードが最新のローカル変更と一致しているかは、次チャット開始時に再確認してください。

---

## 27. 開発方針

今後も以下を維持します。

- 一度に大きく変更しない
- 1ステップずつ進める
- なぜ変更するのか理解してから実装する
- GitHubの実コードを確認してから変更案を出す
- UIと業務処理を分離する
- PageとComponentの責務を分離する
- Backendを最終Validation保証とする
- 型安全を維持する
- 不要な共通化を避ける
- 動作確認してから次へ進む
- 区切りの良いタイミングでCommitする
- フェーズやチャットの区切りでドキュメントを更新する

---

## 28. 次回チャットへの指示

次回チャットでは、

```text
1. project-overview.md
2. architecture.md
3. handover_phase.md
```

を読み込みます。

その後、GitHubの、

```text
eswm223-oss/bizsc
```

の最新コードを確認します。

現在地点を確認後、

> **Phase4 Step7-1：Repositoryにソート条件を追加**

から再開します。

一度にStep7全体を実装せず、これまでと同様に1ステップずつ進めます。
