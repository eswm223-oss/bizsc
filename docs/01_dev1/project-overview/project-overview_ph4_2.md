# BizSC Project Overview

## 1. プロジェクト概要

プロジェクト名：**BizSC**

BizSC は、業務管理機能を段階的に構築しながら、Webアプリケーション開発の設計・実装・運用を学習するための個人開発プロジェクトです。

短期的に機能を増やすことだけを目的とせず、以下を重視します。

- 可読性
- 保守性
- 拡張性
- 型安全
- テスタビリティ
- 責務分離
- 理解しながら開発すること

---

## 2. 開発環境

### OS

- Windows

### 開発ツール

- Cursor
- GitHub
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus

### リポジトリ

```text
https://github.com/eswm223-oss/bizsc
```

コード確認が必要な場合は、引継ぎ資料だけを前提に推測せず、必ず上記GitHubリポジトリの最新コードを確認します。

特に実装変更前は、対象ファイルの現在の内容をGitHubで確認してから変更案を出します。

---

## 3. 技術スタック

### Frontend

- React
- TypeScript
- Vite
- React Router
- Axios
- CSS

### Backend

- Python 3.13
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Pydantic v2
- Alembic
- Argon2
- pytest

### Database

- PostgreSQL 17

---

## 4. Docker構成

Docker Composeで以下の3サービスを管理します。

```text
Docker Compose
├── frontend
├── backend
└── db
```

主なポート：

```text
Frontend    5173
Backend     8000
PostgreSQL  5432
```

Frontendは開発時にViteを使用します。

BackendはFastAPI + Uvicornで動作します。

---

## 5. システム構成

```text
Browser
    │
    ▼
React
    │
    ▼
React Router
    │
    ▼
Pages
    │
    ▼
API Module
    │
    ▼
Axios
    │
    ▼
FastAPI
    │
    ▼
Router
    │
    ▼
Service
    │
    ▼
Repository
    │
    ▼
SQLAlchemy
    │
    ▼
PostgreSQL
```

FrontendとBackendの責務を分離し、Backend内部でもLayered Architectureを採用します。

---

## 6. Backend構成

主な構成：

```text
backend/app/

api/
core/
db/
models/
repositories/
schemas/
services/
main.py
```

基本的な処理の流れ：

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

- URL定義
- Path / Query / Body の受け取り
- Service呼び出し
- Response返却

### Service

担当：

- 業務ロジック
- Password Hash
- Validation
- 独自例外
- Repository呼び出し

### Repository

担当：

- CRUD
- SQLAlchemyによるDB操作
- Query条件の組み立て

---

## 7. Frontend構成

主な構成：

```text
frontend/src/

api/
components/
layouts/
pages/
routes/
types/
```

### Pages

現在の主なPage：

```text
HomePage
UserListPage
UserDetailPage
UserCreatePage
UserEditPage
NotFoundPage
```

Page側の主な責務：

- API通信の呼び出し
- State管理
- Validation
- Error処理
- Loading状態管理
- 画面遷移
- 画面固有の表示処理

### Components

現在の主な共通UI：

```text
Badge
Button
Card
ErrorMessage
Input
Loading
UserForm
```

その他：

```text
Header
Sidebar
Footer
```

基本方針：

> 共通UIはComponentへ、業務処理や画面固有処理はPage側へ置く。

---

## 8. Routing

現在の主なルート：

```text
/
    HomePage

/users
    UserListPage

/users/new
    UserCreatePage

/users/:userId
    UserDetailPage

/users/:userId/edit
    UserEditPage

*
    NotFoundPage
```

React RouterによるSPA遷移を行います。

---

## 9. User API

現在利用可能なUser CRUD：

```text
POST    /users
GET     /users
GET     /users/{id}
PATCH   /users/{id}
DELETE  /users/{id}
```

Health：

```text
GET /health
GET /health/db
```

