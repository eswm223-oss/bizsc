from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel

from .params import (
    OperatingMarginStreakParams,
    PriceDrawdownParams,
)

# 評価項目コード
MetricCode = Literal[
    "operating_margin_streak",
    "price_drawdown",
]


# 評価項目定義
@dataclass(frozen=True)
class MetricDefinition:
    label: str
    params_model: type[BaseModel]


# 評価項目一覧
METRICS: dict[str, MetricDefinition] = {
    "operating_margin_streak": MetricDefinition(
        label="営業利益率の連続上昇",
        params_model=OperatingMarginStreakParams,
    ),
    "price_drawdown": MetricDefinition(
        label="高値からの株価下落率",
        params_model=PriceDrawdownParams,
    ),
}
