from datetime import date
from app.services import UserService
from fastapi import APIRouter, Depends, status
from app.services.apiTest import ApiTestService
import os
import threading
import debugpy

router = APIRouter(
    prefix="/apiTest",
    tags=["apiTest"],
)

api_test_service = ApiTestService()

@router.get("")
async def get_testApiCheck() -> dict[str, str]:
    return {"status": "ok"}

@router.get(
    "/{target_date}",
    response_model=str,
)
async def get_testApiRes(
    target_date: date,
) -> str:
    res = api_test_service.get_testApiRes(target_date)
    return res

@router.get("/debug-status")
async def get_debug_status():
    return {
        "connected": debugpy.is_client_connected(),
        "pid": os.getpid(),
        "thread": threading.current_thread().name,
        "file": __file__,
    }