# BizSC EDINET API 接続・書類一覧取得 Phase

## 1. このドキュメントの目的

このドキュメントは、BizSC Backend に **EDINET APIへの接続処理と書類一覧取得処理だけ** を追加するための実装指示書です。

このPhaseでは、EDINETから財務データを解析したり、DBへ保存したり、Frontendから利用したりしません。

目的は次の2点だけです。

1. BizSC Backend から EDINET API Version 2 へ安全に接続できること
2. 指定日の「提出書類一覧及びメタデータ」を取得できること

このPhaseが完了するまで、次Phaseの設計・実装には進まないでください。

---

## 2. 最重要ルール

### 一度に全て実装しない

このmdを読み込んだ直後に、記載された変更を一括で実装しないでください。

必ず後述の Step 単位で進めてください。

各Stepでは次の順序を守ってください。

1. 変更前の既存コードを確認する
2. そのStepに必要な最小変更だけを行う
3. 変更内容を簡潔に説明する
4. 必要な確認コマンドを実行または提示する
5. そのStepで停止する
6. ユーザーの確認後に次Stepへ進む

ユーザーから次へ進む指示があるまでは、次Stepを先回りして実装しないでください。

---

## 3. 必ず先に読む資料

実装開始前に以下を確認してください。

- `docs/development-guidelines.md`
- `docs/architecture.md`
- 現在のGitHub / ローカルコード

特に既存の以下のファイルを確認してください。

- `backend/app/core/config.py`
- `backend/requirements.txt`
- `.gitignore`
- `compose.yaml`

既存コードを推測して変更しないでください。

---

## 4. 現在のBizSCで確認済みの前提

2026-08-23時点のBizSCでは以下を確認済みです。

### Backend

主な構成:

```text
backend/app/
├─ api/
├─ core/
├─ db/
├─ models/
├─ repositories/
├─ schemas/
├─ services/
└─ main.py
```

### HTTPクライアント

`backend/requirements.txt` には `httpx` が既に存在します。

そのため、このPhaseでは新しいHTTP通信ライブラリを追加しないでください。

### 環境変数

`backend/app/core/config.py` では `pydantic-settings` の `BaseSettings` を利用し、`.env` を読み込んでいます。

EDINET APIキーも同じ仕組みを利用します。

### `.env`

`.gitignore` では `.env` および `.env.*` がGit管理対象外になっています。

APIキーをソースコードへ直接記述しないでください。

---

## 5. EDINET公式仕様

このPhaseでは **EDINET API Version 2** を使用します。

公式仕様書:

- EDINET API仕様書（Version 2）
- 2026年6月版
- EDINET公式サイト「操作ガイド等」に掲載されている最新版を正とする

公式仕様ページ:

```text
https://disclosure2dl.edinet-fsa.go.jp/guide/static/disclosure/WZEK0110.html
```

API仕様書PDF:

```text
https://disclosure2dl.edinet-fsa.go.jp/guide/static/disclosure/download/ESE140206.pdf
```

仕様変更の可能性があるため、実装時に公式仕様と矛盾を発見した場合は、勝手に推測して実装せずユーザーへ報告してください。

---

## 6. 今回利用するEDINET API

### 書類一覧API

HTTP Method:

```text
GET
```

Endpoint:

```text
https://api.edinet-fsa.go.jp/api/v2/documents.json
```

### Request parameters

#### `date`

必須。

取得対象となるファイル日付を次の形式で指定します。

```text
YYYY-MM-DD
```

#### `type`

今回使用する値:

```text
2
```

`type=2` は、

```text
提出書類一覧及びメタデータ
```

を取得する指定です。

#### `Subscription-Key`

必須。

EDINETから発行されたAPIキーを指定します。

例としてURL全体をログ出力してはいけません。

APIキーがQuery Parameterに含まれるため、URLをログへ出すとAPIキーが漏洩する危険があります。

---

## 7. 通信条件

