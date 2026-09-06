# BizSC EDINET機能 引継ぎ資料

## 1. この資料の目的

この資料は、BizSC に追加中の EDINET 財務データ取得機能について、別チャットへ移行した際に現在地点から安全に再開するための引継ぎ資料です。

次チャットでは、この資料と以下の既存資料を前提に進めてください。

- `docs/development-guidelines.md`
- `docs/architecture.md`
- `01-edinet-api-fetch.md`
- `02-edinet-document-inventory.md`

GitHubリポジトリ:

```text
https://github.com/eswm223-oss/bizsc
```

コード確認が必要な場合は、推測せず最新コードを確認してください。

---

## 2. 現在の目的

最終的な目的は、

> 現在上場している企業について、過去10年間のEDINET上のCSV取得可能データを可能な限り取得し、将来的にBizSCのDBへキャッシュする

ことです。

ただし、一度に全機能を実装せず、Phaseごとに小さく進めます。

現在はまだ以下には進んでいません。

- CSV本体の大量取得
- DB保存
- 財務データ解析
- Frontend利用

---

## 3. 現在までに確定している方針

### 対象企業

現在上場している企業のみ。

上場判定は **証券コードを基準** にする。

ただし、過去の書類一覧に `secCode` が存在するだけで「現在も上場している」と判定しない。

現在時点のEDINETコードリストから証券コード集合を作り、その証券コードと過去10年間の書類を照合する方針。

証券コードは数値ではなく文字列として扱う。

### 対象期間

```text
現在日から過去10年間
```

提出日ベースで判定する。

固定日付ではなく、実行日の現在日から動的に10年前を算出する。

### 取得対象

書類種別を最初から限定しない。

```text
csvFlag == "1"
```

の書類をすべて棚卸しする。

例:

- 有価証券報告書
- 訂正有価証券報告書
- 半期報告書
- 過去の四半期報告書
- 訂正四半期報告書
- 臨時報告書
- 有価証券届出書
- その他CSVが存在するEDINET提出書類

`docTypeCode` ごとに件数を集計し、どの種類のCSVが実際に存在するかを確認してから次へ進む。

---

## 4. TDnetについて

決算短信や決算説明資料は、基本的にEDINETではなくTDnet側の資料。

ただしTDnetは費用面の問題があるため、現時点では別の方法を検討する方針。

今回のEDINET実装にはTDnetを混ぜない。

---

## 5. Phase 01 完了内容

使用資料:

```text
01-edinet-api-fetch.md
```

目的:

```text
BizSC BackendからEDINET APIへ安全に接続し、指定日の書類一覧JSONを取得できること
```

### Step 1: 現状確認

完了。

確認済み:

- `backend/app/core/config.py`
- `backend/requirements.txt`
- `.gitignore`
- `compose.yaml`
- `backend/app/`

確認事項:

- `pydantic-settings` 使用
- `.env` 読み込み
- `httpx` 既存
- `.env` / `.env.*` はGit除外
- `clients/` は既存構成と衝突しない

### Step 2: EDINET APIキー設定

完了。

`backend/app/core/config.py` に追加:

```python
from typing import Optional
```

```python
edinet_api_key: Optional[str] = None
```

環境変数:

```text
EDINET_API_KEY
```

APIキー未設定でも、EDINET以外の既存Backendは起動可能。

ユーザー側で `backend/.env` に実APIキーを設定済み。

APIキーそのものはチャットやコードへ貼らない。

### Step 3: EDINET Client追加

完了。

追加ファイル:

```text
backend/app/clients/edinet.py
backend/app/clients/__init__.py
```

主な公開関数:

```python
fetch_document_list(target_date: date)
```

使用Endpoint:

```text
https://api.edinet-fsa.go.jp/api/v2/documents.json
```

送信内容:

```text
date=<YYYY-MM-DD>
type=2
Subscription-Key=<APIキー>
```

