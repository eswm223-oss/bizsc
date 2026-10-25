from datetime import date, datetime

from app.db.base import Base
from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class CacheMgmt(Base):
    __tablename__ = "cache_mgmt"

    # DB内部ID（YYYYMMDD-HHMMSS）
    id: Mapped[str] = mapped_column(String(15), primary_key=True)

    from_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    to_date: Mapped[str] = mapped_column(
        Date,
        nullable=False,
    )

    # 銘柄コード
    company_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    status_master: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    status_dailyBar: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    status_valuation: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    status_summary: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    # DB更新日時
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
