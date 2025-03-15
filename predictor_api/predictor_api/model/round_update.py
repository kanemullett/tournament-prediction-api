from typing import Optional

from db_handler.db_handler.model.database_record import DatabaseRecord


class RoundUpdate(DatabaseRecord):
    name: Optional[str] = None
    twoLegs: Optional[bool] = None
    extraTime: Optional[bool] = None
    awayGoals: Optional[bool] = None
