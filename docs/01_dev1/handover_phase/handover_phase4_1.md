# BizSC Handover — Phase4開始前

## 1. このドキュメントの目的

本ドキュメントは、BizSC の現在の開発状況を次のチャットへ引き継ぐための資料です。

次回は以下の3資料を基準として開発を再開します。

```text
project-overview.md
architecture.md
handover_phase.md
```

コード変更時は、引継ぎ資料だけを前提に推測せず、GitHub上の最新コードも確認します。

対象リポジトリ：

```text
eswm223-oss/bizsc
```

---

# 2. 現在の開発状況

現在は **Phase3 完了**。

Phase3では、Frontend側のUser CRUD UIと共通UIの整理まで完了しました。

完了済み：

```text
User一覧
User詳細
User新規作成
User編集
User削除
React Router
Axios API通信
Loading表示
Error表示
Badge表示
UserForm共通化
共通UI見直し
各User画面表示確認
CRUD全体動作確認
Frontend build確認
```

Phase3完了後、変更内容はGitHubへPush済みです。

---

# 3. 現在利用可能なUser機能

以下のUser CRUDをFrontendから利用できます。

```text
POST    /users
GET     /users
GET     /users/{id}
PATCH   /users/{id}
DELETE  /users/{id}
```

Frontend画面：

```text
/users
/users/new
/users/:userId
/users/:userId/edit
```

React RouterによりSPA遷移します。

---

# 4. Backend状況

BackendのUser CRUDは完成済みです。

基本構成：

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

技術：

```text
FastAPI
Python 3.13
SQLAlchemy 2.x
Pydantic v2
Alembic
PostgreSQL 17
```

Health API：

```text
GET /health
GET /health/db
```

Phase4開始時点で、Backendを大きく変更する必要はありません。

Frontend側の新機能に応じて、必要なAPIだけ追加・拡張します。

---

# 5. Frontend構成

主要構成：

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
Badge
Button
Card
ErrorMessage
Input
Loading
UserForm
```

その他の共通Component：

```text
Header
Sidebar
Footer
```

---

# 6. Frontend設計方針

Frontendでは、以下の責務分離を維持します。

```text
Page
├─ API通信
├─ State
├─ Validation
├─ Error処理
├─ Loading状態
├─ 画面遷移
└─ 画面固有処理

