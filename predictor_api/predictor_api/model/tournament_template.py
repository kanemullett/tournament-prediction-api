from typing import ClassVar

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.model.league_template import LeagueTemplate


class TournamentTemplate(DatabaseRecord):
    name: str
    league: LeagueTemplate
    knockout: KnockoutTemplate

    TARGET_TABLE: ClassVar[str] = "tournament-templates"
