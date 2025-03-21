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
from predictor_api.predictor_api.model.result import Result
from predictor_api.predictor_api.model.type.winner import Winner
from predictor_api.predictor_api.service.result_service import ResultService
from predictor_common.test_resources.assertions import Assertions


class TestResultService:

    __query_service: MagicMock = MagicMock()
    __tournament_service: MagicMock = MagicMock()

    __service: ResultService = ResultService(
        __query_service,
        __tournament_service
    )

    def setup_method(self):
        self.__tournament_service.get_tournament_by_id.reset_mock()
        self.__tournament_service.get_tournament_by_id.return_value = None
        self.__tournament_service.get_tournament_by_id.side_effect = None

    def test_should_create_results(self):
        # Given
        results: list[Result] = [
            Result(
                id=UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
                homeGoals=2,
                awayGoals=1,
                afterExtraTime=True,
                afterPenalties=False
            ),
            Result(
                id=UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
                homeGoals=3,
                awayGoals=3,
                afterExtraTime=True,
                afterPenalties=True,
                penaltiesWinner=Winner.AWAY
            )
        ]

        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
            recordCount=2,
            records=[
                {
                    "id": "1db1fe5c-97d4-42e9-974f-633edb1dc0c4"
                },
                {
                    "id": "a1212f49-534f-4d36-90f4-f3ec9f0d9735"
                }
            ]
        )

        # When
        created: list[Result] = self.__service.create_results(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            results
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        query_args, query_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, query_args[0])

        query_request: QueryRequest = query_args[0]

        query_table: Table = query_request.table
        Assertions.assert_equals("predictor", query_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            query_table.table
        )

        Assertions.assert_equals(
            1,
            len(query_request.conditionGroup.conditions)
        )

        query_condition: QueryCondition = (
            query_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["id"], query_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.IN,
            query_condition.operator
        )
        Assertions.assert_equals(
            [
                UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
                UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735")
            ],
            query_condition.value
        )

        update_args, update_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, update_args[0])

        update_request: UpdateRequest = update_args[0]
        Assertions.assert_equals(SqlOperator.INSERT, update_request.operation)

        update_table: Table = update_request.table
        Assertions.assert_equals("predictor", update_table.schema_)
        Assertions.assert_equals(
            "results_5341cff8-df9f-4068-8a42-4b4288ecba87",
            update_table.table
        )

        Assertions.assert_equals(2, len(update_request.records))

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_equals(
            UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
            record1["id"]
        )
        Assertions.assert_equals(2, record1["homeGoals"])
        Assertions.assert_equals(1, record1["awayGoals"])
        Assertions.assert_true(record1["afterExtraTime"])
        Assertions.assert_false(record1["afterPenalties"])
        Assertions.assert_true("penaltiesWinner" not in record1.keys())

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_equals(
            UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
            record2["id"]
        )
        Assertions.assert_equals(3, record2["homeGoals"])
        Assertions.assert_equals(3, record2["awayGoals"])
        Assertions.assert_true(record2["afterExtraTime"])
        Assertions.assert_true(record2["afterPenalties"])
        Assertions.assert_equals(Winner.AWAY, record2["penaltiesWinner"])

        Assertions.assert_equals(2, len(created))

        result1: Result = results[0]
        Assertions.assert_equals(
            UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
            result1.id
        )
        Assertions.assert_equals(2, result1.homeGoals)
        Assertions.assert_equals(1, result1.awayGoals)
        Assertions.assert_true(result1.afterExtraTime)
        Assertions.assert_false(result1.afterPenalties)
        Assertions.assert_none(result1.penaltiesWinner)

        result2: Result = results[1]
        Assertions.assert_equals(
            UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
            result2.id
        )
        Assertions.assert_equals(3, result2.homeGoals)
        Assertions.assert_equals(3, result2.awayGoals)
        Assertions.assert_true(result2.afterExtraTime)
        Assertions.assert_true(result2.afterPenalties)
        Assertions.assert_equals(Winner.AWAY, result2.penaltiesWinner)

    def test_should_error_tournament_not_exists_create_results(self):
        # Given
        results: list[Result] = [
            Result(
                id=UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
                homeGoals=2,
                awayGoals=1,
                afterExtraTime=True,
                afterPenalties=False
            ),
            Result(
                id=UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
                homeGoals=3,
                awayGoals=3,
                afterExtraTime=True,
                afterPenalties=True,
                penaltiesWinner=Winner.AWAY
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
            self.__service.create_results(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                results
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )

    def test_should_error_match_not_exists_create_results(self):
        # Given
        results: list[Result] = [
            Result(
                id=UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
                homeGoals=2,
                awayGoals=1,
                afterExtraTime=True,
                afterPenalties=False
            ),
            Result(
                id=UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
                homeGoals=3,
                awayGoals=3,
                afterExtraTime=True,
                afterPenalties=True,
                penaltiesWinner=Winner.AWAY
            )
        ]

        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
            recordCount=1,
            records=[
                {
                    "id": "1db1fe5c-97d4-42e9-974f-633edb1dc0c4"
                }
            ]
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.create_results(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                results
            )

        # Then
        Assertions.assert_equals(400, httpe.value.status_code)
        Assertions.assert_equals(
            "One or more results does not have a corresponding match record.",
            httpe.value.detail
        )

    def test_should_update_results(self):
        # Given
        results: list[Result] = [
            Result(
                id=UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
                homeGoals=2,
                awayGoals=1,
                afterExtraTime=True,
                afterPenalties=False
            ),
            Result(
                id=UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
                homeGoals=3,
                awayGoals=3,
                afterExtraTime=True,
                afterPenalties=True,
                penaltiesWinner=Winner.AWAY
            )
        ]

        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
            recordCount=2,
            records=[
                {
                    "id": "1db1fe5c-97d4-42e9-974f-633edb1dc0c4",
                    "homeGoals": 2,
                    "awayGoals": 1,
                    "afterExtraTime": True,
                    "afterPenalties": False,
                    "penaltiesWinner": None
                },
                {
                    "id": "a1212f49-534f-4d36-90f4-f3ec9f0d9735",
                    "homeGoals": 3,
                    "awayGoals": 3,
                    "afterExtraTime": True,
                    "afterPenalties": True,
                    "penaltiesWinner": "AWAY"
                }
            ]
        )

        # When
        created: list[Result] = self.__service.update_results(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            results
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        update_args, update_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, update_args[0])

        update_request: UpdateRequest = update_args[0]
        Assertions.assert_equals(SqlOperator.INSERT, update_request.operation)

        update_table: Table = update_request.table
        Assertions.assert_equals("predictor", update_table.schema_)
        Assertions.assert_equals(
            "results_5341cff8-df9f-4068-8a42-4b4288ecba87",
            update_table.table
        )

        Assertions.assert_equals(2, len(update_request.records))

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_equals(
            UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
            record1["id"]
        )
        Assertions.assert_equals(2, record1["homeGoals"])
        Assertions.assert_equals(1, record1["awayGoals"])
        Assertions.assert_true(record1["afterExtraTime"])
        Assertions.assert_false(record1["afterPenalties"])
        Assertions.assert_true("penaltiesWinner" not in record1.keys())

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_equals(
            UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
            record2["id"]
        )
        Assertions.assert_equals(3, record2["homeGoals"])
        Assertions.assert_equals(3, record2["awayGoals"])
        Assertions.assert_true(record2["afterExtraTime"])
        Assertions.assert_true(record2["afterPenalties"])
        Assertions.assert_equals(Winner.AWAY, record2["penaltiesWinner"])

        query_args, query_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, query_args[0])

        query_request: QueryRequest = query_args[0]

        query_table: Table = query_request.table
        Assertions.assert_equals("predictor", query_table.schema_)
        Assertions.assert_equals(
            "results_5341cff8-df9f-4068-8a42-4b4288ecba87",
            query_table.table
        )

        Assertions.assert_equals(
            1,
            len(query_request.conditionGroup.conditions)
        )

        query_condition: QueryCondition = (
            query_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["id"], query_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.IN,
            query_condition.operator
        )
        Assertions.assert_equals(
            [
                UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
                UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735")
            ],
            query_condition.value
        )

        Assertions.assert_equals(2, len(created))

        result1: Result = results[0]
        Assertions.assert_equals(
            UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
            result1.id
        )
        Assertions.assert_equals(2, result1.homeGoals)
        Assertions.assert_equals(1, result1.awayGoals)
        Assertions.assert_true(result1.afterExtraTime)
        Assertions.assert_false(result1.afterPenalties)
        Assertions.assert_none(result1.penaltiesWinner)

        result2: Result = results[1]
        Assertions.assert_equals(
            UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
            result2.id
        )
        Assertions.assert_equals(3, result2.homeGoals)
        Assertions.assert_equals(3, result2.awayGoals)
        Assertions.assert_true(result2.afterExtraTime)
        Assertions.assert_true(result2.afterPenalties)
        Assertions.assert_equals(Winner.AWAY, result2.penaltiesWinner)

    def test_should_error_tournament_not_exists_update_results(self):
        # Given
        results: list[Result] = [
            Result(
                id=UUID("1db1fe5c-97d4-42e9-974f-633edb1dc0c4"),
                homeGoals=2,
                awayGoals=1,
                afterExtraTime=True,
                afterPenalties=False
            ),
            Result(
                id=UUID("a1212f49-534f-4d36-90f4-f3ec9f0d9735"),
                homeGoals=3,
                awayGoals=3,
                afterExtraTime=True,
                afterPenalties=True,
                penaltiesWinner=Winner.AWAY
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
            self.__service.update_results(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                results
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )
