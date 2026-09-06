from datetime import date, datetime
from unittest.mock import MagicMock, patch

import pytest

from app.models import EdinetInventoryRun
from app.services.edinet_inventory import (
    EdinetInventoryService,
    inventory_start_date,
    summarize_one_day_inventory,
)

TARGET_DATE = date(2026, 8, 21)


def test_inventory_start_date_is_ten_years_before_end_date() -> None:
    end_date = date(2026, 8, 21)

    start_date = inventory_start_date(end_date)

    assert start_date == date(2016, 8, 21)


def test_inventory_start_date_handles_february_29() -> None:
    end_date = date(2024, 2, 29)

    start_date = inventory_start_date(end_date)

    assert start_date == date(2014, 2, 28)


def test_summarize_one_day_inventory_filters_listed_then_csv_flag() -> None:
    listed_sec_codes = {"72030", "130A0"}
    results = [
        {"secCode": "72030", "csvFlag": "1", "docTypeCode": "120"},
        {"secCode": "72030", "csvFlag": "0", "docTypeCode": "120"},
        {"secCode": "130A0", "csvFlag": "1", "docTypeCode": "160"},
        {"secCode": "130A0", "csvFlag": "1", "docTypeCode": "160"},
        {"secCode": "99990", "csvFlag": "1", "docTypeCode": "120"},
        {"secCode": 72030, "csvFlag": "1", "docTypeCode": "120"},
        {"secCode": None, "csvFlag": "1", "docTypeCode": "120"},
        {"csvFlag": "1", "docTypeCode": "120"},
    ]

    summary = summarize_one_day_inventory(results, listed_sec_codes)

    assert summary.total_count == 8
    assert summary.listed_match_count == 4
    assert summary.csv_flag_count == 3
    assert summary.doc_type_counts == {"120": 1, "160": 2}


def test_summarize_one_day_inventory_empty_results() -> None:
    summary = summarize_one_day_inventory([], {"130A0"})

    assert summary.total_count == 0
    assert summary.listed_match_count == 0
    assert summary.csv_flag_count == 0
    assert summary.doc_type_counts == {}


def _completed_run() -> EdinetInventoryRun:
    return EdinetInventoryRun(
        target_date=TARGET_DATE,
        status="completed",
        total_count=9,
        listed_match_count=4,
        csv_flag_count=2,
        listed_sec_code_count=8,
        error_message="old error",
    )


@patch("app.services.edinet_inventory.fetch_document_list")
@patch("app.services.edinet_inventory.fetch_listed_sec_codes")
def test_refresh_one_day_reruns_completed_and_saves_filtered_documents(
    mock_fetch_listed_sec_codes,
    mock_fetch_document_list,
) -> None:
    run = _completed_run()
    repository = MagicMock()
    repository.get_run_by_target_date.return_value = run
    run_statuses: list[str] = []

    def add_run(_db, inventory_run: EdinetInventoryRun) -> EdinetInventoryRun:
        run_statuses.append(inventory_run.status)
        return inventory_run

    repository.add_run.side_effect = add_run
    mock_fetch_listed_sec_codes.return_value = {"130A0"}
    mock_fetch_document_list.return_value = {
        "results": [
            {
                "docID": "S100A001",
                "secCode": "130A0",
                "csvFlag": "1",
                "docTypeCode": "120",
                "submitDateTime": "2026-08-21 15:00",
                "periodStart": "2025-04-01",
                "periodEnd": "2026-03-31",
            },
            {
                "docID": "S100A002",
                "secCode": "130A0",
                "csvFlag": "0",
                "docTypeCode": "120",
                "submitDateTime": "2026-08-21 16:00",
            },
            {
                "docID": "S100A003",
                "secCode": "99990",
                "csvFlag": "1",
                "docTypeCode": "120",
            },
        ]
    }
    db = MagicMock()
    service = EdinetInventoryService(repository)

    summary = service.refresh_one_day(db, TARGET_DATE)

    assert "processing" in run_statuses
    assert run.status == "completed"
    assert summary.total_count == 3
    assert summary.listed_match_count == 2
    assert summary.csv_flag_count == 1
    assert db.commit.call_count == 2
    repository.delete_documents_by_target_date.assert_called_once_with(db, TARGET_DATE)
    added_documents = repository.add_documents.call_args.args[1]
    assert len(added_documents) == 1
    saved = added_documents[0]
    assert saved.sec_code == "130A0"
    assert saved.csv_flag == "1"
    assert saved.doc_id == "S100A001"
    assert saved.submit_date_time == datetime(2026, 8, 21, 15, 0)
    assert saved.submit_date_time.tzinfo is None
    assert saved.period_start == date(2025, 4, 1)
    assert run.listed_sec_code_count == 1


@patch("app.services.edinet_inventory.fetch_document_list")
@patch("app.services.edinet_inventory.fetch_listed_sec_codes")
def test_refresh_one_day_marks_failed_and_reraises(
    mock_fetch_listed_sec_codes,
    mock_fetch_document_list,
) -> None:
    run = _completed_run()
    repository = MagicMock()
    repository.get_run_by_target_date.return_value = run
    mock_fetch_listed_sec_codes.side_effect = RuntimeError(
        "Subscription-Key=secret-should-not-be-saved"
    )
    db = MagicMock()
    service = EdinetInventoryService(repository)

    with pytest.raises(RuntimeError):
        service.refresh_one_day(db, TARGET_DATE)

    db.rollback.assert_called()
    assert run.status == "failed"
    assert run.error_message == "RuntimeError"
    assert "secret-should-not-be-saved" not in (run.error_message or "")
    db.commit.assert_called()
    repository.delete_documents_by_target_date.assert_not_called()
