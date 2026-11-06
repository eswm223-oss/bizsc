from datetime import datetime
from typing import Any

from app.db.base import Base
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class ScreeningRule(Base):
    __tablename__ = "screening_rule"
    __table_args__ = (
        UniqueConstraint(
            "group_id",
            "sequence",
            name="screening_rule_groupid_sequence",
        ),
    )

    # DB内部ID（group_id-sequence）
    id: Mapped[str] = mapped_column(String(20), primary_key=True)

    # screening_groupのid
    group_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("screening_group.id"), nullable=False
    )

    # 連番
    sequence: Mapped[int] = mapped_column(nullable=False)

    # metric_registryのcode
    metric_code: Mapped[str] = mapped_column(String(50), nullable=False)

    # 評価項目ごとに異なるパラメータ
    params: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # DB更新日時
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
