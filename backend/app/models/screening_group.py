from datetime import datetime

from app.db.base import Base
from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class ScreeningGroup(Base):
    __tablename__ = "screening_group"

    # DB内部ID
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    cache_status: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    cache_remarks: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    # 最後にcacheされた日時
    cached_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # DB更新日時
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
