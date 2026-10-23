from app.models import JQuantsValuation
from sqlalchemy import select
from sqlalchemy.orm import Session


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
        db.commit()
        db.refresh(data)
        return data

    def createOrUpdate(self, db: Session, data: JQuantsValuation) -> JQuantsValuation:
        source = db.merge(data)
        db.commit()
        db.refresh(source)
        return source

    def delete(self, db: Session, data: JQuantsValuation) -> None:
        db.delete(data)
        db.commit()
