import json
from datetime import date
from typing import Any

import httpx
from app.core.config import settings

JQUANTS_BASE_URL = "https://api.jquants.com/v2"
REQUEST_TIMEOUT_SECONDS = 30.0


class JQuantsClientError(Exception):
    """J-Quants Client のエラー。"""


class JQuantsApiKeyNotConfiguredError(JQuantsClientError):
    """J-Quants APIキーが未設定の場合のエラー。"""


class JQuantsHttpError(JQuantsClientError):
    """J-Quants API が HTTP エラーを返した場合のエラー。"""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(message)


class JQuantsTimeoutError(JQuantsClientError):
    """J-Quants API への接続がタイムアウトした場合のエラー。"""


class JQuantsInvalidJsonError(JQuantsClientError):
    """J-Quants API のレスポンスが JSON ではない場合のエラー。"""


def _parse_json_body(response: httpx.Response) -> Any:
    try:
        return response.json()
    except json.JSONDecodeError:
        raise JQuantsInvalidJsonError(
            "J-Quants API response is not valid JSON"
        ) from None


# --------------------------------------------------
# APIキー
# --------------------------------------------------
def _require_api_key() -> str:
    api_key = settings.jquants_api_key

    if api_key is None or not api_key.strip():
        raise JQuantsApiKeyNotConfiguredError("J-Quants API key is not configured")

    return api_key


# --------------------------------------------------
# 上場銘柄一覧
# --------------------------------------------------
EQUITIES_MASTER_URL = f"{JQUANTS_BASE_URL}/equities/master"


def fetch_listed_issues(date: date, code: str = "") -> Any:
    api_key = _require_api_key()

    headers = {
        "x-api-key": api_key,
    }

    try:
        response = httpx.get(
            EQUITIES_MASTER_URL,
            headers=headers,
            params={"code": code, "date": date.isoformat()},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except httpx.TimeoutException:
        raise JQuantsTimeoutError("J-Quants API(master) request timed out") from None
    except httpx.RequestError:
        raise JQuantsClientError("J-Quants API(master) request failed") from None

    if response.status_code != 200:
        raise JQuantsHttpError(
            response.status_code,
            f"J-Quants API returned HTTP {response.status_code}",
        )

    return _parse_json_body(response)


# --------------------------------------------------
# 株価四本値
# --------------------------------------------------
EQUITIES_DAILY_URL = f"{JQUANTS_BASE_URL}/v2/equities/bars/daily"


def fetch_bars_daily(date: date, code: str = "") -> Any:
    api_key = _require_api_key()

    headers = {
        "x-api-key": api_key,
    }

    try:
        response = httpx.get(
            EQUITIES_DAILY_URL,
            params={"code": code, "date": date.isoformat()},
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except httpx.TimeoutException:
        raise JQuantsTimeoutError(
            "J-Quants API(bars_daily) request timed out"
        ) from None
    except httpx.RequestError:
        raise JQuantsClientError("J-Quants API(bars_daily) request failed") from None

    if response.status_code != 200:
        raise JQuantsHttpError(
            response.status_code,
            f"J-Quants API(bars_daily) returned HTTP {response.status_code}",
        )

    return _parse_json_body(response)


# --------------------------------------------------
# バリュエーション指標
# --------------------------------------------------
EQUITIES_VALUATION_URL = f"{JQUANTS_BASE_URL}/v2/equities/valuation"


def fetch_valuation(date: date, code: str = "") -> Any:
    api_key = _require_api_key()

    headers = {
        "x-api-key": api_key,
    }

    try:
        response = httpx.get(
            EQUITIES_VALUATION_URL,
            params={"code": code, "date": date.isoformat()},
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except httpx.TimeoutException:
        raise JQuantsTimeoutError("J-Quants API(valuation) request timed out") from None
    except httpx.RequestError:
        raise JQuantsClientError("J-Quants API(valuation) request failed") from None

    if response.status_code != 200:
        raise JQuantsHttpError(
            response.status_code,
            f"J-Quants API(bars_daily) returned HTTP {response.status_code}",
        )

    return _parse_json_body(response)


# --------------------------------------------------
# 財務情報
# --------------------------------------------------
EQUITIES_SUMMARY_URL = f"{JQUANTS_BASE_URL}/v2/fins/summary"


def fetch_summary(date: date, code: str = "") -> Any:
    api_key = _require_api_key()

    headers = {
        "x-api-key": api_key,
    }

    try:
        response = httpx.get(
            EQUITIES_SUMMARY_URL,
            params={"code": code, "date": date.isoformat()},
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except httpx.TimeoutException:
        raise JQuantsTimeoutError("J-Quants API(summary) request timed out") from None
    except httpx.RequestError:
        raise JQuantsClientError("J-Quants API(summary) request failed") from None

    if response.status_code != 200:
        raise JQuantsHttpError(
            response.status_code,
            f"J-Quants API(summary) returned HTTP {response.status_code}",
        )

    return _parse_json_body(response)
