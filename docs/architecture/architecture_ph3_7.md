# BizSC Architecture

## 目的

本ドキュメントは、BizSC の設計思想と現在のシステム構成を記録する。

コードだけでは伝わりにくい「なぜこの設計にしたのか」を残し、将来の保守性・拡張性を高めることを目的とする。

---

# 基本設計方針

本プロジェクトでは、以下を優先する。

- 可読性
- 保守性
- 拡張性
- 型安全
- テスタビリティ
- 理解しながら開発すること

短期的な実装速度だけを優先せず、長期的に保守しやすい構成を採用する。

---

# システム構成

```text
Browser
    │
    ▼
React（Vite）
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
Axios Client
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

すべて Docker Compose 上で動作する。

```text
Docker Compose
├── frontend
├── backend
└── db
```

---

# 技術スタック

## Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- Alembic
- Argon2
- pytest

## Frontend

- React 19
- TypeScript
- Vite
- React Router
- Axios

## Database

- PostgreSQL 17

## Development

- Cursor
- Docker Desktop
- Docker Compose
- GitHub Desktop
- TablePlus

---

# ディレクトリ構成

## Frontend

```text
frontend/src/

api/
components/
    Badge/
    Button/
    Card/
    ErrorMessage/
    Input/
    Loading/
    UserForm/
layouts/
pages/
routes/
types/
```

## Backend

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

責務ごとのレイヤー分離を維持する。

---

# Frontend設計

## Pages

Pagesは画面単位の責務を持つ。

現在実装済み

- HomePage
- UserListPage
- UserDetailPage
- UserCreatePage
- UserEditPage
- NotFoundPage

担当する責務

- URL取得
- API呼び出し
- State管理
- Loading表示
- Error表示
- 画面遷移
- 画面固有のデータ表示・整形

---

## Components

共通UI

- Badge
- Button
- Card
- ErrorMessage
- Input
- Loading
- UserForm

複数画面で利用できるUIのみ配置する。

### Badge

Phase3のUI改善で追加したステータス表示用の共通UI。

担当

- 子要素の表示
- variantに応じた見た目の切り替え
- success / neutral のスタイル提供

担当しないもの

- Userの状態判定
- `is_active` の解釈
- 業務ロジック

状態判定はPage側で行い、Badgeは表示だけを担当する。

例：

```tsx
<Badge variant={user.is_active ? "success" : "neutral"}>
  {user.is_active ? "有効" : "無効"}
</Badge>
```

---

## UserForm

Phase3で追加した共通フォーム。

目的

- Create/Edit画面の重複削減
- UI統一
- 保守性向上

担当

- Email入力
- Password入力（Createのみ）
- Active入力（Editのみ）
- Submitボタン
- Submit状態表示

担当しないもの

- API通信
- バリデーション
- 画面遷移
- Axiosエラー処理

これらはPage側で管理する。

### UserFormのUI方針

Submitボタンは `user-form__actions` で配置領域を分離する。

```text
UserForm
├── Input
├── Input / Active
└── Actions
    └── Button
```

`UserForm.css` でフォーム固有の余白・配置を管理し、Button自体の見た目は共通Buttonコンポーネントへ任せる。

---

## UserDetailPage

Phase3のUI改善で詳細画面の構造を整理した。

### 情報表示

`dl / dt / dd` を利用し、CSS Gridで「項目名 / 値」の2列表示にする。

```text
ID            値
メールアドレス  値
ステータス      Badge
作成日時        値
更新日時        値
```

### 操作エリア

操作部分は情報表示から分離する。

```text
一覧へ戻る                         編集  削除
```

- 左側：一覧へ戻る
- 右側：編集・削除
- 削除：Buttonの `danger` variantを使用

画面固有の配置は `UserDetailPage.css` で管理する。

### 日時表示

APIから受け取る `created_at` / `updated_at` は `string` として保持し、画面表示時だけ整形する。

```tsx
function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}
```

現段階ではUserDetailPage内に置き、他画面でも日時整形が必要になった時点で共通化を検討する。

---

## API Module

画面からAxiosを直接利用しない。

```text
Page
    │
    ▼
API Module
    │
    ▼
Axios Client
```

現在

`users.ts`

- getUsers()
- getUser()
- createUser()
- updateUser()
- deleteUser()

---

## Types

共通型は `src/types` へ集約する。

User関連

- User
- UserListResponse
- UserCreate
- UserUpdate

Userの日時項目は現在以下の型で扱う。

```ts
created_at: string;
updated_at: string;
```

---

# Routing

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

React Router により SPA遷移を行う。

---

# Backendアーキテクチャ

Layered Architecture

```text
Request
    │
