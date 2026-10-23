from datetime import date, timedelta

from app.clients.jquants import (
    fetch_bars_daily,
    fetch_listed_issues,
    fetch_summary,
    fetch_valuation,
)
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
                    date=date.fromisoformat(record["Date"]),
                    code=record["Code"],
                    record_name=record["CoName"],
                    record_name_en=record["CoNameEn"],
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
                    date=date.fromisoformat(record["Date"]),
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
                    date=date.fromisoformat(record["Date"]),
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
                    disclosure_date=date.fromisoformat(record["DiscDate"]),
                    disclosure_time=record["DiscTime"],
                    code=record["Code"],
                    disclosure_number=record["DiscNo"],
                    document_type=record["DocType"],
                    current_period_type=record["CurPerType"],
                    current_period_start=date.fromisoformat(record["CurPerSt"]),
                    current_period_end=date.fromisoformat(record["CurPerEn"]),
                    current_fiscal_year_start=date.fromisoformat(record["CurFYSt"]),
                    current_fiscal_year_end=date.fromisoformat(record["CurFYEn"]),
                    sales=record["Sales"],
                    operating_profit=record["OP"],
                    ordinary_profit=record["OdP"],
                    net_profit=record["NP"],
                    eps=record["EPS"],
                    diluted_eps=record["DEPS"],
                    total_assets=record["TA"],
                    equity=record["Eq"],
                    shareholders_equity=record["ShEq"],
                    equity_ratio=record["EqAR"],
                    bps=record["BPS"],
                    roe=record["ROE"],
                    cash_flow_operating=record["CFO"],
                    cash_flow_investing=record["CFI"],
                    cash_flow_financing=record["CFF"],
                    cash_and_equivalents=record["CashEq"],
                    dividend_annual=record["DivAnn"],
                    forecast_dividend_annual=record["FDivAnn"],
                    next_forecast_dividend_annual=record["NxFDivAnn"],
                    annual_payout_ratio=record["PayoutRatioAnn"],
                    forecast_annual_payout_ratio=record["FPayoutRatioAnn"],
                    shares_outstanding=record["ShOutFY"],
                    treasury_shares=record["TrShFY"],
                    average_shares=record["AvgSh"],
                    forecast_sales_2q=record["FSales2Q"],
                    forecast_operating_profit_2q=record["FOP2Q"],
                    forecast_ordinary_profit_2q=record["FOdP2Q"],
                    forecast_net_profit_2q=record["FNP2Q"],
                    forecast_eps_2q=record["FEPS2Q"],
                    forecast_sales=record["FSales"],
                    forecast_operating_profit=record["FOP"],
                    forecast_ordinary_profit=record["FOdP"],
                    forecast_net_profit=record["FNP"],
                    forecast_eps=record["FEPS"],
                    next_forecast_sales_2q=record["NxFSales2Q"],
                    next_forecast_operating_profit_2q=record["NxFOP2Q"],
                    next_forecast_ordinary_profit_2q=record["NxFOdP2Q"],
                    next_forecast_net_profit_2q=record["NxFNp2Q"],
                    next_forecast_eps_2q=record["NxFEPS2Q"],
                    next_forecast_sales=record["NxFSales"],
                    next_forecast_operating_profit=record["NxFOP"],
                    next_forecast_ordinary_profit=record["NxFOdP"],
                    next_forecast_net_profit=record["NxFNp"],
                    next_forecast_eps=record["NxFEPS"],
                )
                service.createOrUpdate(db, data)
