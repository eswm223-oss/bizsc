from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)


class GroupSearchRequest(BaseModel):
    group_id: int
    keyword: str | None = None


class GroupData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cache_status: str | None
    cache_remarks: str | None
    cache_started_at: datetime | None
    cached_at: datetime | None
    updated_at: datetime


class GroupList(BaseModel):
    data: list[GroupData]
    total: int


class RuleData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: int
    metric_code: str
    params: dict[str, Any]
    points: int
    updated_at: datetime


class RuleList(BaseModel):
    data: list[RuleData]


class ResultData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    group_id: int
    rule_id: int
    company_code: str
    score: int
    updated_at: datetime


class ResultList(BaseModel):
    data: list[ResultData]
    total: int
