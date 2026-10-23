from sqlalchemy.orm import Session

from backend.app.models import JQuantsFinancialSummary
from backend.app.repositories.financial_summary import JQuantsFinancialSummaryRepository


class financial_summary:
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
