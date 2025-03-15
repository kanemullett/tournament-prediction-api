from datetime import datetime
from typing import Optional

from db_handler.db_handler.model.database_record import DatabaseRecord


class MatchBase(DatabaseRecord):
    kickoff: datetime
    groupMatchDay: Optional[int] = None
