import logging

from app.services.jquants.cache.jquants_cache import jquants_cache

logger = logging.getLogger(__name__)


def run_cache(mgmtId: str) -> str:
    try:
        logger.info("J-Quantsキャッシュ処理バッチ：開始")

        # キャッシュ処理
        result = jquants_cache(mgmtId)

        if result["status"] == "error":
            raise ValueError(result["message"])

        logger.info("J-Quants：キャッシュ処理バッチ：正常終了")

    except Exception:
        logger.exception(f"J-Quants：キャッシュ処理バッチ：異常終了:{Exception}")
        raise

    return mgmtId
