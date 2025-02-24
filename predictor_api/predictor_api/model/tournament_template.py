from typing import ClassVar

from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament_template_base import TournamentTemplateBase


class TournamentTemplate(TournamentTemplateBase):
    league: LeagueTemplate
    knockout: KnockoutTemplate

    TARGET_TABLE: ClassVar[str] = "tournament-templates"
