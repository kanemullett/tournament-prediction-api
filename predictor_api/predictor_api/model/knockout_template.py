from typing import ClassVar

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.knockout_round import KnockoutRound


class KnockoutTemplate(DatabaseRecord):
    name: str
    rounds: list[KnockoutRound]

    TARGET_TABLE: ClassVar[str] = "knockout-templates"
