from datetime import date, datetime
from decimal import Decimal

from app.db.base import Base
from sqlalchemy import Date, DateTime, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column


class JQuantsValuation(Base):
    __tablename__ = "jq_valuations"
    __table_args__ = (
        UniqueConstraint(
            "code",
            "date",
            name="uq_jq_valuations_code_date",
        ),
    )

    # DB内部ID（Code-Date）
    id: Mapped[str] = mapped_column(String(20), primary_key=True)

    # Date:日付（YYYY-MM-DD）
    date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )

    # Code:銘柄コード（5桁）
    code: Mapped[str] = mapped_column(
        String(10),
        index=True,
        nullable=False,
    )

    # EPS:1株当たり利益（実績・円）
    # 直近12ヶ月（TTM）の純利益をもとに算出
    eps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FwdEPS:1株当たり利益（予想・円）
    # 進行期の予想純利益をもとに算出
    forward_eps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # BPS:1株当たり純資産（円）
    bps: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # ROE:自己資本利益率（実績・小数）
    # 例:0.2310 = 23.1%
    roe: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FwdROE:自己資本利益率（予想・小数）
    # 例:0.2310 = 23.1%
    forward_roe: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # PER:株価収益率（実績・倍）
    per: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # FwdPER:株価収益率（予想・倍）
    forward_per: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # PBR:株価純資産倍率（倍）
    pbr: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # MktCap:時価総額（百万円）
    # 自己株式を控除した株式数を用いて算出
    market_cap: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    # DB登録日時
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # DB更新日時
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
