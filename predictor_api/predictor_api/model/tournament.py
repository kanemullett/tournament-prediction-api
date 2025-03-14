from typing import Optional, ClassVar
from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.type.confederation import Confederation


class Tournament(DatabaseRecord):
    """
    Object representing a tournament.

    A tournament is a representation of the real-world football tournament
    that predictions are being made for.

    Tournaments are unique and can be used by multiple competitions in order
    to allow multiple separate groups of users to compete in enclosed spaces
    for the same tournament.

    The reusability of tournaments allows single users participating in
    multiple competitions to only make a set of predictions once, with them
    being shared across competitions.

    Each tournament's structure is defined within its template and required
    groups, rounds and matches are created at the point of tournament
    creation.

    Attributes:
        year (Optional[int]): The year of the tournament.
        confederation (Optional[Confederation]): The confederation of the
            tournament.
        templateId (Optional[UUID]): The id of the tournament's template.
    """
    name: Optional[str] = None
    year: Optional[int] = None
    confederation: Optional[Confederation] = None
    templateId: Optional[UUID] = None

    TARGET_TABLE: ClassVar[str] = "tournaments"
