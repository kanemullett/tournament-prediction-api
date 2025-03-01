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
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament_template import TournamentTemplate
from predictor_api.predictor_api.util.predictor_constants import PredictorConstants


class LeagueTemplateService:
    """
    Service for performing league template-related actions.

    Attributes:
        __database_query_service (DatabaseQueryService): The database query service.
    """

    def __init__(self, database_query_service: DatabaseQueryService):
        """
        Initialise the LeagueTemplateService.

        Args:
            database_query_service (DatabaseQueryService): The database query service.
        """
        self.__database_query_service = database_query_service

    def get_league_templates(self) -> list[LeagueTemplate]:
        """
        Retrieve stored league templates.

        Returns:
            list[LeagueTemplate]: The stored league templates.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=LeagueTemplate.TARGET_TABLE
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        return list(map(lambda record: LeagueTemplate.model_validate(record), query_response.records))

    def create_league_templates(self, league_templates: list[LeagueTemplate]) -> list[LeagueTemplate]:
        """
        Create new league templates.

        Args:
            league_templates (list[LeagueTemplate]): The new league templates to create.

        Returns:
            list[LeagueTemplate]: The newly created league templates.
        """
        records: list[dict[str, Any]] = list(
            map(lambda league_template: league_template.model_dump(), league_templates)
        )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.INSERT,
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=LeagueTemplate.TARGET_TABLE
            ),
            records=records
        )

        self.__database_query_service.update_records(update_request)

        return league_templates

    def get_league_template_by_id(self, league_template_id: UUID) -> LeagueTemplate:
        """
        Retrieve a single stored league template by its id.

        Args:
            league_template_id (UUID): The id of the league template to retrieve.

        Returns:
            LeagueTemplate: The retrieved league template.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=LeagueTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column(
                            parts=[StoreConstants.ID]
                        ),
                        operator=ConditionOperator.EQUAL,
                        value=league_template_id
                    )
                ]
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        if len(query_response.records) == 0:
            raise HTTPException(status_code=404, detail="No league templates found with a matching id.")

        return list(map(lambda record: LeagueTemplate.model_validate(record), query_response.records))[0]

    def delete_league_template_by_id(self, league_template_id: UUID):
        """
        Delete a single stored league template by its id.

        Args:
            league_template_id (UUID): The id of the league template to delete.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=TournamentTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column(
                            parts=["leagueTemplateId"]
                        ),
                        operator=ConditionOperator.EQUAL,
                        value=league_template_id
                    )
                ]
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        if query_response.recordCount > 0:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete league template as it is part of an existing tournament template."
            )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.DELETE,
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=LeagueTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column(
                            parts=[StoreConstants.ID]
                        ),
                        operator=ConditionOperator.EQUAL,
                        value=league_template_id
                    )
                ]
            )
        )

        self.__database_query_service.update_records(update_request)
