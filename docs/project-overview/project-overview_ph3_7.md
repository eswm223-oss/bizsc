# BizSC Project Overview

## 1. プロジェクト概要

プロジェクト名：**BizSC**

BizSC は、業務管理機能を段階的に構築しながら、Webアプリケーション開発の設計・実装・運用を学習するための個人開発プロジェクトである。

短期的に機能を増やすことだけを目的とせず、以下を重視する。

- 可読性
- 保守性
- 拡張性
- 型安全
- テスタビリティ
- 責務分離
- 理解しながら開発すること

---

# 2. 開発環境

## OS

- Windows

## 開発ツール

- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus

## リポジトリ

```text
eswm223-oss/bizsc
```

コード確認時は、引継ぎ資料だけで推測せず、必要に応じてGitHub上の最新コードを確認する。

---

# 3. 技術スタック

## Frontend

- React 19
- TypeScript
- Vite
- React Router
- Axios

## Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- Alembic
- Argon2
- pytest

## Database

- PostgreSQL 17

---

# 4. Docker構成

Docker Composeで以下の3サービスを管理する。

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

Frontendは開発時にViteを使用する。

BackendはFastAPI + Uvicornで動作する。

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

FrontendとBackendの責務を分離し、Backend内部でもLayered Architectureを採用する。

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

- URL定義
- Request受け取り
- Service呼び出し
- Response返却

## Service

担当：

- 業務ロジック
- Password Hash
- Validation
- 独自例外

## Repository

担当：

- CRUD
- SQLAlchemyによるDB操作

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

- API通信の呼び出し
- State管理
- Validation
- Error処理
- Loading状態管理
- 画面遷移
- 画面固有の表示処理

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

原則：

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

React RouterによるSPA遷移を行う。

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

FrontendからUser CRUDを利用できる状態になっている。

---

# 10. User機能

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

User CRUDの基本機能は完成している。

---

# 11. API Module

FrontendではPageからAxiosを直接利用せず、API Moduleを経由する。

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

- API通信処理の集約
- Pageの責務削減
- 将来的なAPI変更への対応
- テストしやすい構造

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

共通型は `frontend/src/types` で管理する。

---

# 13. UserForm

Create/EditフォームのUI重複を減らすため、共通 `UserForm` を導入済み。

UserFormの担当：

- Email
- Password
- Active
- Submitボタン
- Submit状態表示

UserFormに持たせないもの：

- API通信
- Validationロジック
- Axiosエラー処理
- 画面遷移

これらはPage側で管理する。

---

# 14. UserForm UI改善

Phase3終盤でSubmitボタンの配置を改善した。

構造：

```tsx
<div className="user-form__actions">
  <Button type="submit" disabled={isSubmitting}>
    {isSubmitting ? submittingLabel : submitLabel}
  </Button>
</div>
```

`UserForm.css` で配置を管理する。

現在の基本方針：

```css
.user-form__actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}
```

目的：

- 入力欄とボタンの余白確保
- Submitボタン右寄せ
- 配置責務をButton本体から分離

---

# 15. Badge

Phase3のUI改善でステータス表示用の共通 `Badge` を追加した。

構成：

```text
components/Badge/
├── Badge.tsx
└── Badge.css
```

現在のvariant：

```text
success
neutral
```

使用例：

```tsx
<Badge variant={user.is_active ? "success" : "neutral"}>
  {user.is_active ? "有効" : "無効"}
</Badge>
```

BadgeはUser固有の業務ロジックを持たない。

状態判定はPage側で行う。

---

# 16. User一覧 UI

User一覧ではステータス表示を改善済み。

以前：

```text
Active
Inactive
```

現在：

```text
有効
無効
```

Badgeを利用して表示する。

これによりステータスの視認性と、一覧・詳細画面間の表示統一を行った。

---

# 17. User詳細 UI

Phase3終盤でUser詳細画面を改善した。

## 詳細情報

`dl / dt / dd` を利用し、CSS Gridで2列表示にした。

```text
ID              値
メールアドレス    値
ステータス        Badge
作成日時          値
更新日時          値
```

## 操作エリア

現在：

```text
一覧へ戻る                         編集  削除
```

- 「一覧へ戻る」は左側
- 「編集」「削除」は右側
- 削除は `Button variant="danger"` を利用

