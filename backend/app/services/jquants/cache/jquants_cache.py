from datetime import date, timedelta

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
from app.repositories.daily_quote import JQuantsDailyQuoteRepository
from app.repositories.equities_master import JQuantsListedIssueRepository
from app.repositories.financial_summary import JQuantsFinancialSummaryRepository
from app.repositories.valuation import JQuantsValuationRepository
from app.services.jquants.db.daily_quote import daily_quote_service
from app.services.jquants.db.equities_master import equities_master_service
from app.services.jquants.db.financial_summary import financial_summary_service
from app.services.jquants.db.valuation import valuation_service

# ==================================
# JQuantsデータキャッシュ処理
# ==================================

to_date = cmm_string.to_date
to_decimal = cmm_number.to_decimal


# --------------------------------------------------
# 上場銘柄一覧
# --------------------------------------------------
def equities_master_cache(fromDate: date, toDate: date, code: str = ""):

    service = equities_master_service(JQuantsListedIssueRepository())
    for i in range((toDate - fromDate).days + 1):
        current_date = fromDate + timedelta(days=i)

        # APIから取得
        result = fetch_listed_issues(current_date, code)

        # DBにキャッシュ
        with SessionLocal.begin() as db:
            for record in result["data"]:
                data = JQuantsListedIssue(
                    date=to_date(record["Date"]),
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
def daily_quote_cache(fromDate: date, toDate: date, code: str = ""):

    service = daily_quote_service(JQuantsDailyQuoteRepository())
    for i in range((toDate - fromDate).days + 1):
        current_date = fromDate + timedelta(days=i)

        # APIから取得
        result = fetch_bars_daily(current_date, code)

        # DBにキャッシュ
        with SessionLocal.begin() as db:
            for record in result["data"]:
                data = JQuantsDailyQuote(
                    date=to_date(record["Date"]),
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
def valuation_cache(fromDate: date, toDate: date, code: str = ""):

    service = valuation_service(JQuantsValuationRepository())
    for i in range((toDate - fromDate).days + 1):
        current_date = fromDate + timedelta(days=i)

        # APIから取得
        result = fetch_valuation(current_date, code)

        # DBにキャッシュ
        with SessionLocal.begin() as db:
            for record in result["data"]:
                data = JQuantsValuation(
                    date=to_date(record["Date"]),
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
def summary_cache(fromDate: date, toDate: date, code: str = ""):

    service = financial_summary_service(JQuantsFinancialSummaryRepository())
    for i in range((toDate - fromDate).days + 1):
        current_date = fromDate + timedelta(days=i)

        # APIから取得
        result = fetch_summary(current_date, code)

        # DBにキャッシュ
        with SessionLocal.begin() as db:
            for record in result["data"]:
                data = JQuantsFinancialSummary(
                    disclosure_date=to_date(record["DiscDate"]),
                    disclosure_time=record["DiscTime"],
                    code=record["Code"],
                    disclosure_number=record["DiscNo"],
                    document_type=record["DocType"],
                    current_period_type=record["CurPerType"],
                    current_period_start=to_date(record["CurPerSt"]),
                    current_period_end=to_date(record["CurPerEn"]),
                    current_fiscal_year_start=to_date(record["CurFYSt"]),
                    current_fiscal_year_end=to_date(record["CurFYEn"]),
                    sales=to_decimal(record["Sales"]),
                    operating_profit=to_decimal(record["OP"]),
                    ordinary_profit=to_decimal(record["OdP"]),
                    net_profit=to_decimal(record["NP"]),
                    eps=to_decimal(record["EPS"]),
                    diluted_eps=to_decimal(record["DEPS"]),
                    total_assets=to_decimal(record["TA"]),
                    equity=to_decimal(record["Eq"]),
                    shareholders_equity=to_decimal(record["ShEq"]),
                    equity_ratio=to_decimal(record["EqAR"]),
                    bps=to_decimal(record["BPS"]),
                    roe=to_decimal(record["ROE"]),
                    cash_flow_operating=to_decimal(record["CFO"]),
                    cash_flow_investing=to_decimal(record["CFI"]),
                    cash_flow_financing=to_decimal(record["CFF"]),
                    cash_and_equivalents=to_decimal(record["CashEq"]),
                    dividend_annual=to_decimal(record["DivAnn"]),
                    forecast_dividend_annual=to_decimal(record["FDivAnn"]),
                    next_forecast_dividend_annual=to_decimal(record["NxFDivAnn"]),
                    annual_payout_ratio=to_decimal(record["PayoutRatioAnn"]),
                    forecast_annual_payout_ratio=to_decimal(record["FPayoutRatioAnn"]),
                    shares_outstanding=to_decimal(record["ShOutFY"]),
                    treasury_shares=to_decimal(record["TrShFY"]),
                    average_shares=to_decimal(record["AvgSh"]),
                    forecast_sales_2q=to_decimal(record["FSales2Q"]),
                    forecast_operating_profit_2q=to_decimal(record["FOP2Q"]),
                    forecast_ordinary_profit_2q=to_decimal(record["FOdP2Q"]),
                    forecast_net_profit_2q=to_decimal(record["FNP2Q"]),
                    forecast_eps_2q=to_decimal(record["FEPS2Q"]),
                    forecast_sales=to_decimal(record["FSales"]),
                    forecast_operating_profit=to_decimal(record["FOP"]),
                    forecast_ordinary_profit=to_decimal(record["FOdP"]),
                    forecast_net_profit=to_decimal(record["FNP"]),
                    forecast_eps=to_decimal(record["FEPS"]),
                    next_forecast_sales_2q=to_decimal(record["NxFSales2Q"]),
                    next_forecast_operating_profit_2q=to_decimal(record["NxFOP2Q"]),
                    next_forecast_ordinary_profit_2q=to_decimal(record["NxFOdP2Q"]),
                    next_forecast_net_profit_2q=to_decimal(record["NxFNp2Q"]),
                    next_forecast_eps_2q=to_decimal(record["NxFEPS2Q"]),
                    next_forecast_sales=to_decimal(record["NxFSales"]),
                    next_forecast_operating_profit=to_decimal(record["NxFOP"]),
                    next_forecast_ordinary_profit=to_decimal(record["NxFOdP"]),
                    next_forecast_net_profit=to_decimal(record["NxFNp"]),
                    next_forecast_eps=to_decimal(record["NxFEPS"]),
                )
                service.createOrUpdate(db, data)
