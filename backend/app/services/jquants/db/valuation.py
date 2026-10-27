from app.models import JQuantsValuation
from app.repositories.valuation import JQuantsValuationRepository
from app.schemas.jqunats import SearchRequest
from sqlalchemy.orm import Session


class Valuation_service:
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

    def search(
        self,
        db: Session,
        search: SearchRequest | None = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        page: int = 1,
        limit: int = 50,
    ) -> tuple[list[JQuantsValuation], int]:

        resList = self.repository.getAllSearch(
            db=db,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            limit=limit,
        )
        resToral = self.repository.count_all(db=db, search=search)
        return resList, resToral
