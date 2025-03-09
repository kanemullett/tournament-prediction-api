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
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class TeamService:
    """
    Service for performing team-related actions.

    Attributes:
        __query_service (DatabaseQueryService): The database query service.
    """

    def __init__(self, database_query_service: DatabaseQueryService) -> None:
        """
        Initialise the TeamService.

        Args:
            database_query_service (DatabaseQueryService): The database query
                service.
        """
        self.__query_service = database_query_service

    def get_teams(
            self,
            confederation: Confederation = None,
            tournament_id: UUID = None) -> list[Team]:
        """
        Retrieve stored teams.

        Returns:
            list[Team]: The stored teams.
        """
        if tournament_id is not None:
            raise HTTPException(
                status_code=501,
                detail="Filtering teams by tournamentId is not yet "
                       "implemented."
            )

        conditions: list[QueryCondition] = []

        if confederation is not None:
            conditions.append(
                QueryCondition.of(
                    Column.of("confederation"),
                    confederation
                )
            )

        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Team.TARGET_TABLE
                ),
                conditionGroup=(
                    QueryConditionGroup(
                        conditions=conditions
                    ) if len(conditions) > 0
                    else None
                ),
                orderBy=OrderBy.of(
                    Column.of("name")
                )
            )
        )

        return list(
            map(
                lambda record:
                Team.model_validate(record),
                response.records
            )
        )

    def create_teams(self, teams: list[Team]) -> list[Team]:
        """
        Create new teams.

        Args:
            teams (list[Team]): The new teams to create.

        Returns:
            list[Team]: The newly created teams.
        """
        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.INSERT,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Team.TARGET_TABLE
                ),
                records=list(
                    map(
                        lambda team:
                        team.model_dump(exclude_none=True),
                        teams
                    )
                )
            )
        )

        return teams

    def update_teams(self, teams: list[Team]) -> list[Team]:
        """
        Update existing teams.

        Args:
            teams (list[Team]): The teams to update.

        Returns:
            list[Team]: The newly updated teams.
        """
        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.UPDATE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Team.TARGET_TABLE
                ),
                records=list(
                    map(
                        lambda team:
                        team.model_dump(exclude_none=True),
                        teams
                    )
                )
            )
        )

        updated_ids: list[UUID] = list(
            map(
                lambda team:
                team.id,
                teams
            )
        )

        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Team.TARGET_TABLE
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition(
                        column=Column.of(StoreConstants.ID),
                        operator=ConditionOperator.IN,
                        value=updated_ids
                    )
                ),
                orderBy=OrderBy.of(
                    Column.of("name")
                )
            )
        )

        return list(
            map(
                lambda record:
                Team.model_validate(record),
                response.records
            )
        )

    def get_team_by_id(self, team_id: UUID) -> Team:
        """
        Retrieve a single stored team by its id.

        Args:
            team_id (UUID): The id of the team to retrieve.

        Returns:
            Team: The retrieved team.
        """
        query_response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Team.TARGET_TABLE
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        team_id
                    )
                )
            )
        )

        if query_response.recordCount == 0:
            raise HTTPException(
                status_code=404,
                detail="No teams found with a matching id."
            )

        return Team.model_validate(query_response.records[0])

    def delete_team_by_id(self, team_id: UUID) -> None:
        """
        Delete a single stored team by its id.

        Args:
            team_id (UUID): The id of the team to delete.
        """
        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.DELETE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Team.TARGET_TABLE
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        team_id
                    )
                )
            )
        )
