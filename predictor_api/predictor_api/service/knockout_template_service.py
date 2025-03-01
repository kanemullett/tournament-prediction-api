from typing import Any
from uuid import UUID

from fastapi import HTTPException

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import DatabaseQueryService
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.model.tournament_template import TournamentTemplate
from predictor_api.predictor_api.util.predictor_constants import PredictorConstants


class KnockoutTemplateService:
    """
    Service for performing knockout template-related actions.

    Attributes:
        __database_query_service (DatabaseQueryService): The database query service.
    """

    def __init__(self, database_query_service: DatabaseQueryService):
        """
        Initialise the KnockoutTemplateService.

        Args:
            database_query_service (DatabaseQueryService): The database query service.
        """
        self.__database_query_service = database_query_service

    def get_knockout_templates(self) -> list[KnockoutTemplate]:
        """
        Retrieve stored knockout templates.

        Returns:
            list[KnockoutTemplate]: The stored knockout templates.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=KnockoutTemplate.TARGET_TABLE
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        return list(map(lambda record: KnockoutTemplate.model_validate(record), query_response.records))

    def create_knockout_templates(self, knockout_templates: list[KnockoutTemplate]) -> list[KnockoutTemplate]:
        """
        Create new knockout templates.

        Args:
            knockout_templates (list[KnockoutTemplate]): The new knockout templates to create.

        Returns:
            list[KnockoutTemplate]: The newly created knockout templates.
        """
        records: list[dict[str, Any]] = list(
            map(lambda knockout_template: knockout_template.model_dump(), knockout_templates)
        )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.INSERT,
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=KnockoutTemplate.TARGET_TABLE
            ),
            records=records
        )

        self.__database_query_service.update_records(update_request)

        return knockout_templates

    def get_knockout_template_by_id(self, knockout_template_id: UUID) -> KnockoutTemplate:
        """
        Retrieve a single stored knockout template by its id.

        Args:
            knockout_template_id (UUID): The id of the knockout template to retrieve.

        Returns:
            KnockoutTemplate: The retrieved knockout template.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=KnockoutTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition.of(Column.of(StoreConstants.ID), knockout_template_id)
                ]
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        if len(query_response.records) == 0:
            raise HTTPException(status_code=404, detail="No knockout templates found with a matching id.")

        return list(map(lambda record: KnockoutTemplate.model_validate(record), query_response.records))[0]

    def delete_knockout_template_by_id(self, knockout_template_id: UUID):
        """
        Delete a single stored knockout template by its id.

        Args:
            knockout_template_id (UUID): The id of the knockout template to delete.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=TournamentTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition.of(Column.of("knockoutTemplateId"), knockout_template_id)
                ]
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        if query_response.recordCount > 0:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete knockout template as it is part of an existing tournament template."
            )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.DELETE,
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=KnockoutTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition.of(Column.of(StoreConstants.ID), knockout_template_id)
                ]
            )
        )

        self.__database_query_service.update_records(update_request)
