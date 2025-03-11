from typing import Optional
from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.team import Team


class Group(DatabaseRecord):
    name: str
    teams: Optional[list[Team]] = None

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"groups_{tournament_id}"
