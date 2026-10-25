from datetime import date

__all__ = ["to_hhmmss", "to_str", "to_yyyymmdd"]


def to_str(value: date | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def to_yyyymmdd(value: date | None) -> str | None:
    if value is None:
        return None
    return value.strftime("%Y%m%d")


def to_hhmmss(value: date | None) -> str | None:
    if value is None:
        return None
    return value.strftime("%H%M%S")
