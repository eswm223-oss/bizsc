from app.models import ScreeningResult
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session


class ScreeningResultRepository:
    def get_by_id(
        self,
        db: Session,
        id: int,
    ) -> ScreeningResult | None:
        statement = select(ScreeningResult).where(ScreeningResult.id == id)
        return db.scalar(statement)

    def crate_or_update(self, db: Session, data: ScreeningResult) -> ScreeningResult:
        source = db.merge(data)
        db.refresh(data)
        db.commit()
        return source

    def delete(self, db: Session, data: ScreeningResult) -> None:
        db.delete(data)
        db.commit()

    def delete_by_group(self, db: Session, group_id) -> None:
        db.execute(delete(ScreeningResult).where(ScreeningResult.group_id == group_id))
        db.commit()

    # --------------------------------------------
    # Search処理
    # --------------------------------------------

    def get_result(
        self,
        db: Session,
        group_id: int,
        company_code: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> list[ScreeningResult]:
        statement = select(ScreeningResult)

        # ==========サーチ==========
        statement = statement.where(ScreeningResult.group_id == group_id)

        if company_code:
            statement = statement.where(ScreeningResult.company_code == company_code)

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = (
            statement.order_by(ScreeningResult.id.desc()).offset(offset).limit(limit)
        )

        return list(db.scalars(statement).all())

    def get_result_count(
        self,
        db: Session,
        group_id: int,
        company_code: str | None = None,
    ) -> int:
        statement = select(func.count(ScreeningResult.id))

        # ==========サーチ==========
        statement = statement.where(ScreeningResult.group_id == group_id)

        if company_code:
            statement = statement.where(ScreeningResult.company_code == company_code)

        return db.scalar(statement) or 0
