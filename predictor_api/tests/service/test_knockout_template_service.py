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
from predictor_api.predictor_api.model.knockout_round import KnockoutRound
from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.service.knockout_template_service import KnockoutTemplateService
from predictor_api.predictor_api.util.predictor_constants import PredictorConstants
from predictor_common.test_resources.assertions import Assertions


class TestKnockoutTemplateService:

    __database_query_service: MagicMock = MagicMock()

    __knockout_template_service: KnockoutTemplateService = KnockoutTemplateService(__database_query_service)

    def test_should_return_knockout_templates(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
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

        # When
        knockout_templates: list[KnockoutTemplate] = self.__knockout_template_service.get_knockout_templates()

        # Then
        captured_args_retrieve_records, captured_kwargs = self.__database_query_service.retrieve_records.call_args
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]
        table: Table = query_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("knockout-templates", table.table)

        Assertions.assert_equals(2, len(knockout_templates))

        template1 = knockout_templates[0]
        Assertions.assert_type(KnockoutTemplate, template1)
        Assertions.assert_type(UUID, template1.id)
        Assertions.assert_equals("16-Team Single-Leg", template1.name)
        Assertions.assert_equals(5, len(template1.rounds))

        template1_round1 = template1.rounds[0]
        Assertions.assert_type(KnockoutRound, template1_round1)
        Assertions.assert_equals("Round of 16", template1_round1.name)
        Assertions.assert_equals(16, template1_round1.teamCount)
        Assertions.assert_equals(1, template1_round1.roundOrder)
        Assertions.assert_false(template1_round1.twoLegs)
        Assertions.assert_true(template1_round1.extraTime)
        Assertions.assert_false(template1_round1.awayGoals)

        template1_round2 = template1.rounds[1]
        Assertions.assert_type(KnockoutRound, template1_round2)
        Assertions.assert_equals("Quarter-Finals", template1_round2.name)
        Assertions.assert_equals(8, template1_round2.teamCount)
        Assertions.assert_equals(2, template1_round2.roundOrder)
        Assertions.assert_false(template1_round2.twoLegs)
        Assertions.assert_true(template1_round2.extraTime)
        Assertions.assert_false(template1_round2.awayGoals)

        template1_round3 = template1.rounds[2]
        Assertions.assert_type(KnockoutRound, template1_round3)
        Assertions.assert_equals("Semi-Finals", template1_round3.name)
        Assertions.assert_equals(4, template1_round3.teamCount)
        Assertions.assert_equals(3, template1_round3.roundOrder)
        Assertions.assert_false(template1_round3.twoLegs)
        Assertions.assert_true(template1_round3.extraTime)
        Assertions.assert_false(template1_round3.awayGoals)

        template1_round4 = template1.rounds[3]
        Assertions.assert_type(KnockoutRound, template1_round4)
        Assertions.assert_equals("Third-Place Play-Off", template1_round4.name)
        Assertions.assert_equals(2, template1_round4.teamCount)
        Assertions.assert_equals(4, template1_round4.roundOrder)
        Assertions.assert_false(template1_round4.twoLegs)
        Assertions.assert_true(template1_round4.extraTime)
        Assertions.assert_false(template1_round4.awayGoals)

        template1_round5 = template1.rounds[4]
        Assertions.assert_type(KnockoutRound, template1_round5)
        Assertions.assert_equals("Final", template1_round5.name)
        Assertions.assert_equals(2, template1_round5.teamCount)
        Assertions.assert_equals(5, template1_round5.roundOrder)
        Assertions.assert_false(template1_round5.twoLegs)
        Assertions.assert_true(template1_round5.extraTime)
        Assertions.assert_false(template1_round5.awayGoals)

        template2 = knockout_templates[1]
        Assertions.assert_type(KnockoutTemplate, template2)
        Assertions.assert_type(UUID, template2.id)
        Assertions.assert_equals("8-Team Double-Leg Away Goals", template2.name)
        Assertions.assert_equals(3, len(template2.rounds))

        template2_round1 = template2.rounds[0]
        Assertions.assert_type(KnockoutRound, template2_round1)
        Assertions.assert_equals("Quarter-Finals", template2_round1.name)
        Assertions.assert_equals(8, template2_round1.teamCount)
        Assertions.assert_equals(1, template2_round1.roundOrder)
        Assertions.assert_true(template2_round1.twoLegs)
        Assertions.assert_true(template2_round1.extraTime)
        Assertions.assert_true(template2_round1.awayGoals)

        template2_round2 = template2.rounds[1]
        Assertions.assert_type(KnockoutRound, template2_round2)
        Assertions.assert_equals("Semi-Finals", template2_round2.name)
        Assertions.assert_equals(4, template2_round2.teamCount)
        Assertions.assert_equals(2, template2_round2.roundOrder)
        Assertions.assert_true(template2_round2.twoLegs)
        Assertions.assert_true(template2_round2.extraTime)
        Assertions.assert_true(template2_round2.awayGoals)

        template2_round3 = template2.rounds[2]
        Assertions.assert_type(KnockoutRound, template2_round3)
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
                    KnockoutRound(
                        name="Round of 16",
                        teamCount=16,
                        roundOrder=1,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    ),
                    KnockoutRound(
                        name="Quarter-Finals",
                        teamCount=8,
                        roundOrder=2,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    ),
                    KnockoutRound(
                        name="Semi-Finals",
                        teamCount=4,
                        roundOrder=3,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    ),
                    KnockoutRound(
                        name="Third-Place Play-Off",
                        teamCount=2,
                        roundOrder=4,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    ),
                    KnockoutRound(
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
                    KnockoutRound(
                        name="Quarter-Finals",
                        teamCount=8,
                        roundOrder=1,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    KnockoutRound(
                        name="Semi-Finals",
                        teamCount=4,
                        roundOrder=2,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    KnockoutRound(
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
        created: list[KnockoutTemplate] = self.__knockout_template_service.create_knockout_templates(created)

        # Then
        captured_args_retrieve_records, captured_kwargs = self.__database_query_service.update_records.call_args
        Assertions.assert_type(UpdateRequest, captured_args_retrieve_records[0])

        update_request: UpdateRequest = captured_args_retrieve_records[0]
        Assertions.assert_equals(SqlOperator.INSERT, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("knockout-templates", table.table)

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_type(UUID, record1["id"])
        Assertions.assert_equals("16-Team Single-Leg", record1["name"])

        Assertions.assert_equals(5, len(record1["rounds"]))

        record1_round1: dict[str, Any] = record1["rounds"][0]
        Assertions.assert_equals("Round of 16", record1_round1["name"])
        Assertions.assert_equals(16, record1_round1["teamCount"])
        Assertions.assert_equals(1, record1_round1["roundOrder"])
        Assertions.assert_false(record1_round1["twoLegs"])
        Assertions.assert_true(record1_round1["extraTime"])
        Assertions.assert_false(record1_round1["awayGoals"])

        record1_round2: dict[str, Any] = record1["rounds"][1]
        Assertions.assert_equals("Quarter-Finals", record1_round2["name"])
        Assertions.assert_equals(8, record1_round2["teamCount"])
        Assertions.assert_equals(2, record1_round2["roundOrder"])
        Assertions.assert_false(record1_round2["twoLegs"])
        Assertions.assert_true(record1_round2["extraTime"])
        Assertions.assert_false(record1_round2["awayGoals"])

        record1_round3: dict[str, Any] = record1["rounds"][2]
        Assertions.assert_equals("Semi-Finals", record1_round3["name"])
        Assertions.assert_equals(4, record1_round3["teamCount"])
        Assertions.assert_equals(3, record1_round3["roundOrder"])
        Assertions.assert_false(record1_round3["twoLegs"])
        Assertions.assert_true(record1_round3["extraTime"])
        Assertions.assert_false(record1_round3["awayGoals"])

        record1_round4: dict[str, Any] = record1["rounds"][3]
        Assertions.assert_equals("Third-Place Play-Off", record1_round4["name"])
        Assertions.assert_equals(2, record1_round4["teamCount"])
        Assertions.assert_equals(4, record1_round4["roundOrder"])
        Assertions.assert_false(record1_round4["twoLegs"])
        Assertions.assert_true(record1_round4["extraTime"])
        Assertions.assert_false(record1_round4["awayGoals"])

        record1_round5: dict[str, Any] = record1["rounds"][4]
        Assertions.assert_equals("Final", record1_round5["name"])
        Assertions.assert_equals(2, record1_round5["teamCount"])
        Assertions.assert_equals(5, record1_round5["roundOrder"])
        Assertions.assert_false(record1_round5["twoLegs"])
        Assertions.assert_true(record1_round5["extraTime"])
        Assertions.assert_false(record1_round5["awayGoals"])

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_type(UUID, record2["id"])
        Assertions.assert_equals("8-Team Double-Leg Away Goals", record2["name"])

        Assertions.assert_equals(3, len(record2["rounds"]))

        record2_round1: dict[str, Any] = record2["rounds"][0]
        Assertions.assert_equals("Quarter-Finals", record2_round1["name"])
        Assertions.assert_equals(8, record2_round1["teamCount"])
        Assertions.assert_equals(1, record2_round1["roundOrder"])
        Assertions.assert_true(record2_round1["twoLegs"])
        Assertions.assert_true(record2_round1["extraTime"])
        Assertions.assert_true(record2_round1["awayGoals"])

        record2_round2: dict[str, Any] = record2["rounds"][1]
        Assertions.assert_equals("Semi-Finals", record2_round2["name"])
        Assertions.assert_equals(4, record2_round2["teamCount"])
        Assertions.assert_equals(2, record2_round2["roundOrder"])
        Assertions.assert_true(record2_round2["twoLegs"])
        Assertions.assert_true(record2_round2["extraTime"])
        Assertions.assert_true(record2_round2["awayGoals"])

        record2_round3: dict[str, Any] = record2["rounds"][2]
        Assertions.assert_equals("Final", record2_round3["name"])
        Assertions.assert_equals(2, record2_round3["teamCount"])
        Assertions.assert_equals(3, record2_round3["roundOrder"])
        Assertions.assert_false(record2_round3["twoLegs"])
        Assertions.assert_true(record2_round3["extraTime"])
        Assertions.assert_false(record2_round3["awayGoals"])

        Assertions.assert_equals(2, len(created))

        created1 = created[0]
        Assertions.assert_type(KnockoutTemplate, created1)
        Assertions.assert_type(UUID, created1.id)
        Assertions.assert_equals("16-Team Single-Leg", created1.name)
        Assertions.assert_equals(5, len(created1.rounds))

        created_round1 = created1.rounds[0]
        Assertions.assert_type(KnockoutRound, created_round1)
        Assertions.assert_equals("Round of 16", created_round1.name)
        Assertions.assert_equals(16, created_round1.teamCount)
        Assertions.assert_equals(1, created_round1.roundOrder)
        Assertions.assert_false(created_round1.twoLegs)
        Assertions.assert_true(created_round1.extraTime)
        Assertions.assert_false(created_round1.awayGoals)

        created1_round2 = created1.rounds[1]
        Assertions.assert_type(KnockoutRound, created1_round2)
        Assertions.assert_equals("Quarter-Finals", created1_round2.name)
        Assertions.assert_equals(8, created1_round2.teamCount)
        Assertions.assert_equals(2, created1_round2.roundOrder)
        Assertions.assert_false(created1_round2.twoLegs)
        Assertions.assert_true(created1_round2.extraTime)
        Assertions.assert_false(created1_round2.awayGoals)

        created1_round3 = created1.rounds[2]
        Assertions.assert_type(KnockoutRound, created1_round3)
        Assertions.assert_equals("Semi-Finals", created1_round3.name)
        Assertions.assert_equals(4, created1_round3.teamCount)
        Assertions.assert_equals(3, created1_round3.roundOrder)
        Assertions.assert_false(created1_round3.twoLegs)
        Assertions.assert_true(created1_round3.extraTime)
        Assertions.assert_false(created1_round3.awayGoals)

        created1_round4 = created1.rounds[3]
        Assertions.assert_type(KnockoutRound, created1_round4)
        Assertions.assert_equals("Third-Place Play-Off", created1_round4.name)
        Assertions.assert_equals(2, created1_round4.teamCount)
        Assertions.assert_equals(4, created1_round4.roundOrder)
        Assertions.assert_false(created1_round4.twoLegs)
        Assertions.assert_true(created1_round4.extraTime)
        Assertions.assert_false(created1_round4.awayGoals)

        created1_round5 = created1.rounds[4]
        Assertions.assert_type(KnockoutRound, created1_round5)
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
        Assertions.assert_type(KnockoutRound, created2_round1)
        Assertions.assert_equals("Quarter-Finals", created2_round1.name)
        Assertions.assert_equals(8, created2_round1.teamCount)
        Assertions.assert_equals(1, created2_round1.roundOrder)
        Assertions.assert_true(created2_round1.twoLegs)
        Assertions.assert_true(created2_round1.extraTime)
        Assertions.assert_true(created2_round1.awayGoals)

        created2_round2 = created2.rounds[1]
        Assertions.assert_type(KnockoutRound, created2_round2)
        Assertions.assert_equals("Semi-Finals", created2_round2.name)
        Assertions.assert_equals(4, created2_round2.teamCount)
        Assertions.assert_equals(2, created2_round2.roundOrder)
        Assertions.assert_true(created2_round2.twoLegs)
        Assertions.assert_true(created2_round2.extraTime)
        Assertions.assert_true(created2_round2.awayGoals)

        created2_round3 = created2.rounds[2]
        Assertions.assert_type(KnockoutRound, created2_round3)
        Assertions.assert_equals("Final", created2_round3.name)
        Assertions.assert_equals(2, created2_round3.teamCount)
        Assertions.assert_equals(3, created2_round3.roundOrder)
        Assertions.assert_false(created2_round3.twoLegs)
        Assertions.assert_true(created2_round3.extraTime)
        Assertions.assert_false(created2_round3.awayGoals)

    def test_should_return_knockout_template_by_id(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
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
        )

        # When
        knockout_template: KnockoutTemplate = self.__knockout_template_service.get_knockout_template_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        )

        # Then
        captured_args_retrieve_records, captured_kwargs = self.__database_query_service.retrieve_records.call_args
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]
        table: Table = query_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("knockout-templates", table.table)

        condition: QueryCondition = query_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"), condition.value)

        Assertions.assert_type(KnockoutTemplate, knockout_template)
        Assertions.assert_equals(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"), knockout_template.id)
        Assertions.assert_equals("16-Team Single-Leg", knockout_template.name)
        Assertions.assert_equals(5, len(knockout_template.rounds))

        round1 = knockout_template.rounds[0]
        Assertions.assert_type(KnockoutRound, round1)
        Assertions.assert_equals("Round of 16", round1.name)
        Assertions.assert_equals(16, round1.teamCount)
        Assertions.assert_equals(1, round1.roundOrder)
        Assertions.assert_false(round1.twoLegs)
        Assertions.assert_true(round1.extraTime)
        Assertions.assert_false(round1.awayGoals)

        round2 = knockout_template.rounds[1]
        Assertions.assert_type(KnockoutRound, round2)
        Assertions.assert_equals("Quarter-Finals", round2.name)
        Assertions.assert_equals(8, round2.teamCount)
        Assertions.assert_equals(2, round2.roundOrder)
        Assertions.assert_false(round2.twoLegs)
        Assertions.assert_true(round2.extraTime)
        Assertions.assert_false(round2.awayGoals)

        round3 = knockout_template.rounds[2]
        Assertions.assert_type(KnockoutRound, round3)
        Assertions.assert_equals("Semi-Finals", round3.name)
        Assertions.assert_equals(4, round3.teamCount)
        Assertions.assert_equals(3, round3.roundOrder)
        Assertions.assert_false(round3.twoLegs)
        Assertions.assert_true(round3.extraTime)
        Assertions.assert_false(round3.awayGoals)

        round4 = knockout_template.rounds[3]
        Assertions.assert_type(KnockoutRound, round4)
        Assertions.assert_equals("Third-Place Play-Off", round4.name)
        Assertions.assert_equals(2, round4.teamCount)
        Assertions.assert_equals(4, round4.roundOrder)
        Assertions.assert_false(round4.twoLegs)
        Assertions.assert_true(round4.extraTime)
        Assertions.assert_false(round4.awayGoals)

        round5 = knockout_template.rounds[4]
        Assertions.assert_type(KnockoutRound, round5)
        Assertions.assert_equals("Final", round5.name)
        Assertions.assert_equals(2, round5.teamCount)
        Assertions.assert_equals(5, round5.roundOrder)
        Assertions.assert_false(round5.twoLegs)
        Assertions.assert_true(round5.extraTime)
        Assertions.assert_false(round5.awayGoals)

    def test_should_raise_exception_if_knockout_template_not_found(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=0,
            records=[]
        )

        # When
        with raises(HTTPException) as httpe:
            self.__knockout_template_service.get_knockout_template_by_id(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"))

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("No knockout templates found with a matching id.", httpe.value.detail)

    def test_should_delete_knockout_template_by_id(self):
        # When
        self.__knockout_template_service.delete_knockout_template_by_id(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"))

        # Then
        captured_args_update_records, captured_kwargs = self.__database_query_service.update_records.call_args
        Assertions.assert_type(UpdateRequest, captured_args_update_records[0])

        update_request: UpdateRequest = captured_args_update_records[0]
        Assertions.assert_equals(SqlOperator.DELETE, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("knockout-templates", table.table)

        condition: QueryCondition = update_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"), condition.value)

    def test_should_not_delete_knockout_template_if_used_by_tournament_template(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
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
        )

        # When
        with raises(HTTPException) as httpe:
            self.__knockout_template_service.delete_knockout_template_by_id(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"))

        # Then
        Assertions.assert_equals(409, httpe.value.status_code)
        Assertions.assert_equals(
            "Cannot delete knockout template as it is part of an existing tournament template.",
            httpe.value.detail
        )

