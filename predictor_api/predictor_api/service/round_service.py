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
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.round import Round
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


class RoundService:

    def __init__(
            self,
            database_query_service: DatabaseQueryService,
            tournament_service: TournamentService) -> None:
        self.__query_service = database_query_service
        self.__tournament_service = tournament_service

    def get_rounds(self, tournament_id: UUID) -> list[Round]:
        self.__tournament_service.get_tournament_by_id(tournament_id)

        if not self.__tournament_has_knockout_stage(tournament_id):
            raise HTTPException(
                status_code=404,
                detail="The tournament with the supplied id does not have a "
                       "knockout stage."
            )

        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Round.get_target_table(tournament_id)
                ),
                orderBy=OrderBy.of(
                    Column.of("roundOrder")
                )
            )
        )

        return list(
            map(
                lambda record:
                Round.model_validate(record),
                response.records
            )
        )

    def __tournament_has_knockout_stage(self, tournament_id: UUID) -> bool:
        """
        Determine whether a tournament has a knockout stage or not.

        Args:
            tournament_id (UUID): The id of the tournament.

        Returns:
            bool: True if the tournament has a knockout stage.
        """
        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                columns=[
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

        return response.records[0]["knockoutTemplateId"] is not None
