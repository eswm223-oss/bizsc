from app.models import JQuantsFinancialSummary, JQuantsListedIssue
from app.schemas.jqunats import SearchRequest
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session


class JQuantsFinancialSummaryRepository:
    def getByCode(
        self,
        db: Session,
        code: str,
    ) -> list[JQuantsFinancialSummary] | None:
        statement = (
            select(JQuantsFinancialSummary)
            .where(JQuantsFinancialSummary.code == code)
            .order_by(JQuantsFinancialSummary.disclosure_date.desc())
        )
        return list(db.scalars(statement).all())

    def create(
        self, db: Session, data: JQuantsFinancialSummary
    ) -> JQuantsFinancialSummary:
        db.add(data)
        return data

    def createOrUpdate(
        self, db: Session, data: JQuantsFinancialSummary
    ) -> JQuantsFinancialSummary:
        source = db.merge(data)
        return source

    def delete(self, db: Session, data: JQuantsFinancialSummary) -> None:
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
    ) -> list[JQuantsFinancialSummary]:
        statement = select(JQuantsFinancialSummary)

        # ==========サーチ==========
        if search:
            statement = (
                statement.outerjoin(
                    JQuantsListedIssue,
                    JQuantsFinancialSummary.code == JQuantsListedIssue.code,
                )
                .where(
                    JQuantsFinancialSummary.disclosure_date.between(
                        search.dateFrom, search.dateTo
                    )
                )
                .where(
                    or_(
                        JQuantsFinancialSummary.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            )

        # ==========ページング==========
        offset = (page - 1) * limit
        statement = (
            statement.order_by(
                JQuantsFinancialSummary.code.asc(),
                JQuantsFinancialSummary.disclosure_date.desc(),
            )
            .offset(offset)
            .limit(limit)
        )

        # ==========ソート==========
        sort_columns = {
            "id": JQuantsFinancialSummary.id,
            "disclosure_date": JQuantsFinancialSummary.disclosure_date,
            "disclosure_time": JQuantsFinancialSummary.disclosure_time,
            "code": JQuantsFinancialSummary.code,
            "disclosure_number": JQuantsFinancialSummary.disclosure_number,
            "document_type": JQuantsFinancialSummary.document_type,
            "current_period_type": JQuantsFinancialSummary.current_period_type,
            "current_period_start": JQuantsFinancialSummary.current_period_start,
            "current_period_end": JQuantsFinancialSummary.current_period_end,
            "current_fiscal_year_start": JQuantsFinancialSummary.current_fiscal_year_start,
            "current_fiscal_year_end": JQuantsFinancialSummary.current_fiscal_year_end,
            "sales": JQuantsFinancialSummary.sales,
            "operating_profit": JQuantsFinancialSummary.operating_profit,
            "ordinary_profit": JQuantsFinancialSummary.ordinary_profit,
            "net_profit": JQuantsFinancialSummary.net_profit,
            "eps": JQuantsFinancialSummary.eps,
            "diluted_eps": JQuantsFinancialSummary.diluted_eps,
            "total_assets": JQuantsFinancialSummary.total_assets,
            "equity": JQuantsFinancialSummary.equity,
            "shareholders_equity": JQuantsFinancialSummary.shareholders_equity,
            "equity_ratio": JQuantsFinancialSummary.equity_ratio,
            "bps": JQuantsFinancialSummary.bps,
            "roe": JQuantsFinancialSummary.roe,
            "cash_flow_operating": JQuantsFinancialSummary.cash_flow_operating,
            "cash_flow_investing": JQuantsFinancialSummary.cash_flow_investing,
            "cash_flow_financing": JQuantsFinancialSummary.cash_flow_financing,
            "cash_and_equivalents": JQuantsFinancialSummary.cash_and_equivalents,
            "dividend_annual": JQuantsFinancialSummary.dividend_annual,
            "forecast_dividend_annual": JQuantsFinancialSummary.forecast_dividend_annual,
            "next_forecast_dividend_annual": JQuantsFinancialSummary.next_forecast_dividend_annual,
            "annual_payout_ratio": JQuantsFinancialSummary.annual_payout_ratio,
            "forecast_annual_payout_ratio": JQuantsFinancialSummary.forecast_annual_payout_ratio,
            "shares_outstanding": JQuantsFinancialSummary.shares_outstanding,
            "treasury_shares": JQuantsFinancialSummary.treasury_shares,
            "average_shares": JQuantsFinancialSummary.average_shares,
            "forecast_sales_2q": JQuantsFinancialSummary.forecast_sales_2q,
            "forecast_operating_profit_2q": JQuantsFinancialSummary.forecast_operating_profit_2q,
            "forecast_ordinary_profit_2q": JQuantsFinancialSummary.forecast_ordinary_profit_2q,
            "forecast_net_profit_2q": JQuantsFinancialSummary.forecast_net_profit_2q,
            "forecast_eps_2q": JQuantsFinancialSummary.forecast_eps_2q,
            "forecast_sales": JQuantsFinancialSummary.forecast_sales,
            "forecast_operating_profit": JQuantsFinancialSummary.forecast_operating_profit,
            "forecast_ordinary_profit": JQuantsFinancialSummary.forecast_ordinary_profit,
            "forecast_net_profit": JQuantsFinancialSummary.forecast_net_profit,
            "forecast_eps": JQuantsFinancialSummary.forecast_eps,
            "next_forecast_sales_2q": JQuantsFinancialSummary.next_forecast_sales_2q,
            "next_forecast_operating_profit_2q": JQuantsFinancialSummary.next_forecast_operating_profit_2q,
            "next_forecast_ordinary_profit_2q": JQuantsFinancialSummary.next_forecast_ordinary_profit_2q,
            "next_forecast_net_profit_2q": JQuantsFinancialSummary.next_forecast_net_profit_2q,
            "next_forecast_eps_2q": JQuantsFinancialSummary.next_forecast_eps_2q,
            "next_forecast_sales": JQuantsFinancialSummary.next_forecast_sales,
            "next_forecast_operating_profit": JQuantsFinancialSummary.next_forecast_operating_profit,
            "next_forecast_ordinary_profit": JQuantsFinancialSummary.next_forecast_ordinary_profit,
            "next_forecast_net_profit": JQuantsFinancialSummary.next_forecast_net_profit,
            "next_forecast_eps": JQuantsFinancialSummary.next_forecast_eps,
            "created_at": JQuantsFinancialSummary.created_at,
            "updated_at": JQuantsFinancialSummary.updated_at,
        }
        sort_column = sort_columns.get(sort_by, JQuantsFinancialSummary.id)
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
        statement = select(func.count(JQuantsFinancialSummary.id))

        if search:
            statement = (
                statement.outerjoin(
                    JQuantsListedIssue,
                    JQuantsFinancialSummary.code == JQuantsListedIssue.code,
                )
                .where(
                    JQuantsFinancialSummary.disclosure_date.between(
                        search.dateFrom, search.dateTo
                    )
                )
                .where(
                    or_(
                        JQuantsFinancialSummary.code.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name.like(f"%{search.keyword}%"),
                        JQuantsListedIssue.company_name_en.like(f"%{search.keyword}%"),
                    )
                )
            )

        return db.scalar(statement) or 0
