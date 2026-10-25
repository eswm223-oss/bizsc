from datetime import date
from typing import Literal, TypedDict

from app.clients.jquants import (
    fetch_bars_daily,
    fetch_listed_issues,
    fetch_summary,
    fetch_valuation,
)
from app.common import cmm_number, cmm_string
from app.db.database import SessionLocal
from app.models import JQuantsListedIssue
from app.models.jquants_daily_quote import JQuantsDailyQuote
from app.models.jquants_financial_summary import JQuantsFinancialSummary
from app.models.jquants_valuation import JQuantsValuation
from app.repositories.cache_mgmt import CacheMgmtRepository
from app.repositories.daily_quote import JQuantsDailyQuoteRepository
from app.repositories.equities_master import JQuantsListedIssueRepository
from app.repositories.financial_summary import JQuantsFinancialSummaryRepository
from app.repositories.valuation import JQuantsValuationRepository
from app.services.jquants.db.cache_manage import (
    ITEM_LITERAL,
    CacheMgmtService,
)
from app.services.jquants.db.daily_quote import Daily_quote_service
from app.services.jquants.db.equities_master import Equities_master_service
from app.services.jquants.db.financial_summary import Financial_summary_service
from app.services.jquants.db.valuation import Valuation_service

# ==================================
# JQuantsデータキャッシュ処理
# ==================================

TO_DATE = cmm_string.to_date
TO_DECIMAL = cmm_number.to_decimal


class Response(TypedDict):
    status: Literal["success", "error"]
    message: str


# --------------------------------------------------
# JQuantsキャッシュ
# --------------------------------------------------
def jquants_cache(mgmtId: str) -> Response:

    progress: ITEM_LITERAL = "other"
    with SessionLocal() as db:
        # ステータス準備
        mgmtSearvice = CacheMgmtService(CacheMgmtRepository())
        management = mgmtSearvice.getById(db, mgmtId)

        if management is None:
            return {
                "status": "error",
                "message": "キャッシュ処理の準備に失敗しました。",
            }

        # キャッシュ処理　開始
        try:
            # 上場銘柄一覧　更新
            if management.status_master == "Waiting":
                progress = "master"
                management = mgmtSearvice.setStatus(
                    db, management.id, progress, "Running"
                )
                _equities_master_cache(management.company_code)
                management = mgmtSearvice.setStatus(
                    db, management.id, progress, "Complete"
                )

            # 上場銘柄一覧　取得
            jquantsSearvice = Equities_master_service(JQuantsListedIssueRepository())
            if management.company_code:
                company = jquantsSearvice.getByCode(db, management.company_code)
                masterList = [company] if company is not None else []
            else:
                masterList = jquantsSearvice.getAll(db)
            if not masterList:
                return {
                    "status": "error",
                    "message": "会社情報を取得できませんでした。",
                }

            # 株価四本値　更新
            if management.status_dailyBar in ["Waiting", "Running", "Error"]:
                progress = "dailyBar"
                management = mgmtSearvice.setStatus(
                    db, management.id, progress, "Running"
                )
                for company in masterList:
                    _daily_quote_cache(
                        company.code, management.from_date, management.to_date
                    )
                management = mgmtSearvice.setStatus(
                    db, management.id, progress, "Complete"
                )

            # バリュエーション指標　更新
            if management.status_valuation in ["Waiting", "Running", "Error"]:
                progress = "valuation"
                management = mgmtSearvice.setStatus(
                    db, management.id, progress, "Running"
                )
                for company in masterList:
                    _valuation_cache(
                        company.code, management.from_date, management.to_date
                    )
                management = mgmtSearvice.setStatus(
                    db, management.id, progress, "Complete"
                )

            # 財務情報　更新
            if management.status_summary in ["Waiting", "Running", "Error"]:
                progress = "summary"
                management = mgmtSearvice.setStatus(
                    db, management.id, progress, "Running"
                )
                for company in masterList:
                    _summary_cache(
                        company.code, management.from_date, management.to_date
                    )
                management = mgmtSearvice.setStatus(
                    db, management.id, progress, "Complete"
                )

        except Exception as e:  # noqa: BLE001
            management = mgmtSearvice.setStatus(
                db, management.id, progress, "Error", str(e)
            )
            return {"status": "error", "message": str(e)}

    return {"status": "success", "message": ""}


