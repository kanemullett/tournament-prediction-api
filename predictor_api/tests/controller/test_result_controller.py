from unittest.mock import MagicMock
from uuid import UUID

import pytest

from fastapi import HTTPException
from pytest import raises

from predictor_api.predictor_api.controller.result_controller import (
    ResultController
)
from predictor_api.predictor_api.model.result import Result
from predictor_api.predictor_api.model.type.winner import Winner
from predictor_common.test_resources.assertions import Assertions


class TestResultController:
    __service: MagicMock = MagicMock()

    __controller: ResultController = ResultController(__service)

    @pytest.mark.asyncio
    async def test_should_pass_created_results(self):
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

        self.__service.create_results.return_value = [
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

        # When
        created: list[Result] = await self.__controller.create_results(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
            results
        )

        # Then
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

    @pytest.mark.asyncio
    async def test_should_pass_error_create_results(self):
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

        self.__service.create_results.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.create_results(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                results
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)

    @pytest.mark.asyncio
    async def test_should_pass_updated_results(self):
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

        self.__service.update_results.return_value = [
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

        # When
        created: list[Result] = await self.__controller.update_results(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
            results
        )

        # Then
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

    @pytest.mark.asyncio
    async def test_should_pass_error_update_results(self):
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

        self.__service.update_results.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.update_results(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                results
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)
