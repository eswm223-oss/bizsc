import datetime

from sqlalchemy.orm import Session

from backend.app.models import JQuantsListedIssue
from backend.app.repositories.equities_master import JQuantsListedIssueRepository


class equities_master_service:
    def __init__(self, repository: JQuantsListedIssueRepository) -> None:
        self.repository = repository

    def createOrUpdate(
        self, db: Session, data: JQuantsListedIssue
    ) -> JQuantsListedIssue | None:
        if data is None:
            return None
        dateStamp = datetime.datetime.now()

        # id生成
        data.id = data.code + "-" + data.date.strftime("%Y%m%d")

        # 登録日時、更新日
        data.created_at = dateStamp
        data.updated_at = data.updated_at if data.updated_at is None else dateStamp

        return self.repository.createOrUpdate(db, data)

    def search(
        self,
        db: Session,
        search: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> list[JQuantsListedIssue] | None:
        return self.repository.getAllSearch(db, search, page, limit)

    def getAll(
        self,
        db: Session,
    ) -> list[JQuantsListedIssue] | None:
        return self.repository.getAll(db)

    def getByCode(self, db: Session, Code: str) -> JQuantsListedIssue | None:
        return self.repository.getByCode(db, Code)