HTTP Client: `httpx`

Timeout: 30秒

リトライなし。

主な例外:

```text
EdinetClientError
EdinetApiKeyNotConfiguredError
EdinetHttpError
EdinetTimeoutError
EdinetInvalidJsonError
```

APIキーやAPIキー入りURLを例外・ログへ出さない設計。

### Step 4: 最小テスト

完了。

追加:

```text
backend/tests/test_edinet_client.py
```

テスト内容:

- date送信確認
- `type=2`
- `Subscription-Key`
- APIキー未設定
- 429
- Timeout
- Invalid JSON
- APIキー漏えい防止

実行:

```text
docker compose run --rm backend pytest -v tests/test_edinet_client.py
```

結果:

```text
5 passed
```

EDINETへの実アクセスはしないテスト。

### Step 5: EDINET実接続確認

成功。

対象日:

```text
2026-08-21
```

結果:

```text
metadata.status          = 200
metadata.message         = OK
metadata.resultset.count = 226
results件数              = 226
```

先頭1件例:

```text
seqNumber       = 1
docID           = S100YRA1
edinetCode      = E11764
secCode         = 空
filerName       = Ｔ＆Ｄアセットマネジメント株式会社
docTypeCode     = 160
submitDateTime  = 2026-08-21 09:00
periodStart     = 2025-11-27
periodEnd       = 2026-11-26
xbrlFlag        = 1
pdfFlag         = 1
csvFlag         = 1
```

Phase 01 は完了。

---

## 6. EDINET書類種別について確認済みのこと

主な `docTypeCode`:

```text
120 = 有価証券報告書
130 = 訂正有価証券報告書
140 = 四半期報告書
150 = 訂正四半期報告書
160 = 半期報告書
170 = 訂正半期報告書
```

今回の方針では、これらだけに限定せず `csvFlag=1` の全書類を棚卸しする。

---

## 7. csvFlagについて

```text
csvFlag = "1"
```

は、そのEDINET提出書類についてCSVが存在することを示す。

書類取得APIでは `type=5` を使うことでCSV ZIPを取得できる。

ただし、現PhaseではCSV本体は取得しない。

---

## 8. legalStatus / disclosureStatus

次Phaseでは以下も保持・集計する方針。

### legalStatus

```text
1 = 縦覧中
2 = 延長期間中
0 = 閲覧期間満了
```

次Phaseで実際のCSVダウンロード可否を判断するために保持する。

### disclosureStatus

不開示状態等の確認用。

このPhaseでは複雑な判定はせず、まず値を保持・集計する。

---

## 9. Phase 02

作成済み資料:

```text
02-edinet-document-inventory.md
```

目的:

> 現在上場企業 × 現在日から過去10年 × csvFlag=1 のEDINET書類を、CSV本体を取得せず安全に棚卸しする

---

## 10. Phase 02 の予定Step

### Step 1: 現状確認のみ

確認対象:

```text
backend/app/clients/edinet.py
backend/app/clients/__init__.py
backend/tests/test_edinet_client.py
backend/app/core/config.py
backend/requirements.txt
.gitignore
```

このStepではコード変更しない。

### Step 2: 現在上場企業の証券コード集合取得方法の調査

ここではまだ実装しない。

確認するもの:

- 最新EDINETコードリストの取得場所
- ファイル形式
- ZIP / CSV
- 文字コード
- ヘッダ位置
- 証券コード列の正確な名称
- 空欄の扱い
- 証券コードを文字列で安全に扱えるか

実ファイルと公式資料を確認して停止。

### Step 3: 現在上場企業の証券コード集合取得処理

```text
現在のEDINETコードリスト
    ↓
証券コードあり
    ↓
現在対象とする証券コード集合
```

まだ過去10年のAPI走査はしない。

### Step 4: 期間計算と1日分フィルタ

