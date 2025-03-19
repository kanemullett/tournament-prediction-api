from pydantic import BaseModel


class ResultResponse(BaseModel):
    homeGoals: int
    awayGoals: int
    afterExtraTime: bool
    afterPenalties: bool
