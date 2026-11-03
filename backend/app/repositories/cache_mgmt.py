from datetime import date

from app.models import CacheMgmt
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class CacheMgmtRepository:
    def getById(
        self,
        db: Session,
        id: str,
    ) -> CacheMgmt | None:
        statement = select(CacheMgmt).where(CacheMgmt.id == id)
        return db.scalar(statement)

    def create(self, db: Session, data: CacheMgmt) -> CacheMgmt:
        db.add(data)
        db.commit()
        db.refresh(data)

        return data

    def update(
        self,
        db: Session,
        data: CacheMgmt,
    ) -> CacheMgmt:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    def delete(self, db: Session, data: CacheMgmt) -> None:
        db.delete(data)
        db.commit()

    # --------------------------------------------
    # Search処理
    # --------------------------------------------

    def getAllSearch(
        self,
        db: Session,
        keyword: str | None = None,
        targetDate: date | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> list[CacheMgmt]:
        statement = select(CacheMgmt)

        # ==========サーチ==========
        if targetDate:
            statement = statement.where(CacheMgmt.from_date <= targetDate).where(
                CacheMgmt.to_date >= targetDate
            )
        if keyword:
            statement = statement.where(CacheMgmt.id.like(f"%{keyword}%"))

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = statement.order_by(CacheMgmt.id.desc()).offset(offset).limit(limit)

        return list(db.scalars(statement).all())

    def count_all(
        self,
        db: Session,
        keyword: str | None = None,
        targetDate: date | None = None,
    ) -> int:
        statement = select(func.count(CacheMgmt.id))

        # ==========サーチ==========
        if targetDate:
            statement = statement.where(CacheMgmt.from_date <= targetDate).where(
                CacheMgmt.to_date >= targetDate
            )
        if keyword:
            statement = statement.where(CacheMgmt.id.like(f"%{keyword}%"))

        return db.scalar(statement) or 0
