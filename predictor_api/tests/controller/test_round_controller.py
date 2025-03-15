from unittest.mock import MagicMock
from uuid import UUID

import pytest

from fastapi import HTTPException
from pytest import raises

from predictor_api.predictor_api.controller.round_controller import (
    RoundController
)
from predictor_api.predictor_api.model.round import Round
from predictor_api.predictor_api.model.round_update import RoundUpdate
from predictor_common.test_resources.assertions import Assertions


class TestRoundController:
    __service: MagicMock = MagicMock()

    __controller: RoundController = RoundController(__service)

    def setup_method(self):
        self.__service.get_groups.reset_mock()
        self.__service.get_groups.return_value = None
        self.__service.get_groups.side_effect = None

        self.__service.update_groups.reset_mock()
        self.__service.update_groups.return_value = None
        self.__service.update_groups.side_effect = None

    @pytest.mark.asyncio
    async def test_should_pass_rounds_as_response(self):
        # Given
        self.__service.get_rounds.return_value = [
            Round(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Round 1",
                teamCount=32,
                roundOrder=1,
                twoLegs=True,
                extraTime=True,
                awayGoals=True
            ),
            Round(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Round 2",
                teamCount=16,
                roundOrder=2,
                twoLegs=True,
                extraTime=True,
                awayGoals=True
            )
        ]

        # When
        rounds: list[Round] = await self.__controller.get_rounds(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797")
        )

        # Then
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
        Assertions.assert_true(round2.awayGoals)

    @pytest.mark.asyncio
    async def test_should_pass_error_get_rounds(self):
        # Given
        self.__service.get_rounds.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.get_rounds(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)

    @pytest.mark.asyncio
    async def test_should_pass_updated_rounds(self):
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

        self.__service.update_rounds.return_value = [
            Round(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Round 1",
                teamCount=32,
                roundOrder=1,
                twoLegs=True,
                extraTime=True,
                awayGoals=True
            ),
            Round(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Round 2",
                teamCount=16,
                roundOrder=2,
                twoLegs=True,
                extraTime=True,
                awayGoals=True
            )
        ]

        # When
        rounds: list[Round] = await self.__controller.update_rounds(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
            round_updates
        )

        # Then
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
        Assertions.assert_true(round2.awayGoals)

    @pytest.mark.asyncio
    async def test_should_pass_error_update_rounds(self):
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

        self.__service.update_rounds.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.update_rounds(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                round_updates
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)

    @pytest.mark.asyncio
    async def test_should_pass_round(self):
        # Given
        self.__service.get_round_by_id.return_value = (
            Round(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Round 1",
                teamCount=32,
                roundOrder=1,
                twoLegs=True,
                extraTime=True,
                awayGoals=True
            )
        )

        # When
        found_round: Round = await self.__controller.get_round_by_id(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659")
        )

        # Then
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            found_round.id
        )
        Assertions.assert_equals("Round 1", found_round.name)
        Assertions.assert_equals(32, found_round.teamCount)
        Assertions.assert_equals(1, found_round.roundOrder)
        Assertions.assert_true(found_round.twoLegs)
        Assertions.assert_true(found_round.extraTime)
        Assertions.assert_true(found_round.awayGoals)

    @pytest.mark.asyncio
    async def test_should_pass_error_get_round_by_id(self):
        # Given
        self.__service.get_round_by_id.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.get_round_by_id(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)
