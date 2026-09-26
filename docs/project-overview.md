# BizSC Project Overview

更新日: 2026-09-26

## 1. Project Name

```text
BizSC
```

---

## 2. Project Purpose

BizSC は、日本株を対象とした個人用の株スクリーニング Web Application です。

目的:

```text
市場・企業データを取得
↓
PostgreSQL に Cache
↓
財務・株価指標を計算
↓
条件検索
↓
候補銘柄を発見
↓
銘柄比較・分析
```

主なスクリーニング例:

- 業績が伸びている
- 利益率が高い
- 財務健全性が高い
- PER / PBR 等が一定条件内
- 配当条件を満たす
- 52週高値から大きく下落
- 直近の株価上昇が限定的
- 業績と株価の乖離がある

---

## 3. Data Source Strategy

2026-09-26 にデータ取得方針を変更。

### Primary

```text
J-Quants API
```

J-Quants から取得したデータを BizSC の PostgreSQL に Cache し、Screening の基礎データとする。

優先 Dataset:

```text
上場銘柄
日足株価
財務情報 Summary
```

### EDINET

EDINET を主データソースにする方針は白紙化。

既存コード・Table はすぐには削除しないが、今後の Screening データ取得の中心にはしない。

### Other Sources

yfinance 等は、J-Quants で不足するデータが明確になった場合に補助ソースとして再検討する。
現時点で Core Architecture には含めない。

---

## 4. J-Quants Plan

契約プランは未確定。

候補:

```text
Light
Standard
その他必要に応じて検討
```

プランによって履歴期間・利用可能 Dataset 等が変わるため、実装開始時に最新公式仕様と契約内容を確認する。

Premium の詳細 BS / PL / CF を必須前提にはしない。
まず財務 Summary と日足株価で成立する Screening を作る。

---

## 5. Development Environment

```text
OS: Windows
Workspace: D:\Development\apps\bizsc
```

Tools:

- Cursor
- GitHub Desktop
- Docker Desktop
- Docker Compose
- TablePlus
- ChatGPT

GitHub:

```text
https://github.com/eswm223-oss/bizsc
```

---

## 6. Technology Stack

Backend:

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL 17
- psycopg
- Alembic
- Pydantic
- pydantic-settings
- pytest
- httpx

Frontend:

- React
- TypeScript
- Vite
- React Router
- Axios
- Bootstrap

Infrastructure:

- Docker Desktop
- Docker Compose

---

## 7. Overall Architecture

```text
J-Quants API
      ↓
Client
      ↓
Service
      ↓
Repository
      ↓
SQLAlchemy Model
      ↓
PostgreSQL
      ↓
Screening Logic
      ↓
FastAPI
      ↓
React
```

Layer responsibilities:

```text
Client      = External API
Service     = Business Logic / Transaction
Repository  = DB Access
Model       = DB Schema
Router      = HTTP API
```

---

## 8. Main Domains

現在:

```text
User
J-Quants（これから実装）
EDINET Legacy
```

将来:

```text
Listed Issues
Market Prices
Financials
Screening
Watchlist
Analysis
```

---

## 9. User Domain

実装済み:

```text
users
```

API:

```text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

Frontend:

- UserListPage
- UserCreatePage
- UserDetailPage
- UserEditPage

Search / Filter / Sort / Pagination まで実装済み。

---

## 10. J-Quants Planned Data Flow

```text
J-Quants API
↓
Response Validation
↓
Normalization
↓
PostgreSQL Cache
↓
Derived Metrics
↓
Screening
```

想定 DB Domain:

```text
Listed Issues
Daily Quotes
Financial Summary
Sync Runs
```

実 Table / Column は実 Response を確認してから確定する。

---

## 11. Listed Issues

目的:

```text
BizSC の対象銘柄 Master
```

保持候補:

- 証券コード
- 会社名
- 市場区分
- 業種
- その他 Screening に必要な銘柄属性

証券コードは `str` で扱う。

---

## 12. Daily Quotes

目的:

```text
株価 Screening と Chart の基礎
```

保持候補:

- Date
- Code
- Open
- High
- Low
- Close
- Volume
- 調整済み値 / 調整係数等、利用 API で必要な項目

ここから計算:

```text
最新株価
52週高値
52週安値
52週高値からの下落率
1M / 3M / 6M / 1Y 騰落率
出来高指標
```

---

## 13. Financial Summary

目的:

```text
企業横断 Screening 用の財務データ
```

主な利用候補:

- 売上高
- 営業利益
- 経常利益
- 純利益
- EPS
- BPS
- 総資産
- 純資産
- 自己資本比率
- 営業 CF
- 投資 CF
- 財務 CF
- 業績予想
- 配当関連で利用可能な Summary 項目

ここから計算:

```text
成長率
利益率
ROE
ROA
FCF
PER
PBR
時価総額
```

実際に利用可能な項目は J-Quants の契約プランと最新 API Response を確認して確定する。

---

## 14. Screening Design

API Data と Derived Metric を分離する。

例:

```text
J-Quants
Close
EPS
BPS
NetSales
OperatingProfit
...

