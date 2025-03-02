from typing import ClassVar, Optional

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.knockout_round import KnockoutRound


class KnockoutTemplate(DatabaseRecord):
    """
    Object representing a knockout template.

    Attributes:
        name (str): The name of the knockout template.
        rounds (Optional[list[KnockoutRound]]): The knockout rounds that make up the knockout phase.
    """
    name: str
    rounds: Optional[list[KnockoutRound]] = None

    TARGET_TABLE: ClassVar[str] = "knockout-templates"
