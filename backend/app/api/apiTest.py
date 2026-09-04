from datetime import date
from app.services import UserService
from fastapi import APIRouter, Depends
from app.services.apiTest import ApiTestService
import debugpy

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

@router.get("/debug-async")
async def debug_async():
    connected = debugpy.is_client_connected()
    debugpy.breakpoint()
    result = "async"
    return {
        "connected": connected,
        "result": result,
    }


@router.get("/debug-sync")
def debug_sync():
    connected = debugpy.is_client_connected()
    debugpy.breakpoint()
    result = "sync"
    return {
        "connected": connected,
        "result": result,
    }

@router.get("/debug-status")
async def get_debug_status():
    return {
        "connected": debugpy.is_client_connected(),
    }


@router.get("")
def get_testApiCheck() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/{target_date}")
def get_testApiRes(
    target_date: date,
) -> str:
    res = api_test_service.get_testApiRes(target_date)
    return res