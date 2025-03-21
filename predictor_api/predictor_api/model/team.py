from typing import ClassVar, Optional

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.type.confederation import Confederation


class Team(DatabaseRecord):
    """
    Object representing a team.

    Teams are unique and shared across all tournaments to reduce replication.

    If a tournament has a specific stated confederation, only teams belonging
    to the same confederation can participate in its matches.

    Attributes:
        name (Optional[str]): The name of the team.
        imagePath (Optional[str]): The path to the team's badge image.
        confederation (Optional[Confederation]): The international
            confederation of which the team is a member.
    """
    name: Optional[str] = None
    imagePath: Optional[str] = None
    confederation: Optional[Confederation] = None

    TARGET_TABLE: ClassVar[str] = "teams"
