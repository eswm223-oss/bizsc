# BizSC Handover — Phase3

## 目的

本ドキュメントは、BizSC の現在の開発状況を次のチャットへ引き継ぐための資料である。

次回は本資料と以下の資料を参照して開発を再開する。

- `project-overview.md`
- `architecture.md`
- `handover_phase.md`

---

# プロジェクト

プロジェクト名：BizSC

開発環境：

- Windows
- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus

技術構成：

```text
Frontend
React + TypeScript + Vite
React Router
Axios

Backend
FastAPI
Python 3.13
SQLAlchemy 2.x
Pydantic v2
Alembic

Database
PostgreSQL 17
```

Docker Compose サービス：

```text
frontend
backend
db
```

---

# 現在のフェーズ

現在は **Phase3 終盤**。

User CRUD の基本機能は完成しており、現在はフロントエンドUIの整理・共通化を進めている。

次回開始位置：

> **Step5：共通UI全体の見直し**

---

# 現在利用可能なUser機能

以下は実装済み。

- User一覧
- User詳細
- User新規作成
- User編集
- User削除
- Active / Inactive管理
- Loading表示
- Error表示
- React Routerによる画面遷移

主なルート：

```text
/
/users
/users/new
/users/:userId
/users/:userId/edit
*
```

---

# Backend状況

User CRUD は実装済み。

API：

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

Backendは現在、大きな機能追加を行う段階ではなく、Phase3ではFrontend UI改善を中心に進めている。

---

# Frontend構成

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

共通UI：

```text
components/
├── Badge/
├── Button/
├── Card/
├── ErrorMessage/
├── Input/
├── Loading/
└── UserForm/
```

---

# UserForm

Create/Editフォームの重複を減らすため、共通 `UserForm` を導入済み。

UserFormの責務：

- Email入力
- Password入力（Create）
- Active入力（Edit）
- Submitボタン
- Submit状態表示

UserFormに持たせない責務：

- API通信
- Validationロジック
- Axiosエラー処理
- 画面遷移

これらはPage側に残している。

---

# 今回のチャットで実施した内容

## Step1

UserForm導入後のUIをブラウザで確認。

確認対象：

- User一覧
- User新規作成
- User編集
- User詳細

---

## Step2：UserForm Submitボタン配置改善

`UserForm` のSubmitボタンを配置用領域で囲んだ。

構造：

```tsx
<div className="user-form__actions">
  <Button type="submit" disabled={isSubmitting}>
    {isSubmitting ? submittingLabel : submitLabel}
  </Button>
</div>
```

`UserForm.css` を追加。

現在の基本方針：

```css
.user-form__actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}
```

目的：

- 入力欄とSubmitボタンの余白確保
- Submitボタン右寄せ
- 将来的な複数ボタン配置への対応

---

# Step3：Badge追加

ステータス表示用の共通UIとして `Badge` を追加。

追加：

```text
frontend/src/components/Badge/
├── Badge.tsx
└── Badge.css
```

Badgeのvariant：

```ts
type BadgeVariant = "success" | "neutral";
```

Badgeは表示のみ担当する。

User固有の `is_active` 判定は持たせない。

使用例：

```tsx
<Badge variant={user.is_active ? "success" : "neutral"}>
  {user.is_active ? "有効" : "無効"}
</Badge>
```

---

# UserListPage Badge対応

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

Badge表示へ変更済み。

状態判定：

```tsx
user.is_active ? "success" : "neutral"
```

---

# UserDetailPage Badge対応

User詳細画面も同じBadgeへ統一済み。

これにより一覧画面と詳細画面でステータス表示が統一された。

---

# Step4：User詳細画面UI改善

## 詳細情報レイアウト

`dl` にクラスを追加。

```tsx
<dl className="user-detail">
```

`UserDetailPage.css` を新規作成。

CSS Gridで、

```text
項目名 | 値
```

の2列構成へ変更。

基本CSS：

```css
.user-detail {
  display: grid;
  grid-template-columns: 140px 1fr;
  row-gap: 16px;
  column-gap: 24px;
  margin: 0;
}

.user-detail dt {
  font-weight: 600;
}

.user-detail dd {
  margin: 0;
}
```

---

# User詳細 操作エリア

以前は、

```text
編集
削除
一覧へ戻る
```

がそのまま並んでいた。

現在は操作領域を分離。

構造：

```tsx
<div className="user-detail-actions">
  <Link to="/users">一覧へ戻る</Link>

  <div className="user-detail-actions__right">
    <Link to={`/users/${user.id}/edit`}>編集</Link>

    <Button
      type="button"
      variant="danger"
      onClick={handleDelete}
      disabled={isDeleting}
    >
      {isDeleting ? "削除中..." : "削除"}
    </Button>
  </div>
</div>
```

配置：

