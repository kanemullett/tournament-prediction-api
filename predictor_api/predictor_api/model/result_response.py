from typing import Optional

from pydantic import BaseModel

from predictor_api.predictor_api.model.type.winner import Winner


class ResultResponse(BaseModel):
    homeGoals: int
    awayGoals: int
    afterExtraTime: bool
    afterPenalties: bool
    penaltiesWinner: Optional[Winner] = None
