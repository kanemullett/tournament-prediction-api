from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from fastapi import HTTPException
from pytest import raises

from predictor_api.predictor_api.controller.match_controller import (
    MatchController
)
from predictor_api.predictor_api.model.match import Match
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_common.test_resources.assertions import Assertions


class TestMatchController:
    __service: MagicMock = MagicMock()

    __controller: MatchController = MatchController(__service)

    @pytest.mark.asyncio
    async def test_should_pass_matches_as_response(self):
        # Given
        self.__service.get_matches.return_value = [
            Match(
                id=UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
                homeTeam=Team(
                    id=UUID("bbec1707-7ea3-49cb-9791-7a1358a2b894"),
                    name="Bosnia & Herzegovina",
                    imagePath="BIH.png",
                    confederation=Confederation.UEFA
                ),
                awayTeam=Team(
                    id=UUID("463de8d9-8520-4fa4-b30c-5aac0f3b363c"),
                    name="Nigeria",
                    imagePath="NGA.png",
                    confederation=Confederation.CAF
                ),
                kickoff=datetime(2025, 6, 1, 14, 0, 0),
                groupMatchDay=1,
                groupId=UUID("4c2c8046-0007-48db-a76a-865f9048d9de")
            ),
            Match(
                id=UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
                homeTeam=Team(
                    id=UUID("977f3f69-0149-43fd-adb0-7c524aea37aa"),
                    name="Argentina",
                    imagePath="ARG.png",
                    confederation=Confederation.CONMEBOL
                ),
                awayTeam=Team(
                    id=UUID("58adea3b-bdda-496a-be74-64501e34622b"),
                    name="Iran",
                    imagePath="IRI.png",
                    confederation=Confederation.AFC
                ),
                kickoff=datetime(2025, 6, 1, 17, 30, 0),
                roundId=UUID("322ab9d0-ae46-49ac-89b3-c789a0d9d889")
            )
        ]

        # When
        matches: list[Match] = await self.__controller.get_matches(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            None,
            None,
            None
        )

        # Then
        Assertions.assert_equals(2, len(matches))

        match1: Match = matches[0]
        Assertions.assert_equals(
            UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
            match1.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 14, 0, 0),
            match1.kickoff
        )
        Assertions.assert_equals(1, match1.groupMatchDay)
        Assertions.assert_equals(
            UUID("4c2c8046-0007-48db-a76a-865f9048d9de"),
            match1.groupId
        )
        Assertions.assert_none(match1.roundId)

        match1_home: Team = match1.homeTeam
        Assertions.assert_equals(
            UUID("bbec1707-7ea3-49cb-9791-7a1358a2b894"),
            match1_home.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", match1_home.name)
        Assertions.assert_equals("BIH.png", match1_home.imagePath)
        Assertions.assert_equals(Confederation.UEFA, match1_home.confederation)

        match1_away: Team = match1.awayTeam
        Assertions.assert_equals(
            UUID("463de8d9-8520-4fa4-b30c-5aac0f3b363c"),
            match1_away.id
        )
        Assertions.assert_equals("Nigeria", match1_away.name)
        Assertions.assert_equals("NGA.png", match1_away.imagePath)
        Assertions.assert_equals(Confederation.CAF, match1_away.confederation)

        match2: Match = matches[1]
        Assertions.assert_equals(
            UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
            match2.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 17, 30, 0),
            match2.kickoff
        )
        Assertions.assert_none(match2.groupMatchDay)
        Assertions.assert_none(match2.groupId)
        Assertions.assert_equals(
            UUID("322ab9d0-ae46-49ac-89b3-c789a0d9d889"),
            match2.roundId
        )

        match2_home: Team = match2.homeTeam
        Assertions.assert_equals(
            UUID("977f3f69-0149-43fd-adb0-7c524aea37aa"),
            match2_home.id
        )
        Assertions.assert_equals("Argentina", match2_home.name)
        Assertions.assert_equals("ARG.png", match2_home.imagePath)
        Assertions.assert_equals(
            Confederation.CONMEBOL,
            match2_home.confederation
        )

        match2_away: Team = match2.awayTeam
        Assertions.assert_equals(
            UUID("58adea3b-bdda-496a-be74-64501e34622b"),
            match2_away.id
        )
        Assertions.assert_equals("Iran", match2_away.name)
        Assertions.assert_equals("IRI.png", match2_away.imagePath)
        Assertions.assert_equals(Confederation.AFC, match2_away.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_error_get_matches(self):
        # Given
        self.__service.get_matches.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.get_matches(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                None,
                None,
                None
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)
