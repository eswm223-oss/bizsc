from app.db.database import get_db
from app.repositories import (
    ScreeningGroupRepository,
    ScreeningResultRepository,
    ScreeningRuleRepository,
)
from app.schemas.screening import GroupListResponse, GroupResponse
from app.services.screening.db.screening_group import ScreeningGroupService
from app.services.screening.db.screening_result import ScreeningResultService
from app.services.screening.db.screening_rule import ScreeningRuleService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

group_service = ScreeningGroupService(ScreeningGroupRepository())
result_service = ScreeningResultService(ScreeningResultRepository())
rule_service = ScreeningRuleService(ScreeningRuleRepository())

router = APIRouter(
    prefix="/screening",
    tags=["screening"],
)


@router.get(
    "/group",
    response_model=GroupListResponse,
)
def get_group(
    keyword: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> GroupListResponse:
    data, total = group_service.search(
        db,
        keyword=keyword,
        page=page,
        limit=limit,
    )
    return GroupListResponse(
        data=[GroupResponse.model_validate(record) for record in data],
        total=total,
    )


@router.post(
    "/group/merge",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
)
def marge_group(
    name: str,
    db: Session = Depends(get_db),
) -> GroupResponse:
    response = group_service.merge(db, name)
    return GroupResponse.model_validate(response)
