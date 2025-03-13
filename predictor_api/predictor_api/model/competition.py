from typing import Optional, ClassVar
from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord


class Competition(DatabaseRecord):
    name: Optional[str] = None
    tournamentId: Optional[UUID] = None

    TARGET_TABLE: ClassVar[str] = "competitions"