```text
一覧へ戻る                         編集  削除
```

CSS：

```css
.user-detail-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 24px;
}

.user-detail-actions__right {
  display: flex;
  align-items: center;
  gap: 12px;
}
```

削除ボタンには既存のButtonコンポーネントの

```tsx
variant="danger"
```

を利用する。

---

# 日時表示改善

User型では、

```ts
created_at: string;
updated_at: string;
```

となっている。

API値をそのまま画面表示するのではなく、UserDetailPageで表示時だけ整形するよう変更。

現在：

```tsx
function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}
```

使用：

```tsx
<dt>作成日時</dt>
<dd>{formatDateTime(user.created_at)}</dd>

<dt>更新日時</dt>
<dd>{formatDateTime(user.updated_at)}</dd>
```

重要：

- APIデータそのものは変更しない
- DBの値も変更しない
- 表示時だけ整形する

現段階では `formatDateTime()` はUserDetailPage内に置く。

他画面でも日時整形が必要になった場合に共通化を検討する。

---

# 現在の設計方針

Frontendでは責務を以下のように分ける。

```text
Page
├── API通信
├── State
├── Validation
├── Error処理
├── 画面遷移
└── 画面固有処理

Component
├── 共通UI
└── 表示
```

特に、

> **UIのみを共通化し、業務処理はPage側へ残す**

方針を維持する。

---

# CSS方針

共通UI：

```text
components/*/*.css
```

画面固有レイアウト：

```text
pages/*Page.css
```

例：

```text
UserForm.css
    → UserForm固有の配置

Badge.css
    → Badgeの見た目

Button.css
    → Buttonの見た目

UserDetailPage.css
    → User詳細画面固有のレイアウト
```

共通コンポーネントにPage固有レイアウトを持たせない。

---

# 次回開始位置

## Step5：共通UI全体の見直し

次回は **コードをすぐ変更せず、まずGitHub上の実装を確認する**。

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

目的：

- 共通化した方がよい部分を確認
- Page側に残した方がよい部分を確認
- 余白の統一
- 見た目の統一
- 不要な共通化を避ける

まず現状分析を行い、その後必要な部分だけ変更する。

---

# 次回の進め方

推奨手順：

```text
Step5-1
GitHub上の共通UIコード確認

Step5-2
共通UIの問題点・改善候補整理

Step5-3
必要なUIだけ修正

Step5-4
各User画面で表示確認

Step5-5
Phase3全体の動作確認
```

一度に大きく変更せず、1ステップずつ進める。

---

# GitHub

コード確認時は以下のリポジトリの実コードを基準にする。

```text
eswm223-oss/bizsc
```

引継ぎ資料だけを前提にコードを推測せず、必要に応じてGitHub上の最新コードを確認してから変更案を出す。

---

# Git / Commit

今回のUI改善では複数ファイルを変更している。

主な変更：

```text
UserForm.tsx
UserForm.css
Badge.tsx
Badge.css
UserListPage.tsx
UserDetailPage.tsx
UserDetailPage.css
```

次のCommit候補：

> **Step5（共通UI全体の見直し）完了後**

ただし、次回開始時にGitの変更状況を確認し、未コミット変更が多い場合はStep5開始前のCommitも検討する。

---

# ドキュメント

今回の引継ぎ時点で更新・生成対象：

```text
architecture.md
handover_phase.md
project-overview.md
```

`architecture.md` は今回のPhase3 UI改善まで反映した最新版を生成済み。

---

# 注意事項

## 1. GitHub実コードを確認する

コード変更を案内する前に、可能な限り最新のGitHubコードを確認する。

## 2. 過剰な共通化をしない

一度しか使用していない処理を、将来使うかもしれないという理由だけで共通化しない。

例：

```text
formatDateTime()
```

は現時点ではUserDetailPage内に残している。

## 3. Backendを不用意に変更しない

現在のUser CRUDは動作している。

Phase3のUI改善ではFrontend中心に変更する。

## 4. UIと業務処理を分離する

BadgeやUserFormへAPI処理などを移さない。

## 5. 小さいステップで進める

変更 → ブラウザ確認 → 次の変更

の流れを維持する。

---

# 現在の到達点

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
共通UI
    ↓
UserForm
    ↓
Button配置改善
    ↓
Badge追加
    ↓
User一覧ステータス改善
    ↓
User詳細ステータス改善
    ↓
User詳細レイアウト改善
    ↓
日時表示改善
    ↓
現在地点
```

次：

```text
共通UI全体の見直し
```

---

# 次回チャットへの指示

次回チャットでは、

1. `project-overview.md`
2. `architecture.md`
3. `handover_phase.md`

を読み込む。

その後、GitHubの `eswm223-oss/bizsc` の最新コードを確認する。

そして、

> **Phase3 Step5：共通UI全体の見直し**

から再開する。
