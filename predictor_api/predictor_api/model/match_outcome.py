from typing import Optional

from pydantic import BaseModel

from predictor_api.predictor_api.model.type.winner import Winner


class MatchOutcome(BaseModel):
    """
    Object representing a match outcome.

    This object is extended by both Prediction and Result objects.

    Attributes:
        homeGoals (int): The number of goals scored by the home team.
        awayGoals (int): The number of goals scored by the away team.
        afterExtraTime (bool): True if the game's conclusion came after extra
            time had been played.
        afterPenalties (bool): True if the game's conclusion came after a
            penalty shoot-out.
        penaltiesWinner (Optional[Winner]): The team who won the penalty
            shoot-out.
    """
    homeGoals: int
    awayGoals: int
    afterExtraTime: bool
    afterPenalties: bool
    penaltiesWinner: Optional[Winner] = None