Component
├─ 共通UI
└─ 表示
```

重要方針：

> UIのみを共通化し、業務処理はPage側へ残す。

---

# 7. CSS設計方針

共通UI自身の見た目：

```text
components/*/*.css
```

画面固有レイアウト：

```text
pages/*Page.css
```

基本原則：

```text
Component CSS
→ Component自身の見た目

Page CSS
→ 画面内での配置・レイアウト
```

過剰に共通CSSへ集約しません。

---

# 8. Phase3で実施した共通UI整理

Phase3終盤では、共通UI全体を確認しました。

確認対象：

```text
Button
Card
Input
Loading
ErrorMessage
Badge
```

大きな設計変更は行わず、現在の責務分離を維持しました。

実施した軽微な修正：

```text
UserFormの縦方向余白整理
UserEditPageのCardタイトル統一
UserListPageのuser-status重複指定整理
UserListPageタイトルの日本語統一
```

---

# 9. UserFormの現在の方針

UserFormはCreate / Editで共通利用します。

担当：

```text
Email入力UI
Password入力UI
Active入力UI
Submitボタン
Submit状態表示
入力項目の配置
```

担当しないもの：

```text
API通信
Axiosエラー処理
画面遷移
業務ロジック
Page固有のValidation判断
```

これらはPage側で管理します。

---

# 10. Badgeの現在の方針

Badgeは状態表示のみ担当します。

現在のvariant：

```text
success
neutral
```

UserのActive状態：

```text
有効
→ success

無効
→ neutral
```

`is_active` の業務判定はBadge内部へ持たせません。

---

# 11. Loading / Error設計

Loading用State：

```text
isLoading
isSubmitting
isDeleting
```

処理中：

```text
Loading表示
Button無効化
二重送信防止
```

Error表示は用途を分けます。

入力項目単位：

```text
Input error
```

画面・API単位：

```text
ErrorMessage
```

Backendを最終的なValidation保証とします。

---

# 12. UserDetailPageの現在の状態

User詳細画面は以下の構成です。

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
一覧へ戻る                 編集  削除
```

削除ボタン：

```text
Button variant="danger"
```

日時表示：

```tsx
function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}
```

現在はUserDetailPage内に残しています。

他画面でも日時整形が必要になった時点で共通化を検討します。

---

# 13. UserListPageの現在の状態

一覧表示：

```text
ID
メールアドレス
ステータス
操作
```

ステータスはBadge表示です。

```text
有効
無効
```

タイトル：

```text
ユーザー一覧
```

共通Badgeが文字の見た目を担当するため、Page側で不要なステータス文字スタイルは持たせません。

---

# 14. UserCreatePageの現在の状態

UserFormを使用します。

主な処理：

```text
Email必須確認
Password8文字以上確認
createUser()
エラー処理
作成後 /users へ遷移
```

Cardタイトル：

```text
ユーザ新規登録
```

---

# 15. UserEditPageの現在の状態

UserFormを使用します。

主な処理：

```text
User情報取得
Email編集
Active編集
updateUser()
エラー処理
更新後 User詳細へ遷移
```

Cardタイトル：

```text
ユーザー編集
```

Phase3終盤で、Card内に直接`h1`を書く方式からCardの`title`へ統一しました。

---

# 16. Phase3最終動作確認

Phase3完了前に以下をブラウザで確認済みです。

```text
User一覧表示
User作成
作成後一覧遷移
User詳細表示
User編集
編集内容反映
User削除
削除後一覧遷移
Badge表示
日時表示
各画面レイアウト
```

Frontend build：

```powershell
docker compose exec frontend npm run build
```

正常完了済み。

---

# 17. Git状況

Phase3完了後の変更はCommit / Push済みです。

次チャット開始時は、まず最新コードをGitHubから確認します。

必要に応じてローカル側でもGitHub Desktopの状態を確認します。

---

# 18. Phase4候補

Phase3までの資料では、Phase4候補として以下が挙げられています。

```text
User検索
ページネーション
ソート
フィルタ
CRUDテスト追加
```

ただし、Phase4内の詳細な順序はまだ確定していません。

次チャットでは、まずPhase4の実装順を整理してから開始します。

---

# 19. Phase4開始前に確認すること

次チャットでは以下の順番で開始します。

```text
Step1
引継ぎ資料確認

Step2
GitHub最新コード確認

Step3
Phase4候補整理

Step4
Phase4の実装順決定

Step5
最初の機能実装開始
```

Phase4候補を一度にすべて実装しません。

小さい単位で進めます。

---

# 20. Phase4の進め方

継続する進め方：

```text
1. 実コード確認
2. 変更理由を整理
3. 小さく実装
4. ブラウザ/API確認
5. 必要なら修正
6. 次のStepへ
```

大きな変更をまとめて行いません。

---

# 21. コード確認時の注意

コード変更前に、可能な限りGitHub上の最新コードを確認します。

対象：

```text
eswm223-oss/bizsc
```

特にPhase4では、新しい機能を追加する前に以下を確認します。

```text
既存User API
User types
UserListPage
users API module
Backend Router
Backend Service
Backend Repository
既存テスト
```

既存コードと重複する仕組みを新しく作らないようにします。

---

# 22. 過剰な共通化を避ける

継続する重要方針です。

一度しか利用していない処理を、

```text
将来使うかもしれない
```

という理由だけで共通化しません。

例えば現在の、

```text
formatDateTime()
```

はUserDetailPage内に残しています。

必要になった段階で共通化します。

---

# 23. Backend変更時の注意

Phase3完了時点でUser CRUDは正常動作しています。

Phase4では、Frontend機能を追加する際に必要なAPI変更だけを行います。

既存Backendを不用意にリファクタリングしません。

変更する場合は、

```text
Router
Service
Repository
Schema
Model
Migration
```

のうち、どこへ変更を入れるべきか責務を確認してから実装します。

---

# 24. Database変更時の注意

DB構造を変更する場合はAlembicを使用します。

```text
Model変更
  ↓
Migration作成
  ↓
Migration内容確認
  ↓
Upgrade
  ↓
TablePlus等で確認
```

Model変更だけでDB変更完了とはしません。

---

# 25. Frontend変更時の注意

PageからAxiosを直接利用しません。

```text
Page
  ↓
API Module
  ↓
Axios Client
```

API通信は既存の`api/`構成を維持します。

共通型は`types/`で管理します。

---

# 26. 開発方針

今後も以下を維持します。

* 一度に大きく変更しない
* 1ステップずつ進める
* なぜ変更するのか理解してから実装する
* 実コードを確認してから変更案を出す
* UIと業務処理を分離する
* PageとComponentの責務を分離する
* Backendを最終Validation保証とする
* 型安全を維持する
* 不要な共通化を避ける
* 動作確認してから次へ進む
* 区切りの良いタイミングでCommitする
* フェーズの区切りでドキュメントを更新する

---

# 27. ドキュメント

次チャットでは以下の3ファイルを参照します。

```text
project-overview.md
architecture.md
handover_phase.md
```

役割：

```text
project-overview.md
→ プロジェクト全体の現在地・進捗

architecture.md
→ 現在のシステム構成・設計思想

handover_phase.md
→ 次チャットで何をするか
```

---

# 28. 現在の到達点

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

---

# 29. 次回開始位置

次回は **Phase4** から開始します。

最初に実装へ入るのではなく、

```text
Phase4候補
├─ User検索
├─ ページネーション
├─ ソート
├─ フィルタ
└─ CRUDテスト追加
```

を確認し、現在のコード構成との関係を整理します。

その後、優先順位を決めて1機能ずつ進めます。

---

# 30. 次回チャットへの指示

次回チャットでは、

```text
1. project-overview.md
2. architecture.md
3. handover_phase.md
```

を読み込みます。

その後、GitHubの、

```text
eswm223-oss/bizsc
```

の最新コードを確認します。

現在の状態を確認後、

> **Phase4の実装計画整理**

から開始します。

Phase4の具体的なStepは、その時点の最新コードを確認してから決定します。
