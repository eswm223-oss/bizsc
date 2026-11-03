from app.models import JQuantsDailyQuote, JQuantsListedIssue
from app.schemas.jqunats import SearchRequest
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session


class JQuantsDailyQuoteRepository:
    def getByCode(
        self,
        db: Session,
        code: str,
    ) -> list[JQuantsDailyQuote] | None:
        statement = (
            select(JQuantsDailyQuote)
            .where(JQuantsDailyQuote.code == code)
            .order_by(JQuantsDailyQuote.date.desc())
        )
        return list(db.scalars(statement).all())

    def create(self, db: Session, data: JQuantsDailyQuote) -> JQuantsDailyQuote:
        db.add(data)
        return data

    def createOrUpdate(self, db: Session, data: JQuantsDailyQuote) -> JQuantsDailyQuote:
        source = db.merge(data)
        return source

    def delete(self, db: Session, data: JQuantsDailyQuote) -> None:
        db.delete(data)

    # --------------------------------------------
    # Search処理
    # --------------------------------------------

    def getAllSearch(
        self,
        db: Session,
        search: SearchRequest | None = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        page: int | None = None,
        limit: int | None = None,
    ) -> list[JQuantsDailyQuote]:
        statement = select(JQuantsDailyQuote)

        # ==========サーチ==========
        if search:
            statement = statement.outerjoin(
                JQuantsListedIssue,
                JQuantsDailyQuote.code == JQuantsListedIssue.code,
            )
            if search.fromDate and search.toDate:
                statement = statement.where(
                    JQuantsDailyQuote.date.between(search.fromDate, search.toDate)
                )
            if search.keyword:
                statement = statement.where(
                    or_(
                        JQuantsDailyQuote.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            if search.targetDate:
                statement = statement.where(JQuantsDailyQuote.date == search.targetDate)

        # ==========ページング==========
        if page and limit:
            offset = (page - 1) * limit
            statement = statement.offset(offset).limit(limit)

        # ==========ソート==========
        sort_columns = {
            "id": JQuantsDailyQuote.id,
            "date": JQuantsDailyQuote.date,
            "code": JQuantsDailyQuote.code,
            "open": JQuantsDailyQuote.open,
            "high": JQuantsDailyQuote.high,
            "low": JQuantsDailyQuote.low,
            "close": JQuantsDailyQuote.close,
            "upper_limit": JQuantsDailyQuote.upper_limit,
            "lower_limit": JQuantsDailyQuote.lower_limit,
            "volume": JQuantsDailyQuote.volume,
            "value": JQuantsDailyQuote.value,
            "adjustment_factor": JQuantsDailyQuote.adjustment_factor,
            "adjusted_open": JQuantsDailyQuote.adjusted_open,
            "adjusted_high": JQuantsDailyQuote.adjusted_high,
            "adjusted_low": JQuantsDailyQuote.adjusted_low,
            "adjusted_close": JQuantsDailyQuote.adjusted_close,
            "adjusted_volume": JQuantsDailyQuote.adjusted_volume,
            "ex_rights_type": JQuantsDailyQuote.ex_rights_type,
            "created_at": JQuantsDailyQuote.created_at,
            "updated_at": JQuantsDailyQuote.updated_at,
        }
        sort_column = sort_columns.get(sort_by, JQuantsDailyQuote.id)
        if sort_order == "desc":
            statement = statement.order_by(sort_column.desc())
        else:
            statement = statement.order_by(sort_column.asc())

        return list(db.scalars(statement).all())

    def count_all(
        self,
        db: Session,
        search: SearchRequest | None = None,
    ) -> int:
        statement = select(func.count(JQuantsDailyQuote.id))

        if search:
            statement = statement.outerjoin(
                JQuantsListedIssue,
                JQuantsDailyQuote.code == JQuantsListedIssue.code,
            )
            if search.fromDate and search.toDate:
                statement = statement.where(
                    JQuantsDailyQuote.date.between(search.fromDate, search.toDate)
                )
            if search.keyword:
                statement = statement.where(
                    or_(
                        JQuantsDailyQuote.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            if search.targetDate:
                statement = statement.where(JQuantsDailyQuote.date == search.targetDate)

        return db.scalar(statement) or 0
