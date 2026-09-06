from datetime import date

from app.services.edinet_inventory import (
    inventory_start_date,
    summarize_one_day_inventory,
)


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
