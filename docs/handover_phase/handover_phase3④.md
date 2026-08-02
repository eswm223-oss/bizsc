# BizSC Handover

## 引き継ぎ概要

本ドキュメントは、Phase3後半（User一覧改善〜User新規作成画面実装完了時点）の実装内容と、次回以降の開発方針をまとめたものです。

---

# 現在の到達点

## Backend

Phase2で実装したバックエンドは完成済み。

### 実装済み

- User CRUD API
- Repository
- Service
- Router
- SQLAlchemy
- Pydantic Validation
- 共通Exception Handler
- Password Hash（Argon2）
- pytestによる基本テスト

正常動作確認済み。

---

## Frontend

Phase3を継続中。

### Routing

実装済み

- BrowserRouter
- AppRoutes
- MainLayout
- HomePage
- UserListPage
- UserDetailPage
- UserCreatePage
- NotFoundPage

現在のルーティング

```text
/

/users

/users/new

/users/:userId
```

---

### API

実装済み

users.ts

- getUsers()
- getUser()
- createUser()

API通信は必ず `src/api` を経由する。

---

### 共通UI

現在

- Button
- Input
- Card
- Loading
- ErrorMessage

---

### User一覧画面

改善完了。

実装済み

- Card適用
- Loading表示
- Error表示
- Empty表示
- Table表示
- User詳細リンク
- 新規作成リンク

---

### User詳細画面

実装済み

表示内容

- ID
- Email
- Active
- created_at
- updated_at

一覧へ戻るリンク実装済み。

---

### User新規作成画面

実装済み

入力項目

- Email
- Password

画面機能

- 必須チェック
- Password8文字以上
- POST /users
- 作成成功時一覧へ戻る
- 送信中ボタン無効化
- 作成中表示

---

### エラーハンドリング

Axios Error Handling

409

- Email入力欄へエラー表示

422

- 入力エラー表示

その他

- 共通エラー表示

---

# 動作確認済み

正常

- User一覧取得
- User詳細取得
- User作成
- User作成後一覧へ戻る
- Loading表示
- Error表示
- Empty表示

異常

- Email重複
- Password不足
- APIエラー表示

---

# 現在のディレクトリ構成

```text
src/

├── api/
│   ├── client.ts
│   ├── health.ts
│   └── users.ts

├── components/
│   ├── Button/
│   ├── Card/
│   ├── ErrorMessage/
│   ├── Input/
│   └── Loading/

├── layouts/

├── pages/
│   ├── HomePage.tsx
│   ├── UserListPage.tsx
│   ├── UserDetailPage.tsx
│   ├── UserCreatePage.tsx
│   └── NotFoundPage.tsx

├── routes/

├── types/
```

---

# 次回開始位置

Phase3を継続する。

## Step1

UserEditPageを実装する。

実装予定

- UserUpdate型追加
- updateUser() API追加
- UserEditPage作成
- PATCH /users/{id}
- 更新成功後詳細画面へ戻る

---

## Step2

User一覧へ編集ボタン追加

```text
一覧

詳細

編集
```

---

## Step3

User詳細画面へ編集導線追加

```text
詳細

編集

一覧へ戻る
```

---

## Step4

削除導線追加

- DELETE API利用
- 確認ダイアログ
- 一覧へ戻る

---

# 開発方針

引き続き以下を維持する。

- Layered Architecture
- 型安全
- API Module経由の通信
- Component分割
- 再利用可能なUI
- 保守性・拡張性を優先

---

# コミット推奨

今回の区切りでは

```text
feat: implement user detail and create pages
```

---

# 次回開始時の最初の作業

1. UserUpdate型追加
2. updateUser() API追加
3. UserEditPage作成
4. /users/:userId/edit ルート追加
5. 編集画面実装

---

# 注意事項

- Backendは完成済みのため、大きな変更は行わない。
- API通信は `src/api` を経由する。
- 型は `src/types` に集約する。
- 共通UIコンポーネントを積極的に利用する。
- React RouterによるSPA遷移を維持する。
- React 19環境では `FormEvent` ではなく `SubmitEvent` を採用しているため、新規フォーム実装時も同様の方針を維持する。