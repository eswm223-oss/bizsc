from app.db.database import SessionLocal
from app.repositories import CacheMgmtRepository
from app.schemas.cache_batch import CacheBatchRequest
from app.services.batches.jquants_sync import run_plain
from app.services.jquants.db.cache_manage import (
    CacheMgmtService,
    NewParameter,
)
from fastapi import APIRouter, BackgroundTasks, status

router = APIRouter(prefix="/batches", tags=["batches"])


@router.post(
    "/jquants/cache/plain",
    status_code=status.HTTP_202_ACCEPTED,
)
def start_jquants_plain_cache(
    body: CacheBatchRequest, background_tasks: BackgroundTasks
):

    # ステータス　準備
    if body.mgmtId is None:
        with SessionLocal() as db:
            nweParam = NewParameter(
                from_date=body.fromDate,
                to_date=body.toDate,
                code=body.code,
                run_master=True,
                run_dailyBar=True,
                run_valuation=True,
                run_summary=True,
            )
            body.mgmtId = (
                CacheMgmtService(CacheMgmtRepository()).create(db, nweParam).id
            )

    # バッチ処理　起動
    background_tasks.add_task(
        run_plain, body.fromDate, body.toDate, body.mgmtId, body.code
    )

    return {"message": "バッチ起動を受け付けました"}
