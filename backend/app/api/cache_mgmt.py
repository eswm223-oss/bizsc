from datetime import date

from app.db.database import get_db
from app.repositories import CacheMgmtRepository
from app.schemas import CacheMgmtListResponse, CacheMgmtResponse
from app.services import CacheMgmtService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/cachemgmt",
    tags=["cache management"],
)

service = CacheMgmtService(CacheMgmtRepository())


@router.get(
    "/list",
    response_model=CacheMgmtListResponse,
)
def get_list(
    keyword: str | None = None,
    date: date | None = None,
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> CacheMgmtListResponse:
    data, resTotal = service.getAllSearch(
        db,
        keyword=keyword,
        targetDate=date,
        page=page,
        limit=limit,
    )

    reslist = [CacheMgmtResponse.model_validate(record) for record in data]

    return CacheMgmtListResponse(
        data=reslist,
        total=resTotal,
    )


@router.get(
    "/{mgmt_id}",
    response_model=CacheMgmtResponse,
)
def get_by_id(
    mgmt_id: str = "",
    db: Session = Depends(get_db),
) -> CacheMgmtResponse | None:
    if not mgmt_id:
        return
    response = service.getById(db, mgmt_id)
    if response is None:
        raise HTTPException(
            status_code=404,
            detail="管理データが見つかりません",
        )

    return CacheMgmtResponse.model_validate(response)


@router.delete(
    "/{mgmt_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_mgmt(
    mgmt_id: str,
    db: Session = Depends(get_db),
) -> None:
    service.deleteMgmt(db, mgmt_id)
