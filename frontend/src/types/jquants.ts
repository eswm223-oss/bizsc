import Decimal from "decimal.js";

export type Master = {
  date: Date | undefined;
  code: string | undefined;
  company_name: string | undefined;
  company_name_en: string | undefined;
  sector17_code: string | undefined;
  sector17_name: string | undefined;
  sector33_code: string | undefined;
  sector33_name: string | undefined;
  scale_category: string | undefined;
  market_code: string | undefined;
  market_name: string | undefined;
  margin_code: string | undefined;
  margin_name: string | undefined;
  product_category: string | undefined;
  created_at: Date;
  updated_at: Date;
};

export type MasterListRsponse = {
  data: Master[];
  total: number;
};

export type DailyQuote = {
  date: Date;
  code: string;
  open: Decimal | undefined;
  high: Decimal | undefined;
  low: Decimal | undefined;
  close: Decimal | undefined;
  upper_limit: string | undefined;
  lower_limit: string | undefined;
  volume: Decimal | undefined;
  value: Decimal | undefined;
  adjustment_factor: Decimal | undefined;
  adjusted_open: Decimal | undefined;
  adjusted_high: Decimal | undefined;
  adjusted_low: Decimal | undefined;
  adjusted_close: Decimal | undefined;
  adjusted_volume: Decimal | undefined;
  ex_rights_type: string | undefined;
  created_at: Date;
  updated_at: Date;
};

export type DailyQuoteListRsponse = {
  data: DailyQuote[];
  total: number;
};

export type Valuation = {
  date: Date;
  code: string;
  eps: Decimal | undefined;
  forward_eps: Decimal | undefined;
  bps: Decimal | undefined;
  roe: Decimal | undefined;
  forward_roe: Decimal | undefined;
  per: Decimal | undefined;
  forward_per: Decimal | undefined;
  pbr: Decimal | undefined;
  market_cap: Decimal | undefined;
  created_at: Date;
  updated_at: Date;
};

export type ValuationListRsponse = {
  data: Valuation[];
  total: number;
};

export type Summary = {
  disclosure_date: Date;
  disclosure_time: string | undefined;
  code: string;
  disclosure_number: string;
  document_type: string | undefined;
  current_period_type: string | undefined;
  current_period_start: Date | undefined;
  current_period_end: Date | undefined;
  current_fiscal_year_start: Date | undefined;
  current_fiscal_year_end: Date | undefined;
  sales: Decimal | undefined;
  operating_profit: Decimal | undefined;
  ordinary_profit: Decimal | undefined;
  net_profit: Decimal | undefined;
  eps: Decimal | undefined;
  diluted_eps: Decimal | undefined;
  total_assets: Decimal | undefined;
  equity: Decimal | undefined;
  shareholders_equity: Decimal | undefined;
  equity_ratio: Decimal | undefined;
  bps: Decimal | undefined;
  roe: Decimal | undefined;
  cash_flow_operating: Decimal | undefined;
  cash_flow_investing: Decimal | undefined;
  cash_flow_financing: Decimal | undefined;
  cash_and_equivalents: Decimal | undefined;
  dividend_annual: Decimal | undefined;
  forecast_dividend_annual: Decimal | undefined;
  next_forecast_dividend_annual: Decimal | undefined;
  annual_payout_ratio: Decimal | undefined;
  forecast_annual_payout_ratio: Decimal | undefined;
  shares_outstanding: Decimal | undefined;
  treasury_shares: Decimal | undefined;
  average_shares: Decimal | undefined;
  forecast_sales_2q: Decimal | undefined;
  forecast_operating_profit_2q: Decimal | undefined;
  forecast_ordinary_profit_2q: Decimal | undefined;
  forecast_net_profit_2q: Decimal | undefined;
  forecast_eps_2q: Decimal | undefined;
  forecast_sales: Decimal | undefined;
  forecast_operating_profit: Decimal | undefined;
  forecast_ordinary_profit: Decimal | undefined;
  forecast_net_profit: Decimal | undefined;
  forecast_eps: Decimal | undefined;
  next_forecast_sales_2q: Decimal | undefined;
  next_forecast_operating_profit_2q: Decimal | undefined;
  next_forecast_ordinary_profit_2q: Decimal | undefined;
  next_forecast_net_profit_2q: Decimal | undefined;
  next_forecast_eps_2q: Decimal | undefined;
  next_forecast_sales: Decimal | undefined;
  next_forecast_operating_profit: Decimal | undefined;
  next_forecast_ordinary_profit: Decimal | undefined;
  next_forecast_net_profit: Decimal | undefined;
  next_forecast_eps: Decimal | undefined;
  created_at: Date;
  updated_at: Date;
};

export type SummaryListRsponse = {
  data: Summary[];
  total: number;
};

export type SearchRequest = {
  keyword: string | undefined;
  dateFrom: Date | undefined;
  dateTo: Date | undefined;
};
