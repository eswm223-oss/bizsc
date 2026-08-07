# BizSC Handover

## 引き継ぎ概要

本ドキュメントは、Phase3終盤（UserForm共通化完了時点）の実装内容と、次回以降の開発方針をまとめたものです。

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

バックエンドへの大きな変更は不要。

---

## Frontend

Phase3終盤まで完了。

### Routing

実装済み

- BrowserRouter
- AppRoutes
- MainLayout
- HomePage
- UserListPage
- UserDetailPage
- UserCreatePage
- UserEditPage
- NotFoundPage

現在のルーティング

```text
/
/users
/users/new
/users/:userId
/users/:userId/edit
```

---

### API

実装済み（src/api/users.ts）

- getUsers()
- getUser()
- createUser()
- updateUser()
- deleteUser()

API通信は必ず `src/api` を経由する。

---

### 共通UI

現在

- Button
- Input
- Card
- Loading
- ErrorMessage
- UserForm

---

### User一覧画面

実装済み

- Loading表示
- Error表示
- Empty表示
- Table表示
- 詳細画面リンク
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

機能

- 編集画面への導線
- 削除ボタン
- 削除確認ダイアログ
- 削除成功後一覧へ戻る
- 一覧へ戻るリンク

---

### User新規作成画面

実装済み

- Email
- Password
- POST /users
- 必須チェック
- Password8文字以上
- Email重複エラー
- APIエラー表示
- 作成成功後一覧へ戻る

フォーム表示は `UserForm` を利用する。

---

### User編集画面

実装済み

- GET /users/{id}
- 初期値表示
- Email更新
- Active更新
- PATCH /users/{id}
- 更新成功後詳細画面へ戻る
- Email重複エラー
- APIエラー表示

フォーム表示は `UserForm` を利用する。

---

### UserForm

Phase3で追加した共通フォーム。

担当

- Email入力
- Password入力（Createのみ）
- Active入力（Editのみ）
- Submitボタン
- Submit状態表示

担当しないもの

- API通信
- バリデーション
- Axiosエラー処理
- 画面遷移

これらは各Pageで管理する。

---

# 動作確認済み

正常

- User一覧取得
- User詳細取得
- User作成
- User編集
- User削除
- Loading表示
- Error表示
- UserForm表示
- Createフォーム
- Editフォーム

異常

- Email重複
- Password不足
- APIエラー表示
- 削除キャンセル

---

# 今回実施したリファクタリング

Create画面・Edit画面に存在していたフォームUIを共通コンポーネントへ切り出した。

追加したコンポーネント

```text
components/
└── UserForm/
    └── UserForm.tsx
```

共通化した内容

- Email入力
- Password入力（Createのみ）
- Active入力（Editのみ）
- Submitボタン
- Submit中表示

共通化しなかった内容

- API通信
- バリデーション
- State管理
- Axiosエラー処理
- 画面遷移

UIのみを共通化し、業務処理はPage側へ残す設計としている。

---

# 次回開始位置

Phase3継続

## Step1

UserForm導入後のUI調整

- Button配置
- 余白調整
- 見た目統一

## Step2

ステータス表示改善

- Active表示
- Badge化検討

## Step3

共通UI見直し

- Card
- Button
- Input
- Loading

必要に応じてデザインを改善する。

---

# 開発方針

引き続き以下を維持する。

- Layered Architecture
- 型安全
- API Module経由の通信
- Component分割
- UserFormによるフォーム共通化
- 再利用可能なUI
- 保守性・拡張性を優先

---

# コミット履歴

今回の区切り

```text
refactor: extract shared user form component
```

---

# 次回開始時の最初の作業

1. UserFormのUI確認
2. Button配置調整
3. ステータス表示改善
4. 共通UI全体のデザイン見直し

---

# 注意事項

- Backendは完成済みのため大きな変更は行わない。
- API通信は `src/api` を経由する。
- 型は `src/types` に集約する。
- UIのみを共通化し、API処理はPage側に残す。
- React RouterによるSPA遷移を維持する。
- React19環境では `SubmitEvent` を利用する。
- UI改善時も責務分離を維持し、共通コンポーネントへ業務ロジックを持たせない。