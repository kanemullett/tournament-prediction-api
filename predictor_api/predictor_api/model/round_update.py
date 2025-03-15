from typing import Optional

from db_handler.db_handler.model.database_record import DatabaseRecord


class RoundUpdate(DatabaseRecord):
    """
    Object representing a round update.

    Attributes:
        name (Optional[str]): The name of the round.
        twoLegs (Optional[bool]): True if the round is to be contested over
            two legs.
        extraTime (Optional[bool]): True if the round should go to extra time
            if tied at full-time.
        awayGoals (Optional[bool]): True if away goals should be applied if
            tied at full-time.
    """
    name: Optional[str] = None
    twoLegs: Optional[bool] = None
    extraTime: Optional[bool] = None
    awayGoals: Optional[bool] = None
