from datetime import date, datetime
from decimal import Decimal

from app.db.base import Base
from sqlalchemy import Date, DateTime, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column


class JQuantsFinancialSummary(Base):
    __tablename__ = "jq_financial_summaries"
    __table_args__ = (
        UniqueConstraint(
            "code",
            "current_period_end",
            "current_period_type",
            "document_type",
            name="uq_jq_financial_summaries_period",
        ),
    )

    # DB内部ID（Code-Date）
    id: Mapped[str] = mapped_column(String(70), primary_key=True)

    # DiscDate：開示日
    disclosure_date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )

    # DiscTime：開示時刻
    disclosure_time: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # Code：銘柄コード（5桁）
    code: Mapped[str] = mapped_column(
        String(10),
        index=True,
        nullable=False,
    )

    # DiscNo：開示番号
    disclosure_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # DocType：書類種別
    document_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # CurPerType：当会計期間の種類
    # 例：1Q / 2Q / 3Q / FY
    current_period_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # CurPerSt：当会計期間の開始日
    current_period_start: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # CurPerEn：当会計期間の終了日
    current_period_end: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # CurFYSt：当事業年度の開始日
    current_fiscal_year_start: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # CurFYEn：当事業年度の終了日
    current_fiscal_year_end: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Sales：売上高
    sales: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # OP：営業利益
    operating_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # OdP：経常利益
    ordinary_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NP：当期純利益
    net_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # EPS：1株当たり当期純利益
    eps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # DEPS：潜在株式調整後1株当たり当期純利益
    diluted_eps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # TA：総資産
    total_assets: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # Eq：純資産
    equity: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # ShEq：株主資本
    shareholders_equity: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # EqAR：自己資本比率
    equity_ratio: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # BPS：1株当たり純資産
    bps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # ROE：自己資本利益率
    roe: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # CFO：営業活動によるキャッシュフロー
    cash_flow_operating: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # CFI：投資活動によるキャッシュフロー
    cash_flow_investing: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # CFF：財務活動によるキャッシュフロー
    cash_flow_financing: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # CashEq：現金及び現金同等物期末残高
    cash_and_equivalents: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # DivAnn：年間配当金
    dividend_annual: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FDivAnn：予想年間配当金
    forecast_dividend_annual: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFDivAnn：翌事業年度予想年間配当金
    next_forecast_dividend_annual: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # PayoutRatioAnn：年間配当性向
    annual_payout_ratio: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FPayoutRatioAnn：予想年間配当性向
    forecast_annual_payout_ratio: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # ShOutFY：期末発行済株式数
    shares_outstanding: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # TrShFY：期末自己株式数
    treasury_shares: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # AvgSh：期中平均株式数
    average_shares: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FSales2Q：第2四半期累計予想売上高
    forecast_sales_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FOP2Q：第2四半期累計予想営業利益
    forecast_operating_profit_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FOdP2Q：第2四半期累計予想経常利益
    forecast_ordinary_profit_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FNP2Q：第2四半期累計予想当期純利益
    forecast_net_profit_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FEPS2Q：第2四半期累計予想EPS
    forecast_eps_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FSales：通期予想売上高
    forecast_sales: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FOP：通期予想営業利益
    forecast_operating_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FOdP：通期予想経常利益
    forecast_ordinary_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FNP：通期予想当期純利益
    forecast_net_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FEPS：通期予想EPS
    forecast_eps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFSales2Q：翌事業年度第2四半期累計予想売上高
    next_forecast_sales_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFOP2Q：翌事業年度第2四半期累計予想営業利益
    next_forecast_operating_profit_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFOdP2Q：翌事業年度第2四半期累計予想経常利益
    next_forecast_ordinary_profit_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFNp2Q：翌事業年度第2四半期累計予想当期純利益
    next_forecast_net_profit_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFEPS2Q：翌事業年度第2四半期累計予想EPS
    next_forecast_eps_2q: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFSales：翌事業年度通期予想売上高
    next_forecast_sales: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFOP：翌事業年度通期予想営業利益
    next_forecast_operating_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFOdP：翌事業年度通期予想経常利益
    next_forecast_ordinary_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFNp：翌事業年度通期予想当期純利益
    next_forecast_net_profit: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # NxFEPS：翌事業年度通期予想EPS
    next_forecast_eps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # DB登録日時
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # DB更新日時
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
