from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


class QueryResponse(BaseModel):
    referenceId: UUID
    recordCount: int
    records: Optional[list[dict[str, Any]]] = None
