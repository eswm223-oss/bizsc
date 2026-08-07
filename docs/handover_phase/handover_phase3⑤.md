# BizSC Handover

## 引き継ぎ概要

本ドキュメントは、Phase3後半（User編集・削除機能実装完了時点）の実装内容と、次回以降の開発方針をまとめたものです。

------------------------------------------------------------------------

# 現在の到達点

## Backend

Phase2で実装したバックエンドは完成済み。

### 実装済み

-   User CRUD API
-   Repository
-   Service
-   Router
-   SQLAlchemy
-   Pydantic Validation
-   共通Exception Handler
-   Password Hash（Argon2）
-   pytestによる基本テスト

バックエンドへの大きな変更は不要。

------------------------------------------------------------------------

## Frontend

Phase3後半まで完了。

### Routing

実装済み

-   BrowserRouter
-   AppRoutes
-   MainLayout
-   HomePage
-   UserListPage
-   UserDetailPage
-   UserCreatePage
-   UserEditPage
-   NotFoundPage

現在のルーティング

``` text
/
/users
/users/new
/users/:userId
/users/:userId/edit
```

------------------------------------------------------------------------

### API

実装済み（src/api/users.ts）

-   getUsers()
-   getUser()
-   createUser()
-   updateUser()
-   deleteUser()

API通信は必ず `src/api` を経由する。

------------------------------------------------------------------------

### 共通UI

現在

-   Button
-   Input
-   Card
-   Loading
-   ErrorMessage

------------------------------------------------------------------------

### User一覧画面

実装済み

-   Loading表示
-   Error表示
-   Empty表示
-   Table表示
-   詳細画面リンク
-   新規作成リンク

------------------------------------------------------------------------

### User詳細画面

実装済み

表示内容

-   ID
-   Email
-   Active
-   created_at
-   updated_at

機能

-   編集画面への導線
-   削除ボタン
-   削除確認ダイアログ
-   削除成功後一覧へ戻る
-   一覧へ戻るリンク

------------------------------------------------------------------------

### User新規作成画面

実装済み

-   Email
-   Password
-   POST /users
-   必須チェック
-   Password8文字以上
-   Email重複エラー
-   APIエラー表示
-   作成成功後一覧へ戻る

------------------------------------------------------------------------

### User編集画面

実装済み

-   GET /users/{id}
-   初期値表示
-   Email更新
-   Active更新
-   PATCH /users/{id}
-   更新成功後詳細画面へ戻る
-   Email重複エラー
-   APIエラー表示

------------------------------------------------------------------------

# 動作確認済み

正常

-   User一覧取得
-   User詳細取得
-   User作成
-   User編集
-   User削除
-   Loading表示
-   Error表示

異常

-   Email重複
-   Password不足
-   APIエラー表示
-   削除キャンセル

------------------------------------------------------------------------

# 次回開始位置

Phase3継続

## Step1

UserCreatePage と UserEditPage の重複処理を確認する。

## Step2

Formコンポーネント共通化を検討する。

-   入力欄
-   バリデーション
-   Submit処理

## Step3

UI改善

-   Button配置
-   ステータス表示
-   画面レイアウト調整

------------------------------------------------------------------------

# 開発方針

引き続き以下を維持する。

-   Layered Architecture
-   型安全
-   API Module経由の通信
-   Component分割
-   再利用可能なUI
-   保守性・拡張性を優先

------------------------------------------------------------------------

# コミット推奨

今回の区切り

``` text
feat: implement user edit and delete features
```

------------------------------------------------------------------------

# 次回開始時の最初の作業

1.  Create/Edit画面の重複箇所を洗い出す
2.  Form共通化方針を決める
3.  共通Formコンポーネントを実装する

------------------------------------------------------------------------

# 注意事項

-   Backendは完成済みのため大きな変更は行わない。
-   API通信は `src/api` を経由する。
-   型は `src/types` に集約する。
-   共通UIコンポーネントを積極的に利用する。
-   React RouterによるSPA遷移を維持する。
-   React 19環境ではフォームイベントは `SubmitEvent` を採用する。
