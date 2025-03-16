from typing import Any
from uuid import UUID

from fastapi import HTTPException

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.order_by import OrderBy
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.group import Group
from predictor_api.predictor_api.model.group_update import GroupUpdate
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.model.tournament_template import (
    TournamentTemplate
)
from predictor_api.predictor_api.service.tournament_service import (
    TournamentService
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class GroupService:
    """
    Service for performing group-related actions.

    Attributes:
        __query_service (DatabaseQueryService): The database query service.
        __tournament_service (TournamentService): The tournament service.
    """

    def __init__(
            self,
            database_query_service: DatabaseQueryService,
            tournament_service: TournamentService) -> None:
        """
        Initialise the GroupService.

        Args:
            database_query_service (DatabaseQueryService): The database query
                service.
            tournament_service (TournamentService): The tournament service.
        """
        self.__query_service = database_query_service
        self.__tournament_service = tournament_service

    def get_groups(self, tournament_id: UUID) -> list[Group]:
        """
        Retrieve stored groups.

        Args:
            tournament_id (UUID): The id of the tournament whose groups are
                to be retrieved.

        Returns:
            list[Group]: The stored groups.
        """
        self.__tournament_service.get_tournament_by_id(tournament_id)

        if not self.__tournament_has_group_stage(tournament_id):
            raise HTTPException(
                status_code=404,
                detail="The tournament with the supplied id does not have a "
                       "group stage."
            )

        return self.__retrieve_and_build_groups(tournament_id)

    def update_groups(
            self,
            tournament_id: UUID,
            groups: list[GroupUpdate]) -> list[Group]:
        """
        Update existing groups.

        Args:
            tournament_id (UUID): The id of the tournament whose groups are
                to be updated.
            groups (list[GroupUpdate]): The groups to update.

        Returns:
            list[Group]: The newly updated groups.
        """
        self.__tournament_service.get_tournament_by_id(tournament_id)

        if not self.__tournament_has_group_stage(tournament_id):
            raise HTTPException(
                status_code=404,
                detail="The tournament with the supplied id does not have a "
                       "group stage."
            )

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.UPDATE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Group.get_target_table(tournament_id)
                ),
                records=list(
                    map(
                        lambda group:
                        group.model_dump(exclude_none=True),
                        groups
                    )
                )
            )
        )

        return self.__retrieve_and_build_groups(
            tournament_id,
            QueryConditionGroup.of(
                QueryCondition(
                    column=Column.of("group", StoreConstants.ID),
                    operator=ConditionOperator.IN,
                    value=list(
                        map(
                            lambda group:
                            group.id,
                            groups
                        )
                    )
                )
            )
        )

    def get_group_by_id(self, tournament_id: UUID, group_id: UUID) -> Group:
        """
        Retrieve a single stored group by its id.

        Args:
            tournament_id (UUID): The id of the tournament the group belongs
                to.
            group_id (UUID): The id of the group to retrieve.

        Returns:
            Group: The retrieved group.
        """
        self.__tournament_service.get_tournament_by_id(tournament_id)

        if not self.__tournament_has_group_stage(tournament_id):
            raise HTTPException(
                status_code=404,
                detail="The tournament with the supplied id does not have a "
                       "group stage."
            )

        group_response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Group.get_target_table(tournament_id)
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        group_id
                    )
                )
            )
        )

        if len(group_response.records) == 0:
            raise HTTPException(
                status_code=404,
                detail="No groups found with a matching id."
            )

        return self.__retrieve_and_build_groups(
            tournament_id,
            QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("group", StoreConstants.ID),
                    group_id
                )
            )
        )[0]

    def add_teams_to_group(
            self,
            tournament_id: UUID,
            group_id: UUID,
            team_ids: list[UUID]) -> Group:
        """
        Add teams to a group.

        Args:
             tournament_id (UUID): The id of the tournament the group belongs
                to.
             group_id (UUID): The id of the group to add teams to.
             team_ids (list[UUID]): The ids of the teams to add to the group.

        Returns:
            Group: The updated group.
        """
        self.__tournament_service.get_tournament_by_id(tournament_id)

        if not self.__tournament_has_group_stage(tournament_id):
            raise HTTPException(
                status_code=404,
                detail="The tournament with the supplied id does not have a "
                       "group stage."
            )

        group_response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Group.get_target_table(tournament_id)
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        group_id
                    )
                )
            )
        )

        if len(group_response.records) == 0:
            raise HTTPException(
                status_code=404,
                detail="No groups found with a matching id."
            )

        team_records: list[dict[str, Any]] = (
            self.__query_service.retrieve_records(
                QueryRequest(
                    table=Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Team.TARGET_TABLE
                    ),
                    conditionGroup=QueryConditionGroup.of(
                        QueryCondition(
                            column=Column.of(StoreConstants.ID),
                            operator=ConditionOperator.IN,
                            value=team_ids
                        )
                    )
                )
            ).records
        )

        existing_ids: list[UUID] = list(
            map(
                lambda team:
                UUID(team[StoreConstants.ID]),
                team_records
            )
        )
        invalid_ids: list[UUID] = list(set(team_ids) - set(existing_ids))

        if len(invalid_ids) > 0:
            raise HTTPException(
                status_code=400,
                detail="No teams found with ids: " + str(
                    list(
                        map(
                            lambda team_id:
                            str(team_id),
                            invalid_ids
                        )
                    )
                )
            )

        group_team_response: QueryResponse = (
            self.__query_service.retrieve_records(
                QueryRequest(
                    table=Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        PredictorConstants.get_group_teams_table(tournament_id)
                    ),
                    conditionGroup=QueryConditionGroup.of(
                        QueryCondition.of(
                            Column.of("groupId"),
                            group_id
                        )
                    )
                )
            )
        )

        template_response: QueryResponse = (
            self.__query_service.retrieve_records(
                QueryRequest(
                    columns=[
                        Column.of("league", "teamsPerGroup")
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
        )

        if (len(group_team_response.records) + len(team_ids)
                > template_response.records[0]["teamsPerGroup"]):
            raise HTTPException(
                status_code=409,
                detail="The number of groups in this tournament's group stage "
                       "has been exceeded."
            )

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.INSERT,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    PredictorConstants.get_group_teams_table(tournament_id)
                ),
                records=list(
                    map(
                        lambda team_id:
                        {
                            "groupId": group_id,
                            "teamId": team_id
                        },
                        team_ids
                    )
                )
            )
        )

        return self.__retrieve_and_build_groups(
            tournament_id,
            QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("group", StoreConstants.ID),
                    group_id
                )
            )
        )[0]

    def remove_team_from_group(
            self,
            tournament_id: UUID,
            group_id: UUID,
            team_id: UUID) -> Group:
        """
        Remove a single team from a group.

        Args:
            tournament_id (UUID): The id of the tournament the group belongs
                to.
            group_id (UUID): The id of the group to remove the team from.
            team_id (UUID): The id of the team to remove from the group.

        Return:
            Group: The updated group.
        """
        self.__tournament_service.get_tournament_by_id(tournament_id)

        if not self.__tournament_has_group_stage(tournament_id):
            raise HTTPException(
                status_code=404,
                detail="The tournament with the supplied id does not have a "
                       "group stage."
            )

        group_response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Group.get_target_table(tournament_id)
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        group_id
                    )
                )
            )
        )

        if len(group_response.records) == 0:
            raise HTTPException(
                status_code=404,
                detail="No groups found with a matching id."
            )

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.DELETE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    PredictorConstants.get_group_teams_table(tournament_id)
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(Column.of("groupId"), group_id),
                    QueryCondition.of(Column.of("teamId"), team_id)
                )
            )
        )

        return self.__retrieve_and_build_groups(
            tournament_id,
            QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("group", StoreConstants.ID),
                    group_id
                )
            )
        )[0]

    def __tournament_has_group_stage(self, tournament_id: UUID) -> bool:
        """
        Determine whether a tournament has a group stage or not.

        Args:
            tournament_id (UUID): The id of the tournament.

        Returns:
            bool: True if the tournament has a group stage.
        """
        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                columns=[
                    Column.of("temp", "leagueTemplateId")
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

        return response.records[0]["leagueTemplateId"] is not None

    def __retrieve_and_build_groups(
            self,
            tournament_id: UUID,
            condition_group: QueryConditionGroup = None) -> list[Group]:
        """
        Retrieve a set of groups and build them into objects containing their
        teams.

        Args:
             tournament_id (UUID): The id of the tournament the groups belong
                to.
             condition_group (QueryConditionGroup): The conditions by which
                to filter the groups by.

        Returns:
            list[Group]: The retrieved groups.
        """
        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Group.get_target_table(tournament_id),
                    "group"
                ),
                conditionGroup=condition_group,
                orderBy=[
                    OrderBy.of(Column.of("group", "name"))
                ]
            )
        )

        groups: list[Group] = list(
            map(
                lambda record:
                Group.model_validate(record),
                response.records
            )
        )

        team_response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                columns=[
                    Column.of("gt", "groupId"),
                    Column.of("team", StoreConstants.ID),
                    Column.of("team", "name"),
                    Column.of("team", "imagePath"),
                    Column.of("team", "confederation")
                ],
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    PredictorConstants.get_group_teams_table(tournament_id),
                    "gt"
                ),
                tableJoins=[
                    TableJoin.of(
                        Table.of(
                            PredictorConstants.PREDICTOR_SCHEMA,
                            Team.TARGET_TABLE,
                            "team"
                        ),
                        QueryCondition.of(
                            Column.of("gt", "teamId"),
                            Column.of("team", StoreConstants.ID)
                        ),
                        TableJoinType.INNER
                    ),
                    TableJoin.of(
                        Table.of(
                            PredictorConstants.PREDICTOR_SCHEMA,
                            Group.get_target_table(tournament_id),
                            "group"
                        ),
                        QueryCondition.of(
                            Column.of("gt", "groupId"),
                            Column.of("group", StoreConstants.ID)
                        ),
                        TableJoinType.INNER
                    )
                ],
                conditionGroup=condition_group,
                orderBy=[
                    OrderBy.of(
                        Column.of("team", "name")
                    )
                ]
            )
        )

        return list(
            map(
                lambda group:
                group.model_copy(update={
                    "teams": list(
                        map(
                            lambda filtered:
                            Team.model_validate(filtered),
                            list(
                                filter(
                                    lambda record:
                                    UUID(record["groupId"]) == group.id,
                                    team_response.records
                                )
                            )
                        )
                    )
                }),
                groups
            )
        )
