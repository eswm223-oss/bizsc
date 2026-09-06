# BizSC Handover Phase

更新日: 2026-09-06

## 1. この資料の目的

この資料は、BizSC の EDINET 実装作業を**別 Chat へ引き継いでそのまま再開するための進捗資料**です。

`architecture.md` が現在の構成・責務・設計原則を扱うのに対し、
この `handover_phase.md` では以下を扱います。

- どこまで実装済みか
- 何を確認済みか
- 何を確定方針としたか
- 次に何をするか
- 次の実装時に崩してはいけない条件
- 実行済みコマンド
- 直近の注意点

---

## 2. Project 情報

Project:

```text
BizSC
```

Workspace:

```text
D:\Development\apps\bizsc
```

GitHub:

```text
https://github.com/eswm223-oss/bizsc
```

Development Environment:

- Windows
- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus

Stack:

- FastAPI
- Python
- SQLAlchemy
- PostgreSQL 17
- Alembic
- pytest
- httpx
- React
- TypeScript
- Vite
- Bootstrap

---

## 3. 開発進行ルール

この Project では以下の進め方を継続する。

```text
Phase
↓
Step
↓
実装
↓
テスト
↓
結果確認
↓
次 Step
```

重要:

- 1 Step ずつ進める
- 必要以上に先へ進まない
- ユーザーが「完了」と言った Step は再度確認しすぎない
- コード確認が必要な場合は GitHub の最新状態を確認する
- 推測で現在コードを決めつけない
- Commit / Push は小変更ごとではなく区切りの良い地点
- 外部 API はいきなり大量アクセスしない
- 実データ確認は小範囲から行う
- 新しい Library / Infrastructure は必要性が出てから導入
- Repository / Service / Client の責務を混在させない
- 正確性優先。不明点は不明とする

---

## 4. EDINET 最終方針

現在確定している棚卸し対象:

```text
現在上場している企業
        ×
現在日から過去10年間
        ×
提出日ベース
        ×
csvFlag == "1"
```

重要:

- 現在上場企業の判定は最新 EDINET Code List を使用
- `上場区分 == "上場"`
- `証券コード` が空でない
- 証券コードは `str` として扱う
- 英字入りコードあり
- `docTypeCode` は事前限定しない
- `csvFlag == "1"` を対象
- CSV ZIP 本体取得は別 Phase
- まず書類一覧を DB に棚卸しする

---

## 5. EDINET Phase 01

Phase 01:

```text
EDINET API 接続
書類一覧取得
```

完了済み。

実装:

```text
backend/app/clients/edinet.py
backend/tests/test_edinet_client.py
```

主要関数:

```python
fetch_document_list(target_date: date)
```

Endpoint:

```text
https://api.edinet-fsa.go.jp/api/v2/documents.json
```

Parameter:

```text
date=YYYY-MM-DD
type=2
Subscription-Key=<EDINET_API_KEY>
```

Timeout:

```text
30 sec
```

API Key:

```text
EDINET_API_KEY
```

---

## 6. EDINET Code List

現在上場企業取得も実装済み。

公開関数:

```python
fetch_listed_sec_codes() -> set[str]
```

取得元:

```text
Edinetcode.zip
└─ EdinetcodeDlInfo.csv
```

Encoding:

```text
CP932
```

現在上場判定:

```text
上場区分 == "上場"
AND
証券コード != 空
```

実接続時の確認例:

```text
count = 3820
```

Sample:

```text
13010
130A0
13320
13330
135A0
13750
13760
13770
13790
137A0
```

重要:

```text
証券コードは int にしない
```

英字入りコードがあるため、
`isdigit()` 前提や数値変換は禁止。

---

## 7. Phase 02 初期棚卸し

既存 Service:

```text
backend/app/services/edinet_inventory.py
```

既存:

```python
inventory_start_date(end_date)
summarize_one_day_inventory(results, listed_sec_codes)
```

`OneDayInventorySummary`:

```text
total_count
listed_match_count
csv_flag_count
doc_type_counts
```

### 3日実測結果

対象:

