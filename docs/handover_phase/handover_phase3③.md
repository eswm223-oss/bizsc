# BizSC Handover

## 引き継ぎ概要

本ドキュメントは、Phase3（フロントエンド基盤）の途中時点における実装内容と、次回以降の開発方針をまとめたものです。

---

# 現在の到達点

## Backend

Phase2で実装したバックエンドは完成済み。

### 実装済み機能

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

Phase3を継続中。

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

以下の共通UIコンポーネントを実装済み。

```text
components/
├── Button/
│   ├── Button.tsx
│   └── Button.css
│
├── Input/
│   ├── Input.tsx
│   └── Input.css
│
├── Card/
│   ├── Card.tsx
│   └── Card.css
│
├── Loading/
│   ├── Loading.tsx
│   └── Loading.css
│
└── ErrorMessage/
    ├── ErrorMessage.tsx
    └── ErrorMessage.css
```

---

### Pages

現在

```text
pages/
├── HomePage.tsx
├── UserListPage.tsx
└── NotFoundPage.tsx
```

HomePageでは共通コンポーネントの動作確認を実施済み。

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
* Button表示
* Input表示
* Card表示
* Loading表示
* ErrorMessage表示
* 各コンポーネントの組み合わせ表示

---

# 現在のディレクトリ構成

```text
src/
├── api/
├── components/
│   ├── Button/
│   ├── Card/
│   ├── ErrorMessage/
│   ├── Input/
│   └── Loading/
├── layouts/
├── pages/
├── routes/
├── types/
└── utils（未使用）
```

---

# 次回開始位置

Phase3を継続する。

## 1. User一覧画面改善

現在の `UserListPage` を改善する。

実施予定

* Card適用
* Loading表示
* Error表示
* Empty表示
* テーブルレイアウト化
* API取得処理の整理

---

## 2. User CRUD画面

作成予定

* UserDetailPage
* UserCreatePage
* UserEditPage
* User削除導線

既存APIを利用して画面を実装する。

---

## 3. レイアウト改善

実施予定

* Sidebar幅固定
* Headerデザイン改善
* Footerデザイン改善
* Flex調整
* レスポンシブ対応

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

今回の区切りでは、以下のコミットメッセージを推奨。

```text
feat: add reusable UI components for frontend
```

---

# 次回開始時の最初の作業

1. `UserListPage.tsx` の現状コードを確認
2. Cardレイアウトへ変更
3. Loading / Error / Empty表示を実装
4. テーブル形式へ改善
5. User詳細画面の実装へ進む

---

# 引き継ぎ時の注意事項

* Backendは完成済みのため、大きな変更は行わない。
* API通信は必ず `src/api` 配下を経由し、画面からAxiosを直接呼び出さない。
* 型定義は `src/types` に集約する。
* 共通UIコンポーネントを積極的に再利用する。
* HomePageは現在、共通コンポーネントのサンプル表示用となっているため、User一覧画面の実装後に本来の役割へ戻す予定。
