# BizSC Project Overview

## 1. プロジェクト概要

プロジェクト名：**BizSC**

BizSC は、業務管理機能を段階的に構築しながら、Webアプリケーション開発の設計・実装・運用を学習するための個人開発プロジェクトです。

短期的に機能を増やすことだけを目的とせず、以下を重視します。

* 可読性
* 保守性
* 拡張性
* 型安全
* テスタビリティ
* 責務分離
* 理解しながら開発すること

---

# 2. 開発環境

## OS

* Windows

## 開発ツール

* Cursor
* GitHub
* GitHub Desktop
* Docker Desktop
* Docker Compose
* TablePlus

## リポジトリ

```text
eswm223-oss/bizsc
```

コード確認時は、引継ぎ資料だけで推測せず、必要に応じてGitHub上の最新コードを確認します。

---

# 3. 技術スタック

## Frontend

* React
* TypeScript
* Vite
* React Router
* Axios
* CSS

## Backend

* Python 3.13
* FastAPI
* Uvicorn
* SQLAlchemy 2.x
* Pydantic v2
* Alembic
* Argon2
* pytest

## Database

* PostgreSQL 17

---

# 4. Docker構成

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

# 5. システム構成

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

# 6. Backend構成

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

## Router

担当：

* URL定義
* Request受け取り
* Service呼び出し
* Response返却

## Service

担当：

* 業務ロジック
* Password Hash
* Validation
* 独自例外

## Repository

担当：

* CRUD
* SQLAlchemyによるDB操作

---

# 7. Frontend構成

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

## Pages

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

* API通信の呼び出し
* State管理
* Validation
* Error処理
* Loading状態管理
* 画面遷移
* 画面固有の表示処理

## Components

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

# 8. Routing

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

# 9. User API

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

# 10. User機能

現在実装済み：

* User一覧
* User詳細
* User新規作成
* User編集
* User削除
* Active / Inactive管理
* Loading表示
* Error表示
* React Routerによる画面遷移

User CRUDの基本機能は完成しています。

---

# 11. API Module

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

目的：

* API通信処理の集約
* Pageの責務削減
* 将来的なAPI変更への対応
* テストしやすい構造

---

# 12. User型

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

# 13. UserForm

Create / EditフォームのUI重複を減らすため、共通 `UserForm` を導入しています。

UserFormの担当：

* Email入力
* Password入力
* Active入力
* 入力項目ごとのError表示
* Submitボタン
* Submit状態表示
* フォーム内レイアウト

UserFormに持たせないもの：

* API通信
* Validation判断
* Axiosエラー処理
* 画面遷移
* 業務ロジック

これらはPage側で管理します。

---

# 14. 共通UI

## Badge

ステータス表示用の共通UI。

現在のvariant：

```text
success
neutral
```

User状態では、

```text
有効 → success
無効 → neutral
```

として利用します。

BadgeはUser固有の業務ロジックを持ちません。

---

## Button

現在の主なvariant：

```text
primary
secondary
danger
```

HTML標準のbutton属性を利用できます。

---

## Card

担当：

* コンテンツ領域
* タイトル
* 枠
* 内部余白

Page固有の業務処理は持ちません。

---

## Input

担当：

* label
* input
* 入力項目単位のError表示

入力欄同士の配置はUserForm等の親Component側で管理します。

---

## Loading

API通信中の読み込み表示に使用します。

---

## ErrorMessage

画面・API単位のエラー表示に使用します。

入力項目単位のエラーはInput側に表示します。

---

# 15. User一覧 UI

User一覧では以下を表示します。

```text
ID
メールアドレス
ステータス
操作
```

ステータスはBadgeで表示します。

```text
有効
無効
```

Cardタイトル：

```text
ユーザー一覧
```

Phase3終盤で、Badgeと重複していたPage側のステータス文字スタイルを整理しました。

---

# 16. User詳細 UI

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

削除には、

```tsx
variant="danger"
```

を利用します。

日時は表示時のみ整形します。

```tsx
function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}
```

現在はUserDetailPage内に置いています。

他画面でも必要になった場合に共通化を検討します。

---

# 17. User新規作成 UI

UserCreatePageではUserFormを利用します。

主な処理：

* Email入力
* Password入力
* Email必須確認
* Password8文字以上確認
* User作成API呼び出し
* API Error処理
* 作成後 `/users` へ遷移

Cardタイトル：

```text
ユーザ新規登録
```

---

# 18. User編集 UI

UserEditPageではUserFormを利用します。

主な処理：

* User情報取得
* Email編集
* Active編集
* User更新API呼び出し
* API Error処理
* 更新後User詳細画面へ遷移

Cardタイトル：

```text
ユーザー編集
```

Phase3終盤で、Card内に直接`h1`を書く方式からCardの`title`を利用する方式へ統一しました。

---

# 19. Loading設計

主なState：

```text
isLoading
isSubmitting
isDeleting
```

処理中：

* Loading表示
* Button無効化
* 二重送信防止

表示例：

```text
読み込み中...
作成中...
更新中...
削除中...
```

---

# 20. Error Handling

## Backend

独自例外を利用します。

例：

```text
AppError
UserNotFoundError
EmailAlreadyRegisteredError
```

Exception HandlerでResponseへ変換します。

## Frontend

主なError：

* Axios Error
* Email重複
* Validation Error
* API取得失敗
* 作成失敗
* 更新失敗
* 削除失敗

FrontendだけでValidation保証を行わず、Backendを最終的なValidation保証とします。

---

# 21. CSS設計

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

---

# 22. 共通化方針

現在共通化済み：

* Badge
* Button
* Card
* ErrorMessage
* Input
* Loading
* UserForm