FrontendからUser CRUDを利用できる状態です。

---

## 10. User一覧 API — Phase4拡張

Phase4では `GET /users` を一覧機能向けに拡張しています。

現在追加済み：

```text
search
is_active
```

例：

```text
GET /users?search=test
GET /users?is_active=true
GET /users?is_active=false
GET /users?search=test&is_active=true
```

### search

メールアドレスの部分一致検索。

検索条件が未指定の場合は全件取得します。

### is_active

Active / Inactive のフィルタ。

```text
未指定 → 条件なし
true   → 有効Userのみ
false  → 無効Userのみ
```

検索条件と同時利用できます。

---

## 11. User機能

現在実装済み：

- User一覧
- User詳細
- User新規作成
- User編集
- User削除
- Active / Inactive管理
- Loading表示
- Error表示
- React Routerによる画面遷移
- User検索
- Activeフィルタ

User CRUDの基本機能は完成しています。

Phase4では一覧機能の拡張を進めています。

---

## 12. API Module

FrontendではPageからAxiosを直接利用せず、API Moduleを経由します。

```text
Page
    ↓
API Module
    ↓
Axios Client
```

User API：

```text
getUsers()
getUser()
createUser()
updateUser()
deleteUser()
```

Phase4の `getUsers()` は概念上以下の条件を受け取ります。

```ts
getUsers(
  search?: string,
  isActive?: boolean,
)
```

Backendへ渡すQuery Parameter：

```text
search
is_active
```

---

## 13. User型

主なUser型：

```ts
export type User = {
  id: number;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};
```

その他：

```text
UserListResponse
UserCreate
UserUpdate
```

共通型は `frontend/src/types` で管理します。

---

## 14. UserForm

Create / EditフォームのUI重複を減らすため、共通 `UserForm` を利用しています。

UserFormの担当：

- Email入力
- Password入力
- Active入力
- 入力項目ごとのError表示
- Submitボタン
- Submit状態表示
- フォーム内レイアウト

UserFormに持たせないもの：

- API通信
- Validation判断
- Axiosエラー処理
- 画面遷移
- 業務ロジック

これらはPage側で管理します。

---

## 15. 共通UI

### Badge

ステータス表示用の共通UI。

現在のvariant：

```text
success
neutral
```

User状態：

```text
有効 → success
無効 → neutral
```

BadgeはUser固有の業務ロジックを持ちません。

### Button

主なvariant：

```text
primary
secondary
danger
```

### Card

担当：

- コンテンツ領域
- タイトル
- 枠
- 内部余白

### Input

担当：

- label
- input
- 入力項目単位のError表示

### Loading

API通信中の読み込み表示に使用します。

### ErrorMessage

画面・API単位のエラー表示に使用します。

---

## 16. User一覧 UI

User一覧では以下を表示します。

```text
ID
メールアドレス
ステータス
操作
```

ステータスはBadgeで表示します。

Phase4で以下を追加済みです。

```text
メールアドレス検索
Activeフィルタ
```

ActiveフィルタUI：

```text
すべて
有効
無効
```

検索とActiveフィルタは組み合わせて利用できます。

---

## 17. User詳細 UI

User詳細画面：

```text
ID
メールアドレス
ステータス
作成日時
更新日時
```

`dl / dt / dd` とCSS Gridによる2列表示です。

操作領域：

```text
一覧へ戻る                         編集  削除
```

削除には `Button variant="danger"` を利用します。

日時は表示時のみ整形します。

---

## 18. User新規作成 UI

UserCreatePageではUserFormを利用します。

主な処理：

- Email入力
- Password入力
- Email必須確認
- Password8文字以上確認
- User作成API呼び出し
- API Error処理
- 作成後 `/users` へ遷移

---

## 19. User編集 UI

UserEditPageではUserFormを利用します。

主な処理：

- User情報取得
- Email編集
- Active編集
- User更新API呼び出し
- API Error処理
- 更新後User詳細画面へ遷移

