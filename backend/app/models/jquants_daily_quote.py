from datetime import date, datetime
from decimal import Decimal

from app.db.base import Base
from sqlalchemy import Date, DateTime, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column


class JQuantsDailyQuote(Base):
    __tablename__ = "jq_daily_quotes"
    __table_args__ = (
        UniqueConstraint(
            "code",
            "date",
            name="uq_jq_daily_quotes_code_date",
        ),
    )

    # DB内部ID（Code-Date）
    id: Mapped[str] = mapped_column(String(20), primary_key=True)

    # Date:日付（YYYY-MM-DD）
    date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )

    # Code:銘柄コード（5桁）
    code: Mapped[str] = mapped_column(
        String(10),
        index=True,
        nullable=False,
    )

    # O:始値（調整前・円単位）
    open: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # H:高値（調整前・円単位）
    high: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # L:安値（調整前・円単位）
    low: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # C:終値（調整前・円単位）
    close: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # UL:日通ストップ高フラグ
    # 0:ストップ高以外 / 1:ストップ高
    upper_limit: Mapped[str | None] = mapped_column(
        String(1),
        nullable=True,
    )

    # LL:日通ストップ安フラグ
    # 0:ストップ安以外 / 1:ストップ安
    lower_limit: Mapped[str | None] = mapped_column(
        String(1),
        nullable=True,
    )

    # Vo:取引高（調整前）
    # 普通株式は株数、ETF・REIT等は口数
    volume: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # Va:取引代金（円単位）
    value: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # AdjFactor:調整係数
    # 例:株式分割1:2の場合、権利落ち日に0.5
    adjustment_factor: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # AdjO:調整済み始値
    adjusted_open: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # AdjH:調整済み高値
    adjusted_high: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # AdjL:調整済み安値
    adjusted_low: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # AdjC:調整済み終値
    adjusted_close: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # AdjVo:調整済み取引高
    adjusted_volume: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # ExRT:権利落種類
    # 1:株式分割 / 2:株式併合 / 3:ライツイシュー
    ex_rights_type: Mapped[str | None] = mapped_column(
        String(10),
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
