from datetime import datetime
from decimal import Decimal

from app.db.base import Base
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column


class ScreeningResult(Base):
    __tablename__ = "screening_result"
    __table_args__ = (
        Index("idx_screening_result", "group_id", "rule_id", "company_code"),
    )

    # DB内部ID（itemId-company_code）
    id: Mapped[str] = mapped_column(String(50), primary_key=True)

    # screening_groupのid
    group_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("screening_group.id"), nullable=False
    )

    # screening_ruleのid
    rule_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("screening_rule.id"), nullable=False
    )

    # 銘柄コード（5桁）
    company_code: Mapped[str] = mapped_column(
        String(10),
        index=True,
        nullable=False,
    )

    # 点数
    score: Mapped[Decimal] = mapped_column(
        Integer,
        nullable=False,
    )

    # DB更新日時
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
