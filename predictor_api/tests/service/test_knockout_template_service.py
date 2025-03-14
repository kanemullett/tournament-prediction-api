from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from predictor_api.predictor_api.model.round_template import RoundTemplate
from predictor_api.predictor_api.model.knockout_template import (
    KnockoutTemplate
)
from predictor_api.predictor_api.service.knockout_template_service import (
    KnockoutTemplateService
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)
from predictor_common.test_resources.assertions import Assertions


class TestKnockoutTemplateService:

    __query_service: MagicMock = MagicMock()

    __service: KnockoutTemplateService = (
        KnockoutTemplateService(__query_service)
    )

    def setup_method(self):
        self.__query_service.retrieve_records.reset_mock()
        self.__query_service.retrieve_records.return_value = None
        self.__query_service.retrieve_records.side_effect = None

        self.__query_service.update_records.reset_mock()
        self.__query_service.update_records.return_value = None
        self.__query_service.update_records.side_effect = None

    def test_should_return_knockout_templates(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=2,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "name": "16-Team Single-Leg",
                        "rounds": [
                            {
                                "name": "Round of 16",
                                "teamCount": 16,
                                "roundOrder": 1,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Quarter-Finals",
                                "teamCount": 8,
                                "roundOrder": 2,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Semi-Finals",
                                "teamCount": 4,
                                "roundOrder": 3,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Third-Place Play-Off",
                                "teamCount": 2,
                                "roundOrder": 4,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Final",
                                "teamCount": 2,
                                "roundOrder": 5,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            }
                        ]
                    },
                    {
                        "id": "6ee28143-1286-4618-a8b9-ad86d348ead1",
                        "name": "8-Team Double-Leg Away Goals",
                        "rounds": [
                            {
                                "name": "Quarter-Finals",
                                "teamCount": 8,
                                "roundOrder": 1,
                                "twoLegs": True,
                                "extraTime": True,
                                "awayGoals": True
                            },
                            {
                                "name": "Semi-Finals",
                                "teamCount": 4,
                                "roundOrder": 2,
                                "twoLegs": True,
                                "extraTime": True,
                                "awayGoals": True
                            },
                            {
                                "name": "Final",
                                "teamCount": 2,
                                "roundOrder": 3,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            }
                        ]
                    }
                ]
            )
        ]

        # When
        knockout_templates: list[KnockoutTemplate] = (
            self.__service.get_knockout_templates()
        )

        # Then
        templates_args, templates_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[0]
        Assertions.assert_type(QueryRequest, templates_args[0])

        templates_request: QueryRequest = templates_args[0]
        tr_table: Table = templates_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            tr_table.schema_
        )
        Assertions.assert_equals("knockout-templates", tr_table.table)

        Assertions.assert_equals(2, len(knockout_templates))

        template1 = knockout_templates[0]
        Assertions.assert_type(KnockoutTemplate, template1)
        Assertions.assert_type(UUID, template1.id)
        Assertions.assert_equals("16-Team Single-Leg", template1.name)
        Assertions.assert_equals(5, len(template1.rounds))

        template1_round1 = template1.rounds[0]
        Assertions.assert_type(RoundTemplate, template1_round1)
        Assertions.assert_equals("Round of 16", template1_round1.name)
        Assertions.assert_equals(16, template1_round1.teamCount)
        Assertions.assert_equals(1, template1_round1.roundOrder)
        Assertions.assert_false(template1_round1.twoLegs)
        Assertions.assert_true(template1_round1.extraTime)
        Assertions.assert_false(template1_round1.awayGoals)

        template1_round2 = template1.rounds[1]
        Assertions.assert_type(RoundTemplate, template1_round2)
        Assertions.assert_equals("Quarter-Finals", template1_round2.name)
        Assertions.assert_equals(8, template1_round2.teamCount)
        Assertions.assert_equals(2, template1_round2.roundOrder)
        Assertions.assert_false(template1_round2.twoLegs)
        Assertions.assert_true(template1_round2.extraTime)
        Assertions.assert_false(template1_round2.awayGoals)

        template1_round3 = template1.rounds[2]
        Assertions.assert_type(RoundTemplate, template1_round3)
        Assertions.assert_equals("Semi-Finals", template1_round3.name)
        Assertions.assert_equals(4, template1_round3.teamCount)
        Assertions.assert_equals(3, template1_round3.roundOrder)
        Assertions.assert_false(template1_round3.twoLegs)
        Assertions.assert_true(template1_round3.extraTime)
        Assertions.assert_false(template1_round3.awayGoals)

        template1_round4 = template1.rounds[3]
        Assertions.assert_type(RoundTemplate, template1_round4)
        Assertions.assert_equals("Third-Place Play-Off", template1_round4.name)
        Assertions.assert_equals(2, template1_round4.teamCount)
        Assertions.assert_equals(4, template1_round4.roundOrder)
        Assertions.assert_false(template1_round4.twoLegs)
        Assertions.assert_true(template1_round4.extraTime)
        Assertions.assert_false(template1_round4.awayGoals)

        template1_round5 = template1.rounds[4]
        Assertions.assert_type(RoundTemplate, template1_round5)
        Assertions.assert_equals("Final", template1_round5.name)
        Assertions.assert_equals(2, template1_round5.teamCount)
        Assertions.assert_equals(5, template1_round5.roundOrder)
        Assertions.assert_false(template1_round5.twoLegs)
        Assertions.assert_true(template1_round5.extraTime)
        Assertions.assert_false(template1_round5.awayGoals)

        template2 = knockout_templates[1]
        Assertions.assert_type(KnockoutTemplate, template2)
        Assertions.assert_type(UUID, template2.id)
        Assertions.assert_equals(
            "8-Team Double-Leg Away Goals",
            template2.name
        )
        Assertions.assert_equals(3, len(template2.rounds))

        template2_round1 = template2.rounds[0]
        Assertions.assert_type(RoundTemplate, template2_round1)
        Assertions.assert_equals("Quarter-Finals", template2_round1.name)
        Assertions.assert_equals(8, template2_round1.teamCount)
        Assertions.assert_equals(1, template2_round1.roundOrder)
        Assertions.assert_true(template2_round1.twoLegs)
        Assertions.assert_true(template2_round1.extraTime)
        Assertions.assert_true(template2_round1.awayGoals)

        template2_round2 = template2.rounds[1]
        Assertions.assert_type(RoundTemplate, template2_round2)
        Assertions.assert_equals("Semi-Finals", template2_round2.name)
        Assertions.assert_equals(4, template2_round2.teamCount)
        Assertions.assert_equals(2, template2_round2.roundOrder)
        Assertions.assert_true(template2_round2.twoLegs)
        Assertions.assert_true(template2_round2.extraTime)
        Assertions.assert_true(template2_round2.awayGoals)

        template2_round3 = template2.rounds[2]
        Assertions.assert_type(RoundTemplate, template2_round3)
        Assertions.assert_equals("Final", template2_round3.name)
        Assertions.assert_equals(2, template2_round3.teamCount)
        Assertions.assert_equals(3, template2_round3.roundOrder)
        Assertions.assert_false(template2_round3.twoLegs)
        Assertions.assert_true(template2_round3.extraTime)
        Assertions.assert_false(template2_round3.awayGoals)

    def test_should_create_knockout_templates(self):
        # Given
        created: list[KnockoutTemplate] = [
            KnockoutTemplate(
                name="16-Team Single-Leg",
                rounds=[
                    RoundTemplate(
                        name="Round of 16",
                        teamCount=16,
                        roundOrder=1,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    ),
                    RoundTemplate(
                        name="Quarter-Finals",
                        teamCount=8,
                        roundOrder=2,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    ),
                    RoundTemplate(
                        name="Semi-Finals",
                        teamCount=4,
                        roundOrder=3,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    ),
                    RoundTemplate(
                        name="Third-Place Play-Off",
                        teamCount=2,
                        roundOrder=4,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    ),
                    RoundTemplate(
                        name="Final",
                        teamCount=2,
                        roundOrder=5,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            ),
            KnockoutTemplate(
                name="8-Team Double-Leg Away Goals",
                rounds=[
                    RoundTemplate(
                        name="Quarter-Finals",
                        teamCount=8,
                        roundOrder=1,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    RoundTemplate(
                        name="Semi-Finals",
                        teamCount=4,
                        roundOrder=2,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    RoundTemplate(
                        name="Final",
                        teamCount=2,
                        roundOrder=3,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            )
        ]

        # When
        created: list[KnockoutTemplate] = (
            self.__service.create_knockout_templates(created)
        )

        # Then
        templates_args, templates_kwargs = (
            self.__query_service.update_records.call_args_list
        )[0]
        Assertions.assert_type(
            UpdateRequest,
            templates_args[0]
        )

        templates_request: UpdateRequest = templates_args[0]
        Assertions.assert_equals(
            SqlOperator.INSERT,
            templates_request.operation
        )

        templates_table: Table = templates_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            templates_table.schema_
        )
        Assertions.assert_equals("knockout-templates", templates_table.table)

        template_record1: dict[str, Any] = templates_request.records[0]
        Assertions.assert_type(UUID, template_record1["id"])
        Assertions.assert_equals(
            "16-Team Single-Leg",
            template_record1["name"]
        )

        template_record2: dict[str, Any] = templates_request.records[1]
        Assertions.assert_type(UUID, template_record2["id"])
        Assertions.assert_equals(
            "8-Team Double-Leg Away Goals",
            template_record2["name"]
        )

        Assertions.assert_equals(2, len(created))

        created1 = created[0]
        Assertions.assert_type(KnockoutTemplate, created1)
        Assertions.assert_type(UUID, created1.id)
        Assertions.assert_equals("16-Team Single-Leg", created1.name)
        Assertions.assert_equals(5, len(created1.rounds))

        created_round1 = created1.rounds[0]
        Assertions.assert_type(RoundTemplate, created_round1)
        Assertions.assert_equals("Round of 16", created_round1.name)
        Assertions.assert_equals(16, created_round1.teamCount)
        Assertions.assert_equals(1, created_round1.roundOrder)
        Assertions.assert_false(created_round1.twoLegs)
        Assertions.assert_true(created_round1.extraTime)
        Assertions.assert_false(created_round1.awayGoals)

        created1_round2 = created1.rounds[1]
        Assertions.assert_type(RoundTemplate, created1_round2)
        Assertions.assert_equals("Quarter-Finals", created1_round2.name)
        Assertions.assert_equals(8, created1_round2.teamCount)
        Assertions.assert_equals(2, created1_round2.roundOrder)
        Assertions.assert_false(created1_round2.twoLegs)
        Assertions.assert_true(created1_round2.extraTime)
        Assertions.assert_false(created1_round2.awayGoals)

        created1_round3 = created1.rounds[2]
        Assertions.assert_type(RoundTemplate, created1_round3)
        Assertions.assert_equals("Semi-Finals", created1_round3.name)
        Assertions.assert_equals(4, created1_round3.teamCount)
        Assertions.assert_equals(3, created1_round3.roundOrder)
        Assertions.assert_false(created1_round3.twoLegs)
        Assertions.assert_true(created1_round3.extraTime)
        Assertions.assert_false(created1_round3.awayGoals)

        created1_round4 = created1.rounds[3]
        Assertions.assert_type(RoundTemplate, created1_round4)
        Assertions.assert_equals("Third-Place Play-Off", created1_round4.name)
        Assertions.assert_equals(2, created1_round4.teamCount)
        Assertions.assert_equals(4, created1_round4.roundOrder)
        Assertions.assert_false(created1_round4.twoLegs)
        Assertions.assert_true(created1_round4.extraTime)
        Assertions.assert_false(created1_round4.awayGoals)

        created1_round5 = created1.rounds[4]
        Assertions.assert_type(RoundTemplate, created1_round5)
        Assertions.assert_equals("Final", created1_round5.name)
        Assertions.assert_equals(2, created1_round5.teamCount)
        Assertions.assert_equals(5, created1_round5.roundOrder)
        Assertions.assert_false(created1_round5.twoLegs)
        Assertions.assert_true(created1_round5.extraTime)
        Assertions.assert_false(created1_round5.awayGoals)

        created2 = created[1]
        Assertions.assert_type(KnockoutTemplate, created2)
        Assertions.assert_type(UUID, created2.id)
        Assertions.assert_equals("8-Team Double-Leg Away Goals", created2.name)
        Assertions.assert_equals(3, len(created2.rounds))

        created2_round1 = created2.rounds[0]
        Assertions.assert_type(RoundTemplate, created2_round1)
        Assertions.assert_equals("Quarter-Finals", created2_round1.name)
        Assertions.assert_equals(8, created2_round1.teamCount)
        Assertions.assert_equals(1, created2_round1.roundOrder)
        Assertions.assert_true(created2_round1.twoLegs)
        Assertions.assert_true(created2_round1.extraTime)
        Assertions.assert_true(created2_round1.awayGoals)

        created2_round2 = created2.rounds[1]
        Assertions.assert_type(RoundTemplate, created2_round2)
        Assertions.assert_equals("Semi-Finals", created2_round2.name)
        Assertions.assert_equals(4, created2_round2.teamCount)
        Assertions.assert_equals(2, created2_round2.roundOrder)
        Assertions.assert_true(created2_round2.twoLegs)
        Assertions.assert_true(created2_round2.extraTime)
        Assertions.assert_true(created2_round2.awayGoals)

        created2_round3 = created2.rounds[2]
        Assertions.assert_type(RoundTemplate, created2_round3)
        Assertions.assert_equals("Final", created2_round3.name)
        Assertions.assert_equals(2, created2_round3.teamCount)
        Assertions.assert_equals(3, created2_round3.roundOrder)
        Assertions.assert_false(created2_round3.twoLegs)
        Assertions.assert_true(created2_round3.extraTime)
        Assertions.assert_false(created2_round3.awayGoals)

    def test_should_return_knockout_template_by_id(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "name": "16-Team Single-Leg",
                        "rounds": [
                            {
                                "name": "Round of 16",
                                "teamCount": 16,
                                "roundOrder": 1,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Quarter-Finals",
                                "teamCount": 8,
                                "roundOrder": 2,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Semi-Finals",
                                "teamCount": 4,
                                "roundOrder": 3,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Third-Place Play-Off",
                                "teamCount": 2,
                                "roundOrder": 4,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Final",
                                "teamCount": 2,
                                "roundOrder": 5,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            }
                        ]
                    }
                ]
            ),
            QueryResponse(
                referenceId="79de70fd-1556-4dec-b2ca-1cef5178007e",
                recordCount=5,
                records=[
                    {
                        "id": "57faec18-532a-4317-83c3-da57cf08d902",
                        "name": "Quarter-Finals",
                        "teamCount": 8,
                        "roundOrder": 2,
                        "twoLegs": False,
                        "extraTime": True,
                        "awayGoals": False,
                        "knockoutTemplateId": "c08fd796-7fea-40d9-9a0a-"
                                              "cb3a49cce2e4"
                    },
                    {
                        "id": "bfa4f1be-d00a-48c8-b14f-7d04ca6a54b4",
                        "name": "Third-Place Play-Off",
                        "teamCount": 2,
                        "roundOrder": 4,
                        "twoLegs": False,
                        "extraTime": True,
                        "awayGoals": False,
                        "knockoutTemplateId": "c08fd796-7fea-40d9-9a0a-"
                                              "cb3a49cce2e4"
                    },
                    {
                        "id": "0bf8c559-0d02-4072-afaa-a153a6178204",
                        "name": "Final",
                        "teamCount": 2,
                        "roundOrder": 5,
                        "twoLegs": False,
                        "extraTime": True,
                        "awayGoals": False,
                        "knockoutTemplateId": "c08fd796-7fea-40d9-9a0a-"
                                              "cb3a49cce2e4"
                    },
                    {
                        "id": "ac408de9-a65f-448d-8ad4-cc36f52d3392",
                        "name": "Semi-Finals",
                        "teamCount": 4,
                        "roundOrder": 3,
                        "twoLegs": False,
                        "extraTime": True,
                        "awayGoals": False,
                        "knockoutTemplateId": "c08fd796-7fea-40d9-9a0a-"
                                              "cb3a49cce2e4"
                    },
                    {
                        "id": "98732577-0ba1-4540-a758-9c33be004c13",
                        "name": "Round of 16",
                        "teamCount": 16,
                        "roundOrder": 1,
                        "twoLegs": False,
                        "extraTime": True,
                        "awayGoals": False,
                        "knockoutTemplateId": "c08fd796-7fea-40d9-9a0a-"
                                              "cb3a49cce2e4"
                    }
                ]
            )
        ]

        # When
        knockout_template: KnockoutTemplate = (
            self.__service.get_knockout_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )
        )

        # Then
        templates_args, templates_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[0]
        Assertions.assert_type(QueryRequest, templates_args[0])

        templates_request: QueryRequest = templates_args[0]
        table: Table = templates_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            table.schema_
        )
        Assertions.assert_equals("knockout-templates", table.table)

        condition: QueryCondition = (
            templates_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            condition.value
        )

        Assertions.assert_type(KnockoutTemplate, knockout_template)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            knockout_template.id
        )
        Assertions.assert_equals("16-Team Single-Leg", knockout_template.name)
        Assertions.assert_equals(5, len(knockout_template.rounds))

        round1 = knockout_template.rounds[0]
        Assertions.assert_type(RoundTemplate, round1)
        Assertions.assert_equals("Round of 16", round1.name)
        Assertions.assert_equals(16, round1.teamCount)
        Assertions.assert_equals(1, round1.roundOrder)
        Assertions.assert_false(round1.twoLegs)
        Assertions.assert_true(round1.extraTime)
        Assertions.assert_false(round1.awayGoals)

        round2 = knockout_template.rounds[1]
        Assertions.assert_type(RoundTemplate, round2)
        Assertions.assert_equals("Quarter-Finals", round2.name)
        Assertions.assert_equals(8, round2.teamCount)
        Assertions.assert_equals(2, round2.roundOrder)
        Assertions.assert_false(round2.twoLegs)
        Assertions.assert_true(round2.extraTime)
        Assertions.assert_false(round2.awayGoals)

        round3 = knockout_template.rounds[2]
        Assertions.assert_type(RoundTemplate, round3)
        Assertions.assert_equals("Semi-Finals", round3.name)
        Assertions.assert_equals(4, round3.teamCount)
        Assertions.assert_equals(3, round3.roundOrder)
        Assertions.assert_false(round3.twoLegs)
        Assertions.assert_true(round3.extraTime)
        Assertions.assert_false(round3.awayGoals)

        round4 = knockout_template.rounds[3]
        Assertions.assert_type(RoundTemplate, round4)
        Assertions.assert_equals("Third-Place Play-Off", round4.name)
        Assertions.assert_equals(2, round4.teamCount)
        Assertions.assert_equals(4, round4.roundOrder)
        Assertions.assert_false(round4.twoLegs)
        Assertions.assert_true(round4.extraTime)
        Assertions.assert_false(round4.awayGoals)

        round5 = knockout_template.rounds[4]
        Assertions.assert_type(RoundTemplate, round5)
        Assertions.assert_equals("Final", round5.name)
        Assertions.assert_equals(2, round5.teamCount)
        Assertions.assert_equals(5, round5.roundOrder)
        Assertions.assert_false(round5.twoLegs)
        Assertions.assert_true(round5.extraTime)
        Assertions.assert_false(round5.awayGoals)

    def test_should_raise_exception_if_knockout_template_not_found(self):
        # Given
        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=0,
            records=[]
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_knockout_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No knockout templates found with a matching id.",
            httpe.value.detail
        )

    def test_should_delete_knockout_template_by_id(self):
        # Given
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=0,
                records=[]
            )
        )

        # When
        self.__service.delete_knockout_template_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        )

        # Then
        template_args, template_kwargs = (
            self.__query_service.update_records.call_args_list
        )[0]
        Assertions.assert_type(UpdateRequest, template_args[0])

        template_request: UpdateRequest = template_args[0]
        Assertions.assert_equals(
            SqlOperator.DELETE,
            template_request.operation
        )

        table: Table = template_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            table.schema_
        )
        Assertions.assert_equals("knockout-templates", table.table)

        condition: QueryCondition = (
            template_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            condition.value
        )

    def test_no_knockout_template_delete_if_used_by_tournament_template(self):
        # Given
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "name": "16-Team Single-Leg"
                    }
                ]
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.delete_knockout_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(409, httpe.value.status_code)
        Assertions.assert_equals(
            "Cannot delete knockout template as it is part of an existing "
            "tournament template.",
            httpe.value.detail
        )
