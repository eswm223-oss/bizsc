from app.models import JQuantsFinancialSummary
from app.repositories.financial_summary import (
    JQuantsFinancialSummaryRepository,
)
from app.schemas.jqunats import SearchRequest
from sqlalchemy.orm import Session


class Financial_summary_service:
    def __init__(self, repository: JQuantsFinancialSummaryRepository) -> None:
        self.repository = repository

    def createOrUpdate(
        self, db: Session, data: JQuantsFinancialSummary
    ) -> JQuantsFinancialSummary | None:
        if (
            data is None
            or data.current_period_end is None
            or data.current_period_type is None
            or data.document_type is None
        ):
            return None
        # id生成
        current_period_end = data.current_period_end.strftime("%Y%m%d")
        data.id = (
            f"{data.code}-"
            f"{current_period_end}-"
            f"{data.current_period_type}-"
            f"{data.document_type}"
        )
        return self.repository.createOrUpdate(db, data)

    def getByCode(self, db: Session, Code: str) -> list[JQuantsFinancialSummary] | None:
        return self.repository.getByCode(db, Code)

    def search(
        self,
        db: Session,
        search: SearchRequest | None = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        page: int = 1,
        limit: int = 50,
    ) -> tuple[list[JQuantsFinancialSummary], int]:

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
