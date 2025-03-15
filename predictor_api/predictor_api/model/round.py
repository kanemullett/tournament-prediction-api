from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.round_template import RoundTemplate


class Round(DatabaseRecord, RoundTemplate):
    """
    Object representing a round.

    Rounds are tournament-scoped and generated upon the creation of their
    parent tournament, using the tournament's template as a guide.
    """
    pass

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"rounds_{tournament_id}"
