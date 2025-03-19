from uuid import UUID

from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.result_response import ResultResponse


class Result(DatabaseRecord, ResultResponse):
    pass

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"results_{tournament_id}"
