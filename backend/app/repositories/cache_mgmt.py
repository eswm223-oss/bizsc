from datetime import date

from app.models import CacheMgmt
from sqlalchemy import select
from sqlalchemy.orm import Session


class CacheMgmtRepository:
    def getById(
        self,
        db: Session,
        id: str,
    ) -> CacheMgmt | None:
        statement = (
            select(CacheMgmt).where(CacheMgmt.id == id).order_by(CacheMgmt.id.desc())
        )
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
        search: date | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> list[CacheMgmt] | None:
        statement = select(CacheMgmt)

        # ==========サーチ==========
        if search:
            statement = statement.where(CacheMgmt.from_date <= search).where(
                CacheMgmt.to_date >= search
            )

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = statement.order_by(CacheMgmt.id.desc()).offset(offset).limit(limit)

        return list(db.scalars(statement).all())
