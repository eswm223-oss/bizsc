from app.models import ScreeningGroup
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class ScreeningGroupRepository:
    def get_by_id(
        self,
        db: Session,
        id: int,
    ) -> ScreeningGroup | None:
        statement = select(ScreeningGroup).where(ScreeningGroup.id == id)
        return db.scalar(statement)

    def create(self, db: Session, data: ScreeningGroup) -> ScreeningGroup:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    def update(
        self,
        db: Session,
        data: ScreeningGroup,
    ) -> ScreeningGroup:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    def delete(self, db: Session, data: ScreeningGroup) -> None:
        db.delete(data)
        db.commit()

    def merge(self, db: Session, data: ScreeningGroup) -> ScreeningGroup:
        source = db.merge(data)
        db.commit()
        db.refresh(source)
        return source

    # --------------------------------------------
    # Search処理
    # --------------------------------------------

    def search(
        self,
        db: Session,
        keyword: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> list[ScreeningGroup]:
        statement = select(ScreeningGroup)

        # ==========サーチ==========
        if keyword:
            statement = statement.where(ScreeningGroup.name.like(f"%{keyword}%"))

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = (
            statement.order_by(ScreeningGroup.id.desc()).offset(offset).limit(limit)
        )

        return list(db.scalars(statement).all())

    def count_search(
        self,
        db: Session,
        keyword: str | None = None,
    ) -> int:
        statement = select(func.count(ScreeningGroup.id))

        # ==========サーチ==========
        if keyword:
            statement = statement.where(ScreeningGroup.name.like(f"%{keyword}%"))

        return db.scalar(statement) or 0
