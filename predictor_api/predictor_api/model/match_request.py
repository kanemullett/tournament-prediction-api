from typing import Optional
from uuid import UUID

from predictor_api.predictor_api.model.match_base import MatchBase


class MatchUpdate(MatchBase):
    """
    Object representing a match, only including the ids of the home and away
    teams.

    Attributes:
        homeTeamId (UUID): The id of the match's home team.
        awayTeamId (UUID): The id of the match's away team.
    """
    homeTeamId: Optional[UUID] = None
    awayTeamId: Optional[UUID] = None
