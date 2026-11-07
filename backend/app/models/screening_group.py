from datetime import datetime

from app.db.base import Base
from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class ScreeningGroup(Base):
    __tablename__ = "screening_group"

    # DB内部ID（自動採番）
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # キャッシュ処理のステータス
    cache_status: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # キャッシュ処理の備考
    cache_remarks: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    # cache開始日時
    cache_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # 最後にcacheされた日時
    cached_at: Mapped[datetime | None] = mapped_column(
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
