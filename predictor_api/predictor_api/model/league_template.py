from typing import ClassVar

from db_handler.db_handler.model.database_record import DatabaseRecord


class LeagueTemplate(DatabaseRecord):
    name: str
    groupCount: int
    teamsPerGroup: int
    homeAndAway: bool

    TARGET_TABLE: ClassVar[str] = "league-templates"
