from typing import Literal

from pydantic import BaseModel, Field


# 営業利益率の連続上昇
class OperatingMarginStreakParams(BaseModel):
    # 何期連続
    count: int = Field(ge=1)


# 高値からの株価下落率
class PriceDrawdownParams(BaseModel):
    # 対象期間
    lookback: Literal["1y", "3y", "5y"]
    # 下落率
    threshold_pct: float = Field(ge=0, le=100)