```text
2026-08-19
2026-08-20
2026-08-21
```

結果:

```text
2026-08-19
total=203
listed=42
csv=28

2026-08-20
total=313
listed=38
csv=29

2026-08-21
total=226
listed=51
csv=39
```

3日合計:

```text
days=3
total=742
listed=131
csv=96
```

この時点で 429 / Error は発生しなかった。

---

## 8. DB 保存設計

当初は棚卸し結果を JSON 保存する案もあったが、
現在は PostgreSQL 保存に変更済み。

使用 Table:

```text
edinet_documents
edinet_inventory_runs
```

---

## 9. edinet_documents

Model:

```text
backend/app/models/edinet_document.py
```

目的:

```text
現在上場企業
×
csvFlag == "1"
```

に一致した EDINET 書類を保存する。

主要方針:

```text
target_date あり
doc_id Unique
sec_code は str
submit_date_time は timezone=False
```

`submitDateTime` は EDINET 元データが timezone を持たないため、

```python
DateTime(timezone=False)
```

へ変更済み。

BizSC 生成日時:

```text
created_at
updated_at
```

は timezone-aware のまま。

---

## 10. edinet_inventory_runs

Model:

```text
backend/app/models/edinet_inventory_run.py
```

目的:

```text
target_date ごとの最新実行状態
```

Status:

```text
processing
completed
failed
```

主要 Column:

```text
target_date
status
total_count
listed_match_count
csv_flag_count
listed_sec_code_count
error_message
started_at
completed_at
created_at
updated_at
```

`target_date` は Unique。

同じ日を再実行しても run 行を増やさず、
同じ 1 行を更新する。

---

## 11. Alembic Migration

EDINET Table 追加 Migration:

```text
2290170f9497
```

内容:

```text
edinet_documents
edinet_inventory_runs
```

追加。

その後、

```text
6fb348a0c9e4
```

で、

```text
edinet_documents.submit_date_time
```

を、

```text
timestamp with time zone
↓
timestamp without time zone
```

へ変更。

Migration 適用済み。

確認済み:

```text
alembic current
→ 6fb348a0c9e4 (head)
```

---

## 12. TablePlus / PostgreSQL 注意点

TablePlus 接続時に以下 Error が出た。

```text
connection to server at "127.0.0.1", port 5432 failed:
FATAL: password authentication failed for user "bizsc"
```

Docker 内では以下で認証成功していた。

```powershell
docker compose exec -e PGPASSWORD=bizsc db psql -h 127.0.0.1 -U bizsc -d bizsc -c "SELECT current_user, current_database();"
```

結果:

```text
bizsc | bizsc
```

原因:

```text
Windows版 PostgreSQL Service が混在
```

Windows 側 PostgreSQL Service を停止したところ、
TablePlus から Docker PostgreSQL へ正常接続できた。

今後 TablePlus 接続異常が出た場合は、
Password だけでなく Windows PostgreSQL Service の 5432 競合も確認する。

---

## 13. EDINET Repository

Step 6-4 完了。

実装:

```text
backend/app/repositories/edinet_inventory.py
backend/app/repositories/__init__.py
```

Class:

```python
EdinetInventoryRepository
```

Method:

```text
get_documents_by_target_date
delete_documents_by_target_date
add_documents
get_run_by_target_date
add_run
```

重要:

```text
Repository 内では commit しない
```

削除・追加とも `flush()` まで。

Transaction は Service 側で制御する。

Repository は、

```text
completed なら skip
```

の判断をしない。

---

## 14. Repository Import 確認

以下で import 成功を確認済み。

```powershell
docker compose run --rm backend python -c "from app.repositories import EdinetInventoryRepository; print(EdinetInventoryRepository)"
```

結果:

```text
<class 'app.repositories.edinet_inventory.EdinetInventoryRepository'>
```

---

## 15. Step 6-5 EdinetInventoryService

実装済み。

対象:

```text
backend/app/services/edinet_inventory.py
backend/app/services/__init__.py
backend/tests/test_edinet_inventory.py
```

Class:

```python
EdinetInventoryService
```

公開 Method:

