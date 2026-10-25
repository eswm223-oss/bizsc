from datetime import date

from pydantic import BaseModel


class CacheBatchRequest(BaseModel):
    fromDate: date
    toDate: date
    mgmtId: str | None = None
    code: str = ""
