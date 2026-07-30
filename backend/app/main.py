from fastapi import (
    Depends, 
    FastAPI,
    APIRouter,
)
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db

from app.api.users import router as users_router
from app.api.health import router as health_router

from app.core.exception_handlers import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
#CORSエラー対策フロントが5173、バックが8000のため
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_exception_handlers(app)

#Router
app.include_router(users_router)
app.include_router(health_router)

@app.get("/")
def root():
    return {
        "message": settings.app_name
    }

@app.get("/health")
def check_database(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }