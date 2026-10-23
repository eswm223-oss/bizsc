from app.models import JQuantsValuation
from app.repositories.valuation import JQuantsValuationRepository
from sqlalchemy.orm import Session


class valuation_service:
    def __init__(self, repository: JQuantsValuationRepository) -> None:
        self.repository = repository

    def createOrUpdate(
        self, db: Session, data: JQuantsValuation
    ) -> JQuantsValuation | None:
        if data is None:
            return None

        # id生成
        data.id = data.code + "-" + data.date.strftime("%Y%m%d")

        return self.repository.createOrUpdate(db, data)

    def getByCode(self, db: Session, Code: str) -> list[JQuantsValuation] | None:
        return self.repository.getByCode(db, Code)
