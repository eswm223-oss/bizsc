from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JQuantsDailyQuote(Base):
    __tablename__ = "jq_daily_quotes"
    __table_args__ = (
        UniqueConstraint("date", "code", name="uq_jq_daily_quotes_date_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(10),
        index=True,
        nullable=False,
    )

    open: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    high: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    low: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    close: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    upper_limit: Mapped[str | None] = mapped_column(
        String(1),
        nullable=True,
    )

    lower_limit: Mapped[str | None] = mapped_column(
        String(1),
        nullable=True,
    )

    volume: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    value: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    adjustment_factor: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    adjusted_open: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    adjusted_high: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    adjusted_low: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    adjusted_close: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    adjusted_volume: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    ex_rights_type: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )