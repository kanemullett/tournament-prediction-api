from typing import ClassVar, Optional

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.type.confederation import Confederation


class Team(DatabaseRecord):
    name: Optional[str] = None
    imagePath: Optional[str] = None
    confederation: Optional[Confederation] = None

    TARGET_TABLE: ClassVar[str] = "teams"
