from typing import Any, Literal

from app.common import cmm_date
from app.models import ScreeningRule
from app.repositories import ScreeningRuleRepository
from app.screening.params_convert import ParamsConvert
from pydantic import BaseModel
from sqlalchemy.orm import Session

DATE_CONVERTER = cmm_date
STATUS_LITERAL = Literal["Running", "Complete", "Error"] | None


class NewParameter(BaseModel):
    group_id: int
    metric_code: str
    params: dict[str, Any]
    points: int


class ScreeningRuleService:
    def __init__(
        self,
        repository: ScreeningRuleRepository,
    ) -> None:
        self.repository = repository

    # 登録 ==============
    def create_or_update(self, db: Session, para: NewParameter) -> ScreeningRule:
        # paramsを検証
        result = ParamsConvert.params_validate(
            params=para.params, metric_code=para.metric_code
        )
        if not result.result or result.params is None:
            raise ValueError(result.error or "パラメータが不正です")

        sorce = ScreeningRule(
            group_id=para.group_id,
            metric_code=para.metric_code,
            params=para.params,
            points=para.points,
        )
        return self.repository.crate_or_update(db, sorce)

    # 削除 ==============
    def delete(
        self,
        db: Session,
        id: int,
    ) -> None:
        sorce = self.get_by_id(db, id)
        if sorce is None:
            return
        self.repository.delete(db, sorce)

    # 取得 ==============
    def get_by_id(self, db: Session, id: int) -> ScreeningRule | None:
        response = self.repository.get_by_id(db, id)
        return response

    def get_by_group(self, db: Session, group_id: int) -> list[ScreeningRule]:
        resList = self.repository.get_by_group(db, group_id)
        return resList
