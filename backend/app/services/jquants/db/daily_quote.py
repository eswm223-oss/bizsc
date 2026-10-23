from sqlalchemy.orm import Session

from backend.app.models import JQuantsDailyQuote
from backend.app.repositories.daily_quote import JQuantsDailyQuoteRepository


class daily_quote_service:
    def __init__(self, repository: JQuantsDailyQuoteRepository) -> None:
        self.repository = repository

    def createOrUpdate(
        self, db: Session, data: JQuantsDailyQuote
    ) -> JQuantsDailyQuote | None:
        if data is None:
            return None
        data.id = data.code + "-" + data.date.strftime("%Y%m%d")
        return self.repository.createOrUpdate(db, data)

    def getByCode(self, db: Session, Code: str) -> list[JQuantsDailyQuote] | None:
        return self.repository.getByCode(db, Code)
