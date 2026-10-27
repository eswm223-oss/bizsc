from app.models import JQuantsListedIssue, JQuantsValuation
from app.schemas.jqunats import SearchRequest
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session


class JQuantsValuationRepository:
    def getByCode(
        self,
        db: Session,
        code: str,
    ) -> list[JQuantsValuation] | None:
        statement = (
            select(JQuantsValuation)
            .where(JQuantsValuation.code == code)
            .order_by(JQuantsValuation.date.desc())
        )
        return list(db.scalars(statement).all())

    def create(self, db: Session, data: JQuantsValuation) -> JQuantsValuation:
        db.add(data)
        return data

    def createOrUpdate(self, db: Session, data: JQuantsValuation) -> JQuantsValuation:
        source = db.merge(data)
        return source

    def delete(self, db: Session, data: JQuantsValuation) -> None:
        db.delete(data)

    # --------------------------------------------
    # Search処理
    # --------------------------------------------

    def getAllSearch(
        self,
        db: Session,
        search: SearchRequest | None = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        page: int = 1,
        limit: int = 50,
    ) -> list[JQuantsValuation]:
        statement = select(JQuantsValuation)

        # ==========サーチ==========
        if search:
            statement = (
                statement.outerjoin(
                    JQuantsListedIssue,
                    JQuantsValuation.code == JQuantsListedIssue.code,
                )
                .where(JQuantsValuation.date.between(search.dateFrom, search.dateTo))
                .where(
                    or_(
                        JQuantsValuation.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            )

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = (
            statement.order_by(
                JQuantsValuation.code.asc(), JQuantsValuation.date.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        # ==========ソート==========
        sort_columns = {
            "id": JQuantsValuation.id,
            "date": JQuantsValuation.date,
            "code": JQuantsValuation.code,
            "eps": JQuantsValuation.eps,
            "forward_eps": JQuantsValuation.forward_eps,
            "bps": JQuantsValuation.bps,
            "roe": JQuantsValuation.roe,
            "forward_roe": JQuantsValuation.forward_roe,
            "per": JQuantsValuation.per,
            "forward_per": JQuantsValuation.forward_per,
            "pbr": JQuantsValuation.pbr,
            "market_cap": JQuantsValuation.market_cap,
            "created_at": JQuantsValuation.created_at,
            "updated_at": JQuantsValuation.updated_at,
        }
        sort_column = sort_columns.get(sort_by, JQuantsValuation.id)
        if sort_order == "desc":
            statement = statement.order_by(sort_column.desc())
        else:
            statement = statement.order_by(sort_column.asc())

        return list(db.scalars(statement).all())

    def count_all(
        self,
        db: Session,
        search: SearchRequest | None = None,
    ) -> int:
        statement = select(func.count(JQuantsValuation.id))

        if search:
            statement = (
                statement.outerjoin(
                    JQuantsListedIssue,
                    JQuantsValuation.code == JQuantsListedIssue.code,
                )
                .where(JQuantsValuation.date.between(search.dateFrom, search.dateTo))
                .where(
                    or_(
                        JQuantsValuation.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            )

        return db.scalar(statement) or 0