---

## 20. Loading設計

主なState：

```text
isLoading
isSubmitting
isDeleting
```

処理中：

- Loading表示
- Button無効化
- 二重送信防止

検索実行時も一覧取得中はLoading状態にします。

---

## 21. Error Handling

### Backend

独自例外を利用します。

例：

```text
AppError
UserNotFoundError
EmailAlreadyRegisteredError
```

Exception HandlerでResponseへ変換します。

### Frontend

主なError：

- Axios Error
- Email重複
- Validation Error
- API取得失敗
- 作成失敗
- 更新失敗
- 削除失敗

検索・フィルタ結果が0件の場合はエラーではなく、一覧の空状態として扱います。

FrontendだけでValidation保証を行わず、Backendを最終的なValidation保証とします。

---

## 22. useEffect / 初回一覧取得

UserListPageの初回一覧取得は `useEffect` から行います。

Phase4中に以下のlint警告へ対応しました。

```text
Calling setState synchronously within an effect can trigger cascading renders
```

初回取得用の非同期処理と、検索・フィルタ実行時の取得処理を分離しています。

Effect側ではcleanup用フラグを利用し、Unmount後のState更新を防止する構成とします。

---

## 23. Reactフォームイベント型

フォームsubmit処理では、現在のプロジェクト方針として `SubmitEvent<HTMLFormElement>` を使用します。

```tsx
function handleSearch(event: SubmitEvent<HTMLFormElement>) {
  event.preventDefault();
}
```

`FormEvent` / `FormEventHandler` は使用しない方針です。

---

## 24. CSS設計

共通UIのCSS：

```text
components/
├── Badge/Badge.css
├── Button/Button.css
├── Card/Card.css
├── ErrorMessage/ErrorMessage.css
├── Input/Input.css
├── Loading/Loading.css
└── UserForm/UserForm.css
```

画面固有CSS：

```text
pages/
├── UserListPage.css
└── UserDetailPage.css
```

基本方針：

> 共通UIの見た目と、画面固有のレイアウトを分離する。

User一覧の検索・フィルタ・今後のソートUIは `UserListPage.css` 側で管理します。

---

## 25. 共通化方針

現在共通化済み：

- Badge
- Button
- Card
- ErrorMessage
- Input
- Loading
- UserForm

共通化の判断基準：

- 複数画面で利用するか
- 責務が明確か
- 業務ロジックを持たないか
- 共通化によって複雑にならないか

以下だけを理由に共通化しません。

```text
将来使うかもしれない
なんとなく再利用できそう
コードが短くなる
```

必要になった時点で共通化します。

---

## 26. TypeScript方針

TypeScriptの型安全性を優先します。

原則：

- `any` を安易に使用しない
- API Responseは型を定義する
- catchしたerrorは安全に型判定する
- Component Propsを明示する
- optional値を明確に扱う
- Reactの現在の型定義に合わせる

---

## 27. 開発フェーズ

### Phase1

環境構築。

主な内容：

- Windows開発環境
- Cursor
- Docker Desktop
- Docker Compose
- Frontend
- Backend
- PostgreSQL
- GitHub連携

**完了。**

### Phase2

Backend / User CRUD。

主な内容：

- SQLAlchemy Model
- Repository
- Pydantic Schema
- Service
- Router
- Alembic
- Exception Handler
- Password Hash
- User CRUD

**完了。**

### Phase3

Frontend CRUD / 共通UI。

主な内容：

- React Router
- API Module
- User一覧
- User詳細
- User作成
- User編集
- User削除
- Loading
- ErrorMessage
- Button
- Card
- Input
- UserForm
- Badge
- User詳細UI改善
- 共通UI全体見直し
- CRUD最終動作確認
- Frontend build確認

**完了。**

---

## 28. Phase4

Phase4では、User一覧機能の拡張とテスト強化を進めます。

