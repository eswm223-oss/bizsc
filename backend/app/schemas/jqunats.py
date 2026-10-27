from datetime import date, datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
)


class SearchRequest(BaseModel):
    keyword: str | None
    dateFrom: date | None
    dateTo: date | None


class MasterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    code: str
    company_name: str
    company_name_en: str | None
    sector17_code: str | None
    sector17_name: str | None
    sector33_code: str | None
    sector33_name: str | None
    scale_category: str | None
    market_code: str | None
    market_name: str | None
    margin_code: str | None
    margin_name: str | None
    product_category: str | None
    created_at: datetime
    updated_at: datetime


class MasterListResponse(BaseModel):
    data: list[MasterResponse]
    total: int


class DailyQuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    code: str
    open: Decimal | None
    high: Decimal | None
    low: Decimal | None
    close: Decimal | None
    upper_limit: str | None
    lower_limit: str | None
    volume: Decimal | None
    value: Decimal | None
    adjustment_factor: Decimal | None
    adjusted_open: Decimal | None
    adjusted_high: Decimal | None
    adjusted_low: Decimal | None
    adjusted_close: Decimal | None
    adjusted_volume: Decimal | None
    ex_rights_type: str | None
    created_at: datetime
    updated_at: datetime


class DailyQuoteListResponse(BaseModel):
    data: list[DailyQuoteResponse]
    total: int


class ValuationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    code: str
    eps: Decimal | None
    forward_eps: Decimal | None
    bps: Decimal | None
    roe: Decimal | None
    forward_roe: Decimal | None
    per: Decimal | None
    forward_per: Decimal | None
    pbr: Decimal | None
    market_cap: Decimal | None
    created_at: datetime
    updated_at: datetime


class ValuationListResponse(BaseModel):
    data: list[ValuationResponse]
    total: int


class SummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    disclosure_date: date
    disclosure_time: str | None
    code: str
    disclosure_number: str
    document_type: str | None
    current_period_type: str | None
    current_period_start: date | None
    current_period_end: date | None
    current_fiscal_year_start: date | None
    current_fiscal_year_end: date | None
    sales: Decimal | None
    operating_profit: Decimal | None
    ordinary_profit: Decimal | None
    net_profit: Decimal | None
    eps: Decimal | None
    diluted_eps: Decimal | None
    total_assets: Decimal | None
    equity: Decimal | None
    shareholders_equity: Decimal | None
    equity_ratio: Decimal | None
    bps: Decimal | None
    roe: Decimal | None
    cash_flow_operating: Decimal | None
    cash_flow_investing: Decimal | None
    cash_flow_financing: Decimal | None
    cash_and_equivalents: Decimal | None
    dividend_annual: Decimal | None
    forecast_dividend_annual: Decimal | None
    next_forecast_dividend_annual: Decimal | None
    annual_payout_ratio: Decimal | None
    forecast_annual_payout_ratio: Decimal | None
    shares_outstanding: Decimal | None
    treasury_shares: Decimal | None
    average_shares: Decimal | None
    forecast_sales_2q: Decimal | None
    forecast_operating_profit_2q: Decimal | None
    forecast_ordinary_profit_2q: Decimal | None
    forecast_net_profit_2q: Decimal | None
    forecast_eps_2q: Decimal | None
    forecast_sales: Decimal | None
    forecast_operating_profit: Decimal | None
    forecast_ordinary_profit: Decimal | None
    forecast_net_profit: Decimal | None
    forecast_eps: Decimal | None
    next_forecast_sales_2q: Decimal | None
    next_forecast_operating_profit_2q: Decimal | None
    next_forecast_ordinary_profit_2q: Decimal | None
    next_forecast_net_profit_2q: Decimal | None
    next_forecast_eps_2q: Decimal | None
    next_forecast_sales: Decimal | None
    next_forecast_operating_profit: Decimal | None
    next_forecast_ordinary_profit: Decimal | None
    next_forecast_net_profit: Decimal | None
    next_forecast_eps: Decimal | None
    created_at: datetime
    updated_at: datetime


class SummaryListResponse(BaseModel):
    data: list[SummaryResponse]
    total: int