```python
refresh_one_day(
    db: Session,
    target_date: date,
) -> OneDayInventorySummary
```

---

## 16. refresh_one_day の処理

現在の流れ:

```text
target_date の run 取得
        ↓
run がなければ新規
        ↓
status = processing
        ↓
started_at
counts = 0
error_message = None
        ↓
commit
        ↓
fetch_listed_sec_codes()
        ↓
fetch_document_list(target_date)
        ↓
results 検証
        ↓
summarize_one_day_inventory()
        ↓
現在上場企業
×
csvFlag == "1"
だけ EdinetDocument 化
        ↓
delete_documents_by_target_date()
        ↓
add_documents()
        ↓
run = completed
        ↓
件数更新
        ↓
commit
```

---

## 17. 再実行方針

重要な確定仕様:

```text
completed でも再実行する
failed でも再実行する
processing でも再実行する
```

`completed` は Skip Gate にしない。

理由:

- completed 誤設定の可能性を排除しない
- EDINET 側の後日変更に対応
- 1日単位なら再取得を許容
- 手動刷新可能にする

---

## 18. 日単位 Refresh 方針

同じ `target_date` を実行した場合:

```text
既存 target_date documents
↓
DELETE
↓
新しい documents
↓
INSERT
```

とする。

重要:

```text
DELETE 後に途中 commit しない
```

以下は 1 Transaction:

```text
DELETE
INSERT
run completed
commit
```

---

## 19. 失敗時 Transaction

失敗時:

```text
Exception
↓
db.rollback()
↓
run 再取得
↓
status = failed
completed_at 設定
error_message 設定
↓
db.commit()
↓
元 Exception を re-raise
```

これにより、既存正常 Documents を刷新途中の Error で消さない。

---

## 20. error_message 方針

秘密情報を保存しない。

`EdinetClientError`:

```text
Client 側で安全化した message を使用
```

予期しない Exception:

```text
type(exc).__name__
```

など、安全な情報だけ保存。

以下は禁止:

```text
Subscription-Key
API Key
Request URL 全体
Secret を含む RuntimeError message
```

---

## 21. EDINET Response 検証

Step 6-5.1 で安全性向上済み。

正常:

```python
payload が dict
AND
payload["results"] が list
```

空:

```python
"results": []
```

は正常。

異常:

```text
payload が dict でない
results が存在しない
results が list でない
```

この場合は Exception。

理由:

```text
不正 Response
↓
[] と誤認
↓
既存 Documents 全削除
```

を防ぐため。

---

## 22. EdinetDocument Mapping

主な Mapping:

```text
target_date        <- refresh 対象日
doc_id             <- docID
edinet_code        <- edinetCode
sec_code           <- secCode
filer_name         <- filerName
ordinance_code     <- ordinanceCode
form_code          <- formCode
doc_type_code      <- docTypeCode
period_start       <- periodStart
period_end         <- periodEnd
submit_date_time   <- submitDateTime
doc_description    <- docDescription
parent_doc_id      <- parentDocID
withdrawal_status  <- withdrawalStatus
doc_info_edit_status <- docInfoEditStatus
disclosure_status  <- disclosureStatus
xbrl_flag          <- xbrlFlag
pdf_flag           <- pdfFlag
csv_flag           <- csvFlag
legal_status       <- legalStatus
```

### periodStart / periodEnd

```text
None / ""
→ None
```

値あり:

```python
date.fromisoformat(...)
```

### submitDateTime

```text
None / ""
→ None
```

値あり:

```text
YYYY-MM-DD HH:MM
```

を naive datetime に変換。

timezone を追加しない。

---

## 23. Step 6-5 Test

実行:

```powershell
docker compose run --rm backend pytest -v tests/test_edinet_inventory.py
```

結果:

```text
7 passed in 0.42s
```

通過 Test:

```text
test_inventory_start_date_is_ten_years_before_end_date
test_inventory_start_date_handles_february_29
test_summarize_one_day_inventory_filters_listed_then_csv_flag
test_summarize_one_day_inventory_empty_results
test_refresh_one_day_reruns_completed_and_saves_filtered_documents
test_refresh_one_day_marks_failed_and_reraises
test_refresh_one_day_rejects_payload_without_results_list
```