実装順：

```text
Step5  User検索
Step6  Activeフィルタ
Step7  ソート
Step8  ページネーション
Step9  CRUD / 一覧APIテスト追加
Step10 Phase4最終確認
```

現在：

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

## 29. Phase4 Step5 — User検索

完了済み：

```text
Repository検索対応
Service検索条件対応
Router search Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPage検索UI
ブラウザ動作確認
```

確認済み：

```text
検索なし → 全件表示
検索あり → 該当Userのみ
該当なし → 0件表示
空検索 → 全件表示
```

---

## 30. Phase4 Step6 — Activeフィルタ

完了済み：

```text
Repository検索＋Active条件対応
Service is_active対応
Router is_active Query Parameter対応
Swagger UI確認
Frontend API Module対応
UserListPage ActiveフィルタUI
検索＋Activeフィルタのブラウザ動作確認
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

## 31. 次回開始位置

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

Step7予定：

```text
Step7-1 Repositoryにソート条件を追加
Step7-2 Service対応
Step7-3 Router対応
Step7-4 Swagger UI確認
Step7-5 Frontend API Module対応
Step7-6 UserListPageにソートUI追加
Step7-7 ブラウザ動作確認
```

---

## 32. Phase5以降の候補

将来的なBizSC拡張候補：

- 業務管理
- 権限管理
- ダッシュボード
- マスタ管理
- ログ管理

現段階では詳細設計を固定しません。

---

## 33. Git運用

基本方針：

- 小さい単位でCommit
- 動作確認後Commit
- フェーズ単位でPush
- 区切りの良いタイミングでドキュメント更新

---

## 34. ドキュメント

主要ドキュメント：

```text
README.md
project-overview.md
architecture.md
handover_phase.md
decisions/
```

### project-overview.md

プロジェクト全体の現在地・進捗・今後の予定。

### architecture.md

設計思想・責務分離・システム構成。

### handover_phase.md

次回チャットへ引き継ぐための詳細な作業状況。

### decisions/

重要な設計判断を記録します。

---

## 35. コード確認ルール

コードの確認が必要な場合は、以下のGitHubリポジトリを確認します。

```text
https://github.com/eswm223-oss/bizsc
```

特に以下の場合は、資料だけで推測せずGitHub上の最新コードを確認します。

- 新しいStepを開始するとき
- 既存コードの変更案を出すとき
- エラー原因をコードから確認するとき
- Backend / Frontend間の引数や型を確認するとき
- 以前のチャット内容と現在コードに差がある可能性があるとき
- Push済みコードの確認を依頼されたとき

確認対象の例：

```text
backend/app/api/users.py
backend/app/services/user.py
backend/app/repositories/user.py

frontend/src/api/users.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
frontend/src/types/user.ts
```

GitHub上の最新コードを事実として優先し、引継ぎ資料との不一致がある場合は、その差を明示してから進めます。

---

## 36. 開発方針

今後も以下を維持します。

- 一度に大きく変更しない
- 1ステップずつ進める
- なぜ変更するのか理解してから実装する
- GitHub実コードを確認してから変更案を出す
- UIと業務処理を分離する
- PageとComponentの責務を分離する
- Backendを最終Validation保証とする
- 型安全を維持する
- 不要な共通化を避ける
- 動作確認してから次へ進む
- 区切りの良いタイミングでCommitする
- フェーズやチャットの区切りでドキュメントを更新する

---

## 37. 現在のステータス

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

Phase4
User一覧機能拡張
  ↓
User検索 完了
  ↓
Activeフィルタ 完了
  ↓
Step7 ソート ← 次回ここから
```

現在地点：

> **Phase4 Step6完了 / Step7ソート開始前**

次チャットでは `project-overview.md`、`architecture.md`、`handover_phase.md` を読み込み、その後GitHubの最新コードを確認して、**Phase4 Step7-1** から再開します。