# --------------------------------------------------
# 上場銘柄一覧
# --------------------------------------------------
def _equities_master_cache(code: str | None = "") -> None:

    service = Equities_master_service(JQuantsListedIssueRepository())

    # APIから取得
    result = fetch_listed_issues(None, code)

    # DBにキャッシュ
    with SessionLocal.begin() as db:
        for record in result["data"]:
            data = JQuantsListedIssue(
                date=TO_DATE(record["Date"]),
                code=record["Code"],
                company_name=record["CoName"],
                company_name_en=record["CoNameEn"],
                sector17_code=record["S17"],
                sector17_name=record["S17Nm"],
                sector33_code=record["S33"],
                sector33_name=record["S33Nm"],
                scale_category=record["ScaleCat"],
                market_code=record["Mkt"],
                market_name=record["MktNm"],
                margin_code=record["Mrgn"],
                margin_name=record["MrgnNm"],
                product_category=record["ProdCat"],
            )
            service.createOrUpdate(db, data)


# --------------------------------------------------
# 株価四本値
# --------------------------------------------------
def _daily_quote_cache(code: str, fromDate: date | None, toDate: date | None) -> None:

    service = Daily_quote_service(JQuantsDailyQuoteRepository())

    # APIから取得
    result = fetch_bars_daily(code, fromDate, toDate)

    # DBにキャッシュ
    with SessionLocal.begin() as db:
        for record in result["data"]:
            data = JQuantsDailyQuote(
                date=TO_DATE(record["Date"]),
                code=record["Code"],
                open=record["O"],
                high=record["H"],
                low=record["L"],
                close=record["C"],
                upper_limit=record["UL"],
                lower_limit=record["LL"],
                volume=record["Vo"],
                value=record["Va"],
                adjustment_factor=record["AdjFactor"],
                adjusted_open=record["AdjO"],
                adjusted_high=record["AdjH"],
                adjusted_low=record["AdjL"],
                adjusted_close=record["AdjC"],
                adjusted_volume=record["AdjVo"],
                ex_rights_type=record["ExRT"],
            )
            service.createOrUpdate(db, data)


# --------------------------------------------------
# バリュエーション指標
# --------------------------------------------------
def _valuation_cache(code: str, fromDate: date | None, toDate: date | None) -> None:

    service = Valuation_service(JQuantsValuationRepository())

    # APIから取得
    result = fetch_valuation(code, fromDate, toDate)

    # DBにキャッシュ
    with SessionLocal.begin() as db:
        for record in result["data"]:
            data = JQuantsValuation(
                date=TO_DATE(record["Date"]),
                code=record["Code"],
                eps=record["EPS"],
                forward_eps=record["FwdEPS"],
                bps=record["BPS"],
                roe=record["ROE"],
                forward_roe=record["FwdROE"],
                per=record["PER"],
                forward_per=record["FwdPER"],
                pbr=record["PBR"],
                market_cap=record["MktCap"],
            )
            service.createOrUpdate(db, data)


