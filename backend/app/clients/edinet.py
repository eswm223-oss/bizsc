import csv
import io
import json
import zipfile
from datetime import date
from typing import Any, Optional

import httpx

from app.core.config import settings

DOCUMENTS_LIST_URL = "https://api.edinet-fsa.go.jp/api/v2/documents.json"
DOCUMENT_LIST_TYPE = 2
REQUEST_TIMEOUT_SECONDS = 30.0
EDINET_CODE_LIST_URL = (
    "https://disclosure2dl.edinet-fsa.go.jp/searchdocument/codelist/Edinetcode.zip"
)
EDINET_CODE_LIST_CSV_NAME = "EdinetcodeDlInfo.csv"
EDINET_CODE_LIST_ENCODING = "cp932"
LISTED_STATUS_COLUMN = "上場区分"
LISTED_STATUS_VALUE = "上場"
SEC_CODE_COLUMN = "証券コード"


class EdinetClientError(Exception):
    """EDINET Client のエラー。"""


class EdinetApiKeyNotConfiguredError(EdinetClientError):
    """EDINET APIキーが未設定の場合のエラー。"""


class EdinetHttpError(EdinetClientError):
    """EDINET API が HTTP エラーを返した場合のエラー。"""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(message)


class EdinetTimeoutError(EdinetClientError):
    """EDINET API への接続がタイムアウトした場合のエラー。"""


class EdinetInvalidJsonError(EdinetClientError):
    """EDINET API のレスポンスを JSON として解釈できない場合のエラー。"""


def fetch_document_list(target_date: date) -> Any:
    api_key = _require_api_key()
    params = {
        "date": target_date.isoformat(),
        "type": DOCUMENT_LIST_TYPE,
        "Subscription-Key": api_key,
    }

    try:
        response = httpx.get(
            DOCUMENTS_LIST_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except httpx.TimeoutException:
        raise EdinetTimeoutError("EDINET API request timed out") from None
    except httpx.RequestError:
        raise EdinetClientError("EDINET API request failed") from None

    if response.status_code != 200:
        raise EdinetHttpError(
            response.status_code,
            _http_error_message(response),
        )

    return _parse_json_body(response)


def fetch_listed_sec_codes() -> set[str]:
    zip_bytes = _download_edinet_code_list_zip()
    return _parse_listed_sec_codes_from_zip(zip_bytes)


def _download_edinet_code_list_zip() -> bytes:
    try:
        response = httpx.get(
            EDINET_CODE_LIST_URL,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except httpx.TimeoutException:
        raise EdinetTimeoutError("EDINET code list request timed out") from None
    except httpx.RequestError:
        raise EdinetClientError("EDINET code list request failed") from None

    if response.status_code != 200:
        raise EdinetHttpError(
            response.status_code,
            _http_error_message(response),
        )
    return response.content


def _parse_listed_sec_codes_from_zip(zip_bytes: bytes) -> set[str]:
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
            try:
                csv_bytes = archive.read(EDINET_CODE_LIST_CSV_NAME)
            except KeyError:
                raise EdinetClientError(
                    "EDINET code list ZIP does not contain EdinetcodeDlInfo.csv"
                ) from None
    except zipfile.BadZipFile:
        raise EdinetClientError("EDINET code list response is not a valid ZIP") from None

    try:
        csv_text = csv_bytes.decode(EDINET_CODE_LIST_ENCODING)
    except UnicodeDecodeError:
        raise EdinetClientError(
            "EDINET code list CSV is not valid CP932"
        ) from None

    stream = io.StringIO(csv_text)
    try:
        next(stream)
    except StopIteration:
        raise EdinetClientError("EDINET code list CSV is empty") from None

    reader = csv.DictReader(stream)
    if reader.fieldnames is None:
        raise EdinetClientError("EDINET code list CSV header is missing")
    if (
        LISTED_STATUS_COLUMN not in reader.fieldnames
        or SEC_CODE_COLUMN not in reader.fieldnames
    ):
        raise EdinetClientError(
            "EDINET code list CSV is missing required columns"
        )

    sec_codes: set[str] = set()
    for row in reader:
        listed_status = (row.get(LISTED_STATUS_COLUMN) or "").strip()
        sec_code = (row.get(SEC_CODE_COLUMN) or "").strip()
        if listed_status == LISTED_STATUS_VALUE and sec_code:
            sec_codes.add(sec_code)
    return sec_codes


def _require_api_key() -> str:
    api_key = settings.edinet_api_key
    if api_key is None or not api_key.strip():
        raise EdinetApiKeyNotConfiguredError(
            "EDINET API key is not configured"
        )
    return api_key


def _parse_json_body(response: httpx.Response) -> Any:
    try:
        return response.json()
    except json.JSONDecodeError:
        raise EdinetInvalidJsonError(
            "EDINET API response is not valid JSON"
        ) from None


def _http_error_message(response: httpx.Response) -> str:
    status_code = response.status_code
    default_messages = {
        400: "EDINET API returned 400 Bad Request",
        401: "EDINET API key is invalid or was not accepted",
        404: "EDINET API returned 404 Not Found",
        429: "EDINET API returned 429 Too Many Requests",
        500: "EDINET API returned 500 server error",
    }
    message = default_messages.get(
        status_code,
        f"EDINET API returned HTTP {status_code}",
    )

    edinet_message = _safe_edinet_message(response)
    if edinet_message:
        return f"{message}: {edinet_message}"
    return message


def _safe_edinet_message(response: httpx.Response) -> Optional[str]:
    try:
        payload = response.json()
    except json.JSONDecodeError:
        return None

    if not isinstance(payload, dict):
        return None

    metadata = payload.get("metadata")
    if isinstance(metadata, dict):
        metadata_message = metadata.get("message")
        if isinstance(metadata_message, str) and metadata_message:
            return metadata_message

    body_message = payload.get("message")
    if isinstance(body_message, str) and body_message:
        return body_message

    return None
