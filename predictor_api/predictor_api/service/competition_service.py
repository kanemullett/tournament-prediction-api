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
from predictor_api.predictor_api.model.competition import Competition
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class CompetitionService:

    def __init__(self, database_query_service: DatabaseQueryService) -> None:
        self.__query_service = database_query_service

    def get_competitions(self) -> list[Competition]:
        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Competition.TARGET_TABLE
                )
            )
        )

        return list(
            map(
                lambda record:
                Competition.model_validate(record),
                response.records
            )
        )

    def create_competitions(
            self,
            competitions: list[Competition]) -> list[Competition]:
        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.INSERT,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Competition.TARGET_TABLE
                ),
                records=list(
                    map(
                        lambda competition:
                        competition.model_dump(exclude_none=True),
                        competitions
                    )
                )
            )
        )

        return competitions

    def update_competitions(
            self,
            competitions: list[Competition]) -> list[Competition]:
        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.UPDATE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Competition.TARGET_TABLE
                ),
                records=list(
                    map(
                        lambda competition:
                        competition.model_dump(exclude_none=True),
                        competitions
                    )
                )
            )
        )

        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Competition.TARGET_TABLE
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition(
                        column=Column.of(StoreConstants.ID),
                        operator=ConditionOperator.IN,
                        value=list(
                            map(
                                lambda competition:
                                competition.id,
                                competitions
                            )
                        )
                    )
                )
            )
        )

        return list(
            map(
                lambda record:
                Competition.model_validate(record),
                response.records
            )
        )

    def get_competition_by_id(self, competition_id: UUID) -> Competition:
        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Competition.TARGET_TABLE
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        competition_id
                    )
                )
            )
        )

        if response.recordCount == 0:
            raise HTTPException(
                status_code=404,
                detail="No competitions found with a matching id."
            )

        return Competition.model_validate(response.records[0])

    def delete_competition_by_id(self, competition_id: UUID) -> None:
        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.DELETE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Competition.TARGET_TABLE
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        competition_id
                    )
                )
            )
        )