共通化の判断基準：

* 複数画面で利用するか
* 責務が明確か
* 業務ロジックを持たないか
* 共通化によって複雑にならないか

以下だけを理由に共通化しません。

```text
将来使うかもしれない
なんとなく再利用できそう
コードが短くなる
```

必要になった時点で共通化します。

---

# 23. 開発フェーズ

## Phase1

環境構築。

主な内容：

* Windows開発環境
* Cursor
* Docker Desktop
* Docker Compose
* Frontend
* Backend
* PostgreSQL
* GitHub連携

**完了。**

---

## Phase2

Backend / User CRUD。

主な内容：

* SQLAlchemy Model
* Repository
* Pydantic Schema
* Service
* Router
* Alembic
* Exception Handler
* Password Hash
* User CRUD

**完了。**

---

## Phase3

Frontend CRUD / 共通UI。

主な内容：

* React Router
* API Module
* User一覧
* User詳細
* User作成
* User編集
* User削除
* Loading
* ErrorMessage
* Button
* Card
* Input
* UserForm
* Badge
* User詳細UI改善
* 共通UI全体見直し
* CRUD最終動作確認
* Frontend build確認

**完了。**

Phase3完了後の変更はGitHubへPush済みです。

---

# 24. Phase3終盤で実施した内容

Phase3終盤では以下を実施しました。

```text
Step1
UserForm導入後のUI確認

Step2
UserForm Submitボタン配置改善

Step3
Badgeコンポーネント追加

Step3
User一覧ステータスBadge化

Step3
User詳細ステータスBadge化

Step4
User詳細情報の2列レイアウト化

Step4
User詳細操作エリア整理

Step4
削除ボタンdanger表示

Step4
日時表示改善

Step5
共通UI全体見直し
```

Step5ではさらに以下を実施しました。

```text
UserFormの縦方向余白整理
UserEditPageのCardタイトル統一
UserListPageの不要なステータス文字スタイル整理
UserListPageタイトルの日本語統一
各User画面の表示確認
User CRUD全体の動作確認
Frontend build確認
```

---

# 25. Phase3最終確認

Phase3完了前に、ブラウザ上で以下を確認済みです。

```text
User一覧表示
User新規作成
作成後一覧遷移
User詳細表示
User編集
編集内容反映
User削除
削除後一覧遷移
Badge表示
日時表示
画面レイアウト
```

Frontend build：

```powershell
docker compose exec frontend npm run build
```

正常完了済みです。

---

# 26. 現在の到達点

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
Frontend CRUD
    ↓
React Router
    ↓
API Module
    ↓
共通UI
    ↓
UserForm
    ↓
Badge
    ↓
User詳細UI改善
    ↓
共通UI全体見直し
    ↓
CRUD最終動作確認
    ↓
Frontend build確認
    ↓
Phase3 完了
    ↓
GitHub Push済み
```

現在地点：

> **Phase3完了 / Phase4開始前**

---

# 27. Phase4候補

Phase4候補：

* User検索
* ページネーション
* ソート
* フィルタ
* CRUDテスト追加

詳細な実装順はまだ確定していません。

Phase4開始時に、GitHub上の最新コードと既存構成を確認してから順序を決定します。

---

# 28. Phase4開始時の進め方

次チャットでは、以下の順番で開始します。

```text
Step1
引継ぎ資料確認

Step2
GitHub最新コード確認

Step3
Phase4候補整理

Step4
Phase4実装順決定

Step5
最初の機能実装
```

一度にすべて実装せず、1機能ずつ進めます。

---

# 29. Phase5以降の候補

将来的なBizSC拡張候補：

* 業務管理
* 権限管理
* ダッシュボード
* マスタ管理
* ログ管理

現段階では詳細設計を固定しません。

---

# 30. Git運用

基本方針：

* 小さい単位でCommit
* 動作確認後Commit
* フェーズ単位でPush
* 区切りの良いタイミングでドキュメント更新

Phase3完了時点の変更はCommit / Push済みです。

---

# 31. ドキュメント

主要ドキュメント：

```text
README.md
project-overview.md
architecture.md
handover_phase.md
decisions/
```

## project-overview.md

プロジェクト全体の現在地・進捗・今後の予定。

## architecture.md

設計思想・責務分離・システム構成。

## handover_phase.md

次回チャットへ引き継ぐための詳細な作業状況。

## decisions/

重要な設計判断を記録します。

---

# 32. 次回チャットでの参照資料

次回は以下の3ファイルを基準にします。

```text
project-overview.md
architecture.md
handover_phase.md
```

さらにコード変更時はGitHubリポジトリ：

```text
eswm223-oss/bizsc
```

の最新コードを確認します。

---

# 33. 開発方針

今後も以下を維持します。

* 一度に大きく変更しない
* 1ステップずつ進める
* なぜ変更するのか理解してから実装する
* GitHub実コードを確認してから変更案を出す
* UIと業務処理を分離する
* PageとComponentの責務を分離する
* Backendを最終Validation保証とする
* 型安全を維持する
* 不要な共通化を避ける
* 動作確認してから次へ進む
* 区切りの良いタイミングでCommitする
* フェーズ区切りでドキュメントを更新する

---

# 34. 現在のステータス

**Phase3 完了**

実装済み：

* Backend User CRUD
* Frontend User CRUD
* React Router
* API Module
* 共通UI
* UserForm
* Badge
* User詳細UI改善
* 共通UI全体見直し
* CRUD最終動作確認
* Frontend build確認

GitHub：

> **Phase3完了時点までPush済み**

次：

> **Phase4の実装計画整理**

Phase4の詳細なStepは、次チャットで最新コードを確認してから決定します。
