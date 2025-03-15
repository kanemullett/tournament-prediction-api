from datetime import datetime
from typing import Optional
from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord


class MatchBase(DatabaseRecord):
    kickoff: Optional[datetime] = None
    groupMatchDay: Optional[int] = None
    groupId: Optional[UUID] = None
    roundId: Optional[UUID] = None
