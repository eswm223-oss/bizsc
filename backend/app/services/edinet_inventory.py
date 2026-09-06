from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.clients.edinet import (
    EdinetClientError,
    fetch_document_list,
    fetch_listed_sec_codes,
)
from app.models import EdinetDocument, EdinetInventoryRun
from app.repositories import EdinetInventoryRepository


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


class EdinetInventoryService:
    def __init__(
        self,
        repository: EdinetInventoryRepository,
    ) -> None:
        self.repository = repository

    def refresh_one_day(
        self,
        db: Session,
        target_date: date,
    ) -> OneDayInventorySummary:
        self._mark_run_processing(db, target_date)
        try:
            listed_sec_codes = fetch_listed_sec_codes()
            payload = fetch_document_list(target_date)
            results = _document_list_results(payload)
            summary = summarize_one_day_inventory(results, listed_sec_codes)
            documents = [
                _to_edinet_document(target_date, document)
                for document in results
                if _is_listed_csv_document(document, listed_sec_codes)
            ]
            self.repository.delete_documents_by_target_date(db, target_date)
            self.repository.add_documents(db, documents)
            self._mark_run_completed(
                db,
                target_date,
                summary,
                listed_sec_code_count=len(listed_sec_codes),
            )
            db.commit()
            return summary
        except Exception as exc:
            db.rollback()
            self._mark_run_failed(db, target_date, exc)
            raise

    def _mark_run_processing(
        self,
        db: Session,
        target_date: date,
    ) -> EdinetInventoryRun:
        run = self.repository.get_run_by_target_date(db, target_date)
        if run is None:
            run = EdinetInventoryRun(target_date=target_date, status="processing")
        run.status = "processing"
        run.started_at = datetime.now(timezone.utc)
        run.completed_at = None
        run.error_message = None
        run.total_count = 0
        run.listed_match_count = 0
        run.csv_flag_count = 0
        run.listed_sec_code_count = 0
        self.repository.add_run(db, run)
        db.commit()
        return run

    def _mark_run_completed(
        self,
        db: Session,
        target_date: date,
        summary: OneDayInventorySummary,
        listed_sec_code_count: int,
    ) -> None:
        run = self.repository.get_run_by_target_date(db, target_date)
        if run is None:
            run = EdinetInventoryRun(target_date=target_date, status="completed")
        run.status = "completed"
        run.total_count = summary.total_count
        run.listed_match_count = summary.listed_match_count
        run.csv_flag_count = summary.csv_flag_count
        run.listed_sec_code_count = listed_sec_code_count
        run.completed_at = datetime.now(timezone.utc)
        run.error_message = None
        self.repository.add_run(db, run)

    def _mark_run_failed(
        self,
        db: Session,
        target_date: date,
        exc: BaseException,
    ) -> None:
        run = self.repository.get_run_by_target_date(db, target_date)
        if run is None:
            return
        run.status = "failed"
        run.completed_at = datetime.now(timezone.utc)
        run.error_message = _safe_error_message(exc)
        self.repository.add_run(db, run)
        db.commit()


def _document_list_results(payload: Any) -> list[Any]:
    if not isinstance(payload, dict) or "results" not in payload:
        raise ValueError("EDINET document list response has invalid results")
    results = payload["results"]
    if not isinstance(results, list):
        raise ValueError("EDINET document list response has invalid results")
    return results


def _is_listed_csv_document(
    document: Any,
    listed_sec_codes: set[str],
) -> bool:
    if not isinstance(document, dict):
        return False
    return (
        _sec_code_matches_listed(document, listed_sec_codes)
        and document.get("csvFlag") == "1"
    )


def _to_edinet_document(
    target_date: date,
    document: dict[str, Any],
) -> EdinetDocument:
    return EdinetDocument(
        target_date=target_date,
        doc_id=_require_str(document.get("docID")),
        edinet_code=_optional_str(document.get("edinetCode")),
        sec_code=_optional_str(document.get("secCode")),
        filer_name=_optional_str(document.get("filerName")),
        ordinance_code=_optional_str(document.get("ordinanceCode")),
        form_code=_optional_str(document.get("formCode")),
        doc_type_code=_optional_str(document.get("docTypeCode")),
        period_start=_parse_optional_date(document.get("periodStart")),
        period_end=_parse_optional_date(document.get("periodEnd")),
        submit_date_time=_parse_submit_date_time(document.get("submitDateTime")),
        doc_description=_optional_str(document.get("docDescription")),
        parent_doc_id=_optional_str(document.get("parentDocID")),
        withdrawal_status=_optional_str(document.get("withdrawalStatus")),
        doc_info_edit_status=_optional_str(document.get("docInfoEditStatus")),
        disclosure_status=_optional_str(document.get("disclosureStatus")),
        xbrl_flag=_optional_str(document.get("xbrlFlag")),
        pdf_flag=_optional_str(document.get("pdfFlag")),
        csv_flag=_optional_str(document.get("csvFlag")),
        legal_status=_optional_str(document.get("legalStatus")),
    )


def _require_str(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("EDINET document is missing docID")
    return value


def _optional_str(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return value


def _parse_optional_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str) or not value.strip():
        return None
    return date.fromisoformat(value.strip())


def _parse_submit_date_time(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    if not isinstance(value, str) or not value.strip():
        return None
    return datetime.fromisoformat(value.strip())


def _safe_error_message(exc: BaseException) -> str:
    if isinstance(exc, EdinetClientError):
        return str(exc)
    return type(exc).__name__
