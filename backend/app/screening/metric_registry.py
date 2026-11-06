from .metric_definition import MetricDefinition
from .params import (
    OperatingMarginStreakParams,
    PriceDrawdownParams,
)

METRICS: dict[str, MetricDefinition] = {
    "operating_margin_streak": MetricDefinition(
        code="operating_margin_streak",
        label="営業利益率の連続上昇",
        params_model=OperatingMarginStreakParams,
    ),
    "price_drawdown": MetricDefinition(
        code="price_drawdown",
        label="高値からの株価下落率",
        params_model=PriceDrawdownParams,
    ),
}
