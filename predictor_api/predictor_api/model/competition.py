from typing import Optional, ClassVar
from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord


class Competition(DatabaseRecord):
    """
    Object representing a competition.

    Attributes:
        name (Optional[str]): The name of the competition.
        tournamentId (Optional[UUID]): The id of the competition's tournament.
    """
    name: Optional[str] = None
    tournamentId: Optional[UUID] = None

    TARGET_TABLE: ClassVar[str] = "competitions"
