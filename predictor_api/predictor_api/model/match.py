from uuid import UUID

from predictor_api.predictor_api.model.match_base import MatchBase
from predictor_api.predictor_api.model.team import Team


class Match(MatchBase):
    homeTeam: Team
    awayTeam: Team

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"matches_{tournament_id}"
