import argparse
from datetime import date

from app.db.database import SessionLocal
from app.repositories import EdinetInventoryRepository
from app.services import EdinetInventoryService


def _parse_iso_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid date '{value}'; expected YYYY-MM-DD"
        ) from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Refresh EDINET inventory for a date range.",
    )
    parser.add_argument(
        "--start-date",
        required=True,
        type=_parse_iso_date,
        help="Start date in YYYY-MM-DD",
    )
    parser.add_argument(
        "--end-date",
        required=True,
        type=_parse_iso_date,
        help="End date in YYYY-MM-DD",
    )
    args = parser.parse_args(argv)

    db = SessionLocal()
    try:
        service = EdinetInventoryService(EdinetInventoryRepository())
        summaries = service.refresh_date_range(
            db,
            args.start_date,
            args.end_date,
        )
        for target_date, summary in summaries:
            print(
                f"{target_date.isoformat()} "
                f"total={summary.total_count} "
                f"listed={summary.listed_match_count} "
                f"csv={summary.csv_flag_count}"
            )
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
