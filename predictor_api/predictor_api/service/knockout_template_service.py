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
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.knockout_template import (
    KnockoutTemplate
)
from predictor_api.predictor_api.model.tournament_template import (
    TournamentTemplate
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class KnockoutTemplateService:
    """
    Service for performing knockout template-related actions.

    Attributes:
        __query_service (DatabaseQueryService): The database query service.
    """

    def __init__(self, database_query_service: DatabaseQueryService):
        """
        Initialise the KnockoutTemplateService.

        Args:
            database_query_service (DatabaseQueryService): The database query
                service.
        """
        self.__query_service = database_query_service

    def get_knockout_templates(self) -> list[KnockoutTemplate]:
        """
        Retrieve stored knockout templates.

        Returns:
            list[KnockoutTemplate]: The stored knockout templates.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                KnockoutTemplate.TARGET_TABLE
            )
        )

        query_response: QueryResponse = (
            self.__query_service.retrieve_records(query_request)
        )

        return list(
            map(
                lambda record:
                KnockoutTemplate.model_validate(record),
                query_response.records
            )
        )

    def create_knockout_templates(
            self,
            knockout_templates: list[KnockoutTemplate]
    ) -> list[KnockoutTemplate]:
        """
        Create new knockout templates.

        Args:
            knockout_templates (list[KnockoutTemplate]): The new knockout
                templates to create.

        Returns:
            list[KnockoutTemplate]: The newly created knockout templates.
        """
        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.INSERT,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    KnockoutTemplate.TARGET_TABLE
                ),
                records=list(
                    map(
                        lambda template:
                        template.model_dump(exclude_none=True),
                        knockout_templates
                    )
                )
            )
        )

        return knockout_templates

    def get_knockout_template_by_id(
            self,
            knockout_template_id: UUID) -> KnockoutTemplate:
        """
        Retrieve a single stored knockout template by its id.

        Args:
            knockout_template_id (UUID): The id of the knockout template to
                retrieve.

        Returns:
            KnockoutTemplate: The retrieved knockout template.
        """
        query_response: QueryResponse = (
            self.__query_service.retrieve_records(
                QueryRequest(
                    table=Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        KnockoutTemplate.TARGET_TABLE
                    ),
                    conditionGroup=QueryConditionGroup.of(
                        QueryCondition.of(
                            Column.of(StoreConstants.ID),
                            knockout_template_id
                        )
                    )
                )
            )
        )

        if len(query_response.records) == 0:
            raise HTTPException(
                status_code=404,
                detail="No knockout templates found with a matching id."
            )

        return KnockoutTemplate.model_validate(
            query_response.records[0]
        )

    def delete_knockout_template_by_id(
            self,
            knockout_template_id: UUID) -> None:
        """
        Delete a single stored knockout template by its id.

        Args:
            knockout_template_id (UUID): The id of the knockout template to
                delete.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                TournamentTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("knockoutTemplateId"),
                    knockout_template_id
                )
            )
        )

        query_response: QueryResponse = (
            self.__query_service.retrieve_records(query_request)
        )

        if query_response.recordCount > 0:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete knockout template as it is part of an "
                       "existing tournament template."
            )

        self.__query_service.update_records(
            UpdateRequest(
                operation=SqlOperator.DELETE,
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    KnockoutTemplate.TARGET_TABLE
                ),
                conditionGroup=QueryConditionGroup.of(
                    QueryCondition.of(
                        Column.of(StoreConstants.ID),
                        knockout_template_id
                    )
                )
            )
        )
