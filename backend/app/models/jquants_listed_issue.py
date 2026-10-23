from datetime import date, datetime

from app.db.base import Base
from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class JQuantsListedIssue(Base):
    __tablename__ = "jq_listed_issues"

    # DB内部ID（Code）
    id: Mapped[str] = mapped_column(String(20), primary_key=True)

    # Date：情報適用年月日（YYYY-MM-DD）
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # Code：銘柄コード（5桁）
    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
        nullable=False,
    )

    # CoName：会社名
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # CoNameEn：会社名（英語）
    company_name_en: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # S17：17業種コード
    sector17_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # S17Nm：17業種コード名
    sector17_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # S33：33業種コード
    sector33_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # S33Nm：33業種コード名
    sector33_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # ScaleCat：規模コード
    # 例：TOPIX Large70 / TOPIX Mid400 / TOPIX Small 1
    scale_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Mkt：市場区分コード
    market_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # MktNm：市場区分名
    # 例：プライム / スタンダード / グロース
    market_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Mrgn：貸借信用区分
    # 1：信用 / 2：貸借 / 3：その他
    margin_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # MrgnNm：貸借信用区分名
    margin_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # ProdCat：商品区分コード
    # 普通株、ETF、REIT等の区分に利用
    product_category: Mapped[str | None] = mapped_column(
        String(10),
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