確認内容:

- 10年前の日付
- 2月29日
- 現在上場 Filter
- csvFlag Filter
- completed 再実行
- processing 保存
- 削除 → 追加
- completed
- `130A0` を文字列保存
- csvFlag != 1 を除外
- submitDateTime naive
- rollback
- failed
- re-raise
- Secret 非保存
- 不正 results 拒否
- 不正 Response で Documents 削除しない

---

## 24. Step 6-6 実 DB 保存

対象日:

```text
2026-08-21
```

実行済み。

実行コマンド:

```powershell
docker compose run --rm backend python -c "from datetime import date; from app.db.database import SessionLocal; from app.repositories import EdinetInventoryRepository; from app.services import EdinetInventoryService; db=SessionLocal(); summary=EdinetInventoryService(EdinetInventoryRepository()).refresh_one_day(db, date(2026, 8, 21)); print(summary); db.close()"
```

実 DB へ登録されることを確認済み。

TablePlus で:

```text
edinet_documents
edinet_inventory_runs
```

へ登録確認済み。

---

## 25. Step 6-6 再実行確認

同じ:

```text
2026-08-21
```

を再実行済み。

確認済み:

```text
edinet_documents が2倍に増えない
target_date 単位で刷新される
edinet_inventory_runs が同日2行に増えない
status = completed
error_message = NULL
```

よって、

```text
1日単位 Refresh
```

は実 DB でも正常動作確認済み。

---

## 26. 現在の完了地点

ここまで完了:

```text
Phase 01
EDINET API 接続
↓
完了

Phase 02
現在上場企業判定
↓
完了

1日棚卸し
↓
完了

DB Model
↓
完了

Alembic Migration
↓
完了

Repository
↓
完了

EdinetInventoryService.refresh_one_day
↓
完了

Response Safety
↓
完了

Unit Test
↓
7 passed

実 DB 保存
↓
完了

同日再実行 / Refresh
↓
完了
```

---

## 27. 次の Step

次は:

```text
Step 7-1
複数日を順番に刷新する Service
```

実装予定 Method:

```python
refresh_date_range(
    db: Session,
    start_date: date,
    end_date: date,
) -> list[tuple[date, OneDayInventorySummary]]
```

---

## 28. Step 7-1 の確定方針

目的:

```text
start_date
↓
1日ずつ
↓
end_date
```

まで順番に `refresh_one_day` 相当の処理を行う。

ただし重要:

```text
fetch_listed_sec_codes()
```

は各日ごとに取得しない。

1回の範囲処理につき 1回だけ取得する。

理由:

- 現在上場企業判定は同じ最新一覧を使う
- 不要な HTTP 通信を減らす

---

## 29. Step 7-1 実装時の構成案

既存:

```python
refresh_one_day(...)
```

は壊さない。

必要なら内部処理を private Method 化:

```text
refresh_one_day
↓
fetch_listed_sec_codes()
↓
private 1日刷新処理
```

複数日:

```text
refresh_date_range
↓
fetch_listed_sec_codes() 1回
↓
private 1日刷新処理
↓
private 1日刷新処理
↓
...
```

既存 1日 Test を維持する。

---

## 30. Step 7-1 処理仕様

### 入力 Validation

```text
start_date > end_date
```

なら:

```python
ValueError
```

例:

```text
start_date must be on or before end_date
```

この場合:

```text
fetch_listed_sec_codes
fetch_document_list
DB Refresh
```

を実行しない。

### 日付走査

`start_date` / `end_date` 両端を含む。

例:

```text
2026-08-19
2026-08-20
2026-08-21
```

### 各日

```text
processing
↓
fetch_document_list
↓
Filter
↓
DELETE
↓
INSERT
↓
completed
↓
commit
```

### Error

1日で Error:

```text
その日を failed
↓
Exception re-raise
↓
範囲処理停止
```

現 Step では:

```text
失敗しても次の日へ進む
```

