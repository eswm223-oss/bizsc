from datetime import date

import debugpy
from fastapi import APIRouter

from app.services.apiTest import ApiTestService


router = APIRouter(
    prefix="/apiTest",
    tags=["apiTest"],
)

api_test_service = ApiTestService()


@router.get("")
def get_testApiCheck() -> dict[str, str]:
    debugpy.breakpoint()
    return {"status": "ok"}


# 動的ルートは最後に置く
@router.get(
    "/{target_date}",
    response_model=str,
)
def get_testApiRes(
    target_date: date,
) -> str:
    res = api_test_service.get_testApiRes(target_date)
    return res