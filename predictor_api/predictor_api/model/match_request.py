from uuid import UUID

from predictor_api.predictor_api.model.match_base import MatchBase


class MatchRequest(MatchBase):
    homeTeamId: UUID
    awayTeamId: UUID
