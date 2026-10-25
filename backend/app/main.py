from app.api.apiTest import router as apiTest_router
from app.api.cache_batch import router as cache_batch_router
from app.api.health import router as health_router
from app.api.users import router as users_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.db.database import get_db
from fastapi import (
    Depends,
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()
# CORSエラー対策フロントが5173、バックが8000のため
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_exception_handlers(app)

# Router
app.include_router(users_router)
app.include_router(health_router)
app.include_router(apiTest_router)
app.include_router(cache_batch_router)


@app.get("/")
def root():
    return {"message": settings.app_name}


@app.get("/health")
def check_database(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
