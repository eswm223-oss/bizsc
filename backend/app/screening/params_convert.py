from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ValidationError

from .metric_registry import METRICS

T = TypeVar("T", bound=BaseModel)


class ParamsResponse(BaseModel, Generic[T]):
    result: bool
    params: T | None = None
    error: str | None = None


class ParamsConvert:
    @staticmethod
    def params_validate(
        params: dict[str, Any],
        metric_code: str,
    ) -> ParamsResponse[BaseModel]:

        model_type = METRICS.get(metric_code)

        if model_type is None:
            raise ValueError(f"未対応の評価項目です: {metric_code}")

        return _validate(params, model_type.params_model)

    @staticmethod
    def params_convert(
        params: dict[str, Any],
        model_type: type[T],
    ) -> ParamsResponse[T]:

        result = _validate(params, model_type)

        if not result.result or result.params is None:
            raise ValueError(f"評価項目の変換失敗です: {params}")

        return result


def _validate(params: dict[str, Any], model_type: type[T]) -> ParamsResponse[T]:
    try:
        validated_params = model_type.model_validate(params)
        return ParamsResponse[T](result=True, params=validated_params)

    except ValidationError as e:
        return ParamsResponse[T](result=False, error=(str(e)))
