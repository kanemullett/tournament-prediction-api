from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from predictor_api.predictor_api.model.competition import Competition
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class CompetitionService:

    def __init__(self, database_query_service: DatabaseQueryService) -> None:
        self.__query_service = database_query_service

    def get_competitions(self) -> list[Competition]:
        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Competition.TARGET_TABLE
                )
            )
        )

        return list(
            map(
                lambda record:
                Competition.model_validate(record),
                response.records
            )
        )
