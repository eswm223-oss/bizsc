from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


class CacheBatchRequest(BaseModel):
    fromDate: date
    toDate: date
    mgmtId: str | None = None
    code: str = ""


class CacheMgmtResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    from_date: date
    to_date: date
    company_code: str | None
    status_master: str | None
    status_dailyBar: str | None
    status_valuation: str | None
    status_summary: str | None
    remarks: str | None
    updated_at: datetime


class CacheMgmtListResponse(BaseModel):
    data: list[CacheMgmtResponse]
    total: int