# --------------------------------------------------
# 財務情報
# --------------------------------------------------
def _summary_cache(code: str, fromDate: date | None, toDate: date | None) -> None:

    service = Financial_summary_service(JQuantsFinancialSummaryRepository())

    # APIから取得
    result = fetch_summary(code, fromDate, toDate)

    # DBにキャッシュ
    with SessionLocal.begin() as db:
        for record in result["data"]:
            data = JQuantsFinancialSummary(
                disclosure_date=TO_DATE(record["DiscDate"]),
                disclosure_time=record["DiscTime"],
                code=record["Code"],
                disclosure_number=record["DiscNo"],
                document_type=record["DocType"],
                current_period_type=record["CurPerType"],
                current_period_start=TO_DATE(record["CurPerSt"]),
                current_period_end=TO_DATE(record["CurPerEn"]),
                current_fiscal_year_start=TO_DATE(record["CurFYSt"]),
                current_fiscal_year_end=TO_DATE(record["CurFYEn"]),
                sales=TO_DECIMAL(record["Sales"]),
                operating_profit=TO_DECIMAL(record["OP"]),
                ordinary_profit=TO_DECIMAL(record["OdP"]),
                net_profit=TO_DECIMAL(record["NP"]),
                eps=TO_DECIMAL(record["EPS"]),
                diluted_eps=TO_DECIMAL(record["DEPS"]),
                total_assets=TO_DECIMAL(record["TA"]),
                equity=TO_DECIMAL(record["Eq"]),
                shareholders_equity=TO_DECIMAL(record["ShEq"]),
                equity_ratio=TO_DECIMAL(record["EqAR"]),
                bps=TO_DECIMAL(record["BPS"]),
                roe=TO_DECIMAL(record["ROE"]),
                cash_flow_operating=TO_DECIMAL(record["CFO"]),
                cash_flow_investing=TO_DECIMAL(record["CFI"]),
                cash_flow_financing=TO_DECIMAL(record["CFF"]),
                cash_and_equivalents=TO_DECIMAL(record["CashEq"]),
                dividend_annual=TO_DECIMAL(record["DivAnn"]),
                forecast_dividend_annual=TO_DECIMAL(record["FDivAnn"]),
                next_forecast_dividend_annual=TO_DECIMAL(record["NxFDivAnn"]),
                annual_payout_ratio=TO_DECIMAL(record["PayoutRatioAnn"]),
                forecast_annual_payout_ratio=TO_DECIMAL(record["FPayoutRatioAnn"]),
                shares_outstanding=TO_DECIMAL(record["ShOutFY"]),
                treasury_shares=TO_DECIMAL(record["TrShFY"]),
                average_shares=TO_DECIMAL(record["AvgSh"]),
                forecast_sales_2q=TO_DECIMAL(record["FSales2Q"]),
                forecast_operating_profit_2q=TO_DECIMAL(record["FOP2Q"]),
                forecast_ordinary_profit_2q=TO_DECIMAL(record["FOdP2Q"]),
                forecast_net_profit_2q=TO_DECIMAL(record["FNP2Q"]),
                forecast_eps_2q=TO_DECIMAL(record["FEPS2Q"]),
                forecast_sales=TO_DECIMAL(record["FSales"]),
                forecast_operating_profit=TO_DECIMAL(record["FOP"]),
                forecast_ordinary_profit=TO_DECIMAL(record["FOdP"]),
                forecast_net_profit=TO_DECIMAL(record["FNP"]),
                forecast_eps=TO_DECIMAL(record["FEPS"]),
                next_forecast_sales_2q=TO_DECIMAL(record["NxFSales2Q"]),
                next_forecast_operating_profit_2q=TO_DECIMAL(record["NxFOP2Q"]),
                next_forecast_ordinary_profit_2q=TO_DECIMAL(record["NxFOdP2Q"]),
                next_forecast_net_profit_2q=TO_DECIMAL(record["NxFNp2Q"]),
                next_forecast_eps_2q=TO_DECIMAL(record["NxFEPS2Q"]),
                next_forecast_sales=TO_DECIMAL(record["NxFSales"]),
                next_forecast_operating_profit=TO_DECIMAL(record["NxFOP"]),
                next_forecast_ordinary_profit=TO_DECIMAL(record["NxFOdP"]),
                next_forecast_net_profit=TO_DECIMAL(record["NxFNp"]),
                next_forecast_eps=TO_DECIMAL(record["NxFEPS"]),
            )
            service.createOrUpdate(db, data)
