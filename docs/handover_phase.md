# BizSC Handover Phase

更新日: 2026-10-27  
確認したGitHubソースのコミット（本更新前）: [`6b577b8`](https://github.com/eswm223-oss/bizsc/commit/6b577b832beb6f661a97a87fd697fa3b9dbaf8ae)

## 1. この資料の目的／次のチャットへの引継ぎ

BizSCは、日本株向けの株式スクリーニングアプリ。**J-Quantsキャッシュ処理のコード実装・レビュー修正、およびホーム・ユーザー画面のMantineへの移行を一区切り完了**した。次は保存データを利用するスクリーニング処理の設計や、必要な実データ確認・Frontend連携へ進められる状態にある。

重要: 「コード実装の完了」と「全条件での長期間バッチ稼働検証済み」は区別する。GitHubの確認済みソースを基準に記述しており、この資料更新に際してDBや実APIの結合実行は行っていない。UIについては利用者からビルド成功・正常動作の報告があった。

GitHub: <https://github.com/eswm223-oss/bizsc>  
Workspace: `D:\Development\apps\bizsc`

## 2. 既存基盤

- Docker Compose: backend/FastAPI（8000）、frontend/React+Vite（5173）、db/PostgreSQL17（5432）。
- Python 3.12、SQLAlchemy、Alembic、Pydantic、httpx、pytest。
- User CRUD / 検索・フィルタ・ページングのUI実装済み。ホーム・ユーザー画面はMantine版へ切替済み（サンプル）。
- EDINETの棚卸し実装・テーブルはLegacyとして保持。新しい主データソースはJ-Quants。
- WindowsのローカルPostgreSQLとDocker PostgreSQLの5432番競合に注意。

## 3. J-Quants実装済み範囲

| Dataset | Client | Model / DB |
|---|---|---|
| 上場銘柄 | `fetch_listed_issues` | `JQuantsListedIssue` / `jq_listed_issues` |
| 日足株価 | `fetch_bars_daily` | `JQuantsDailyQuote` / `jq_daily_quotes` |
| バリュエーション | `fetch_valuation` | `JQuantsValuation` / `jq_valuations` |
| 財務サマリー | `fetch_summary` | `JQuantsFinancialSummary` / `jq_financial_summaries` |
| ジョブ管理 | ― | `CacheMgmt` / `cache_mgmt` |

- 主キー: ListedIssueは`code`、DailyQuote/Valuationは`code-YYYYMMDD`、FinancialSummaryは`code-期間終了日-期間種別-書類種別`。
- `db.merge()`で同一キーの登録・更新を共通化。J-Quants本体のRepositoryには行ごとのcommitを置かず、`SessionLocal.begin()`で確定。
- 銘柄マスタは最新を取得し、既存レコードより古いレコードでは上書きしない。
- J-Quantsの数値・日付変換は共通モジュールを使用。財務項目の空文字列はNULLへ変換。
- API呼び出し前の`time.sleep(1)`は、日足株価・バリュエーション・財務サマリーに存在。

## 4. キャッシュ起動API

ファイル: `backend/app/api/cache_batch.py`  
Router登録: `backend/app/main.py`  
Endpoint: `POST /batches/jquants/cache/plain`  
応答: HTTP `202 Accepted`

新規起動例（Swagger UIまたはREST Client）:

```json
{
  "fromDate": "2026-10-01",
  "toDate": "2026-10-23",
  "code": "13010"
}
```

`mgmtId`は省略可能。省略すると管理レコードを作成して管理IDを返す。`code`を省略または空文字列にすると、マスタに登録されている全銘柄が対象となる。実行時間に大きく影響するため、**初回確認は1銘柄・短期間から**行う。

受け付け時のレスポンス例:

```json
{
  "message": "バッチ起動を受け付けました",
  "mgmtId": "20261025-195000"
}
```

※ 上記IDは書式例。202応答の時点でバッチは完了していない。

再実行例:

```json
{
  "fromDate": "2026-10-01",
  "toDate": "2026-10-23",
  "code": "13010",
  "mgmtId": "20261025-195000"
}
```

既存`mgmtId`が渡されると、キャッシュ本体は`cache_mgmt`の保存済み条件を参照する。APIボディ中の日付・コードの指定と食い違わないようにすること。

## 5. 実行経路と確認先

```text
api/cache_batch.py
  → BackgroundTasks.add_task(run_cache, mgmtId)
  → services/batches/jquants_sync.py : run_cache(mgmtId)
  → services/jquants/cache/jquants_cache.py : jquants_cache(mgmtId)
  → services/jquants/db/cache_manage.py : CacheMgmtService
  → repositories/cache_mgmt.py : CacheMgmtRepository
  → models/cache_mgmt.py : CacheMgmt
```

4つのDataset保存は `jquants_cache.py` の `_equities_master_cache` / `_daily_quote_cache` / `_valuation_cache` / `_summary_cache` が担当。JSONを各Modelに変換し、Service経由でRepositoryへ渡す。

`cache_mgmt`の主要ステータス:

```text
Waiting → Running → Complete
                    └→ Error（API/DB/変換失敗等）
```

`Waiting`、`Running`、`Error`は次回起動時の処理対象。`Complete`はスキップ。`remarks`にはエラーメッセージを最大300文字保存する。

## 6. 主な変更履歴（概要）

- `jquants_service_2` 系: J-Quants 4種類のModel / Repository / Service / Cacheを整理。`db.merge`、日付範囲・企業名検索を実装。
- `jquants_cache_process`: `cache_mgmt`、キャッシュ起動API、BackgroundTasks、バッチServiceを導入。
- `jquants_chche_process_fix` ～ `fix_3`: Router登録、`SessionLocal()`利用、引数順、ステータス表記、銘柄絞り込み、日付条件、リトライとエラー処理を修正。
- **`jquants_chche_process_fix_4`**: ClientのHTTPエラー時にレスポンス本文の`message`を例外へ反映。Cache内の処理状態変数を整理し、日足株価・Valuation・財務サマリーAPI前に1秒間隔を追加。API側で空の`mgmtId`も新規扱い。
- **Mantine UI移行（2026-10-27確認）**: `@mantine/core` / `@mantine/hooks` 9.7.4 を採用。Bootstrap npm依存を削除。ホーム・ユーザーCRUD画面と共通レイアウトをMantine版へ切替。J-Quants画面・テスト画面は既存レイアウト側に残す。

### UI移行後の確認事項

- `frontend/src/main.tsx`: MantineのCSS、`MantineProvider defaultColorScheme="auto"`、`BrowserRouter` を設定済み。
- `frontend/src/routes/AppRoutes.tsx`: `/`、`/users`、`/users/new`、`/users/:userId`、`/users/:userId/edit` をMantine版で提供。`/jquants/master` と `/test` は従来の `MainLayout` のまま。
- `frontend/src/layouts/MainLayoutMantine.tsx`: `AppShell`、メニュー、ライト／ダーク切替。`frontend/src/components/UserForm/UserFormMantine.tsx`: 共通ユーザーフォーム。
- ユーザー一覧はMantine `Table`／`Pagination`。TanStack Table v9は `components/test/TanstackTable.tsx` で維持。
- 旧Bootstrapベースの画面や共通UIソースは一部リポジトリに残存。依存パッケージを削除したことと、旧ソースの削除完了は別事項。
- 利用者の実行結果: `docker compose exec frontend npm run build` は成功し、ブラウザで正常動作を確認済み。生成JSは約605KBで500KB超の警告あり（エラーではない）。この文書更新では再実行していない。

## 7. 次の作業候補（再開時の優先順位）

### Step 1: 小範囲の取得・保存結果を確認

推奨: 1銘柄（例: `13010`）、数営業日の範囲。Swagger UIから起動し、返された`mgmtId`で管理状況を確認する。

```sql
SELECT id, from_date, to_date, company_code,
       status_master, "status_dailyBar", status_valuation,
       status_summary, remarks, updated_at
FROM cache_mgmt
ORDER BY id DESC
LIMIT 20;
```

注意: `status_dailyBar`はModelの識別子に大文字Bを含むため、実DB上のカラム名・引用符の必要性はAlembic生成結果を確認すること。

各DBテーブルでも指定銘柄のデータ件数、日付範囲、キー重複、数値NULLの扱いを確認する。最新コミット確認以外の結合動作検証は本資料では未実施。

### Step 2: スクリーニング条件と取得済みデータの対応を整理

最初に、最新株価、52週高値・安値、高値からの下落率、直近騰落率、PER、PBR、時価総額、売上高・営業利益・純利益の伸び等を「API値」「DB保存値」「BizSCで計算する指標」に分類する。

### Step 3: ScreeningのRepository / Service / API設計

銘柄一覧、条件検索、業績が伸びているのに株価が低迷する銘柄の抽出を小さいStepで実装。FrontendはBackendで必要なクエリが成立してから進める。

## 8. 未決定事項／意図的に保留するもの

- **ページネーション自動取得:** Postmanの大きな範囲で全件取得できたとのユーザー確認により、現時点では未実装・保留。
- **管理IDの同秒重複:** 発生頻度が低いため対策しない判断。これを繰り返し指摘しない。
- **上場廃止対応:** 現在のListedIssueマスタから不要銘柄を除去する処理は将来検討。
- **実行停止・排他・中断後の再開:** FastAPI `BackgroundTasks`は同一アプリプロセス内。Docker停止でバッチが中断する可能性があり、自動継続はしない。
- **長時間の全銘柄取得:** 各Datasetで銘柄単位のAPI呼び出し＋約1秒の間隔がある。全件処理時間・API制限・コンテナ停止時の復旧は別途評価。
- **状態管理の補助API:** 現在は起動エンドポイントを確認。進捗照会用GET APIは実装済みとみなさない。
- **入力バリデーション・ID照合:** `fromDate <= toDate`の検証や存在しない管理IDへのHTTP事前エラーは、現時点で独立した対応が必要な候補。

## 9. GitHubとDBの確認コマンド

```powershell
cd D:\Development\apps\bizsc
docker compose up -d
docker compose ps
docker compose exec backend alembic current
docker compose exec backend alembic heads
# Frontend（UI変更時）
docker compose exec frontend npm run build
# マイグレーション内容を確認してから実行
docker compose exec backend alembic upgrade head
# 必要な場合のみ
docker compose exec backend pytest -v
```

※ 直近の開発レビューではテストコード実装をスキップする方針だった。今後もユーザーの希望を確認してから追加する。

## 10. 新チャットへの申し送り

1. `docs/architecture.md`、`docs/handover_phase.md`、`docs/project-overview.md` を参照。
2. **GitHub最新コードを再確認**してから説明・変更案を出す。
3. EDINET解析の続きではなく、J-Quantsキャッシュ後のスクリーニング設計を主軸とする。
4. 実装済みと動作検証済みを混同しない。根拠のない成功宣言は避ける。
5. 開発は小さいStep単位で進め、不要なLibrary・別サービスを追加しない。
6. 新しいUIはMantine標準コンポーネントを優先。J-Quants画面の旧レイアウトとMantine版の適用範囲を区別する。
