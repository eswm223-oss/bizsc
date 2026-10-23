from app.models import JQuantsDailyQuote
from sqlalchemy import select
from sqlalchemy.orm import Session

# 　selfはクラスのインスタンスメソッドとして使用するために必須の設定値、インスタンスで使用される


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
        db.commit()
        db.refresh(data)
        return data

    def createOrUpdate(self, db: Session, data: JQuantsDailyQuote) -> JQuantsDailyQuote:
        source = db.merge(data)
        db.commit()
        db.refresh(source)
        return source

    def delete(self, db: Session, data: JQuantsDailyQuote) -> None:
        db.delete(data)
        db.commit()
