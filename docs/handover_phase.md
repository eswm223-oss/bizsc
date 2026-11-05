# BizSC Handover Phase

更新日: 2026-11-05  
確認したGitHubソースのコミット（本更新前）: [`e0d43a3`](https://github.com/eswm223-oss/bizsc/commit/e0d43a38f4d1286d1cbac7cdc0d87e11b6e6f3f1)

## 1. この資料の目的／次のチャットへの引継ぎ

BizSCは、日本株向けの株式スクリーニングアプリ。**J-Quantsのキャッシュ実行・管理APIおよび管理画面・4種データ一覧を実装し、現行画面のMantine移行を一区切り完了**した。次は保存データを利用するスクリーニング処理の設計や、必要な実データ確認・Frontend連携へ進められる状態にある。

重要: 「コード実装の完了」と「全条件での長期間バッチ稼働検証済み」は区別する。GitHubの確認済みソースを基準に記述しており、この資料更新に際してDBや実APIの結合実行は行っていない。利用者から2026-11-04のFrontendビルド成功の報告があった。今回の資料更新では結合実行・ブラウザ操作をしていない。

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

## 4. キャッシュ起動・管理API

Backendの起動APIは`backend/app/api/cache_batch.py`の **`POST /batches/jquants/cache/start`**。HTTP 202を返し、FastAPIの`BackgroundTasks`から`run_cache(mgmtId)`を起動する。

新規起動JSON例:

```json
{
  "fromDate": "2026-11-01",
  "toDate": "2026-11-03",
  "code": "13010"
}
```

- `fromDate`/`toDate`は必須の日付（`YYYY-MM-DD`）、`code`は省略・空文字で全銘柄。
- `mgmtId`を省略・null・空文字にすると管理IDを新規発行。既存の`mgmtId`指定では保存済みの対象期間・銘柄コードを使用して再実行する。
- 202受付の応答例: `{"message":"バッチ起動を受け付けました","mgmtId":"20261105-123000"}`（IDは形式例であり実データではない）。

管理API（`backend/app/api/cache_mgmt.py`）:

| HTTP | Endpoint | 内容 |
|---|---|---|
| GET | `/cachemgmt/list` | 管理ID部分一致`keyword`、対象日`date`、`page`、`limit` |
| GET | `/cachemgmt/{mgmt_id}` | 管理詳細。不存在は404 |
| DELETE | `/cachemgmt/{mgmt_id}` | 管理レコード削除。204。実行中も削除制限なし |

データ参照API: `GET /jquants/master`、`GET /jquants/dailyquote`、`GET /jquants/valuation`、`GET /jquants/summary`（キーワード・日付検索、ページング）。

## 5. 画面とバッチ実行経路

`frontend/src/routes/AppRoutes.tsx`は現行画面すべてを`MainLayoutMantine`配下に接続。

| 画面 | URL | 主な操作 |
|---|---|---|
| 管理一覧 | `/jquants/cache` | ID検索、対象日検索、ページング、Dataset別ステータス |
| 新規キャッシュ | `/jquants/cache/detail` | 日付範囲・銘柄を指定し起動 |
| 管理詳細 | `/jquants/cache/detail/:mgmtId` | 保存条件・状態・備考を確認、再実行、削除 |
| データ一覧 | `/jquants/master`、`/jquants/dailyquote`、`/jquants/valuation`、`/jquants/summary` | 検索・ページング |

```text
CacheBatch / CacheDetail → frontend/src/api/cache.ts
  → POST /batches/jquants/cache/start
  → BackgroundTasks.add_task(run_cache, mgmtId)
  → services/batches/jquants_sync.py
  → services/jquants/cache/jquants_cache.py
  → J-Quants Client / CacheMgmtService / Repository → PostgreSQL
```

`cache_mgmt`のDataset別ステータスは`Waiting`、`Running`、`Complete`、`Error`（対象外はNULL）。`remarks`にはエラーを最大300文字保存。完了済みDatasetは再実行時スキップし、未完了部分を処理する。

バッチ本体は実行開始時に`Running`または4つとも`Complete`を検出すれば拒否する。ただし判定はAPIの202応答後であり、厳密なDB排他制御は未実装（限定的な競合は許容する方針）。管理レコードの実行中削除も許容する。

FrontendはMantine 9、TanStack Query、Mantine Notificationsを利用。キャッシュ管理一覧・詳細に自動ポーリングは未実装であり、進捗は画面再表示等で確認する。

## 6. 主な変更履歴（概要）

- `jquants_service_2` 系: J-Quants 4種類のModel / Repository / Service / Cacheを整理。`db.merge`、日付範囲・企業名検索を実装。
- `jquants_cache_process`: `cache_mgmt`、キャッシュ起動API、BackgroundTasks、バッチServiceを導入。
- `jquants_chche_process_fix` ～ `fix_3`: Router登録、`SessionLocal()`利用、引数順、ステータス表記、銘柄絞り込み、日付条件、リトライとエラー処理を修正。
- **`jquants_chche_process_fix_4`**: ClientのHTTPエラー時にレスポンス本文の`message`を例外へ反映。Cache内の処理状態変数を整理し、日足株価・Valuation・財務サマリーAPI前に1秒間隔を追加。API側で空の`mgmtId`も新規扱い。
- **Mantine UI移行（2026-11-05確認）**: ホーム・ユーザーCRUDに加えてJ-Quants管理／一覧画面もMantine版へ切替。`jquants_front作成`〜`fix3`で画面連携と型を修正し、`jquants_cache_front`で旧レイアウト・`/test`画面を整理。

### UI移行後の確認事項（2026-11-05）

- `frontend/src/main.tsx`: Mantine CSS・theme、QueryClientProvider、Notifications、BrowserRouterを設定。
- `AppRoutes.tsx`: ユーザーCRUDとJ-Quantsの4種データ一覧・キャッシュ管理をMantineレイアウトへ接続。旧`MainLayout.tsx`と`/test`ルートは削除済み。
- 管理一覧は画面固有のTanStack Query queryKey、Mantine Table/Pagination、検索適用・リセットを使用。
- 利用者が2026-11-04に`docker compose exec frontend npm run build`の成功を報告。JS 727.69 kB（gzip 220.08 kB）、500 kB超警告のみ。資料更新時にはビルド未実行。

## 7. 次の作業候補（再開時の優先順位）

### Step 1: 小範囲の取得・保存結果を確認

推奨: 1銘柄（例: `13010`）、数営業日の範囲。キャッシュ新規画面またはSwagger UIから起動し、管理一覧・詳細画面で状態を確認する。

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
- **実行停止・排他・中断後の再開:** FastAPI `BackgroundTasks`は同一アプリプロセス内。Docker停止で中断する可能性があり、自動継続はしない。厳密な排他は頻度が限定的として現状保留。
- **長時間の全銘柄取得:** 各Datasetで銘柄単位のAPI呼び出し＋約1秒の間隔がある。全件処理時間・API制限・コンテナ停止時の復旧は別途評価。
- **状態管理API:** 管理一覧・詳細GETと削除DELETEは実装済み。自動更新やリアルタイム通知は未実装。
- **入力バリデーション・ID照合:** 新規起動画面では`fromDate <= toDate`を検証。管理詳細GETは不存在で404。起動API側の追加検証・存在事前確認は今後必要に応じて検討。

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
6. 新しいUIはMantine標準コンポーネントを優先。現在のJ-Quants管理・一覧画面はMantineレイアウトに統合済み。
