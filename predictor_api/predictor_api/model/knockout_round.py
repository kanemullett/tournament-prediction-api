from pydantic import BaseModel


class KnockoutRound(BaseModel):
    name: str
    teamCount: int
    roundOrder: int
    twoLegs: bool
    extraTime: bool
    awayGoals: bool
