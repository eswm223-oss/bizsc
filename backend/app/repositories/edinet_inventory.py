from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import EdinetDocument, EdinetInventoryRun


class EdinetInventoryRepository:
    def get_documents_by_target_date(
        self,
        db: Session,
        target_date: date,
    ) -> list[EdinetDocument]:
        statement = select(EdinetDocument).where(
            EdinetDocument.target_date == target_date
        )
        return list(db.scalars(statement).all())

    def delete_documents_by_target_date(
        self,
        db: Session,
        target_date: date,
    ) -> None:
        db.execute(
            delete(EdinetDocument).where(
                EdinetDocument.target_date == target_date
            )
        )
        db.flush()

    def add_documents(
        self,
        db: Session,
        documents: list[EdinetDocument],
    ) -> list[EdinetDocument]:
        db.add_all(documents)
        db.flush()
        return documents

    def get_run_by_target_date(
        self,
        db: Session,
        target_date: date,
    ) -> EdinetInventoryRun | None:
        statement = select(EdinetInventoryRun).where(
            EdinetInventoryRun.target_date == target_date
        )
        return db.scalar(statement)

    def add_run(
        self,
        db: Session,
        run: EdinetInventoryRun,
    ) -> EdinetInventoryRun:
        db.add(run)
        db.flush()
        return run
