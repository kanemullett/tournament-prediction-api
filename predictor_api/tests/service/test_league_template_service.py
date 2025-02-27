from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.condition_operator import ConditionOperator
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.service.league_template_service import LeagueTemplateService
from predictor_api.predictor_api.util.predictor_constants import PredictorConstants
from predictor_common.test_resources.assertions import Assertions


class TestLeagueTemplateService:

    __database_query_service: MagicMock = MagicMock()

    __league_template_service: LeagueTemplateService = LeagueTemplateService(__database_query_service)

    def test_should_return_league_templates(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=2,
            records=[
                {
                    "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                    "name": "8x4 Group-Stage Single-Game",
                    "groupCount": 8,
                    "teamsPerGroup": 4,
                    "homeAndAway": False
                },
                {
                    "id": "6ee28143-1286-4618-a8b9-ad86d348ead1",
                    "name": "6x4 Group-Stage Single-Game",
                    "groupCount": 6,
                    "teamsPerGroup": 4,
                    "homeAndAway": False
                }
            ]
        )

        # When
        league_templates: list[LeagueTemplate] = self.__league_template_service.get_league_templates()

        # Then
        captured_args_retrieve_records, captured_kwargs = self.__database_query_service.retrieve_records.call_args
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]
        table: Table = query_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("league-templates", table.table)

        Assertions.assert_equals(2, len(league_templates))

        template1 = league_templates[0]
        Assertions.assert_type(LeagueTemplate, template1)
        Assertions.assert_type(UUID, template1.id)
        Assertions.assert_equals("8x4 Group-Stage Single-Game", template1.name)
        Assertions.assert_equals(8, template1.groupCount)
        Assertions.assert_equals(4, template1.teamsPerGroup)
        Assertions.assert_false(template1.homeAndAway)

        template2 = league_templates[1]
        Assertions.assert_type(LeagueTemplate, template2)
        Assertions.assert_type(UUID, template2.id)
        Assertions.assert_equals("6x4 Group-Stage Single-Game", template2.name)
        Assertions.assert_equals(6, template2.groupCount)
        Assertions.assert_equals(4, template2.teamsPerGroup)
        Assertions.assert_false(template2.homeAndAway)

    def test_should_create_league_templates(self):
        # Given
        league_templates: list[LeagueTemplate] = [
            LeagueTemplate(
                name="8x4 Group-Stage Single-Game",
                groupCount=8,
                teamsPerGroup=4,
                homeAndAway=False
            ),
            LeagueTemplate(
                name="6x4 Group-Stage Single-Game",
                groupCount=6,
                teamsPerGroup=4,
                homeAndAway=False
            )
        ]

        # When
        created: list[LeagueTemplate] = self.__league_template_service.create_league_templates(league_templates)

        # Then
        captured_args_retrieve_records, captured_kwargs = self.__database_query_service.update_records.call_args
        Assertions.assert_type(UpdateRequest, captured_args_retrieve_records[0])

        update_request: UpdateRequest = captured_args_retrieve_records[0]
        Assertions.assert_equals(SqlOperator.INSERT, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("league-templates", table.table)

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_type(UUID, record1["id"])
        Assertions.assert_equals("8x4 Group-Stage Single-Game", record1["name"])
        Assertions.assert_equals(8, record1["groupCount"])
        Assertions.assert_equals(4, record1["teamsPerGroup"])
        Assertions.assert_false(record1["homeAndAway"])

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_type(UUID, record2["id"])
        Assertions.assert_equals("6x4 Group-Stage Single-Game", record2["name"])
        Assertions.assert_equals(6, record2["groupCount"])
        Assertions.assert_equals(4, record2["teamsPerGroup"])
        Assertions.assert_false(record2["homeAndAway"])

        Assertions.assert_equals(2, len(created))

        template1 = created[0]
        Assertions.assert_type(LeagueTemplate, template1)
        Assertions.assert_type(UUID, template1.id)
        Assertions.assert_equals("8x4 Group-Stage Single-Game", template1.name)
        Assertions.assert_equals(8, template1.groupCount)
        Assertions.assert_equals(4, template1.teamsPerGroup)
        Assertions.assert_false(template1.homeAndAway)

        template2 = created[1]
        Assertions.assert_type(LeagueTemplate, template2)
        Assertions.assert_type(UUID, template2.id)
        Assertions.assert_equals("6x4 Group-Stage Single-Game", template2.name)
        Assertions.assert_equals(6, template2.groupCount)
        Assertions.assert_equals(4, template2.teamsPerGroup)
        Assertions.assert_false(template2.homeAndAway)

    def test_should_return_league_template_by_id(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=1,
            records=[
                {
                    "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                    "name": "8x4 Group-Stage Single-Game",
                    "groupCount": 8,
                    "teamsPerGroup": 4,
                    "homeAndAway": False
                }
            ]
        )

        # When
        league_template: LeagueTemplate = self.__league_template_service.get_league_template_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        )

        # Then
        captured_args_retrieve_records, captured_kwargs = self.__database_query_service.retrieve_records.call_args
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]
        table: Table = query_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("league-templates", table.table)

        condition: QueryCondition = query_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"), condition.value)

        Assertions.assert_type(LeagueTemplate, league_template)
        Assertions.assert_equals(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"), league_template.id)
        Assertions.assert_equals("8x4 Group-Stage Single-Game", league_template.name)
        Assertions.assert_equals(8, league_template.groupCount)
        Assertions.assert_equals(4, league_template.teamsPerGroup)
        Assertions.assert_false(league_template.homeAndAway)

    def test_should_raise_exception_if_league_template_not_found(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=0,
            records=[]
        )

        # When
        with raises(HTTPException) as httpe:
            self.__league_template_service.get_league_template_by_id(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"))

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("No league templates found with a matching id.", httpe.value.detail)

    def test_should_delete_league_template_by_id(self):
        # When
        self.__league_template_service.delete_league_template_by_id(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"))

        # Then
        captured_args_update_records, captured_kwargs = self.__database_query_service.update_records.call_args
        Assertions.assert_type(UpdateRequest, captured_args_update_records[0])

        update_request: UpdateRequest = captured_args_update_records[0]
        Assertions.assert_equals(SqlOperator.DELETE, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("league-templates", table.table)

        condition: QueryCondition = update_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"), condition.value)

    def test_should_not_delete_league_template_if_used_by_tournament_template(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=1,
            records=[
                {
                    "id": "793c861f-f541-4ef7-adfa-a8cdd60c7d06",
                    "name": "32-Team Group & Knockout",
                    "leagueTemplateId": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                    "knockoutTemplateId": "8b065f5c-75a0-470b-b0f9-ac7a2e033723"
                }
            ]
        )

        # When
        with raises(HTTPException) as httpe:
            self.__league_template_service.delete_league_template_by_id(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"))

        # Then
        Assertions.assert_equals(409, httpe.value.status_code)
        Assertions.assert_equals(
            "Cannot delete league template as it is part of an existing tournament template.",
            httpe.value.detail
        )
