from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DatabaseRecord(BaseModel):
    """
    Object representing a database record.

    Attributes:
        id (UUID): The record's unique id.
    """
    id: UUID = Field(default_factory=uuid4)
