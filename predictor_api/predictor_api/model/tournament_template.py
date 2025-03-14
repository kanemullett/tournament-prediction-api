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

    Tournament templates are a required component of tournaments as they
    define their structure.

    Tournament templates must have at least one of either league or knockout
    template defined.

    Attributes:
        league (Optional[LeagueTemplate]): The template of the tournament's
            league phase.
        knockout (Optional[KnockoutTemplate]): The template of the
            tournament's knockout phase.
    """
    league: Optional[LeagueTemplate] = None
    knockout: Optional[KnockoutTemplate] = None

    TARGET_TABLE: ClassVar[str] = "tournament-templates"
