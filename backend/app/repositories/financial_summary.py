from datetime import date

from app.models import JQuantsFinancialSummary, JQuantsListedIssue
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.orm import Session


class SearchRequest(BaseModel):
    keyword: str
    dateFrom: date
    dateTo: date


class JQuantsFinancialSummaryRepository:
    def getByCode(
        self,
        db: Session,
        code: str,
    ) -> list[JQuantsFinancialSummary] | None:
        statement = (
            select(JQuantsFinancialSummary)
            .where(JQuantsFinancialSummary.code == code)
            .order_by(JQuantsFinancialSummary.disclosure_date.desc())
        )
        return list(db.scalars(statement).all())

    def create(
        self, db: Session, data: JQuantsFinancialSummary
    ) -> JQuantsFinancialSummary:
        db.add(data)
        return data

    def createOrUpdate(
        self, db: Session, data: JQuantsFinancialSummary
    ) -> JQuantsFinancialSummary:
        source = db.merge(data)
        return source

    def delete(self, db: Session, data: JQuantsFinancialSummary) -> None:
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
    ) -> list[JQuantsFinancialSummary] | None:
        statement = select(JQuantsFinancialSummary)

        # ==========サーチ==========
        if search:
            statement = (
                statement.outerjoin(
                    JQuantsListedIssue,
                    JQuantsFinancialSummary.code == JQuantsListedIssue.code,
                )
                .where(
                    JQuantsFinancialSummary.disclosure_date.between(
                        search.dateFrom, search.dateTo
                    )
                )
                .where(
                    or_(
                        JQuantsFinancialSummary.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            )

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = (
            statement.order_by(
                JQuantsFinancialSummary.code.asc(),
                JQuantsFinancialSummary.disclosure_date.desc(),
            )
            .offset(offset)
            .limit(limit)
        )

        return list(db.scalars(statement).all())
