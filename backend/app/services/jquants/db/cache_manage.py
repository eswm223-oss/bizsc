import datetime
from datetime import date, datetime
from typing import Literal
from zoneinfo import ZoneInfo

from app.common import cmm_date
from app.models import CacheMgmt
from app.repositories import CacheMgmtRepository
from pydantic import BaseModel
from sqlalchemy.orm import Session

DATE_CONVERTER = cmm_date
ITEM_LITERAL = Literal["other", "master", "dailyBar", "valuation", "summary"]
STATUS_LITERAL = Literal["Waiting", "Running", "Complete", "Error"]


class NewParameter(BaseModel):
    from_date: date
    to_date: date
    code: str | None
    run_master: bool = False
    run_dailyBar: bool = False
    run_valuation: bool = False
    run_summary: bool = False


class CacheMgmtService:
    def __init__(
        self,
        repository: CacheMgmtRepository,
    ) -> None:
        self.repository = repository

    def create(self, db: Session, set: NewParameter) -> CacheMgmt:
        NOW = datetime.now(ZoneInfo("Asia/Tokyo"))
        sorce = CacheMgmt(
            id=f"{DATE_CONVERTER.to_yyyymmdd(NOW)}-{DATE_CONVERTER.to_hhmmss(NOW)}",
            from_date=set.from_date,
            to_date=set.to_date,
            company_code=set.code,
            status_master="Waiting" if set.run_master else None,
            status_dailyBar="Waiting" if set.run_dailyBar else None,
            status_valuation="Waiting" if set.run_valuation else None,
            status_summary="Waiting" if set.run_summary else None,
        )
        return self.repository.create(db, sorce)

    def getById(self, db: Session, id: str) -> CacheMgmt | None:
        return self.repository.getById(db, id)

    def setStatus(
        self,
        db: Session,
        id: str,
        item: ITEM_LITERAL,
        status: STATUS_LITERAL,
        remarks: str | None = None,
    ) -> CacheMgmt:
        sorce = self.getById(db, id)
        if sorce is None:
            raise ValueError("進捗ステータスの取得に失敗しました。")

        match item:
            case "master":
                sorce.status_master = status
            case "dailyBar":
                sorce.status_dailyBar = status
            case "valuation":
                sorce.status_valuation = status
            case "summary":
                sorce.status_summary = status
        if remarks is not None:
            sorce.remarks = remarks[:300]

        response = self.repository.update(db, sorce)
        if response is None:
            raise ValueError("進捗ステータスの更新に失敗しました。")

        return response

    def delete_user(
        self,
        db: Session,
        id: str,
    ) -> None:
        sorce = self.getById(db, id)
        if sorce is None:
            return
        self.repository.delete(db, sorce)
