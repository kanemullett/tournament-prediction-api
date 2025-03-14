from typing import ClassVar

from pydantic import BaseModel


class RoundTemplate(BaseModel):
    """
    Object representing a knockout round.

    Knockout rounds are tournament-scoped and generated upon the creation of
    their parent tournament, using the tournament's template as a guide.

    Attributes:
        name (str): The name of the round.
        teamCount (int): The number of teams participating in the round.
        roundOrder (int): The nth position at which the round is to be played
            within the knockout phase.
        twoLegs (bool): True if the round is to be played over two legs.
        extraTime (bool): True if the round goes to extra-time in the event
            that the teams are tied after regulation time.
        awayGoals (bool): True if the round should be decided on away-goals
            if the aggregate score is tied after regulation time.
    """
    name: str
    teamCount: int
    roundOrder: int
    twoLegs: bool
    extraTime: bool
    awayGoals: bool

    TARGET_TABLE: ClassVar[str] = "rounds"
