from uuid import UUID

from pydantic import BaseModel

from predictor_api.predictor_api.model.type.competition import Competition


class Tournament(BaseModel):
    id: UUID
    year: int
    competition: Competition
