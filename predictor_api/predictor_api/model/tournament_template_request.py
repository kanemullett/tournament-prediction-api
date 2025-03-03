from uuid import UUID

from predictor_api.predictor_api.model.tournament_template_base import (
    TournamentTemplateBase
)


class TournamentTemplateRequest(TournamentTemplateBase):
    """
    Object representing a tournament template, only including the ids of the
    league and knockout templates.

    Attributes:
        leagueTemplateId (UUID): The id of the tournament's league template.
        knockoutTemplateId (UUID): The id of the tournament's knockout
            template.
    """
    leagueTemplateId: UUID = None
    knockoutTemplateId: UUID = None
