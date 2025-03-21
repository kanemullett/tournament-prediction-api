from uuid import UUID

from fastapi import HTTPException

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.match import Match
from predictor_api.predictor_api.model.result import Result
from predictor_api.predictor_api.service.tournament_service import (
    TournamentService
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class ResultService:

    def __init__(
            self,
            database_query_service: DatabaseQueryService,
            tournament_service: TournamentService) -> None:
        self.__query_service = database_query_service
        self.__tournament_service = tournament_service

    def create_results(
            self,
            tournament_id: UUID,
            results: list[Result]) -> list[Result]:
        self.__tournament_service.get_tournament_by_id(tournament_id)

        match_response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Match.get_target_table(tournament_id)
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition(
                        column=Column.of(StoreConstants.ID),
                        operator=ConditionOperator.IN,
                        value=list(
                            map(
                                lambda result:
                                result.id,
                                results
                            )
                        )
                    )
                )
            )
        )

        if match_response.recordCount < len(results):
            raise HTTPException(
                status_code=400,
                detail="One or more results does not have a corresponding "
                       "match record."
            )

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.INSERT,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Result.get_target_table(tournament_id)
                ),
                records=list(
                    map(
                        lambda result:
                        result.model_dump(exclude_none=True),
                        results
                    )
                )
            )
        )

        return results
