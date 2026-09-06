from collections import Counter
from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class OneDayInventorySummary:
    total_count: int
    listed_match_count: int
    csv_flag_count: int
    doc_type_counts: dict[str, int]


def inventory_start_date(end_date: date) -> date:
    try:
        return end_date.replace(year=end_date.year - 10)
    except ValueError:
        return date(end_date.year - 10, end_date.month, 28)


def summarize_one_day_inventory(
    results: Any,
    listed_sec_codes: set[str],
) -> OneDayInventorySummary:
    documents = results if isinstance(results, list) else []
    listed_matches = [
        document
        for document in documents
        if _sec_code_matches_listed(document, listed_sec_codes)
    ]
    csv_documents = [
        document
        for document in listed_matches
        if isinstance(document, dict) and document.get("csvFlag") == "1"
    ]
    doc_type_counts = Counter(
        _doc_type_code(document) for document in csv_documents
    )
    return OneDayInventorySummary(
        total_count=len(documents),
        listed_match_count=len(listed_matches),
        csv_flag_count=len(csv_documents),
        doc_type_counts=dict(doc_type_counts),
    )


def _sec_code_matches_listed(document: Any, listed_sec_codes: set[str]) -> bool:
    if not isinstance(document, dict):
        return False
    sec_code = document.get("secCode")
    return isinstance(sec_code, str) and sec_code in listed_sec_codes


def _doc_type_code(document: dict[str, Any]) -> str:
    doc_type_code = document.get("docTypeCode")
    if isinstance(doc_type_code, str):
        return doc_type_code
    return ""
