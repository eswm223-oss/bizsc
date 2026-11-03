from app.models import JQuantsListedIssue
from app.schemas.jqunats import SearchRequest
from sqlalchemy import func, or_, select
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
        search: SearchRequest | None = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        page: int | None = None,
        limit: int | None = None,
    ) -> list[JQuantsListedIssue]:
        statement = select(JQuantsListedIssue)

        # ==========サーチ==========
        if search:
            if search.keyword:
                statement = statement.where(
                    or_(
                        JQuantsListedIssue.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            if search.targetDate:
                statement = statement.where(
                    JQuantsListedIssue.date == search.targetDate
                )
            if search.code:
                statement = statement.where(JQuantsListedIssue.code == search.code)
        # ==========ページング==========
        if page and limit:
            offset = (page - 1) * limit
            statement = statement.offset(offset).limit(limit)

        # ==========ソート==========
        sort_columns = {
            "id": JQuantsListedIssue.id,
            "date": JQuantsListedIssue.date,
            "code": JQuantsListedIssue.code,
            "company_name": JQuantsListedIssue.company_name,
            "company_name_en": JQuantsListedIssue.company_name_en,
            "sector17_code": JQuantsListedIssue.sector17_code,
            "sector17_name": JQuantsListedIssue.sector17_name,
            "sector33_code": JQuantsListedIssue.sector33_code,
            "sector33_name": JQuantsListedIssue.sector33_name,
            "scale_category": JQuantsListedIssue.scale_category,
            "market_code": JQuantsListedIssue.market_code,
            "market_name": JQuantsListedIssue.market_name,
            "margin_code": JQuantsListedIssue.margin_code,
            "margin_name": JQuantsListedIssue.margin_name,
            "product_category": JQuantsListedIssue.product_category,
            "created_at": JQuantsListedIssue.created_at,
            "updated_at": JQuantsListedIssue.updated_at,
        }
        sort_column = sort_columns.get(sort_by, JQuantsListedIssue.id)
        if sort_order == "desc":
            statement = statement.order_by(sort_column.desc())
        else:
            statement = statement.order_by(sort_column.asc())

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

    def count_all(
        self,
        db: Session,
        search: SearchRequest | None = None,
    ) -> int:
        statement = select(func.count(JQuantsListedIssue.id))

        if search:
            if search.keyword:
                statement = statement.where(
                    or_(
                        JQuantsListedIssue.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            if search.targetDate:
                statement = statement.where(
                    JQuantsListedIssue.date == search.targetDate
                )
            if search.code:
                statement = statement.where(JQuantsListedIssue.code == search.code)

        return db.scalar(statement) or 0
