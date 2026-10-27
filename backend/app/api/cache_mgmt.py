from datetime import date

from app.db.database import get_db
from app.repositories import CacheMgmtRepository
from app.schemas import CacheMgmtListResponse, CacheMgmtResponse
from app.services import CacheMgmtService
from fastapi import APIRouter, Depends
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
def get_users(
    search: date | None = None,
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> CacheMgmtListResponse:
    data, resTotal = service.getAllSearch(
        db,
        search=search,
        page=page,
        limit=limit,
    )

    reslist = [CacheMgmtResponse.model_validate(record) for record in data]

    return CacheMgmtListResponse(
        data=reslist,
        total=resTotal,
    )
