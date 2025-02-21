from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.service.database_query_service import DatabaseQueryService
from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.util.predictor_constants import PredictorConstants


class TournamentService:

    def __init__(self, database_query_service: DatabaseQueryService) -> None:
        self.__database_query_service = database_query_service

    def get_tournaments(self) -> list[Tournament]:

        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table="tournaments"
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        return list(map(lambda record: Tournament.model_validate(record), query_response.records))