画面固有のレイアウトは `UserDetailPage.css` で管理する。

---

# 18. 日時表示

Userの日時はAPI上では `string` として扱う。

```text
created_at
updated_at
```

UserDetailPageでは表示時だけ整形する。

```tsx
function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}
```

重要：

- DB値は変更しない
- API値も変更しない
- Frontend表示時のみ変換する

現在はUserDetailPage内に置き、必要になるまで共通化しない。

---

# 19. Loading設計

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

---

# 20. Error Handling

## Backend

独自例外：

```text
AppError
UserNotFoundError
EmailAlreadyRegisteredError
```

Exception Handlerを利用する。

## Frontend

- Axios Error
- Email重複
- Validation Error
- 共通ErrorMessage

Frontendだけで保証せず、Backendを最終的なValidation保証とする。

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

将来使う可能性だけを理由に、過剰な共通化は行わない。

---

# 23. 開発フェーズ

## Phase1

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

完了。

## Phase2

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

完了。

## Phase3

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
- UI改善

**現在Phase3終盤。**

---

# 24. Phase3終盤で実施した内容

今回の開発で以下を実施した。

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
```

---

# 25. 現在の到達点

```text
Phase1
環境構築
    ↓
Phase2
Backend / User CRUD
    ↓
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
Button配置改善
    ↓
Badge
    ↓
User一覧ステータス改善
    ↓
User詳細ステータス改善
    ↓
User詳細UI改善
    ↓
日時表示改善
    ↓
現在地点
```

---

# 26. 次回開始位置

次回は、

> **Phase3 Step5：共通UI全体の見直し**

から開始する。

最初はコードを変更せず、GitHub上の現在の実装を確認する。

確認対象：

```text
Button
Card
Input
Loading
ErrorMessage
Badge
```

あわせて各PageのCSSも確認する。

確認するポイント：

- 共通化すべき部分
- Page側に残す部分
- 余白の統一
- 見た目の統一
- CSS責務
- 不要な共通化がないか

---

# 27. Phase3完了に向けた予定

Step5後：

```text
共通UI見直し
    ↓
User各画面の表示確認
    ↓
User CRUD全体の動作確認
    ↓
必要な軽微修正
    ↓
Phase3完了
```

区切りの良い地点でCommit / Pushを行う。

---

# 28. Phase4候補

Phase3完了後の候補：

- User検索
- ページネーション
- ソート
- フィルタ
- CRUDテスト追加

詳細な順序はPhase3完了後に決定する。

---

# 29. Phase5以降の候補

将来的なBizSC拡張候補：

- 業務管理
- 権限管理
- ダッシュボード
- マスタ管理
- ログ管理

現段階では詳細設計を固定しない。

---

# 30. Git運用

基本方針：

- 小さい単位でCommit
- 動作確認後Commit
- フェーズ単位でPush
- 区切りの良いタイミングでドキュメント更新

現在のPhase3 UI改善は変更がまとまっている。

次回、Gitの変更状況を確認し、Step5開始前またはStep5完了後をCommit候補とする。

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

役割：

## project-overview.md

プロジェクト全体の現在地・進捗・今後の予定。

## architecture.md

設計思想・責務分離・システム構成。

## handover_phase.md

次回チャットへ引き継ぐための詳細な作業状況。

---

# 32. 次回チャットでの参照資料

次回は以下の3ファイルを基準にする。

```text
project-overview.md
architecture.md
handover_phase.md
```

さらにコード変更時はGitHubリポジトリ：

```text
eswm223-oss/bizsc
```

の最新コードを確認する。

---

# 33. 開発方針

今後も以下を維持する。

- 一度に大きく変更しない
- 1ステップずつ進める
- なぜ変更するのか理解してから実装する
- UIと業務処理を分離する
- PageとComponentの責務を分離する
- Backendを最終Validation保証とする
- 型安全を維持する
- 不要な共通化を避ける
- 動作確認してから次へ進む
- 区切りの良いタイミングでCommitする

---

# 34. 現在のステータス

**Phase3終盤**

実装済み：

- Backend User CRUD
- Frontend User CRUD
- React Router
- API Module
- 共通UI
- UserForm
- Badge
- User詳細UI改善
- 日時表示改善

次：

> **共通UI全体の見直し（Step5）**

その後、Phase3全体の最終確認へ進む。
