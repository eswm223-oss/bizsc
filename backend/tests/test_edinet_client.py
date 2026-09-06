import io
import zipfile
from datetime import date
from unittest.mock import patch

import httpx
import pytest

from app.clients.edinet import (
    DOCUMENTS_LIST_URL,
    EDINET_CODE_LIST_URL,
    EdinetApiKeyNotConfiguredError,
    EdinetClientError,
    EdinetHttpError,
    EdinetInvalidJsonError,
    EdinetTimeoutError,
    fetch_document_list,
    fetch_listed_sec_codes,
    _parse_listed_sec_codes_from_zip,
)

FAKE_API_KEY = "test-edinet-key-secret"
TARGET_DATE = date(2026, 8, 21)
SAFE_REQUEST_URL = "https://api.edinet-fsa.go.jp/api/v2/documents.json"


def _mock_response(status_code: int, **kwargs: object) -> httpx.Response:
    request = httpx.Request(
        "GET",
        f"{SAFE_REQUEST_URL}?date=2026-08-21&type=2&Subscription-Key={FAKE_API_KEY}",
    )
    return httpx.Response(status_code, request=request, **kwargs)


def _assert_no_secret_in_exception(exc: BaseException) -> None:
    message = str(exc)
    assert FAKE_API_KEY not in message
    assert f"Subscription-Key={FAKE_API_KEY}" not in message
    assert f"{SAFE_REQUEST_URL}?" not in message


@patch("app.clients.edinet.settings")
@patch("app.clients.edinet.httpx.get")
def test_fetch_document_list_sends_date_type_and_subscription_key(
    mock_get,
    mock_settings,
) -> None:
    mock_settings.edinet_api_key = FAKE_API_KEY
    mock_get.return_value = _mock_response(
        200,
        json={"metadata": {"status": "200", "message": "OK"}, "results": []},
    )

    payload = fetch_document_list(TARGET_DATE)

    mock_get.assert_called_once()
    _args, kwargs = mock_get.call_args
    assert _args[0] == DOCUMENTS_LIST_URL
    assert kwargs["params"]["date"] == "2026-08-21"
    assert kwargs["params"]["type"] == 2
    assert kwargs["params"]["Subscription-Key"] == FAKE_API_KEY
    assert payload["metadata"]["status"] == "200"


@patch("app.clients.edinet.settings")
@patch("app.clients.edinet.httpx.get")
def test_fetch_document_list_raises_when_api_key_is_missing(
    mock_get,
    mock_settings,
) -> None:
    mock_settings.edinet_api_key = None

    with pytest.raises(EdinetApiKeyNotConfiguredError) as exc_info:
        fetch_document_list(TARGET_DATE)

    mock_get.assert_not_called()
    _assert_no_secret_in_exception(exc_info.value)


@patch("app.clients.edinet.settings")
@patch("app.clients.edinet.httpx.get")
def test_fetch_document_list_raises_http_error_on_429_without_retry(
    mock_get,
    mock_settings,
) -> None:
    mock_settings.edinet_api_key = FAKE_API_KEY
    mock_get.return_value = _mock_response(
        429,
        json={"metadata": {"status": "429", "message": "Too Many Requests"}},
    )

    with pytest.raises(EdinetHttpError) as exc_info:
        fetch_document_list(TARGET_DATE)

    assert exc_info.value.status_code == 429
    assert mock_get.call_count == 1
    _assert_no_secret_in_exception(exc_info.value)


@patch("app.clients.edinet.settings")
@patch("app.clients.edinet.httpx.get")
def test_fetch_document_list_raises_timeout_error(
    mock_get,
    mock_settings,
) -> None:
    mock_settings.edinet_api_key = FAKE_API_KEY
    mock_get.side_effect = httpx.TimeoutException("timed out")

    with pytest.raises(EdinetTimeoutError) as exc_info:
        fetch_document_list(TARGET_DATE)

    mock_get.assert_called_once()
    _assert_no_secret_in_exception(exc_info.value)


@patch("app.clients.edinet.settings")
@patch("app.clients.edinet.httpx.get")
def test_fetch_document_list_raises_invalid_json_error(
    mock_get,
    mock_settings,
) -> None:
    mock_settings.edinet_api_key = FAKE_API_KEY
    mock_get.return_value = _mock_response(200, text="not-json")

    with pytest.raises(EdinetInvalidJsonError) as exc_info:
        fetch_document_list(TARGET_DATE)

    _assert_no_secret_in_exception(exc_info.value)


def _code_list_csv(
    rows: list[tuple[str, str]],
    metadata: str = "ダウンロード日:2026-09-06",
) -> str:
    lines = [
        metadata,
        "ＥＤＩＮＥＴコード,上場区分,証券コード",
    ]
    for listed_status, sec_code in rows:
        lines.append(f"E00001,{listed_status},{sec_code}")
    return "\n".join(lines) + "\n"


def _code_list_zip_bytes(csv_text: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("EdinetcodeDlInfo.csv", csv_text.encode("cp932"))
    return buffer.getvalue()


def test_parse_listed_sec_codes_keeps_strings_and_filters_rows() -> None:
    zip_bytes = _code_list_zip_bytes(
        _code_list_csv(
            [
                ("上場", "72030"),
                ("上場", "72030"),
                ("上場", "01230"),
                ("非上場", "99990"),
                ("上場", ""),
                ("上場", "   "),
                (" 上場 ", "13010"),
            ]
        )
    )

    sec_codes = _parse_listed_sec_codes_from_zip(zip_bytes)

    assert sec_codes == {"72030", "01230", "13010"}
    assert all(isinstance(sec_code, str) for sec_code in sec_codes)


@patch("app.clients.edinet.httpx.get")
def test_fetch_listed_sec_codes_downloads_official_zip(mock_get) -> None:
    zip_bytes = _code_list_zip_bytes(
        _code_list_csv([("上場", "72030"), ("非上場", "11110")])
    )
    request = httpx.Request("GET", EDINET_CODE_LIST_URL)
    mock_get.return_value = httpx.Response(
        200,
        request=request,
        content=zip_bytes,
    )

    sec_codes = fetch_listed_sec_codes()

    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == EDINET_CODE_LIST_URL
    assert "params" not in kwargs or "Subscription-Key" not in kwargs.get("params", {})
    assert sec_codes == {"72030"}


@patch("app.clients.edinet.httpx.get")
def test_fetch_listed_sec_codes_raises_timeout_error(mock_get) -> None:
    mock_get.side_effect = httpx.TimeoutException("timed out")

    with pytest.raises(EdinetTimeoutError):
        fetch_listed_sec_codes()


def test_parse_listed_sec_codes_raises_when_csv_is_missing() -> None:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("other.csv", "x".encode("cp932"))

    with pytest.raises(EdinetClientError):
        _parse_listed_sec_codes_from_zip(buffer.getvalue())
