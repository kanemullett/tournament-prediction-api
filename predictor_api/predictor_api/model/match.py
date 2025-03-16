from typing import Optional
from uuid import UUID

from predictor_api.predictor_api.model.match_base import MatchBase
from predictor_api.predictor_api.model.team import Team


class Match(MatchBase):
    homeTeam: Optional[Team] = None
    awayTeam: Optional[Team] = None
    groupMatchDay: Optional[int] = None
    groupId: Optional[UUID] = None
    roundId: Optional[UUID] = None

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"matches_{tournament_id}"
