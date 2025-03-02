from typing import ClassVar, Optional

from predictor_api.predictor_api.model.knockout_template import (
    KnockoutTemplate
)
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament_template_base import (
    TournamentTemplateBase
)


class TournamentTemplate(TournamentTemplateBase):
    """
    Object representing a tournament template.

    Attributes:
        league (Optional[LeagueTemplate]): The template of the tournament's
            league phase.
        knockout (Optional[KnockoutTemplate]): The template of the
            tournament's knockout phase.
    """
    league: Optional[LeagueTemplate] = None
    knockout: Optional[KnockoutTemplate] = None

    TARGET_TABLE: ClassVar[str] = "tournament-templates"
