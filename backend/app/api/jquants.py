from datetime import date

from app.db.database import get_db
from app.repositories import (
    JQuantsDailyQuoteRepository,
    JQuantsFinancialSummaryRepository,
    JQuantsListedIssueRepository,
    JQuantsValuationRepository,
)
from app.schemas.jqunats import (
    DailyQuoteListResponse,
    DailyQuoteResponse,
    MasterListResponse,
    MasterResponse,
    SearchRequest,
    SummaryListResponse,
    SummaryResponse,
    ValuationListResponse,
    ValuationResponse,
)
from app.services.jquants.db.daily_quote import Daily_quote_service
from app.services.jquants.db.equities_master import Equities_master_service
from app.services.jquants.db.financial_summary import Financial_summary_service
from app.services.jquants.db.valuation import Valuation_service
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

master_service = Equities_master_service(JQuantsListedIssueRepository())
daily_quote_service = Daily_quote_service(JQuantsDailyQuoteRepository())
summary_service = Financial_summary_service(JQuantsFinancialSummaryRepository())
valuation_service = Valuation_service(JQuantsValuationRepository())


router = APIRouter(
    prefix="/jquants",
    tags=["jquants"],
)


@router.get(
    "/master",
    response_model=MasterListResponse,
)
def get_masters(
    search: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> MasterListResponse:
    data, total = master_service.search(
        db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )

    return MasterListResponse(
        data=[MasterResponse.model_validate(record) for record in data],
        total=total,
    )


@router.get(
    "/valuation",
    response_model=ValuationListResponse,
)
def get_valuation(
    keyword: str | None = None,
    fromDate: date | None = None,
    todate: date | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> ValuationListResponse:
    search = SearchRequest(keyword=keyword, dateFrom=fromDate, dateTo=todate)
    data, total = valuation_service.search(
        db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )

    return ValuationListResponse(
        data=[ValuationResponse.model_validate(record) for record in data],
        total=total,
    )


@router.get(
    "/dailyquote",
    response_model=DailyQuoteListResponse,
)
def get_daily_quote(
    keyword: str | None = None,
    fromDate: date | None = None,
    todate: date | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> DailyQuoteListResponse:
    search = SearchRequest(keyword=keyword, dateFrom=fromDate, dateTo=todate)
    data, total = daily_quote_service.search(
        db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )

    return DailyQuoteListResponse(
        data=[DailyQuoteResponse.model_validate(record) for record in data],
        total=total,
    )


@router.get(
    "/summary",
    response_model=SummaryListResponse,
)
def get_summary_quote(
    keyword: str | None = None,
    fromDate: date | None = None,
    todate: date | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> SummaryListResponse:
    search = SearchRequest(keyword=keyword, dateFrom=fromDate, dateTo=todate)
    data, total = summary_service.search(
        db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )

    return SummaryListResponse(
        data=[SummaryResponse.model_validate(record) for record in data],
        total=total,
    )
