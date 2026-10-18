from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JQuantsListedIssue(Base):
    __tablename__ = "jq_listed_issues"

    id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
        nullable=False,
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    company_name_en: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    sector17_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    sector17_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    sector33_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    sector33_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    scale_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    market_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    market_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    margin_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    margin_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    product_category: Mapped[str | None] = mapped_column(
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