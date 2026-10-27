from app.models import JQuantsListedIssue
from app.repositories.equities_master import JQuantsListedIssueRepository
from sqlalchemy.orm import Session


class Equities_master_service:
    def __init__(self, repository: JQuantsListedIssueRepository) -> None:
        self.repository = repository

    def createOrUpdate(
        self, db: Session, data: JQuantsListedIssue
    ) -> JQuantsListedIssue | None:
        if data is None:
            return None

        before = self.repository.getByCode(db, data.code)
        if before is not None and before.date > data.date:
            return None

        # id生成
        data.id = data.code

        return self.repository.createOrUpdate(db, data)

    def search(
        self,
        db: Session,
        search: str | None = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        page: int = 1,
        limit: int = 50,
    ) -> tuple[list[JQuantsListedIssue], int]:
        resList = self.repository.getAllSearch(
            db=db,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            limit=limit,
        )
        resToral = self.repository.count_all(db=db, search=search)

        return resList, resToral

    def getAll(
        self,
        db: Session,
    ) -> list[JQuantsListedIssue] | None:
        return self.repository.getAll(db)

    def getByCode(self, db: Session, Code: str) -> JQuantsListedIssue | None:
        return self.repository.getByCode(db, Code)
