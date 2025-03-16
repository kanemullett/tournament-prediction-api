from datetime import datetime
from typing import Optional

from db_handler.db_handler.model.database_record import DatabaseRecord


class MatchBase(DatabaseRecord):
    """
    Base object representing a match to be inherited by Match and
    MatchRequest objects.

    Attributes:
        kickoff (Optional[datetime]): The date and time at which the match
            kicks off.
    """
    kickoff: Optional[datetime] = None