EDINET APIはTLS 1.2以上を使用します。

FrontendのJavaScriptからEDINET APIを直接呼び出さないでください。

今回の通信は必ずBizSC Backendから行います。

---

## 8. このPhaseの実装範囲

今回実装してよいものは以下だけです。

### 8.1 EDINET APIキー設定

既存の `Settings` にEDINET APIキー設定を追加します。

環境変数名:

```text
EDINET_API_KEY
```

既存機能を壊さないため、EDINET機能を使用していない状態でもBackendが起動できる設計にしてください。

したがって、設定値は必要に応じてOptionalとして扱い、

**EDINET APIを実際に呼び出す時点でAPIキーが存在しない場合に明確なエラーとする**

方式を優先してください。

既存のDB設定やその他設定を変更しないでください。

---

### 8.2 EDINET API Client

外部サービスであるEDINETとのHTTP通信を、既存のRepositoryやDB処理へ混在させないでください。

このPhaseでは、次のディレクトリ追加を候補とします。

```text
backend/app/clients/
```

想定ファイル:

```text
backend/app/clients/__init__.py
backend/app/clients/edinet.py
```

ただし、実装前に既存構成を確認し、この配置が明らかに既存設計と衝突する場合は勝手に変更せずユーザーへ報告してください。

### Clientの責務

EDINET Clientが担当するのは以下だけです。

- EDINET APIのURL管理
- APIキーの付与
- 指定日の書類一覧取得
- HTTPレスポンスの確認
- EDINETから返されたJSONの返却
- 最小限の通信エラー処理

以下は担当しません。

- DB保存
- 財務項目抽出
- XBRL解析
- CSV解析
- 書類の絞り込み
- 業務ロジック
- Frontend向けAPI提供

---

## 9. 書類一覧取得処理の期待仕様

外部から概ね次の情報を渡して呼び出せる構造にしてください。

```text
target_date
```

型はPythonの `date` など、日付であることが明確になる型を優先してください。

EDINETへ送信する際に次へ変換します。

```text
YYYY-MM-DD
```

リクエストでは以下を指定します。

```text
date=<YYYY-MM-DD>
type=2
Subscription-Key=<APIキー>
```

取得成功時はEDINETから返されたJSONを返してください。

このPhaseでは、レスポンス内容を独自のPydantic Schemaへ全面変換しないでください。

レスポンス構造の正式なモデリングは、実際の取得内容を確認した後の別Phaseで検討します。

---

## 10. 成功レスポンスの最低限の確認

`type=2` の成功レスポンスでは、少なくとも次を確認できる想定です。

```text
metadata
results
```

`metadata` には成功時に概ね以下が含まれます。

```text
status = "200"
message = "OK"
```

ただし、EDINET公式仕様を正としてください。

レスポンス構造が想定と異なる場合は、無理に補正せず実データと公式仕様を確認してください。

---

## 11. エラー処理方針

このPhaseでは複雑なリトライ機構を実装しません。

最低限、以下を区別できるようにしてください。

- APIキー未設定
- 400 Bad Request
- 401 APIキー不正または未指定
- 404 Not Found
- 429 Too Many Requests
- 500 EDINET側エラー
- 接続タイムアウト
- JSONとして解釈できないレスポンス

EDINET公式仕様では429が定義されています。

このPhaseでは429発生時に自動で繰り返しアクセスしないでください。

エラー内容をユーザーが判断できる形にはしますが、以下は出力してはいけません。

```text
EDINET_API_KEY
Subscription-Keyの値
APIキーを含む完全なRequest URL
```

### 特に重要

`Subscription-Key` はURLのQuery Parameterとして送信されます。

そのため、HTTPライブラリの例外メッセージやRequest URLをそのままログ出力すると、APIキーが表示される可能性があります。

エラー処理ではAPIキーを含むURLをログ・例外メッセージへ出さない設計にしてください。