Router
    │
Service
    │
Repository
    │
Database
```

## Router

担当

- URL定義
- Request受け取り
- Service呼び出し
- Response返却

## Service

担当

- 業務ロジック
- Password Hash
- Validation
- 独自例外送出

## Repository

担当

- CRUD
- SQLAlchemy操作

---

# API

現在利用

```text
GET     /health
GET     /health/db

POST    /users
GET     /users
GET     /users/{id}
PATCH   /users/{id}
DELETE  /users/{id}
```

FrontendはUser CRUDをすべて利用している。

---

# バリデーション

Frontend

- 必須
- Password8文字以上

Backend

- EmailStr
- model_validator
- Request Schema

Backendを最終保証とする。

---

# エラーハンドリング

Backend

- AppError
- UserNotFoundError
- EmailAlreadyRegisteredError

Frontend

- Axios
- Email重複
- Validation Error
- 共通Error表示

---

# Loading設計

State

- isLoading
- isSubmitting
- isDeleting

処理中

- Loading表示
- ボタン無効
- 二重送信防止

---

# CSS / UI設計

共通コンポーネントの見た目は各コンポーネントのCSSで管理する。

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

画面固有のレイアウトはPage側のCSSで管理する。

例：

```text
pages/
├── UserListPage.css
└── UserDetailPage.css
```

原則として、共通UIの見た目と画面固有レイアウトを分離する。

---

# 共通化方針

現在共通化済み

- Badge
- Button
- Card
- ErrorMessage
- Input
- Loading
- UserForm

処理を何でも共通化するのではなく、まず **UIの共通化** を優先する。

共通化の判断基準

- 複数画面で利用するか
- 責務が明確か
- Page固有の業務処理を持たないか
- 共通化によってコードが逆に複雑にならないか

現時点では、一度しか使わない処理を無理に `utils` 等へ切り出さない。

---

# Phase3 UI改善で実施した内容

- UserFormのSubmitボタン配置領域追加
- UserFormのボタン右寄せ・余白調整
- Badgeコンポーネント追加
- User一覧のActive / Inactive表示を「有効 / 無効」Badgeへ変更
- User詳細のActive / Inactive表示を「有効 / 無効」Badgeへ変更
- User詳細情報を2列レイアウトへ変更
- User詳細の操作エリアを整理
- 削除ボタンをdanger表示へ変更
- User詳細の日時表示を `ja-JP` 形式へ整形

---

# 今後の予定

## Phase3 続き

次回開始位置：共通UI全体の見直し

確認対象

- Button
- Card
- Input
- Loading
- ErrorMessage
- Badge
- 各PageのCSS

目的

- 共通化した方がよい部分の確認
- Page側に残すべき部分の確認
- 余白・見た目の統一
- 不要な共通化を避ける

## Phase4

- User検索
- ページネーション
- ソート
- フィルタ
- CRUDテスト追加

## Phase5

- 業務管理
- 権限管理
- ダッシュボード
- マスタ管理
- ログ管理

---

# Git運用

- 小さい単位でCommit
- フェーズ単位でPush
- 動作確認後Commit
- 区切りの良いタイミングでドキュメント更新

今回のPhase3 UI改善は変更がまとまっているため、共通UI全体の見直し完了後を次のCommit候補とする。

---

# ドキュメント

継続更新

- README.md
- project-overview.md
- architecture.md
- handover_phase.md
- decisions/

---

# 設計原則

継続する方針

- Layered Architecture
- Repository Pattern
- Service Layer
- SQLAlchemy 2.x
- Pydantic v2
- Dependency Injection
- Exception Handler
- React Router
- Axios
- API Module
- UserFormによるUI共通化
- Badge等の再利用可能なUI共通化
- PageとComponentの責務分離
- 共通UIと画面固有CSSの分離
- 型安全
- 保守性・拡張性優先
- 過剰な共通化を避ける

---

# 現在の到達点

Phase3終盤。

現在利用可能

- User一覧
- User詳細
- User新規作成
- User編集
- User削除
- 共通レイアウト
- 共通UI
- UserForm共通化
- Badgeによるステータス表示
- User詳細画面のUI改善
- 日時の表示整形

次回は **共通UI全体の見直し（Step5）** から開始する。
