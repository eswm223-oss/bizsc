from app.models import ScreeningRule
from sqlalchemy import delete, select
from sqlalchemy.orm import Session


class ScreeningRuleRepository:
    def get_by_id(
        self,
        db: Session,
        id: int,
    ) -> ScreeningRule | None:
        statement = select(ScreeningRule).where(ScreeningRule.id == id)
        return db.scalar(statement)

    def crate_or_update(self, db: Session, data: ScreeningRule) -> ScreeningRule:
        source = db.merge(data)
        db.refresh(source)
        db.commit()
        return source

    def delete(self, db: Session, data: ScreeningRule) -> None:
        db.delete(data)
        db.commit()

    def delete_by_group(self, db: Session, group_id) -> None:
        db.execute(delete(ScreeningRule).where(ScreeningRule.group_id == group_id))
        db.commit()

    def get_by_group(
        self,
        db: Session,
        group_id: int,
    ) -> list[ScreeningRule]:
        statement = select(ScreeningRule)
        statement = statement.where(ScreeningRule.group_id == group_id)

        return list(db.scalars(statement).all())
