from app.models import JQuantsFinancialSummary
from sqlalchemy import select
from sqlalchemy.orm import Session


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
