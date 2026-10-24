from decimal import Decimal

__all__ = [
    "to_Number",
    "to_decimal",
]


def to_decimal(value: str | None) -> Decimal | None:
    if value is None or value == "":
        return None
    return Decimal(value)


def to_Number(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(value)
