from app.db.database import get_db
from app.models.screening_group import ScreeningGroup
from app.repositories import (
    ScreeningGroupRepository,
    ScreeningResultRepository,
    ScreeningRuleRepository,
)
from app.schemas.screening import GroupData, GroupList
from app.services.screening.db.screening_group import ScreeningGroupService
from app.services.screening.db.screening_result import ScreeningResultService
from app.services.screening.db.screening_rule import ScreeningRuleService
from fastapi import APIRouter, Depends, HTTPException, status
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
    response_model=GroupList,
)
def get_group(
    keyword: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> GroupList:
    data, total = group_service.search(
        db,
        keyword=keyword,
        page=page,
        limit=limit,
    )
    return GroupList(
        data=[GroupData.model_validate(record) for record in data],
        total=total,
    )


@router.post(
    "/group/merge",
    response_model=GroupData,
    status_code=status.HTTP_201_CREATED,
)
def marge_group(
    name: str,
    id: int | None = None,
    db: Session = Depends(get_db),
) -> GroupData:
    source = ScreeningGroup()
    if id:
        source = group_service.get_by_id(db, id)
        if source is None:
            raise HTTPException(
                status_code=404,
                detail="管理データが見つかりません",
            )
    source.name = name

    response = group_service.merge(db, source)
    return GroupData.model_validate(response)
