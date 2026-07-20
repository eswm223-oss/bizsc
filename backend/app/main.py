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

from app.core.exception_handlers import register_exception_handlers


app = FastAPI()
register_exception_handlers(app)
app.include_router(users_router)

@app.get("/")
def root():
    return {
        "message": settings.app_name
    }

@app.get("/health/db")
def check_database(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }