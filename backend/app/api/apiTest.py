from datetime import date
from app.services import UserService
from fastapi import APIRouter, Depends, status
from app.services.apiTest import ApiTestService


router = APIRouter(
    prefix="/apiTest",
    tags=["apiTest"],
)

api_test_service = ApiTestService()

@router.get("")
def get_testApiCheck() -> dict[str, str]:
    return {"status": "ok"}

@router.get(
    "/{target_date}",
    response_model=str,
)
def get_testApiRes(
    target_date: date,
) -> str:
    res = api_test_service.get_testApiRes(target_date)
    return res
