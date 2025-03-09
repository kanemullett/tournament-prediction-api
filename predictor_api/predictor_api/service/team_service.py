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
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class TeamService:

    def __init__(self, database_query_service: DatabaseQueryService) -> None:
        self.__query_service = database_query_service

    def get_teams(
            self,
            confederation: Confederation = None,
            tournament_id: UUID = None) -> list[Team]:
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
