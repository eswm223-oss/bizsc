# BizSC Project Overview

更新日: 2026-10-25  
確認したGitHubコミット: [`jquants_chche_process_fix_4`](https://github.com/eswm223-oss/bizsc/commit/1a4f7a9d6804daf8d56340f1c1c5a8d0eb1747ca)

## 1. プロジェクトの目的

**BizSC** は、日本株を対象とした個人用の株式スクリーニングWebアプリです。株価・企業情報・財務指標をDBに蓄積し、投資候補を条件検索・比較できるようにすることを目指します。

特に重視する利用場面:

- 業績が良い、または改善しているのに、株価が下落・横ばいの企業を探す。
- 直近の高値から30％以上下落した銘柄を抽出する。
- 52週高値・安値、短中期の騰落率、出来高を条件にする。
- PER、PBR、時価総額、配当利回り、売上・利益成長率等を組み合わせる。
- 値を多く保存すること自体を目的とせず、スクリーニングで使う情報を選別する。

```text
データ収集（J-Quants）
      ↓
PostgreSQLキャッシュ
      ↓
財務・株価スクリーニング指標の計算
      ↓
条件検索・ランキング・比較
      ↓
Reactによる銘柄分析画面
```

## 2. 主データソースと方針

### J-Quants（現在の主データソース）

2026-09-26にJ-Quants中心へ切り替え。2026-10-25時点で以下の**Client / Model / Repository / Service / キャッシュ起動APIの実装**を確認した。

| Dataset | 主な用途 | DBテーブル |
|---|---|---|
| 上場銘柄マスタ | 企業名、証券コード、市場・業種、検索対象 | `jq_listed_issues` |
| 日足株価 | 最新株価、四本値、出来高、52週高値・安値の計算元 | `jq_daily_quotes` |
| バリュエーション | PER/PBR、EPS/BPS、時価総額等 | `jq_valuations` |
| 財務サマリー | 売上、利益、CF、予想・配当等の取得可能項目 | `jq_financial_summaries` |
| キャッシュ管理 | 起動条件・実行状況・エラー記録 | `cache_mgmt` |

財務データは必要項目を正規化して保存する。今後不足する項目が明確になったときに追加を検討する。過去データはDBに再利用可能な形で保持する。

### EDINET（Legacy）

EDINET API連携、現在上場企業判定、書類棚卸し、PostgreSQLへの保存、日付範囲Refresh、CLIバッチを実装・検証した履歴は残す。EDINETのCSV/XBRLからスクリーニング用財務データを独自解析する計画は停止。既存コードとテーブルは当面維持する。

## 3. 実行環境

- 開発環境: Windows、Cursor、GitHub Desktop、Docker Desktop、TablePlus
- Backend: Python 3.12 / FastAPI / SQLAlchemy / Pydantic / httpx / Alembic
- DB: PostgreSQL 17
- Frontend: React / TypeScript / Vite / React Router / Axios / Bootstrap
- Docker Compose: frontend（5173）、backend（8000）、db（5432）
- Repository: <https://github.com/eswm223-oss/bizsc>
- Workspace: `D:\Development\apps\bizsc`

責務分離:

```text
Frontend → FastAPI Router → Service → Repository → PostgreSQL
                                  ↑
                     Batch / Cache Service → J-Quants Client → J-Quants API
```

## 4. J-Quantsキャッシュ機能の現在地

### 実装済み

- 4種類のDataset取得Client、APIキー・タイムアウト・HTTPエラー処理。
- SQLAlchemy Model、Alembicを使ったDB管理、Repository／Service。
- 主キーの生成と`merge`による同一レコード上書き。
- 財務APIの欠損値変換（空文字列→NULL相当）。
- 管理ID単位のキャッシュ起動: `POST /batches/jquants/cache/plain`（HTTP 202）。
- `cache_mgmt`テーブルに開始日・終了日・銘柄コード・Dataset別ステータス・remarksを保存。
- `Waiting`→`Running`→`Complete`／`Error`、ステータスに基づく再実行。
- 指定銘柄のみ、またはマスタ全銘柄を対象にキャッシュ処理。
- 最新の銘柄マスタ情報を取得し、古い情報で上書きしない制御。
- Dataset・銘柄単位のTransaction。APIのエラー本文`message`を例外として扱い、進捗管理の`remarks`へ保存する経路。
- 日足株価・バリュエーション・財務サマリー取得前に約1秒の間隔を置く処理。

### 実行上の留意点

APIの202応答は受付完了であってバッチ完了ではない。バックグラウンド処理はFastAPIのプロセス内で動くため、停止・再起動・長時間実行時の運用設計は将来検討する。

「実装済み」はGitHubソースに確認できるという意味であり、本資料作成時に全銘柄・全期間の統合テストを実施したものではない。

## 5. 現在までの開発進捗

| 領域 | 状態 | 補足 |
|---|---|---|
| Docker / FastAPI / DB / Reactの基盤 | 完了 | 基本起動環境 |
| User CRUD / React画面 | 完了 | 一覧・検索・フィルタ・ソート・ページングを含む |
| EDINET書類棚卸し | Legacyとして実装済み | 主データソースからは移行 |
| J-Quants API Client | 実装済み | 4 Dataset |
| J-Quantsデータ保存Model・Repository・Service | 実装済み | 銘柄・株価・Valuation・財務 |
| J-Quantsキャッシュ実行API・状態管理 | 実装済み | BackgroundTasks、cache_mgmt |
| Screening指標計算 | 今後の実装 | 定義と優先順位の整理が次の候補 |
| Screening条件検索API・画面 | 今後の実装 | キャッシュしたデータを利用 |
| 日次自動Scheduler / 外部ワーカー | 未導入 | 必要性を見て検討 |

## 6. Screeningの今後の機能要件

### 株価から計算・判定するもの

- 最新の終値または基準日時点の株価
- 1か月・3か月・6か月・1年の騰落率
- 52週高値／安値
- 52週高値からの下落率（例: 30％以上）
- 出来高の変化・売買代金

### 財務・バリュエーションから判断するもの

- 売上高、営業利益、経常利益、当期純利益
- 売上・利益の前年同期比・成長率
- 利益率、自己資本比率、キャッシュフロー
- EPS / BPS / PER / PBR / 時価総額 / 配当関連データ

### 核となるスクリーニング像

```text
売上・利益の改善
AND
株価の上昇が限定的 または 52週高値から大きく下落
AND
必要に応じて Valuation / 配当 / 財務健全性 の条件
↓
投資候補銘柄一覧
```

APIに含まれる指標とBizSC側で計算する派生値を分けて設計する。

## 7. 今後の開発ロードマップ

### 次の優先候補

1. **保存データの小範囲確認**: 1銘柄・短期間の登録、管理ステータス、欠損値、検索結果を確認。
2. **Screening指標の仕様確定**: 指標・期間・比較基準・計算式、対象データが不足する場合の扱いを決める。
3. **Screening Backend**: 複数テーブルの連結、条件検索、ソート、ページングを実装。
4. **Screening Frontend**: 条件入力、結果一覧、銘柄詳細、チャートなどを小さく段階追加。
5. **運用改善**: 必要に応じて進捗参照API、定期取得、ジョブ排他・中断処理などを追加。

### 意図的に保留する項目

- J-Quants Clientのページネーション自動取得。Postmanでの取得確認を受け、現時点では追加しない。
- 同一秒に発生するキャッシュ管理ID重複への対策。発生状況が限定的との判断。
- 上場廃止銘柄の整理方法。今後必要になった段階で判断。
- EDINETベースの独自財務解析の再開。

## 8. 開発・ドキュメント運用

- 一度に広い変更を加えず、Stepごとに設計・実装・確認する。
- コードに関するレビューや変更ではGitHubの最新コミットを確認し、古い資料だけを根拠にしない。
- 実装済み・検証済み・未実装・保留を明確に分ける。
- APIキーや`.env`に含まれる秘密情報をGitHubへ公開しない。
- SQLAlchemy Modelの変更はAlembic revisionを確認してから適用する。
- Commit / Pushは適切な区切りで行う。

主なドキュメント:

```text
docs/architecture.md        # 現在の構成と実装上の決定
docs/handover_phase.md      # 具体的な進捗、次回の着手点
docs/project-overview.md    # プロジェクトの目的とロードマップ
```

---

**現在地（2026-10-25）**: J-Quantsデータのキャッシュ処理を実装。次の主題は、キャッシュ済み株価・財務データを活用するスクリーニング機能の設計・実装。
