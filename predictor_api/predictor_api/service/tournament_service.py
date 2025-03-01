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
    """
    Service for performing tournament-related actions.

    Attributes:
        __database_query_service (DatabaseQueryService): The database query service.
    """

    def __init__(self, database_query_service: DatabaseQueryService) -> None:
        """
        Initialise the TournamentService.

        Args:
            database_query_service (DatabaseQueryService): The database query service.
        """
        self.__database_query_service = database_query_service

    def get_tournaments(self) -> list[Tournament]:
        """
        Retrieve stored tournaments.

        Returns:
            list[Tournament]: The stored tournaments.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE)
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        return list(map(lambda record: Tournament.model_validate(record), query_response.records))

    def create_tournaments(self, tournaments: list[Tournament]) -> list[Tournament]:
        """
        Create new tournaments.

        Args:
            tournaments (list[Tournament]): The new tournaments to create.

        Returns:
            list[Tournament]: The newly created tournaments.
        """
        records: list[dict[str, Any]] = list(map(lambda tournament: tournament.model_dump(), tournaments))

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.INSERT,
            table=Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE),
            records=records
        )

        self.__database_query_service.update_records(update_request)

        return tournaments

    def update_tournaments(self, tournaments: list[Tournament]) -> list[Tournament]:
        """
        Update existing tournaments.

        Args:
            tournaments (list[Tournament]): The tournaments to update.

        Returns:
            list[Tournament]: The newly updated tournaments.
        """
        records: list[dict[str, Any]] = list(
            map(lambda tournament: tournament.model_dump(exclude_none=True), tournaments)
        )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.UPDATE,
            table=Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE),
            records=records
        )

        self.__database_query_service.update_records(update_request)

        included_ids: list[UUID] = list(map(lambda tournament: tournament.id, tournaments))
        included_records: list[dict[str, Any]] = self.__database_query_service.retrieve_records(QueryRequest(
            table=Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition(
                    column=Column.of(StoreConstants.ID),
                    operator=ConditionOperator.IN,
                    value=included_ids
                )
            )
        )).records

        return list(map(lambda record: Tournament.model_validate(record), included_records))

    def get_tournament_by_id(self, tournament_id: UUID) -> Tournament:
        """
        Retrieve a single stored tournament by its id.

        Args:
            tournament_id (UUID): The id of the tournament to retrieve.

        Returns:
            Tournament: The retrieved tournament.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE),
            conditionGroup=QueryConditionGroup.of(QueryCondition.of(Column.of(StoreConstants.ID), tournament_id))
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        if len(query_response.records) == 0:
            raise HTTPException(status_code=404, detail="No tournaments found with a matching id.")

        return list(map(lambda record: Tournament.model_validate(record), query_response.records))[0]

    def delete_tournament_by_id(self, tournament_id: UUID) -> None:
        """
        Delete a single stored tournament by its id.

        Args:
            tournament_id (UUID): The id of the tournament to delete.
        """
        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.DELETE,
            table=Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE),
            conditionGroup=QueryConditionGroup.of(QueryCondition.of(Column.of(StoreConstants.ID), tournament_id))
        )

        self.__database_query_service.update_records(update_request)
