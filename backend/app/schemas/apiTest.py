
from pydantic import (
    BaseModel
)

class ApiResTest(BaseModel):
    res: str | None = None
