from datetime import datetime
from typing import Any

from app.db.base import Base
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class ScreeningRule(Base):
    __tablename__ = "screening_rule"

    # DB内部ID（自動採番）
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # screening_groupのid
    group_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("screening_group.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # metric_registryのcode
    metric_code: Mapped[str] = mapped_column(String(50), nullable=False)

    # 評価項目ごとに異なるパラメータ
    params: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # 条件を満たした際の加点・減点
    points: Mapped[int] = mapped_column(
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
