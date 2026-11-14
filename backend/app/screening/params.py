from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# 営業利益率の連続上昇
class OperatingMarginStreakParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # 何期連続
    count: int = Field(ge=1)


# 高値からの株価下落率
class PriceDrawdownParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # 対象期間
    lookback: Literal["1y", "3y", "5y"]
    # 下落率
    threshold_pct: float = Field(ge=0, le=100)
