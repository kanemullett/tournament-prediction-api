from typing import Any

from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
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

    def create_tournaments(self, tournaments: list[Tournament]) -> list[Tournament]:

        records: list[dict[str, Any]] = list(map(lambda tournament: tournament.model_dump(), tournaments))

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.INSERT,
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table="tournaments"
            ),
            records=records
        )

        self.__database_query_service.update_records(update_request)

        return tournaments
