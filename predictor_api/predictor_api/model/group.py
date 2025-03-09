from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord


class Group(DatabaseRecord):
    name: str

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"groups_{tournament_id}"
