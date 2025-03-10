from typing import Optional, ClassVar
from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.type.confederation import Confederation


class Tournament(DatabaseRecord):
    """
    Object representing a tournament.

    Attributes:
        year (Optional[int]): The year of the tournament.
        confederation (Optional[Confederation]): The confederation of the
            tournament.
        templateId (Optional[UUID]): The id of the tournament's template.
    """
    name: Optional[str] = None
    year: Optional[int] = None
    confederation: Optional[Confederation] = None
    templateId: Optional[UUID] = None

    TARGET_TABLE: ClassVar[str] = "tournaments"
