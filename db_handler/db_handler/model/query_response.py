from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


class QueryResponse(BaseModel):
    """
    Object representing the response to a database query.

    Attributes:
        referenceId (UUID): The unique id of the query for referencing.
        recordCount (int): The number of records retrieved or updated by the query.
        records (Optional[list[dict[str, Any]]]): The records returned from the query.
    """
    referenceId: UUID
    recordCount: int
    records: Optional[list[dict[str, Any]]] = None
