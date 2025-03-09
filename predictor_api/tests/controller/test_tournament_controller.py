from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from predictor_api.predictor_api.controller.tournament_controller import (
    TournamentController
)
from predictor_api.predictor_api.model.tournament import Tournament

import pytest

from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_common.test_resources.assertions import Assertions


class TestTournamentController:

    __service: MagicMock = MagicMock()

    __controller: TournamentController = TournamentController(__service)

    @pytest.mark.asyncio
    async def test_should_pass_tournaments_as_response(self):
        # Given
        self.__service.get_tournaments.return_value = [
            Tournament(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                year=2024,
                confederation=Confederation.UEFA
            ),
            Tournament(
                id="6ee28143-1286-4618-a8b9-ad86d348ead1",
                year=2026
            )
        ]

        # When
        tournaments: list[Tournament] = await (
            self.__controller.get_tournaments()
        )

        # Then
        Assertions.assert_equals(2, len(tournaments))

        tournament1 = tournaments[0]
        Assertions.assert_type(Tournament, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals(2024, tournament1.year)
        Assertions.assert_equals(Confederation.UEFA, tournament1.confederation)

        tournament2 = tournaments[1]
        Assertions.assert_type(Tournament, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals(2026, tournament2.year)
        Assertions.assert_none(tournament2.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_created_tournaments_as_response(self):
        # Given
        tournaments: list[Tournament] = [
            Tournament(
                year=2024,
                confederation=Confederation.UEFA
            ),
            Tournament(
                year=2026
            )
        ]

        self.__service.create_tournaments.return_value = [
            Tournament(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                year=2024,
                confederation=Confederation.UEFA
            ),
            Tournament(
                id="6ee28143-1286-4618-a8b9-ad86d348ead1",
                year=2026
            )
        ]

        # When
        created: list[Tournament] = await (
            self.__controller.create_tournaments(tournaments)
        )

        # Then
        Assertions.assert_equals(2, len(created))

        tournament1 = created[0]
        Assertions.assert_type(Tournament, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals(2024, tournament1.year)
        Assertions.assert_equals(Confederation.UEFA, tournament1.confederation)

        tournament2 = created[1]
        Assertions.assert_type(Tournament, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals(2026, tournament2.year)
        Assertions.assert_none(tournament2.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_updated_tournaments_as_response(self):
        # Given
        tournaments: list[Tournament] = [
            Tournament(
                id=UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
                confederation=Confederation.UEFA
            ),
            Tournament(
                id=UUID("023b3aa0-7f61-4331-8206-d75232f49ebc"),
                year=2026
            )
        ]

        self.__service.update_tournaments.return_value = [
            Tournament(
                id=UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
                year=2024,
                confederation=Confederation.UEFA
            ),
            Tournament(
                id=UUID("023b3aa0-7f61-4331-8206-d75232f49ebc"),
                year=2026
            )
        ]

        # When
        updated: list[Tournament] = await (
            self.__controller.update_tournaments(tournaments)
        )

        # Then
        Assertions.assert_equals(2, len(updated))

        tournament1 = updated[0]
        Assertions.assert_type(Tournament, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals(2024, tournament1.year)
        Assertions.assert_equals(Confederation.UEFA, tournament1.confederation)

        tournament2 = updated[1]
        Assertions.assert_type(Tournament, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals(2026, tournament2.year)
        Assertions.assert_none(tournament2.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_found_tournament_as_response(self):
        # Given
        self.__service.get_tournament_by_id.return_value = Tournament(
            id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            year=2024,
            confederation=Confederation.UEFA
        )

        # When
        tournament: Tournament = await self.__controller.get_tournament_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        )

        # Then
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            tournament.id
        )
        Assertions.assert_equals(2024, tournament.year)
        Assertions.assert_equals(Confederation.UEFA, tournament.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_error_if_tournament_not_found(self):
        # Given
        self.__service.get_tournament_by_id.side_effect = HTTPException(
            status_code=404,
            detail="No tournaments found with a matching id."
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.get_tournament_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )
