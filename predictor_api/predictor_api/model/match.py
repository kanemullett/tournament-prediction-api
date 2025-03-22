from typing import Optional
from uuid import UUID

from predictor_api.predictor_api.model.group import Group
from predictor_api.predictor_api.model.match_base import MatchBase
from predictor_api.predictor_api.model.match_outcome import MatchOutcome
from predictor_api.predictor_api.model.round import Round
from predictor_api.predictor_api.model.team import Team


class Match(MatchBase):
    """
    Object representing a match.

    Matches are a representation of the fixtures that make up the real-world
    tournament and form the basis upon which users can make predictions.

    Matches are created upon the creation of their tournaments.

    Attributes:
        homeTeam (Optional[Team]): The team playing the match at home.
        awayTeam (Optional[Team]): The team playing the match away.
        groupMatchDay (Optional[int]): The match day on which the match is
            played during the group stage.
        groupId (Optional[UUID]): The id of the group the match is a part of.
        roundId (Optional[UUID]): The id of the round the match is a part of.
    """
    homeTeam: Optional[Team] = None
    awayTeam: Optional[Team] = None
    groupMatchDay: Optional[int] = None
    group: Optional[Group] = None
    round: Optional[Round] = None
    groupId: Optional[UUID] = None
    roundId: Optional[UUID] = None
    result: Optional[MatchOutcome] = None

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"matches_{tournament_id}"
