import logging
from datetime import date

from app.db.database import get_db
from app.repositories import CacheMgmtRepository
from app.services.jquants.cache.jquants_cache import jquants_cache
from app.services.jquants.db.cache_manage import (
    CacheMgmtService,
    NewParameter,
)
from fastapi import Depends

logger = logging.getLogger(__name__)


def run_plain(
    fromDate: date, toDate: date, mgmtId: str | None = None, code: str = ""
) -> None:
    try:
        logger.info("J-Quantsキャッシュ処理バッチ：開始")

        # ステイタス準備
        db = Depends(get_db)
        if mgmtId is None:
            nweParam = NewParameter(
                from_date=fromDate,
                to_date=toDate,
                code=code,
                run_master=True,
                run_dailyBar=True,
                run_valuation=True,
                run_summary=True,
            )
            mgmtId = CacheMgmtService(CacheMgmtRepository()).create(db, nweParam).id

        # キャッシュ処理
        result = jquants_cache(fromDate, toDate, mgmtId, code)

        if result["status"] == "error":
            raise ValueError(result["message"])

        logger.info("J-Quants：キャッシュ処理バッチ：正常終了")

    except Exception:
        logger.exception(f"J-Quants：キャッシュ処理バッチ：異常終了:{Exception}")
        raise
