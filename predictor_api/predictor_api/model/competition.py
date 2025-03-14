from typing import Optional, ClassVar
from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord


class Competition(DatabaseRecord):
    """
    Object representing a competition.

    A competition is defined as a game-like session within which users can
    compete against each other to make predictions on the outcome of matches.

    Each competition is based around a single tournament such as the 2026
    FIFA World Cup or the 2028 UEFA European Championships.

    Tournaments can be shared between multiple competitions, allowing users
    assigned to multiple competitions based around the same tournament to
    make one set of predictions that apply to ALL competitions.

    Attributes:
        name (Optional[str]): The name of the competition.
        tournamentId (Optional[UUID]): The id of the competition's tournament.
    """
    name: Optional[str] = None
    tournamentId: Optional[UUID] = None

    TARGET_TABLE: ClassVar[str] = "competitions"
