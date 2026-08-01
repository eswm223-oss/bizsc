# BizSC Handover

## 引き継ぎ概要

本ドキュメントは Phase3（フロントエンド基盤）の途中時点における実装内容と、次回以降の開発方針をまとめたものです。

---

# 現在の到達点

## Backend

Phase2で実装したバックエンドは完成済み。

実装済み機能

* User CRUD API
* Repository
* Service
* Router
* SQLAlchemy
* Pydantic Validation
* 共通Exception Handler
* Password Hash（Argon2）
* pytestによる基本テスト

正常に動作確認済み。

---

## Frontend

Phase3の基盤構築を実施。

現在は以下が実装済み。

### Routing

* BrowserRouter
* AppRoutes
* HomePage
* UserListPage
* NotFoundPage

---

### API

Axios導入済み。

共通API Clientを作成済み。

```text
src/api/
├── client.ts
├── health.ts
└── users.ts
```

環境変数

```text
VITE_API_BASE_URL
```

でAPI接続先を管理している。

---

### Layout

共通レイアウト完成。

```text
MainLayout
├── Header
├── Sidebar
├── Outlet
└── Footer
```

MainLayout.css により

* Header
* Sidebar
* Content

のレイアウト基盤を作成済み。

---

### Components

現在

```text
components/
├── Header.tsx
├── Sidebar.tsx
└── Footer.tsx
```

のみ実装。

---

### Pages

現在

```text
pages/
├── HomePage.tsx
├── UserListPage.tsx
└── NotFoundPage.tsx
```

---

### Types

現在

```text
types/
├── health.ts
└── user.ts
```

---

# 動作確認済み

正常動作確認済み。

* React Router
* Headerリンク
* Sidebar表示
* Footer表示
* Health API通信
* User一覧取得
* React ⇔ FastAPI通信

---

# 現在のディレクトリ構成

```text
src/
├── api/
├── components/
├── layouts/
├── pages/
├── routes/
├── types/
└── utils（未使用）
```

---

# 次回開始位置

Phase3を継続する。

以下の順番で進める予定。

## 1. 共通UIコンポーネント

作成予定

```text
components/
├── Button
├── Input
├── Card
├── Loading
└── ErrorMessage
```

目的

* UIの共通化
* 再利用性向上
* デザイン変更容易化

---

## 2. レイアウト改善

実施予定

* Sidebar幅固定
* Headerデザイン
* Footerデザイン
* Flex調整
* レスポンシブ対応

---

## 3. User一覧改善

予定

* テーブル表示
* Loading表示
* Error表示
* Empty表示

---

## 4. User CRUD画面

作成予定

* UserDetailPage
* UserCreatePage
* UserEditPage

既存APIを利用して画面を実装する。

---

# 開発方針

引き続き以下を維持する。

* Layered Architecture
* 型安全
* コンポーネント分割
* API処理とUI処理の分離
* 再利用可能な構成
* 保守性・拡張性を優先

---

# コミット推奨

Phase3基盤構築完了として、以下のコミットメッセージを推奨。

```text
feat: build frontend foundation with routing, layout and API integration
```

---

# 引き継ぎ時の注意事項

* Backendは完成済みのため、大きな変更は行わない。
* Frontendは基盤構築が完了し、次回からUIの充実とCRUD画面実装へ進む。
* 新しいコンポーネントを追加する際も、責務を明確に分離する。
* API通信は必ず `src/api` 配下を経由し、画面からAxiosを直接呼び出さない。
* 型定義は `src/types` に集約し、コンポーネント内で重複定義しない。
