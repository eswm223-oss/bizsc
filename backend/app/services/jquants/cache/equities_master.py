from datetime import date, timedelta

from app.clients.jquants import (
    fetch_listed_issues,
)
from app.db.database import SessionLocal
from app.models import JQuantsListedIssue
from app.repositories.equities_master import JQuantsListedIssueRepository
from app.services.jquants.db.equities_master import equities_master_service


def cache_equities_master(fromDate: date, toDate: date):

    service = equities_master_service(JQuantsListedIssueRepository())
    for i in range((toDate - fromDate).days + 1):
        current_date = fromDate + timedelta(days=i)

        # APIから取得
        result = fetch_listed_issues(current_date)
        with SessionLocal() as db:
            # DBにキャッシュ
            for company in result["data"]:
                print(company["Code"], company["CoName"])
                data = JQuantsListedIssue(
                    date=date.fromisoformat(company["Date"]),
                    code=company["Code"],
                    company_name=company["CoName"],
                    company_name_en=company["CoNameEn"],
                    sector17_code=company["S17"],
                    sector17_name=company["S17Nm"],
                    sector33_code=company["S33"],
                    sector33_name=company["S33Nm"],
                    scale_category=company["ScaleCat"],
                    market_code=company["Mkt"],
                    market_name=company["MktNm"],
                    margin_code=company["Mrgn"],
                    margin_name=company["MrgnNm"],
                    product_category=company["ProdCat"],
                )
                service.createOrUpdate(db, data)
