from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from app.batches.edinet_inventory import main
from app.services.edinet_inventory import OneDayInventorySummary


def _summary(total: int, listed: int, csv: int) -> OneDayInventorySummary:
    return OneDayInventorySummary(
        total_count=total,
        listed_match_count=listed,
        csv_flag_count=csv,
        doc_type_counts={},
    )


@patch("app.batches.edinet_inventory.EdinetInventoryService")
@patch("app.batches.edinet_inventory.SessionLocal")
def test_main_prints_one_line_per_day_and_closes_session(
    mock_session_local,
    mock_service_class,
    capsys,
) -> None:
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_service = MagicMock()
    mock_service_class.return_value = mock_service
    mock_service.refresh_date_range.return_value = [
        (date(2026, 8, 19), _summary(203, 42, 28)),
        (date(2026, 8, 20), _summary(313, 38, 29)),
        (date(2026, 8, 21), _summary(150, 20, 15)),
    ]

    exit_code = main(
        [
            "--start-date",
            "2026-08-19",
            "--end-date",
            "2026-08-21",
        ]
    )

    assert exit_code == 0
    mock_session_local.assert_called_once()
    mock_service_class.assert_called_once()
    mock_service.refresh_date_range.assert_called_once_with(
        mock_db,
        date(2026, 8, 19),
        date(2026, 8, 21),
    )
    mock_db.close.assert_called_once()
    output = capsys.readouterr().out
    assert "2026-08-19 total=203 listed=42 csv=28" in output
    assert "2026-08-20 total=313 listed=38 csv=29" in output
    assert "2026-08-21 total=150 listed=20 csv=15" in output


@patch("app.batches.edinet_inventory.SessionLocal")
def test_main_exits_before_session_on_invalid_date(
    mock_session_local,
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--start-date",
                "2026/08/19",
                "--end-date",
                "2026-08-21",
            ]
        )

    assert exc_info.value.code == 2
    mock_session_local.assert_not_called()


@patch("app.batches.edinet_inventory.EdinetInventoryService")
@patch("app.batches.edinet_inventory.SessionLocal")
def test_main_closes_session_when_refresh_raises(
    mock_session_local,
    mock_service_class,
) -> None:
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_service = MagicMock()
    mock_service_class.return_value = mock_service
    mock_service.refresh_date_range.side_effect = RuntimeError("refresh failed")

    with pytest.raises(RuntimeError, match="refresh failed"):
        main(
            [
                "--start-date",
                "2026-08-19",
                "--end-date",
                "2026-08-21",
            ]
        )

    mock_db.close.assert_called_once()
