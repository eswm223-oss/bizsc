from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JQuantsValuation(Base):
    __tablename__ = "jq_valuations"
    __table_args__ = (
        UniqueConstraint(
            "date",
            "code",
            name="uq_jq_valuations_date_code",
        ),
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

    eps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    forward_eps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    bps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    roe: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    forward_roe: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    per: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    forward_per: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    pbr: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    market_cap: Mapped[Decimal | None] = mapped_column(
        Numeric,
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