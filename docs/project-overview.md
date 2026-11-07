# BizSC Project Overview

更新日: 2026-11-07  
確認したGitHubソースのコミット（本更新前）: [`03dd928`](https://github.com/eswm223-oss/bizsc/commit/03dd9288d526cbc814696d5da4912121bd9dd4b5)

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

2026-09-26にJ-Quants中心へ切り替え。2026-11-05時点で以下の**Client / Model / Repository / Service / キャッシュ起動・管理API、およびFrontendの管理・一覧画面の実装**を確認した。

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
- Frontend: React / TypeScript / Vite / React Router / Axios / Mantine 9 / TanStack Table v9
- Docker Compose: frontend（5173）、backend（8000）、db（5432）
- Repository: <https://github.com/eswm223-oss/bizsc>
- Workspace: `D:\Development\apps\bizsc`

責務分離:

```text
Frontend → FastAPI Router → Service → Repository → PostgreSQL
                                  ↑
                     Batch / Cache Service → J-Quants Client → J-Quants API
```

### Frontend UIの現在地（2026-11-05）

- BootstrapからMantine 9へ移行。現行ルート（ホーム、ユーザーCRUD、J-Quantsデータ一覧、キャッシュ管理）は`MainLayoutMantine`配下。
- キャッシュ管理画面では管理一覧検索・状態表示、新規起動、詳細確認、未完了分の再実行、削除を操作できる。
- `/jquants/master`、`/jquants/dailyquote`、`/jquants/valuation`、`/jquants/summary`にデータ一覧を配置。
- TanStack QueryでAPI結果をキャッシュし、Mantine Notificationsで起動・削除結果を表示。旧`MainLayout.tsx`と`/test`ルートは削除済み。
- 利用者から2026-11-04のFrontendビルド成功報告あり。JSチャンク500 kB超の警告はあるがビルドエラーはなし。

## 4. J-Quantsキャッシュ機能の現在地

### 実装済み

- 4種類のDataset取得Client、APIキー・タイムアウト・HTTPエラー処理。
- SQLAlchemy Model、Alembicを使ったDB管理、Repository／Service。
- 主キーの生成と`merge`による同一レコード上書き。
- 財務APIの欠損値変換（空文字列→NULL相当）。
- 管理ID単位のキャッシュ起動: `POST /batches/jquants/cache/start`（HTTP 202）。
- 管理API: `GET /cachemgmt/list`、`GET /cachemgmt/{mgmt_id}`、`DELETE /cachemgmt/{mgmt_id}`。
- Reactのキャッシュ管理一覧・新規起動・詳細・削除画面、およびJ-Quantsの4種類のデータ一覧を実装。
- `cache_mgmt`テーブルに開始日・終了日・銘柄コード・Dataset別ステータス・remarksを保存。
- `Waiting`→`Running`→`Complete`／`Error`、ステータスに基づく再実行。
- 指定銘柄のみ、またはマスタ全銘柄を対象にキャッシュ処理。
- 最新の銘柄マスタ情報を取得し、古い情報で上書きしない制御。
- Dataset・銘柄単位のTransaction。APIのエラー本文`message`を例外として扱い、進捗管理の`remarks`へ保存する経路。
- 日足株価・バリュエーション・財務サマリー取得前に約1秒の間隔を置く処理。

### 実行上の留意点

APIの202応答は受付完了であってバッチ完了ではない。バックグラウンド処理はFastAPIのプロセス内で動く。バッチ本体にRunning/Completeの確認はあるが厳密なDB排他は未実装。停止・再起動・長時間実行時の復旧は必要に応じて検討する。実行中の管理レコード削除は許容する方針。

「実装済み」はGitHubソースに確認できるという意味であり、本資料作成時に全銘柄・全期間の統合テストを実施したものではない。

## 5. 現在までの開発進捗

| 領域 | 状態 | 補足 |
|---|---|---|
| Docker / FastAPI / DB / Reactの基盤 | 完了 | 基本起動環境 |
| User CRUD / React画面 | 完了 | サンプルのホーム・ユーザー画面をMantine化。一覧・検索・フィルタ・ソート・ページングを含む |
| Frontend UI基盤のMantine移行 | 完了（現行ルート） | J-Quants画面もMantineへ統合。旧レイアウト・`/test`を削除 |
| EDINET書類棚卸し | Legacyとして実装済み | 主データソースからは移行 |
| J-Quants API Client | 実装済み | 4 Dataset |
| J-Quantsデータ保存Model・Repository・Service | 実装済み | 銘柄・株価・Valuation・財務 |
| J-Quantsキャッシュ実行・管理APIと画面 | 実装済み | BackgroundTasks、cache_mgmt、管理一覧・新規・詳細・削除 |
| Screeningテーブルモデル・DBマイグレーション | 実装済み・DB適用報告あり | group / rule / result の3テーブル、Alembic `6f4a06038265`。CASCADE動作テストは未確認 |
| Screening指標計算・キャッシュ実行 | 未実装 | ルールに基づくスコア計算、刷新、状態遷移は今後実装 |
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

### 評価ルール方式（2026-11-07時点でDBモデル作成済み）

- 利用者が評価項目（`metric_code`）、条件（`params`）、加点・減点（`points`、整数）をルールごとに設定する方式。
- 評価項目ごとに条件の形が異なるため、`params`はPostgreSQLの`JSONB`で保持。指標コードとパラメータ型の対応・検証は今後のアプリケーション実装で扱う。
- `screening_group`は名称・キャッシュ状態・実行開始日時・最終キャッシュ日時を持ち、`screening_rule`はグループ配下のルールを保持。
- `screening_result`は**1銘柄 × 1ルール**ごとの計算結果を保持し、`group_id`で対象グループを絞り込み、銘柄別に`SUM(score)`してランキングする。結果はグループ単位で刷新する。
- グループ削除時はルール・結果を`ON DELETE CASCADE`で削除。結果側の`rule_id`は外部キー制約を設けず、ルール単体の編集・削除を許容する（再計算前の古い結果を最新として扱わない制御は今後実装）。
- 作成したDBモデル：`backend/app/models/screening_{group,rule,result}.py`。Alembic：`6f4a06038265_add_screening_cascade_delete.py`。利用者から`alembic upgrade head`成功の報告あり。削除連動とスコア集計の実動作は未検証。

## 7. 今後の開発ロードマップ

### 次の優先候補

1. **保存データの小範囲確認**: 1銘柄・短期間の登録、管理ステータス、欠損値、検索結果を確認。
2. **Screening指標の仕様確定**: `metric_code`とPydanticパラメータ型の対応、期間・比較基準・計算式、欠損値の扱いを決める。
3. **Screening Backend**: group/ruleのCRUD、ルール別採点、グループ単位のキャッシュ刷新・状態管理、合計スコア順の一覧APIを実装。
4. **Screening Frontend**: Mantineを標準UIとして、条件入力、結果一覧、銘柄詳細、チャートなどを小さく段階追加。TanStack Table v9は必要に応じて利用。
5. **運用改善**: 必要に応じて進捗画面の自動更新、定期取得、ジョブ中断・復旧を追加。厳密な排他は状況が限定的として現状保留。

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

**現在地（2026-11-07）**: J-Quantsキャッシュ処理・管理APIと画面、4種のデータ一覧、Mantine移行は実装済み。スクリーニングの3テーブルとAlembic適用まで完了報告あり。次は評価指標Registry・Pydanticによる条件検証、group/rule CRUD、スコア計算・結果キャッシュ刷新・一覧APIの実装。
