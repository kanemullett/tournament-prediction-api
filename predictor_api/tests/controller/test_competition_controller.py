from unittest.mock import MagicMock
from uuid import UUID

import pytest

from predictor_api.predictor_api.controller.competition_controller import (
    CompetitionController
)
from predictor_api.predictor_api.model.competition import Competition
from predictor_common.test_resources.assertions import Assertions


class TestCompetitionController:

    __service: MagicMock = MagicMock()

    __controller: CompetitionController = CompetitionController(__service)

    @pytest.mark.asyncio
    async def test_should_pass_competitions_as_response(self):
        # Given
        self.__service.get_competitions.return_value = [
            Competition(
                id=UUID("71d14fb4-ba29-47f7-a235-d2675028d700"),
                name="The Boys",
                tournamentId=UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
            ),
            Competition(
                id=UUID("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900"),
                name="Meine Familie",
                tournamentId=UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
            )
        ]

        # When
        competitions: list[Competition] = await (
            self.__controller.get_competitions()
        )

        # Then
        Assertions.assert_equals(2, len(competitions))

        competition1: Competition = competitions[0]
        Assertions.assert_equals(
            UUID("71d14fb4-ba29-47f7-a235-d2675028d700"),
            competition1.id
        )
        Assertions.assert_equals("The Boys", competition1.name)
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            competition1.tournamentId
        )

        competition2: Competition = competitions[1]
        Assertions.assert_equals(
            UUID("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900"),
            competition2.id
        )
        Assertions.assert_equals("Meine Familie", competition2.name)
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            competition2.tournamentId
        )

    @pytest.mark.asyncio
    async def test_should_pass_created_competitions_as_response(self):
        # Given
        competitions: list[Competition] = [
            Competition(
                name="The Boys",
                tournamentId=UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
            ),
            Competition(
                name="Meine Familie",
                tournamentId=UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
            )
        ]

        self.__service.create_competitions.return_value = [
            Competition(
                id=UUID("71d14fb4-ba29-47f7-a235-d2675028d700"),
                name="The Boys",
                tournamentId=UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
            ),
            Competition(
                id=UUID("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900"),
                name="Meine Familie",
                tournamentId=UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
            )
        ]

        # When
        created: list[Competition] = await (
            self.__controller.create_competitions(competitions)
        )

        # Then
        Assertions.assert_equals(2, len(created))

        competition1: Competition = created[0]
        Assertions.assert_equals(
            UUID("71d14fb4-ba29-47f7-a235-d2675028d700"),
            competition1.id
        )
        Assertions.assert_equals("The Boys", competition1.name)
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            competition1.tournamentId
        )

        competition2: Competition = created[1]
        Assertions.assert_equals(
            UUID("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900"),
            competition2.id
        )
        Assertions.assert_equals("Meine Familie", competition2.name)
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            competition2.tournamentId
        )
