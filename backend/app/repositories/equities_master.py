from app.models import JQuantsListedIssue
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

# 　selfはクラスのインスタンスメソッドとして使用するために必須の設定値、インスタンスで使用される


class JQuantsListedIssueRepository:
    def getByCode(
        self,
        db: Session,
        code: str,
    ) -> JQuantsListedIssue | None:
        statement = select(JQuantsListedIssue).where(JQuantsListedIssue.code == code)
        return db.scalar(statement)

    def getAll(
        self,
        db: Session,
    ) -> list[JQuantsListedIssue] | None:
        statement = select(JQuantsListedIssue).order_by(JQuantsListedIssue.code.asc())
        return list(db.scalars(statement).all())

    def getAllSearch(
        self,
        db: Session,
        search: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> list[JQuantsListedIssue] | None:
        statement = select(JQuantsListedIssue)

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = statement.offset(offset).limit(limit)

        # ==========サーチ==========
        if search:
            statement = statement.where(
                or_(
                    JQuantsListedIssue.code.like(f"%{search}%"),
                    JQuantsListedIssue.company_name.like(f"%{search}%"),
                    JQuantsListedIssue.company_name_en.like(f"%{search}%"),
                )
            ).order_by(JQuantsListedIssue.code.asc())

        return list(db.scalars(statement).all())

    def create(self, db: Session, data: JQuantsListedIssue) -> JQuantsListedIssue:
        db.add(data)
        return data

    def createOrUpdate(
        self, db: Session, data: JQuantsListedIssue
    ) -> JQuantsListedIssue:
        source = db.merge(data)
        return source

    def delete(self, db: Session, data: JQuantsListedIssue) -> None:
        db.delete(data)