```text
1日分の書類一覧
    ↓
現在証券コード集合と照合
    ↓
csvFlag == "1"
```

確認:

```text
当日書類総件数
証券コード一致件数
csvFlag=1件数
docTypeCode別件数
```

### Step 5: 3～7日程度の小期間で棚卸し確認

10年分はまだ実行しない。

### Step 6: 保存形式・途中再開方法の決定

10年分を実行する前に、以下を決める。

```text
保存形式
保存場所
途中再開方法
Git管理対象
一時ファイル方針
```

このStepでは提案だけ。

### Step 7: 1か月程度の実データ確認

10年分の前にAPI負荷や429発生有無を確認する。

### Step 8: 過去10年分の棚卸し

ユーザー了承後にのみ実行。

CSV本体はまだダウンロードしない。

---

## 11. 過去10年走査時の重要方針

書類一覧APIは1日単位。

10年間では概ね3650回以上のAPIアクセスになる。

そのため:

- いきなり10年分を実行しない
- 全暦日を対象とする
- 並列アクセスしない
- asyncio大量並列禁止
- ThreadPoolExecutor禁止
- multiprocessing禁止
- 429で無限リトライしない
- APIキーをログへ出さない
- 途中再開可能な設計を検討する

---

## 12. Phase 02 の棚卸し項目

最低限保持予定:

```text
docID
edinetCode
secCode
filerName
ordinanceCode
formCode
docTypeCode
periodStart
periodEnd
submitDateTime
docDescription
parentDocID
withdrawalStatus
docInfoEditStatus
disclosureStatus
xbrlFlag
pdfFlag
csvFlag
legalStatus
```

---

## 13. Phase 02 完了時に確認したい集計

```text
現在上場企業として使用した証券コード数
調査開始日
調査終了日
調査日数
全書類件数
現在上場企業一致件数
csvFlag=1件数
docTypeCode別件数
legalStatus別件数
disclosureStatus別件数
CSV取得候補件数
エラー件数
429発生有無
```

---

## 14. 現在まだ実装しないもの

以下には進まない。

```text
CSV ZIPダウンロード
CSV展開
CSV解析
XBRL解析
財務数値抽出
SQLAlchemy Model
Repository
Alembic Migration
PostgreSQL保存
DBキャッシュ
FastAPI Router
Frontend
Redis
Celery
定期バッチ
```

---

## 15. 次チャット開始時の指示

次チャットではまず、Cursorへ以下を指示する。

```text
02-edinet-document-inventory.md を読み、
記載されたルールに従って Step 1 のみ実施してください。

コードは必要がなければ変更せず、
確認結果を報告したところで停止してください。
```

CursorのStep 1結果を確認してからStep 2へ進む。

---

## 16. 開発進行ルール

BizSC共通ルール:

- 一度に大量変更しない
- 1Stepずつ進める
- ユーザー確認前に先へ進まない
- 既存コードを推測しない
- 必要ならGitHub最新コードを確認する
- 既存User CRUDを壊さない
- 不要なリファクタリングをしない
- 不要なDependencyを追加しない
- Docker Compose経由で確認する
- Commit / Pushは区切りのよいところだけ
- APIキーや秘密情報をチャットへ貼らない

---

## 17. GitHub状態についての注意

Phase 01の実装内容はローカルで確認・実行されている。

この引継ぎ資料作成時点では、Phase 01の最新変更がGitHub `main` へすべてPush済みかは最終確認していない。

次チャットでコード確認が必要な場合は、ローカルまたはGitHubの最新状態を確認してから判断すること。

---

## 18. 現在地点

```text
Phase 01
EDINET API 接続・書類一覧取得
→ 完了

Phase 02
過去10年・現在上場企業・csvFlag=1 書類棚卸し
→ md作成済み
→ 未着手
→ 次は Step 1
```

次に行うこと:

```text
02-edinet-document-inventory.md
Step 1 現状確認
```

以上。
