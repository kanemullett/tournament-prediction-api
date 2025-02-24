from uuid import UUID

from predictor_api.predictor_api.model.tournament_template_base import TournamentTemplateBase


class TournamentTemplateRequest(TournamentTemplateBase):
    leagueTemplateId: UUID = None
    knockoutTemplateId: UUID = None
