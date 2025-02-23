from typing import Optional

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.type.competition import Competition


class Tournament(DatabaseRecord):
    """
    Object representing a tournament.

    Attributes:
        year (Optional[int]): The year of the tournament.
        competition (Optional[Competition]): The type of competition.
    """
    year: Optional[int] = None
    competition: Optional[Competition] = None
