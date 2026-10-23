from sqlalchemy.orm import Session

from backend.app.models import JQuantsValuation
from backend.app.repositories.valuation import JQuantsValuationRepository


class valuation_service:
    def __init__(self, repository: JQuantsValuationRepository) -> None:
        self.repository = repository

    def createOrUpdate(
        self, db: Session, data: JQuantsValuation
    ) -> JQuantsValuation | None:
        if data is None:
            return None
        data.id = data.code + "-" + data.date.strftime("%Y%m%d")
        return self.repository.createOrUpdate(db, data)

    def getByCode(self, db: Session, Code: str) -> list[JQuantsValuation] | None:
        return self.repository.getByCode(db, Code)
