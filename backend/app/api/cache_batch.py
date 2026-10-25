from app.schemas.cache_batch import CacheBatchRequest
from app.services.batches.jquants_sync import run_plain
from fastapi import APIRouter, BackgroundTasks, status

router = APIRouter(prefix="/batches", tags=["batches"])


@router.post(
    "/jquants/cache/plain",
    status_code=status.HTTP_202_ACCEPTED,
)
def start_jquants_plain_cache(
    body: CacheBatchRequest, background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        run_plain, body.fromDate, body.toDate, body.mgmtId, body.code
    )

    return {"message": "バッチ起動を受け付けました"}
