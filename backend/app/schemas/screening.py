from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


class GroupSearchRequest(BaseModel):
    group_id: int
    keyword: str | None = None


class GroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cache_status: str | None
    cache_remarks: str | None
    cache_started_at: datetime | None
    cached_at: datetime | None
    updated_at: datetime


class GroupListResponse(BaseModel):
    data: list[GroupResponse]
    total: int


class ruleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: int
    metric_code: str
    params: str
    points: int | None
    updated_at: datetime


class ruleListResponse(BaseModel):
    data: list[ruleResponse]


class resultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    group_id: int
    rule_id: int
    company_code: str
    score: int | None
    updated_at: datetime


class resultListResponse(BaseModel):
    data: list[ruleResponse]
    total: int
