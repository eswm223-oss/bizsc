from typing import Literal

from app.common import cmm_date
from app.models import ScreeningResult
from app.repositories import ScreeningResultRepository
from pydantic import BaseModel
from sqlalchemy.orm import Session

DATE_CONVERTER = cmm_date
STATUS_LITERAL = Literal["Running", "Complete", "Error"] | None


class Parameter(BaseModel):
    group_id: int
    rule_id: int
    company_code: str
    score: int


class ScreeningResultService:
    def __init__(
        self,
        repository: ScreeningResultRepository,
    ) -> None:
        self.repository = repository

    def create_or_update(self, db: Session, para: Parameter) -> ScreeningResult:
        sorce = ScreeningResult(
            id=f"{para.rule_id}-{para.company_code}",
            group_id=para.group_id,
            rule_id=para.rule_id,
            company_code=para.company_code,
            score=para.score,
        )
        return self.repository.crate_or_update(db, sorce)

    def get_by_id(self, db: Session, id: str) -> ScreeningResult | None:
        return self.repository.get_by_id(db, id)

    def delete(
        self,
        db: Session,
        id: str,
    ) -> None:
        sorce = self.get_by_id(db, id)
        if sorce is None:
            return
        self.repository.delete(db, sorce)

    def get_by_group(
        self, db: Session, group_id: int
    ) -> tuple[list[ScreeningResult], int]:
        resList = self.repository.get_result(db, group_id)
        resToral = self.repository.get_result_count(db=db, group_id=group_id)
        return resList, resToral