は実装しない。

---

## 31. Step 7-1 Transaction

各日ごとに独立して commit。

例:

```text
2026-08-19
completed → commit

2026-08-20
completed → commit

2026-08-21
failed → rollback / failed commit
```

この場合:

```text
8/19
8/20
```

の completed Data は保持。

---

## 32. Step 7-1 Test 要件

最低限:

```text
1.
2026-08-19 ～ 2026-08-21
→ 3日処理

2.
fetch_listed_sec_codes()
→ 1回だけ

3.
fetch_document_list()
→ 3回

4.
返り値
→ 3日分

5.
start_date > end_date
→ ValueError

6.
Validation Error 時
Client を呼ばない

7.
既存 7 tests を壊さない
```

---

## 33. Step 7-1 ではまだ実装しない

```text
10年全量実行
failed を飛ばして継続
Retry
Sleep
Rate Limit 制御
並列処理
Scheduler
Celery
Redis
API Router
Frontend
CSV ZIP取得
CSV解析
XBRL解析
財務数値抽出
```

---

## 34. Step 7-1 実装後の予定

Step 7-1:

```text
複数日 Service
```

完了後、

```text
3日だけ実 DB で実行
```

予定。

対象候補:

```text
2026-08-19
2026-08-20
2026-08-21
```

確認:

```text
3日分が DB に保存
各 run completed
日別件数
重複なし
```

---

## 35. その後の方向

3日複数日走査が問題なければ、
10年取得向けに追加検討する。

主な論点:

```text
失敗日を飛ばすか
Retry 方針
Rate Limit
Sleep
長時間処理
途中再開
Progress
開始日 / 終了日
何日単位で実行するか
```

ただし、

```text
completed 日を自動 Skip
```

は現時点の確定方針ではない。

再実行で Refresh できる設計を維持する。

---

## 36. 現在未実装

```text
refresh_date_range
10年走査
Retry
失敗継続
Rate Limit 制御
Scheduler
Celery
Redis
EDINET Router
EDINET Frontend
CSV ZIP download
CSV parse
XBRL parse
Financial Data extraction
決算短信
TDnet
```

---

## 37. 参照すべき主要 File

EDINET Client:

```text
backend/app/clients/edinet.py
```

EDINET Service:

```text
backend/app/services/edinet_inventory.py
```

EDINET Repository:

```text
backend/app/repositories/edinet_inventory.py
```

Models:

```text
backend/app/models/edinet_document.py
backend/app/models/edinet_inventory_run.py
```

Tests:

```text
backend/tests/test_edinet_client.py
backend/tests/test_edinet_inventory.py
```

Database:

```text
backend/app/db/database.py
```

Migration:

```text
backend/alembic/versions/
```

---

## 38. 再開時に最初に確認すること

新 Chat では、まずこの資料と `architecture.md` を読む。

その後、GitHub の最新コードを必要に応じて確認。

再開地点:

```text
Step 7-1
refresh_date_range
```

重要:

```text
Step 6-6 まで完了済み
```

なので、1日 Refresh の設計を最初からやり直さない。

---

## 39. 直近の Step 7-1 Cursor 指示要約

Cursor へ渡す内容の要点:

```text
EdinetInventoryService に refresh_date_range を追加

start_date > end_date
→ ValueError

fetch_listed_sec_codes
→ 範囲処理につき1回

start_date ～ end_date
→ 1日ずつ順次

各日
→ 現在の refresh_one_day と同等

1日ごとに commit

失敗時
→ failed
→ re-raise
→ 処理停止

既存 refresh_one_day を壊さない

test追加

Step 7-2 には進まない
```

---

## 40. 現在の状態まとめ

```text
EDINET API
↓
書類一覧取得
↓
現在上場企業判定
↓
csvFlag=1
↓
1日集計
↓
DB Model
↓
Migration
↓
Repository
↓
1日 Refresh Service
↓
安全な Transaction
↓
Error時 rollback
↓
実 DB 登録
↓
同日再実行
↓
正常確認済み
```

次:

```text
複数日 Refresh
```

以上。
