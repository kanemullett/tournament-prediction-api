from typing import Any
from uuid import UUID

from fastapi import HTTPException

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.condition_operator import ConditionOperator
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import DatabaseQueryService
from db_handler.db_handler.util.store_constants import StoreConstants
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

    def update_tournaments(self, tournaments: list[Tournament]) -> list[Tournament]:
        records: list[dict[str, Any]] = list(map(lambda tournament: tournament.model_dump(exclude_none=True), tournaments))

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.UPDATE,
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table="tournaments"
            ),
            records=records
        )

        self.__database_query_service.update_records(update_request)

        included_ids: list[UUID] = list(map(lambda tournament: tournament.id, tournaments))
        included_records: list[dict[str, Any]] = self.__database_query_service.retrieve_records(QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table="tournaments"
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column(
                            parts=[StoreConstants.ID]
                        ),
                        operator=ConditionOperator.IN,
                        value=included_ids
                    )
                ]
            )
        )).records

        return list(map(lambda record: Tournament.model_validate(record), included_records))

    def get_tournament_by_id(self, tournament_id: UUID) -> Tournament:

        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table="tournaments"
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column(
                            parts=[StoreConstants.ID]
                        ),
                        operator=ConditionOperator.EQUAL,
                        value=tournament_id
                    )
                ]
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        if len(query_response.records) == 0:
            raise HTTPException(status_code=404, detail="No tournaments found with a matching id.")

        return list(map(lambda record: Tournament.model_validate(record), query_response.records))[0]
