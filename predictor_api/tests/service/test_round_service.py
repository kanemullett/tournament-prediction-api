from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.order_by import OrderBy
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.order_direction import OrderDirection
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from db_handler.db_handler.model.update_request import UpdateRequest
from predictor_api.predictor_api.model.round import Round
from predictor_api.predictor_api.model.round_update import RoundUpdate
from predictor_api.predictor_api.service.round_service import RoundService
from predictor_common.test_resources.assertions import Assertions


class TestRoundService:

    __query_service: MagicMock = MagicMock()
    __tournament_service: MagicMock = MagicMock()

    __service: RoundService = RoundService(
        __query_service,
        __tournament_service
    )

    def setup_method(self):
        self.__query_service.retrieve_records.reset_mock()
        self.__query_service.retrieve_records.return_value = None
        self.__query_service.retrieve_records.side_effect = None

        self.__query_service.update_records.reset_mock()
        self.__query_service.update_records.return_value = None
        self.__query_service.update_records.side_effect = None

        self.__tournament_service.get_tournament_by_id.reset_mock()
        self.__tournament_service.get_tournament_by_id.return_value = None
        self.__tournament_service.get_tournament_by_id.side_effect = None

    def test_should_return_rounds(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "knockoutTemplateId": "72119bfa-212b-443c-b992-"
                                              "7dc6983c6a1a"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=2,
                records=[
                    {
                        "id": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "name": "Round 1",
                        "teamCount": 32,
                        "roundOrder": 1,
                        "twoLegs": True,
                        "extraTime": True,
                        "awayGoals": True
                    },
                    {
                        "id": "e0ee5d0e-9d57-4c74-b938-0aa306a2313e",
                        "name": "Round 2",
                        "teamCount": 16,
                        "roundOrder": 2,
                        "twoLegs": True,
                        "extraTime": True,
                        "awayGoals": True
                    }
                ]
            )
        ]

        # When
        rounds: list[Round] = self.__service.get_rounds(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87")
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        template_args, template_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[0]
        Assertions.assert_type(QueryRequest, template_args[0])

        template_request: QueryRequest = template_args[0]
        Assertions.assert_equals(1, len(template_request.columns))

        template_column: Column = template_request.columns[0]
        Assertions.assert_equals(
            ["temp", "knockoutTemplateId"],
            template_column.parts
        )

        template_table: Table = template_request.table
        Assertions.assert_equals("predictor", template_table.schema_)
        Assertions.assert_equals("tournaments", template_table.table)
        Assertions.assert_equals("tourn", template_table.alias)

        Assertions.assert_equals(1, len(template_request.tableJoins))

        template_join: TableJoin = template_request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.INNER, template_join.joinType)

        template_join_table: Table = template_join.table
        Assertions.assert_equals("predictor", template_join_table.schema_)
        Assertions.assert_equals(
            "tournament-templates",
            template_join_table.table
        )
        Assertions.assert_equals("temp", template_join_table.alias)

        template_join_condition: QueryCondition = template_join.joinCondition
        Assertions.assert_equals(
            ["tourn", "templateId"],
            template_join_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_join_condition.operator
        )
        Assertions.assert_equals(
            ["temp", "id"],
            template_join_condition.value.parts
        )

        Assertions.assert_equals(
            1,
            len(template_request.conditionGroup.conditions)
        )

        template_condition: QueryCondition = (
            template_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(
            ["tourn", "id"],
            template_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_condition.operator
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            template_condition.value
        )

        round_args, round_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[1]
        Assertions.assert_type(QueryRequest, round_args[0])

        group_request: QueryRequest = round_args[0]

        group_table: Table = group_request.table
        Assertions.assert_equals("predictor", group_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            group_table.table
        )

        group_order_by: OrderBy = group_request.orderBy
        Assertions.assert_equals(
            ["roundOrder"],
            group_order_by.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, group_order_by.direction)

        Assertions.assert_equals(2, len(rounds))

        round1: Round = rounds[0]
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            round1.id
        )
        Assertions.assert_equals("Round 1", round1.name)
        Assertions.assert_equals(32, round1.teamCount)
        Assertions.assert_equals(1, round1.roundOrder)
        Assertions.assert_true(round1.twoLegs)
        Assertions.assert_true(round1.extraTime)
        Assertions.assert_true(round1.awayGoals)

        round2: Round = rounds[1]
        Assertions.assert_equals(
            UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
            round2.id
        )
        Assertions.assert_equals("Round 2", round2.name)
        Assertions.assert_equals(16, round2.teamCount)
        Assertions.assert_equals(2, round2.roundOrder)
        Assertions.assert_true(round2.twoLegs)
        Assertions.assert_true(round2.extraTime)
        Assertions.assert_true(round1.awayGoals)

    def test_should_error_tournament_not_exists_get_rounds(self):
        # Given
        self.__tournament_service.get_tournament_by_id.side_effect = (
            HTTPException(
                status_code=404,
                detail="No tournaments found with a matching id."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_rounds(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )

    def test_should_error_tournament_no_knockout_stage_get_rounds(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "knockoutTemplateId": None
                    }
                ]
            )
        ]

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_rounds(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "The tournament with the supplied id does not have a knockout "
            "stage.",
            httpe.value.detail
        )

    def test_should_update_rounds(self):
        # Given
        round_updates: list[RoundUpdate] = [
            RoundUpdate(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Round 1"
            ),
            RoundUpdate(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Round 2"
            )
        ]

        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "knockoutTemplateId": "72119bfa-212b-443c-b992-"
                                              "7dc6983c6a1a"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=2,
                records=[
                    {
                        "id": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "name": "Round 1",
                        "teamCount": 32,
                        "roundOrder": 1,
                        "twoLegs": True,
                        "extraTime": True,
                        "awayGoals": True
                    },
                    {
                        "id": "e0ee5d0e-9d57-4c74-b938-0aa306a2313e",
                        "name": "Round 2",
                        "teamCount": 16,
                        "roundOrder": 2,
                        "twoLegs": True,
                        "extraTime": True,
                        "awayGoals": True
                    }
                ]
            )
        ]

        # When
        updated: list[Round] = self.__service.update_rounds(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            round_updates
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        template_args, template_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[0]
        Assertions.assert_type(QueryRequest, template_args[0])

        template_request: QueryRequest = template_args[0]
        Assertions.assert_equals(1, len(template_request.columns))

        template_column: Column = template_request.columns[0]
        Assertions.assert_equals(
            ["temp", "knockoutTemplateId"],
            template_column.parts
        )

        template_table: Table = template_request.table
        Assertions.assert_equals("predictor", template_table.schema_)
        Assertions.assert_equals("tournaments", template_table.table)
        Assertions.assert_equals("tourn", template_table.alias)

        Assertions.assert_equals(1, len(template_request.tableJoins))

        template_join: TableJoin = template_request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.INNER, template_join.joinType)

        template_join_table: Table = template_join.table
        Assertions.assert_equals("predictor", template_join_table.schema_)
        Assertions.assert_equals(
            "tournament-templates",
            template_join_table.table
        )
        Assertions.assert_equals("temp", template_join_table.alias)

        template_join_condition: QueryCondition = template_join.joinCondition
        Assertions.assert_equals(
            ["tourn", "templateId"],
            template_join_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_join_condition.operator
        )
        Assertions.assert_equals(
            ["temp", "id"],
            template_join_condition.value.parts
        )

        Assertions.assert_equals(
            1,
            len(template_request.conditionGroup.conditions)
        )

        template_condition: QueryCondition = (
            template_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(
            ["tourn", "id"],
            template_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_condition.operator
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            template_condition.value
        )

        update_args, update_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, update_args[0])

        update_request: UpdateRequest = update_args[0]
        Assertions.assert_equals(SqlOperator.UPDATE, update_request.operation)

        update_table: Table = update_request.table
        Assertions.assert_equals("predictor", update_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            update_table.table
        )

        Assertions.assert_equals(2, len(update_request.records))

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            record1["id"]
        )
        Assertions.assert_equals("Round 1", record1["name"])

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_equals(
            UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
            record2["id"]
        )
        Assertions.assert_equals("Round 2", record2["name"])

        round_args, round_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[1]
        Assertions.assert_type(QueryRequest, round_args[0])

        round_request: QueryRequest = round_args[0]

        round_table: Table = round_request.table
        Assertions.assert_equals("predictor", round_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            round_table.table
        )

        Assertions.assert_equals(
            1,
            len(round_request.conditionGroup.conditions)
        )

        round_condition: QueryCondition = (
            round_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["id"], round_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.IN,
            round_condition.operator
        )
        Assertions.assert_equals(
            [
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e")
            ],
            round_condition.value
        )

        round_order_by: OrderBy = round_request.orderBy
        Assertions.assert_equals(
            ["roundOrder"],
            round_order_by.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, round_order_by.direction)

        Assertions.assert_equals(2, len(updated))

        round1: Round = updated[0]
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            round1.id
        )
        Assertions.assert_equals("Round 1", round1.name)
        Assertions.assert_equals(32, round1.teamCount)
        Assertions.assert_equals(1, round1.roundOrder)
        Assertions.assert_true(round1.twoLegs)
        Assertions.assert_true(round1.extraTime)
        Assertions.assert_true(round1.awayGoals)

        round2: Round = updated[1]
        Assertions.assert_equals(
            UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
            round2.id
        )
        Assertions.assert_equals("Round 2", round2.name)
        Assertions.assert_equals(16, round2.teamCount)
        Assertions.assert_equals(2, round2.roundOrder)
        Assertions.assert_true(round2.twoLegs)
        Assertions.assert_true(round2.extraTime)
        Assertions.assert_true(round2.awayGoals)

    def test_should_error_tournament_not_exists_update_rounds(self):
        # Given
        round_updates: list[RoundUpdate] = [
            RoundUpdate(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A"
            ),
            RoundUpdate(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B"
            )
        ]

        self.__tournament_service.get_tournament_by_id.side_effect = (
            HTTPException(
                status_code=404,
                detail="No tournaments found with a matching id."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.update_rounds(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                round_updates
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )

    def test_should_error_tournament_no_knockout_stage_update_rounds(self):
        # Given
        round_updates: list[RoundUpdate] = [
            RoundUpdate(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A"
            ),
            RoundUpdate(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B"
            )
        ]

        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "knockoutTemplateId": None
                    }
                ]
            )
        ]

        # When
        with raises(HTTPException) as httpe:
            self.__service.update_rounds(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                round_updates
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "The tournament with the supplied id does not have a knockout "
            "stage.",
            httpe.value.detail
        )
