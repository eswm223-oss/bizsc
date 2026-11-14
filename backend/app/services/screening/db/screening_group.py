from datetime import date, datetime
from typing import Literal
from zoneinfo import ZoneInfo

from app.common import cmm_date
from app.models import ScreeningGroup
from app.repositories import ScreeningGroupRepository
from pydantic import BaseModel
from sqlalchemy.orm import Session

DATE_CONVERTER = cmm_date
STATUS_LITERAL = Literal["Running", "Complete", "Error"] | None


class NewParameter(BaseModel):
    from_date: date
    to_date: date
    code: str | None
    run_master: bool = False
    run_dailyBar: bool = False
    run_valuation: bool = False
    run_summary: bool = False


class ScreeningGroupService:
    def __init__(
        self,
        repository: ScreeningGroupRepository,
    ) -> None:
        self.repository = repository

    def merge(self, db: Session, name: str) -> ScreeningGroup:
        sorce = ScreeningGroup(
            name=name,
        )
        return self.repository.merge(db, sorce)

    def get_by_id(self, db: Session, id: int) -> ScreeningGroup | None:
        return self.repository.get_by_id(db, id)

    def set_status(
        self,
        db: Session,
        id: int,
        status: STATUS_LITERAL,
        remarks: str | None = None,
    ) -> ScreeningGroup:
        sorce = self.get_by_id(db, id)
        if sorce is None:
            raise ValueError("進捗ステータスの取得に失敗しました。")

        if remarks is not None:
            sorce.cache_remarks = remarks[:300]

        if status == "Running":
            sorce.cached_at = datetime.now(ZoneInfo("Asia/Tokyo"))

        response = self.repository.update(db, sorce)
        if response is None:
            raise ValueError("進捗ステータスの更新に失敗しました。")
        return response

    def delete(
        self,
        db: Session,
        id: int,
    ) -> None:
        sorce = self.get_by_id(db, id)
        if sorce is None:
            return
        self.repository.delete(db, sorce)

    def search(
        self,
        db: Session,
        keyword: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> tuple[list[ScreeningGroup], int]:
        resList = self.repository.search(db, keyword, page, limit)
        resTotal = self.repository.count_search(db, keyword)
        return resList, resTotal
