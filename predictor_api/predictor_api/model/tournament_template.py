from typing import ClassVar, Optional

from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament_template_base import TournamentTemplateBase


class TournamentTemplate(TournamentTemplateBase):
    league: Optional[LeagueTemplate] = None
    knockout: Optional[KnockoutTemplate] = None

    TARGET_TABLE: ClassVar[str] = "tournament-templates"
