from datetime import date

from app.models import JQuantsDailyQuote, JQuantsListedIssue
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.orm import Session


class SearchRequest(BaseModel):
    keyword: str
    dateFrom: date
    dateTo: date


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
        page: int = 1,
        limit: int = 50,
    ) -> list[JQuantsDailyQuote] | None:
        statement = select(JQuantsDailyQuote)

        # ==========サーチ==========
        if search:
            statement = (
                statement.outerjoin(
                    JQuantsListedIssue,
                    JQuantsDailyQuote.code == JQuantsListedIssue.code,
                )
                .where(JQuantsDailyQuote.date.between(search.dateFrom, search.dateTo))
                .where(
                    or_(
                        JQuantsDailyQuote.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            )

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = (
            statement.order_by(
                JQuantsDailyQuote.code.asc(), JQuantsDailyQuote.date.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        return list(db.scalars(statement).all())
