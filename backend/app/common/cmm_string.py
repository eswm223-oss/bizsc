from datetime import date

__all__ = [
    "to_date",
]


def to_date(value: str | None) -> date | None:
    if value is None or value == "":
        return None
    return date.fromisoformat(value)
