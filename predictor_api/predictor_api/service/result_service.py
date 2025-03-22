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
    """
    Service for performing result-related actions.

    Attributes:
        __query_service (DatabaseQueryService): The database query service.
        __tournament_service (TournamentService): The tournament service.
    """

    def __init__(
            self,
            database_query_service: DatabaseQueryService,
            tournament_service: TournamentService) -> None:
        """
        Initialise the ResultService.

        Args:
            database_query_service (DatabaseQueryService): The database query
                service.
            tournament_service (TournamentService): The tournament service.
        """
        self.__query_service = database_query_service
        self.__tournament_service = tournament_service

    def create_results(
            self,
            tournament_id: UUID,
            results: list[Result]) -> list[Result]:
        """
        Create new results.

        Args:
            tournament_id (UUID): The id of the tournament to which the
                results belong.
            results (list[Result]): The new results to create.

        Returns:
            list[Result]: The newly created results.
        """
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

    def update_results(
            self,
            tournament_id: UUID,
            results: list[Result]) -> list[Result]:
        """
        Update existing results.

        Args:
            tournament_id (UUID): The id of the tournament to which the
                results belong.
            results (list[Result]): The results to update.

        Returns:
            list[Result]: The newly updated results.
        """
        self.__tournament_service.get_tournament_by_id(tournament_id)

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.UPDATE,
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

        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Result.get_target_table(tournament_id)
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

        return list(
            map(
                lambda record:
                Result.model_validate(record),
                response.records
            )
        )

    def delete_result_by_id(
            self,
            tournament_id: UUID,
            result_id: UUID) -> None:
        """
        Delete a single stored result by its id.

        Args:
            tournament_id (UUID): The id of the tournament to which the
                result belongs.
            result_id (UUID): The id of the result to delete.
        """
        self.__tournament_service.get_tournament_by_id(tournament_id)

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.DELETE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Result.get_target_table(tournament_id)
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        result_id
                    )
                )
            )
        )