HTTPステータスコードやEDINETから返された安全なメッセージだけを利用してください。

---

## 12. Timeout

HTTP通信には明示的なTimeoutを設定してください。

ただし、このPhaseでは複雑なTimeout設定やリトライライブラリを導入しません。

`httpx` 標準機能の範囲で最小限にしてください。

---

## 13. このPhaseでは実装しないもの

以下は **明確に今回の対象外** です。

### Database

実装しない:

- SQLAlchemy Model追加
- Repository追加
- Alembic Migration
- PostgreSQLへのEDINETデータ保存
- キャッシュテーブル
- 重複取得防止処理

### 財務データ

実装しない:

- 財務項目抽出
- 売上高取得
- 営業利益取得
- 経常利益取得
- 純利益取得
- BS / PL / CF解析
- XBRL解析
- CSV解析

### 書類ダウンロード

実装しない:

- 書類取得API
- ZIPダウンロード
- CSVダウンロード
- XBRLダウンロード
- PDFダウンロード

### Backend API

このPhaseではFrontend向けの新規FastAPI Routerを作成しません。

EDINET Clientの取得処理を直接確認します。

### Frontend

変更しない:

```text
frontend/
```

### その他

導入しない:

- Redis
- Celery
- APScheduler
- cron
- バッチ基盤
- Queue
- 新しいDocker Service
- 新しい外部ライブラリ
- 自動定期取得

---

## 14. 既存機能保護

EDINET機能追加のために以下を変更しないでください。

- User CRUDの処理ロジック
- User Model
- User Schema
- User Repository
- User Service
- User API
- Frontend画面
- DB構造
- PostgreSQL設定

既存コードに改善点を見つけても、このPhaseではリファクタリングしないでください。

必要であれば改善候補としてユーザーへ報告するだけにしてください。

---

# 15. 実装Step

## Step 1: 現状確認のみ

このStepではコードを変更しません。

確認対象:

```text
backend/app/core/config.py
backend/requirements.txt
.gitignore
compose.yaml
backend/app/
```

確認事項:

- `pydantic-settings` による環境変数管理方法
- `httpx` が既に利用可能であること
- `.env` がGit管理対象外であること
- 外部API Client用ディレクトリが既に存在しないか
- 今回の追加が既存構成と衝突しないか

確認結果をユーザーへ報告して停止してください。

次Stepへ勝手に進まないでください。

---

## Step 2: APIキー設定

変更対象候補:

```text
backend/app/core/config.py
```

`EDINET_API_KEY` を既存Settingsから参照できるようにします。

APIキーそのものはCursorが作成・推測・ソースコードへ記述してはいけません。

ユーザーがローカルの `.env` に設定します。

例:

```text
EDINET_API_KEY=<ユーザー自身が取得したAPIキー>
```

この文字列を実際のキーに置き換える作業はユーザー側で行います。

`.env` の内容やAPIキーをチャットへ貼り付けるよう要求しないでください。

変更後、既存Backendが起動可能であることを確認して停止してください。

---

## Step 3: EDINET Client追加

候補:

```text
backend/app/clients/__init__.py
backend/app/clients/edinet.py
```

実装する処理:

```text
指定日
  ↓
EDINET APIへのGET
  ↓
type=2
  ↓
JSONレスポンス取得
  ↓
呼び出し元へ返却
```

このStepではService、Repository、Routerを追加しません。

APIキーをログへ出さないことを確認してください。

実装後、コード内容を説明して停止してください。

---

## Step 4: 最小限の自動確認

EDINET APIへ毎回実アクセスするpytestを作らないでください。

テストを追加する場合は、外部EDINET APIへ通信せずに確認できる最小限のテストとしてください。

最低限確認したい内容:

- 指定日が `YYYY-MM-DD` として送信される
- `type=2` が指定される
- APIキー未設定時に安全に失敗する
- エラー表示にAPIキーが含まれない

