import json

import httpx
import pytest

from app.clients.jquants import (
    EQUITIES_MASTER_URL,
    JQuantsApiKeyNotConfiguredError,
    JQuantsHttpError,
    JQuantsInvalidJsonError,
    JQuantsTimeoutError,
    fetch_listed_issues,
)


def test_fetch_listed_issues_success(monkeypatch):
    monkeypatch.setattr(
        "app.clients.jquants.settings.jquants_api_key",
        "test-api-key",
    )

    def mock_get(url, headers, timeout):
        assert url == EQUITIES_MASTER_URL
        assert headers == {
            "x-api-key": "test-api-key",
        }

        request = httpx.Request("GET", url)

        return httpx.Response(
            200,
            request=request,
            json={
                "data": [
                    {
                        "Code": "13010",
                        "CompanyName": "テスト株式会社",
                    }
                ]
            },
        )

    monkeypatch.setattr(
        "app.clients.jquants.httpx.get",
        mock_get,
    )

    result = fetch_listed_issues()

    assert result == {
        "data": [
            {
                "Code": "13010",
                "CompanyName": "テスト株式会社",
            }
        ]
    }


def test_fetch_listed_issues_api_key_not_configured(monkeypatch):
    monkeypatch.setattr(
        "app.clients.jquants.settings.jquants_api_key",
        None,
    )

    with pytest.raises(JQuantsApiKeyNotConfiguredError):
        fetch_listed_issues()


def test_fetch_listed_issues_http_error(monkeypatch):
    monkeypatch.setattr(
        "app.clients.jquants.settings.jquants_api_key",
        "test-api-key",
    )

    def mock_get(url, headers, timeout):
        request = httpx.Request("GET", url)

        return httpx.Response(
            429,
            request=request,
        )

    monkeypatch.setattr(
        "app.clients.jquants.httpx.get",
        mock_get,
    )

    with pytest.raises(JQuantsHttpError) as exc_info:
        fetch_listed_issues()

    assert exc_info.value.status_code == 429


def test_fetch_listed_issues_timeout(monkeypatch):
    monkeypatch.setattr(
        "app.clients.jquants.settings.jquants_api_key",
        "test-api-key",
    )

    def mock_get(url, headers, timeout):
        raise httpx.TimeoutException(
            "timeout"
        )

    monkeypatch.setattr(
        "app.clients.jquants.httpx.get",
        mock_get,
    )

    with pytest.raises(JQuantsTimeoutError):
        fetch_listed_issues()


def test_fetch_listed_issues_invalid_json(monkeypatch):
    monkeypatch.setattr(
        "app.clients.jquants.settings.jquants_api_key",
        "test-api-key",
    )

    def mock_get(url, headers, timeout):
        request = httpx.Request("GET", url)

        response = httpx.Response(
            200,
            request=request,
            content=b"invalid-json",
        )

        def invalid_json():
            raise json.JSONDecodeError(
                "invalid json",
                "invalid-json",
                0,
            )

        response.json = invalid_json
        return response

    monkeypatch.setattr(
        "app.clients.jquants.httpx.get",
        mock_get,
    )

    with pytest.raises(JQuantsInvalidJsonError):
        fetch_listed_issues()