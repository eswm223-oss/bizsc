from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EdinetDocument(Base):
    __tablename__ = "edinet_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    target_date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )
    doc_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    edinet_code: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    sec_code: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
        nullable=True,
    )
    filer_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    ordinance_code: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    form_code: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    doc_type_code: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
        nullable=True,
    )
    period_start: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    period_end: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    submit_date_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=False),
        index=True,
        nullable=True,
    )
    doc_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    parent_doc_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    withdrawal_status: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    doc_info_edit_status: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    disclosure_status: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    xbrl_flag: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    pdf_flag: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    csv_flag: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    legal_status: Mapped[str | None] = mapped_column(
        String(255),
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