BizSC Calculated
PER
PBR
ROE
SalesGrowth
OperatingMargin
52WeekDrawdown
...
```

将来的に条件を組み合わせる。

```text
売上成長率 >= X
AND
営業利益率 >= Y
AND
自己資本比率 >= Z
AND
52週高値からの下落率 >= N
```

---

## 15. Data Cache Policy

毎画面表示で外部 API を直接呼ばない。

```text
External API
↓
Batch / Service
↓
PostgreSQL
↓
BizSC API
↓
Frontend
```

通常運用:

```text
過去データ初期投入
↓
日次 / 決算更新分を追加
↓
必要時に指定期間 Refresh
```

履歴年数は J-Quants プラン確定後に決める。

---

## 16. EDINET Legacy

これまで実装済み:

- EDINET Client
- 上場企業判定
- Document Inventory
- PostgreSQL 保存
- 1日 Refresh
- 複数日 Refresh
- CLI Batch
- Unit Test
- 1か月実データ処理

最終実測:

```text
2026-07-01 ～ 2026-07-31

run_days       = 31
completed_days = 31
failed_days    = 0
document_count = 1848
```

今後は:

```text
EDINET CSV解析
XBRL解析
EDINET財務DB
```

へ進まない。

既存コード / Table は、J-Quants 移行が安定するまでは残す。

---

## 17. Frontend Direction

将来の主要画面:

```text
銘柄一覧
Screening
Screening Results
銘柄詳細
株価 Chart
財務 Chart
銘柄比較
Watchlist
```

まず Backend の J-Quants Cache 基盤を優先する。

---

## 18. Development Policy

```text
Small Step
↓
Implementation
↓
Unit Test
↓
Small Real API Test
↓
DB Verification
↓
Next Step
```

- 大量取得から始めない
- API Secret を漏らさない
- Error を推測で決めつけない
- DB Migration を確認してから適用
- Client / Service / Repository を分離
- 不要な Infrastructure を増やさない
- GitHub 最新コードを基準にする

---

## 19. Current Project Status

```text
BizSC
│
├─ Web Application 基盤
│  └─ 完了
│
├─ User CRUD / Frontend
│  └─ 完了
│
├─ EDINET
│  ├─ Inventory / Batch
│  │  └─ 動作確認済み
│  └─ 今後の主開発
│     └─ 停止
│
└─ J-Quants
   ├─ 採用決定
   ├─ Client
   │  └─ 未実装
   ├─ DB Cache
   │  └─ 未実装
   ├─ Daily Quotes
   │  └─ 未実装
   ├─ Financial Summary
   │  └─ 未実装
   └─ Screening
      └─ 未実装
```

---

## 20. Next Phase

```text
J-Quants Phase 01
```

開始順:

```text
Step JQ-1
契約プラン / 認証 / Dataset / 取得期間の確認

Step JQ-2
J-Quants Client

Step JQ-3
上場銘柄 Master DB

Step JQ-4
日足株価 DB

Step JQ-5
財務 Summary DB

Step JQ-6
Screening 指標
```

EDINET の続きではなく、J-Quants Phase 01 から再開する。

---

## 21. Documentation

```text
architecture.md
→ 現在の構成・設計原則

handover_phase.md
→ 進捗・次 Step

project-overview.md
→ Project の目的・全体像
```

以上。
