import string
from typing import Any
from uuid import UUID

from fastapi import HTTPException

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.column_definition import ColumnDefinition
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_definition import TableDefinition
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.sql_data_type import SqlDataType
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.service.database_table_service import (
    DatabaseTableService
)
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.group import Group
from predictor_api.predictor_api.model.knockout_template import (
    KnockoutTemplate
)
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.round import Round
from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.model.tournament_template import (
    TournamentTemplate
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class TournamentService:
    """
    Service for performing tournament-related actions.

    Attributes:
        __query_service (DatabaseQueryService): The database query service.
    """

    def __init__(
            self,
            database_query_service: DatabaseQueryService,
            database_table_service: DatabaseTableService) -> None:
        """
        Initialise the TournamentService.

        Args:
            database_query_service (DatabaseQueryService): The database query
                service.
        """
        self.__query_service = database_query_service
        self.__table_service = database_table_service

    def get_tournaments(self) -> list[Tournament]:
        """
        Retrieve stored tournaments.

        Returns:
            list[Tournament]: The stored tournaments.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Tournament.TARGET_TABLE
            )
        )

        query_response: QueryResponse = (
            self.__query_service.retrieve_records(query_request)
        )

        return list(
            map(
                lambda record:
                Tournament.model_validate(record),
                query_response.records
            )
        )

    def create_tournaments(
            self,
            tournaments: list[Tournament]) -> list[Tournament]:
        """
        Create new tournaments.

        Args:
            tournaments (list[Tournament]): The new tournaments to create.

        Returns:
            list[Tournament]: The newly created tournaments.
        """
        records: list[dict[str, Any]] = list(
            map(
                lambda tournament:
                tournament.model_dump(),
                tournaments
            )
        )

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.INSERT,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Tournament.TARGET_TABLE
                ),
                records=records
            )
        )

        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                columns=[
                    Column.of("tourn", StoreConstants.ID),
                    Column.of("temp", "leagueTemplateId"),
                    Column.of("temp", "knockoutTemplateId")
                ],
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Tournament.TARGET_TABLE,
                    "tourn"
                ),
                tableJoins=[
                    TableJoin.of(
                        Table.of(
                            PredictorConstants.PREDICTOR_SCHEMA,
                            TournamentTemplate.TARGET_TABLE,
                            "temp"
                        ),
                        QueryCondition.of(
                            Column.of("tourn", "templateId"),
                            Column.of("temp", StoreConstants.ID)
                        ),
                        TableJoinType.LEFT
                    )
                ],
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition(
                        column=Column.of("tourn", StoreConstants.ID),
                        operator=ConditionOperator.IN,
                        value=list(
                            map(
                                lambda tournament:
                                tournament.id,
                                tournaments
                            )
                        )
                    )
                )
            )
        )

        for record in response.records:
            if record["leagueTemplateId"] is not None:
                self.__create_group_tables(UUID(record[StoreConstants.ID]))

            if record["knockoutTemplateId"] is not None:
                self.__create_round_tables(UUID(record[StoreConstants.ID]))

        return tournaments

    def update_tournaments(
            self,
            tournaments: list[Tournament]) -> list[Tournament]:
        """
        Update existing tournaments.

        Args:
            tournaments (list[Tournament]): The tournaments to update.

        Returns:
            list[Tournament]: The newly updated tournaments.
        """
        records: list[dict[str, Any]] = list(
            map(
                lambda tournament:
                tournament.model_dump(exclude_none=True),
                tournaments
            )
        )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.UPDATE,
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Tournament.TARGET_TABLE
            ),
            records=records
        )

        self.__query_service.update_records(update_request)

        included_ids: list[UUID] = list(
            map(
                lambda tournament:
                tournament.id,
                tournaments
            )
        )
        included_records: list[dict[str, Any]] = (
            self.__query_service.retrieve_records(
                QueryRequest(
                    table=Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Tournament.TARGET_TABLE
                    ),
                    conditionGroup=QueryConditionGroup.of(
                        QueryCondition(
                            column=Column.of(StoreConstants.ID),
                            operator=ConditionOperator.IN,
                            value=included_ids
                        )
                    )
                )
            ).records
        )

        return list(
            map(
                lambda record:
                Tournament.model_validate(record),
                included_records
            )
        )

    def get_tournament_by_id(self, tournament_id: UUID) -> Tournament:
        """
        Retrieve a single stored tournament by its id.

        Args:
            tournament_id (UUID): The id of the tournament to retrieve.

        Returns:
            Tournament: The retrieved tournament.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Tournament.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition.of(Column.of(StoreConstants.ID), tournament_id)
            )
        )

        query_response: QueryResponse = (
            self.__query_service.retrieve_records(query_request)
        )

        if len(query_response.records) == 0:
            raise HTTPException(
                status_code=404,
                detail="No tournaments found with a matching id."
            )

        return list(
            map(
                lambda record:
                Tournament.model_validate(record),
                query_response.records
            )
        )[0]

    def delete_tournament_by_id(self, tournament_id: UUID) -> None:
        """
        Delete a single stored tournament by its id.

        Args:
            tournament_id (UUID): The id of the tournament to delete.
        """
        self.__delete_tournament_tables(tournament_id)

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.DELETE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Tournament.TARGET_TABLE
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        tournament_id
                    )
                )
            )
        )

    def __create_group_tables(self, tournament_id: UUID) -> None:
        self.__table_service.create_table(
            TableDefinition(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=Group.get_target_table(tournament_id),
                columns=[
                    ColumnDefinition(
                        name=StoreConstants.ID,
                        dataType=SqlDataType.VARCHAR,
                        primaryKey=True
                    ),
                    ColumnDefinition.of("name", SqlDataType.VARCHAR)
                ]
            )
        )

        self.__table_service.create_table(
            TableDefinition(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=PredictorConstants.get_group_teams_table(tournament_id),
                columns=[
                    ColumnDefinition.of("groupId", SqlDataType.VARCHAR),
                    ColumnDefinition.of("teamId", SqlDataType.VARCHAR)
                ]
            )
        )

        self.__create_groups(tournament_id)

    def __create_groups(self, tournament_id: UUID) -> None:
        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                columns=[
                    Column.of("league", "groupCount")
                ],
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Tournament.TARGET_TABLE,
                    "tourn"
                ),
                tableJoins=[
                    TableJoin.of(
                        Table.of(
                            PredictorConstants.PREDICTOR_SCHEMA,
                            TournamentTemplate.TARGET_TABLE,
                            "temp"
                        ),
                        QueryCondition.of(
                            Column.of("tourn", "templateId"),
                            Column.of("temp", StoreConstants.ID)
                        ),
                        TableJoinType.INNER
                    ),
                    TableJoin.of(
                        Table.of(
                            PredictorConstants.PREDICTOR_SCHEMA,
                            LeagueTemplate.TARGET_TABLE,
                            "league"
                        ),
                        QueryCondition.of(
                            Column.of("temp", "leagueTemplateId"),
                            Column.of("league", StoreConstants.ID)
                        ),
                        TableJoinType.INNER
                    )
                ],
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of("tourn", StoreConstants.ID),
                        tournament_id
                    )
                )
            )
        )

        if response.recordCount > 0:
            group_count: int = response.records[0]["groupCount"]

            self.__query_service.update_records(
                UpdateRequest(
                    operation=SqlOperator.INSERT,
                    table=Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Group.get_target_table(tournament_id)
                    ),
                    records=list(
                        map(
                            lambda group:
                            group.model_dump(exclude_none=True),
                            self.__generate_groups(group_count)
                        )
                    )
                )
            )

    @staticmethod
    def __generate_groups(count: int) -> list[Group]:
        return [
            Group(
                name=f"Group {letter}"
            )
            for letter in string.ascii_uppercase[:count]
        ]

    def __create_round_tables(self, tournament_id: UUID) -> None:
        self.__table_service.create_table(
            TableDefinition(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=Round.get_target_table(tournament_id),
                columns=[
                    ColumnDefinition(
                        name=StoreConstants.ID,
                        dataType=SqlDataType.VARCHAR,
                        primaryKey=True
                    ),
                    ColumnDefinition.of("name", SqlDataType.VARCHAR),
                    ColumnDefinition.of("teamCount", SqlDataType.INTEGER),
                    ColumnDefinition.of("roundOrder", SqlDataType.INTEGER),
                    ColumnDefinition.of("twoLegs", SqlDataType.BOOLEAN),
                    ColumnDefinition.of("extraTime", SqlDataType.BOOLEAN),
                    ColumnDefinition.of("awayGoals", SqlDataType.BOOLEAN)
                ]
            )
        )

        self.__create_rounds(tournament_id)

    def __create_rounds(self, tournament_id: UUID) -> None:
        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                columns=[
                    Column.of("knock", "rounds")
                ],
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Tournament.TARGET_TABLE,
                    "tourn"
                ),
                tableJoins=[
                    TableJoin.of(
                        Table.of(
                            PredictorConstants.PREDICTOR_SCHEMA,
                            TournamentTemplate.TARGET_TABLE,
                            "temp"
                        ),
                        QueryCondition.of(
                            Column.of("tourn", "templateId"),
                            Column.of("temp", StoreConstants.ID)
                        ),
                        TableJoinType.INNER
                    ),
                    TableJoin.of(
                        Table.of(
                            PredictorConstants.PREDICTOR_SCHEMA,
                            KnockoutTemplate.TARGET_TABLE,
                            "knock"
                        ),
                        QueryCondition.of(
                            Column.of("temp", "knockoutTemplateId"),
                            Column.of("knock", StoreConstants.ID)
                        ),
                        TableJoinType.INNER
                    )
                ],
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of("tourn", StoreConstants.ID),
                        tournament_id
                    )
                )
            )
        )

        if response.recordCount > 0:
            rounds: list[Round] = list(
                map(
                    lambda round_dict:
                    Round.model_validate(round_dict),
                    response.records[0]["rounds"]
                )
            )

            self.__query_service.update_records(
                UpdateRequest(
                    operation=SqlOperator.INSERT,
                    table=Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Round.get_target_table(tournament_id)
                    ),
                    records=list(
                        map(
                            lambda knock:
                            knock.model_dump(exclude_none=True),
                            rounds
                        )
                    )
                )
            )

    def __delete_tournament_tables(self, tournament_id: UUID) -> None:
        self.__table_service.delete_table(
            Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Group.get_target_table(tournament_id)
            )
        )

        self.__table_service.delete_table(
            Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                PredictorConstants.get_group_teams_table(tournament_id)
            )
        )

        self.__table_service.delete_table(
            Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Round.get_target_table(tournament_id)
            )
        )
