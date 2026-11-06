from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class MetricDefinition:
    code: str
    label: str
    params_model: type[BaseModel]
