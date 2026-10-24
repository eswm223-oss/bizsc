from datetime import date

from app.models import JQuantsListedIssue, JQuantsValuation
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.orm import Session


class SearchRequest(BaseModel):
    keyword: str
    dateFrom: date
    dateTo: date


class JQuantsValuationRepository:
    def getByCode(
        self,
        db: Session,
        code: str,
    ) -> list[JQuantsValuation] | None:
        statement = (
            select(JQuantsValuation)
            .where(JQuantsValuation.code == code)
            .order_by(JQuantsValuation.date.desc())
        )
        return list(db.scalars(statement).all())

    def create(self, db: Session, data: JQuantsValuation) -> JQuantsValuation:
        db.add(data)
        return data

    def createOrUpdate(self, db: Session, data: JQuantsValuation) -> JQuantsValuation:
        source = db.merge(data)
        return source

    def delete(self, db: Session, data: JQuantsValuation) -> None:
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
    ) -> list[JQuantsValuation] | None:
        statement = select(JQuantsValuation)

        # ==========サーチ==========
        if search:
            statement = (
                statement.outerjoin(
                    JQuantsListedIssue,
                    JQuantsValuation.code == JQuantsListedIssue.code,
                )
                .where(JQuantsValuation.date.between(search.dateFrom, search.dateTo))
                .where(
                    or_(
                        JQuantsValuation.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            )

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = (
            statement.order_by(
                JQuantsValuation.code.asc(), JQuantsValuation.date.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        return list(db.scalars(statement).all())
