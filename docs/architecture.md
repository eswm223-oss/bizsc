# BizSC Architecture

更新日: 2026-10-27  
確認したGitHubソースのコミット（本更新前）: [`6b577b8`](https://github.com/eswm223-oss/bizsc/commit/6b577b832beb6f661a97a87fd697fa3b9dbaf8ae)

## 1. 目的と読み方

この資料は、BizSC の**現在の実装構成、データモデル、責務分離、トランザクション方針**を説明する基準資料です。個別の進捗・未確認事項・作業再開手順は `handover_phase.md`、プロジェクト全体の目的・ロードマップは `project-overview.md` に記載します。

- ここでいう「実装済み」は**GitHub上にコードが存在する**ことを指し、本資料作成時に全件実行や結合テストを実施したことを意味しません。
- 新しいチャットや変更作業では、まずGitHub上の最新コミットを確認してください。

## 2. システム概要

BizSCは、日本株を対象とする個人用の株式スクリーニングWebアプリです。J-Quants APIを主たるデータソースとして、企業情報、日足株価、バリュエーション、財務サマリーをPostgreSQLに保存し、後続の検索・指標計算で利用します。

```text
【Web / User】
Browser → React / TypeScript / Vite → Axios → FastAPI
                                             ↓
                                     Router → Service
                                                ↓
                                           Repository
                                                ↓
                                          PostgreSQL

【J-Quants バッチ】
POST /batches/jquants/cache/plain
  ↓ 202 Accepted + mgmtId
FastAPI BackgroundTasks（同じアプリケーションプロセス内）
  ↓
run_cache(mgmtId)
  ↓
jquants_cache(mgmtId) ← cache_mgmt（対象・期間・実行状態）
  ├─ J-Quants Client → J-Quants API
  ├─ キャッシュ用Service → Repository → jq_* テーブル
  └─ CacheMgmtService → CacheMgmtRepository → cache_mgmt
```

`202 Accepted` は**処理受付**を表します。キャッシュ処理が完了したことを保証するレスポンスではありません。

## 3. 技術スタック・実行環境

| 分野 | 採用技術 |
|---|---|
| Backend | Python 3.12、FastAPI、SQLAlchemy、Pydantic、httpx、Alembic |
| Database | PostgreSQL 17、psycopg |
| Frontend | React 19、TypeScript、Vite、React Router、Axios、Mantine 9（UI）、TanStack Table v9（一部一覧） |
| 開発環境 | Windows、Cursor、GitHub Desktop、Docker Desktop、Docker Compose、TablePlus |
| Backendテスト基盤 | pytest |

- Workspace: `D:\Development\apps\bizsc`
- GitHub: <https://github.com/eswm223-oss/bizsc>
- Compose: `backend` (8000)、`frontend` (5173)、`db` (5432)
- Windows上の別PostgreSQLサービスが5432番ポートを占有すると、Docker側との競合が発生し得ます。

### 3.1 Frontend UI（2026-10-27 時点）

- **BootstrapからMantineへ移行。** `frontend/package.json` に `@mantine/core: ^9.7.4` と `@mantine/hooks: ^9.7.4` があり、`bootstrap` 依存は存在しない。
- `frontend/src/main.tsx` で `@mantine/core/styles.css` を読み込み、`MantineProvider defaultColorScheme="auto"` の内側に `BrowserRouter` と `App` を配置。アプリ全体のテーマ設定はここで行う。
- `frontend/src/routes/AppRoutes.tsx` では、ホーム `/` とユーザーCRUD `/users...` を `MainLayoutMantine` および `*PageMantine.tsx` に接続。ユーザー入力には `components/UserForm/UserFormMantine.tsx` を使用。
- `MainLayoutMantine.tsx` は Mantine `AppShell`、Header、Navbar、Footer、レスポンシブナビゲーション、ライト／ダーク切替を実装。
- `/jquants/master` と `/test` は旧 `MainLayout` に残る。**すべての画面がMantine化済みとはみなさない。** 旧ページ／旧UIコンポーネントのソースは一部残存している。
- `@tanstack/react-table: ^9.3.1` は継続使用。現時点でTanStack Tableを使用するのは主に `components/test/TanstackTable.tsx`。ユーザー一覧はMantine `Table` と `Pagination` を使用する。
- UIコンポーネントは原則Mantine標準品を直接使い、Propsで調整。独自CSSは必要最小限にとどめる。

利用者が2026-10-27に `docker compose exec frontend npm run build` の成功と画面の正常動作を確認。ビルド時にはJSチャンクが500KBを超えるサイズ警告が出たが、ビルドエラーではない。本資料の更新作業ではビルド・ブラウザ操作を再実行していない。

## 4. Backendディレクトリ・役割

```text
backend/
├─ alembic/versions/                     # DBマイグレーション
├─ app/
│  ├─ main.py                             # FastAPIのアプリ・Router登録
│  ├─ api/
│  │  └─ cache_batch.py                   # キャッシュ起動API
│  ├─ schemas/
│  │  └─ cache_batch.py                   # CacheBatchRequest
│  ├─ clients/
│  │  └─ jquants.py                       # J-Quants HTTP API
│  ├─ common/
│  │  ├─ cmm_date.py
│  │  ├─ cmm_number.py
│  │  └─ cmm_string.py
│  ├─ services/
│  │  ├─ batches/jquants_sync.py          # run_cache: バッチ入口
│  │  └─ jquants/
│  │     ├─ cache/jquants_cache.py        # キャッシュ全体と各Dataset処理
│  │     └─ db/
│  │        ├─ cache_manage.py            # 進捗管理Service
│  │        ├─ equities_master.py         # 上場銘柄Service
│  │        ├─ daily_quote.py             # 日足株価Service
│  │        ├─ valuation.py               # Valuation Service
│  │        └─ financial_summary.py       # 財務Summary Service
│  ├─ repositories/
│  │  ├─ cache_mgmt.py
│  │  ├─ equities_master.py
│  │  ├─ daily_quote.py
│  │  ├─ valuation.py
│  │  └─ financial_summary.py
│  ├─ models/
│  │  ├─ cache_mgmt.py
│  │  ├─ jquants_listed_issue.py
│  │  ├─ jquants_daily_quote.py
│  │  ├─ jquants_valuation.py
│  │  └─ jquants_financial_summary.py
│  └─ db/database.py                      # SessionLocal / get_db
└─ tests/
```

主な責務分離:

- **Router / Schema:** HTTP入力の受理、入力型、バックグラウンド処理の登録、HTTPレスポンス。
- **Batch:** 管理IDを引き渡してキャッシュ処理を起動し、ログを記録。
- **Cache:** 進捗状態に従ったDatasetの実行、JSONからModelへの変換、API呼び出し順序。
- **Client:** APIキー、エンドポイント、HTTP通信、タイムアウト、APIエラー本文の解析。
- **Service:** 業務ルール・主キー生成・銘柄マスタの新旧判定・ステータス更新。
- **Repository:** SQLAlchemyによるDB操作。J-Quantsデータ保存では通常`db.merge()`を利用。
- **Model / Alembic:** カラム定義とスキーマ変更。

## 5. J-Quants接続

`backend/app/clients/jquants.py` に実装済み。基底URLは `https://api.jquants.com/v2`、認証ヘッダは `x-api-key`。APIキーは環境設定から参照し、ソースコードや共有資料には記載しません。

| Dataset | Client関数 | APIエンドポイント |
|---|---|---|
| 上場銘柄マスタ | `fetch_listed_issues` | `/equities/master` |
| 日足株価 | `fetch_bars_daily` | `/equities/bars/daily` |
| バリュエーション | `fetch_valuation` | `/equities/valuation` |
| 財務サマリー | `fetch_summary` | `/fins/summary` |

- 上場銘柄マスタは`date`を指定せず最新情報を取得し、`code`指定は可能。
- 他の3 Datasetは銘柄コードおよび`from`/`to`の日付範囲を使用。
- タイムアウトはHTTPリクエストごとに30秒。
- HTTP非200の場合はレスポンスJSONに文字列の`message`があればそれを例外メッセージとして取り出し、なければHTTPステータスで表現。
- JSON解析エラー、タイムアウト、APIキー未設定等を例外として扱う。
- 2026-10-25のコードでは、日足株価・Valuation・財務サマリーの各銘柄API呼び出し前に`time.sleep(1)`がある。
- **ページネーションへの自動追従は未実装**。現時点ではユーザーのPostmanによる取得確認を踏まえ、対応を保留する判断。

## 6. 保存テーブルと識別子

| テーブル | SQLAlchemy Model | キー・保存方針 |
|---|---|---|
| `jq_listed_issues` | `JQuantsListedIssue` | 主キー`id=code`。既存行より取得データの日付が古ければ更新をスキップ。最新の銘柄情報を保持。 |
| `jq_daily_quotes` | `JQuantsDailyQuote` | 主キー`code-YYYYMMDD`。銘柄・取引日ごとに保存、既存行は`merge()`で上書き。 |
| `jq_valuations` | `JQuantsValuation` | 主キー`code-YYYYMMDD`。銘柄・日付ごとに保存、既存行は上書き。 |
| `jq_financial_summaries` | `JQuantsFinancialSummary` | 主キー`code-current_period_end-current_period_type-document_type`。同一期間・種別は上書き。 |
| `cache_mgmt` | `CacheMgmt` | キャッシュ起動単位の管理レコード。日時文字列の主キーとDataset別ステータスを保持。 |

J-Quantsのデータをすべて生JSON保存するのではなく、スクリーニングに使う列を選別して正規化しています。証券コードは文字列、金額等は`Numeric`/`Decimal`、日付は`Date`を用います。財務APIの空文字列は`to_decimal()`/`to_date()`で`None`に変換し、欠損値と0を区別します。

既存Modelには主キーとは別に銘柄コード・日付等のUniqueConstraintが定義されています。Schema変更はAlembicのrevisionを確認してから適用します。

## 7. cache_mgmt：進捗管理

主なカラム:

```text
id                YYYYMMDD-HHMMSS（15文字）
from_date         開始日
to_date           終了日
company_code      個別取得時の銘柄コード（省略可）
status_master     上場銘柄
status_dailyBar   日足株価
status_valuation  バリュエーション
status_summary    財務サマリー
remarks           直近のエラーメッセージ等（最大300文字）
updated_at        DB更新日時
```

Datasetステータスは`Waiting`、`Running`、`Complete`、`Error`（実行対象外は`NULL`）です。

- 作成時に対象Datasetのステータスを`Waiting`に設定。
- 個々のDataset開始前に`Running`、正常終了で`Complete`。
- 例外時に対象Datasetを`Error`にし、例外文字列を`remarks`に最大300文字で保存。
- キャッシュ制御は管理レコードの`from_date`、`to_date`、`company_code`を使用。
- `Waiting`/`Running`/`Error`のDatasetは、同じ管理IDで再度起動した際に処理対象となる。`Complete`はスキップする。
- 管理レコードの`create`/`update`/`delete`は現状、Repository内部で`commit()`を実行する設計。

**留意:** `Running`を再実行対象に含めるため、同じ管理IDを同時に起動させると重複実行の可能性があります。これは運用上の制約であり、排他ロック機構は実装済みとみなさないでください。

## 8. 起動APIと実行フロー

Router: `backend/app/api/cache_batch.py`  
Endpoint: **`POST /batches/jquants/cache/plain`**  
HTTP Status: **202 Accepted**

リクエストSchema (`CacheBatchRequest`):

```json
{
  "fromDate": "2026-10-01",
  "toDate": "2026-10-24",
  "code": "13010",
  "mgmtId": null
}
```

- `fromDate`/`toDate`は必須。
- `code`は省略時`""`（全銘柄）。
- `mgmtId`は省略・`null`・空文字列の場合、API受付側で新規管理レコードを作成。
- 既存`mgmtId`指定では、その管理レコードに保存済みの条件で再実行する。

レスポンス例:

```json
{
  "message": "バッチ起動を受け付けました",
  "mgmtId": "20261025-195000"
}
```

ここでの管理IDは形式例であり、実際に発行した値ではありません。

```text
FastAPI Router
  ├─ 新規管理IDが必要ならCacheMgmtService.create()
  ├─ BackgroundTasks.add_task(run_cache, mgmtId)
  └─ 202 + mgmtIdを返却
            ↓（レスポンス送信後）
         run_cache()
            ↓
       jquants_cache()
         1. 管理レコード取得
         2. 上場銘柄マスタ更新（対象ステータスのみ）
         3. 対象銘柄リスト取得（全件または指定code）
         4. 日足株価キャッシュ
         5. バリュエーションキャッシュ
         6. 財務サマリーキャッシュ
         7. Dataset単位でComplete/Errorを記録
```

## 9. Transaction・Error設計

- 各Datasetの銘柄ごとの取得処理では`with SessionLocal.begin() as db:`を使い、**その銘柄に対するDatasetの登録処理が成功した場合にcommit**。例外ではそのブロック内の処理をrollback。
- `db.merge()`のみではcommitしない。J-QuantsのRepositoryに毎行`commit()`は置かない。
- 進捗管理テーブルは別Session/別commitなので、処理本体が失敗してもErrorの状態を残せる設計。
- **全バッチ一括トランザクションではない**。既に処理を終えた別銘柄・別Datasetの確定データは、後続の失敗では取り消されない。
- `jquants_cache()`は`{status: success|error, message}`を返し、`run_cache()`はerror時に例外を送出してログを記録する。
- `BackgroundTasks`はアプリケーション内のバックグラウンドタスクであり、Dockerコンテナ停止・再起動後に処理の継続・自動再開を保証しない。

## 10. マイグレーションと動作確認

関連するAlembic revisionはGitHubの`backend/alembic/versions/`を確認。キャッシュ管理テーブルの導入・修正のrevisionとして`70d536cc789d`、`1659bc942177`、`c9a27d03baec`、`3b15924e084c`が存在し、`29992610a0a9`は空のupgrade/downgradeです。

実装変更後の基本確認:

```powershell
docker compose up -d
docker compose exec backend alembic current
docker compose exec backend alembic heads
docker compose exec backend alembic upgrade head
docker compose ps
```

起動APIは`http://localhost:8000/docs`のSwagger UIでも確認できます。管理テーブルと保存結果の確認にはTablePlusを利用します。

## 11. 既存機能と将来の責務

- **User Domain:** CRUD、検索、フィルタ、ソート、ページングを維持。ホーム・ユーザー系はMantine版へ切替済み（サンプル機能）。
- **EDINET Legacy:** CSV取得可能書類の棚卸し、日付範囲Refresh、DB保存、CLI Batchを実装済み。2026-09-26以降の主データソースはJ-Quantsへ移行。EDINETのコード・テーブルは維持し、財務解析拡張は行わない方針。
- **Screening:** 価格変動率、52週高値・安値、52週高値からの下落率、PER/PBR/配当利回り、業績と株価の乖離などの判定は今後の業務ロジック/UI対象。

## 12. 現時点で保留する事項・制約

- ページネーション対応：ユーザーの取得確認により現時点では保留。API仕様で将来分割が発生しない保証を確認したものではない。
- 管理IDの同一秒衝突対策：発生頻度が低いとして意図的に保留。
- 上場廃止銘柄をマスタから除外する仕組み：別途検討。
- 入力日付の範囲検証、管理IDの存在事前確認、長時間バッチの排他・中断・復旧、進捗確認用のREST GET API：必要性に応じて今後検討。
- J-Quantsキャッシュ機能は実装済み。全銘柄・長期間の稼働性能や障害復旧まで本資料作成時に検証したものではない。

---

ドキュメントの役割: `architecture.md`＝構成・実装方針、`handover_phase.md`＝引継ぎ・直近作業、`project-overview.md`＝目的・進捗・ロードマップ。
