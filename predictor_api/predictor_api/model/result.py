from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord


class Result(DatabaseRecord):
    homeGoals: int
    awayGoals: int
    afterExtraTime: bool
    afterPenalties: bool

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"results_{tournament_id}"