テストのためだけに大規模なDependency Injection構造や新規ライブラリを導入しないでください。

既存の `pytest` / `httpx` で実現できる範囲にしてください。

実装が過剰になる場合はテスト設計をユーザーへ相談してください。

---

## Step 5: EDINET実接続確認

このStepのみ、ユーザー自身のローカル `EDINET_API_KEY` を利用してEDINETへ実アクセスします。

Frontend向けAPI Routerは作成せず、Backendコンテナ内からClientを直接呼び出して確認します。

確認対象日は、直近の提出書類が存在すると考えられる営業日を利用してください。

ただし、「必ずデータが存在する」と推測せず、0件の場合でもAPI接続自体の成功とレスポンスを区別してください。

確認項目:

```text
metadata.status
metadata.message
metadata.resultset.count
results の件数
```

画面やログへAPIキーを表示しないでください。

大量の `results` 全件をコンソール出力する必要はありません。

例えば次の程度を確認できれば十分です。

```text
status
message
count
resultsの先頭1件の主要項目
```

実接続確認後、このPhaseを終了してください。

---

# 16. Phase完了条件

以下がすべて満たされた場合のみ、このPhaseを完了とします。

- [ ] EDINET APIキーを `.env` から参照できる
- [ ] APIキーなしでもEDINET以外の既存Backend機能を壊さない
- [ ] `httpx` を利用している
- [ ] 新しいHTTPライブラリを追加していない
- [ ] EDINET API Version 2を使用している
- [ ] 書類一覧APIを利用している
- [ ] `date` を指定できる
- [ ] `type=2` を使用している
- [ ] `Subscription-Key` を安全に指定している
- [ ] APIキーをログや例外文へ表示しない
- [ ] 成功時のJSONを取得できる
- [ ] `metadata.status` / `message` を確認できる
- [ ] `results` を取得できる
- [ ] 429等の通信エラーを無限リトライしない
- [ ] DBを変更していない
- [ ] Alembic Migrationを作成していない
- [ ] 財務データ解析を実装していない
- [ ] 書類ダウンロードを実装していない
- [ ] FastAPI Routerを追加していない
- [ ] Frontendを変更していない
- [ ] Redis/Celery等を追加していない
- [ ] 既存User機能を変更していない

---

# 17. Phase完了後に行うこと

このPhase完了後、勝手に次機能を実装しないでください。

まず以下をユーザーへ報告してください。

1. 実際に追加・変更したファイル
2. EDINET API接続確認結果
3. 取得できたレスポンスの構造
4. `results` の主要フィールド
5. 想定と異なっていた点
6. 次Phaseを設計するうえで確認が必要な点

その結果を見てから、次のmdを別途作成します。

候補となる次Phaseは以下ですが、このmdの対象外です。

```text
対象書類の絞り込み
```

または

```text
書類取得APIによるCSV取得
```

どちらを先に行うかは、このPhaseの実データ確認後に決定します。

---

# 18. Cursorへの禁止事項まとめ

以下を厳守してください。

- このmdの全Stepを一括実行しない
- ユーザー確認前に次Stepへ進まない
- APIキーを推測しない
- APIキーをコードへ直書きしない
- APIキーをログ出力しない
- APIキーを含むURLをログ出力しない
- APIキーをGitへCommitしない
- EDINET仕様を推測しない
- EDINETの全データ構造を先にモデル化しない
- DBを作らない
- Migrationを作らない
- Repositoryを作らない
- 財務解析をしない
- CSV解析をしない
- Frontendを変更しない
- FastAPI Routerを追加しない
- Redis等のキャッシュ基盤を追加しない
- バッチ・定期処理を作らない
- 既存機能をリファクタリングしない
- 必要以上にファイルを増やさない
- 不要な依存ライブラリを追加しない

このPhaseの目的は、

> 「BizSC BackendからEDINET APIへ安全に接続し、指定日の書類一覧JSONを取得できること」

だけです。
