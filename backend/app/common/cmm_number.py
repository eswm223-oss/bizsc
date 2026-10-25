from decimal import Decimal


def to_decimal(value: str | None) -> Decimal | None:
    if value is None or value == "":
        return None
    return Decimal(value)


def to_number(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(value)
