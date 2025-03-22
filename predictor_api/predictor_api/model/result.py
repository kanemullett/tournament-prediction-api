from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.match_outcome import MatchOutcome


class Result(DatabaseRecord, MatchOutcome):
    """
    Object representing a Result.

    Results have a 1:1 relationship with matches and as such, share an id.

    Unlike matches however, results are manually created after the conclusion
    of the match.
    """
    pass

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"results_{tournament_id}"
