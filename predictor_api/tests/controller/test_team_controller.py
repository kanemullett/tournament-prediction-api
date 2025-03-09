from unittest.mock import MagicMock
from uuid import UUID

import pytest

from predictor_api.predictor_api.controller.team_controller import (
    TeamController
)
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_common.test_resources.assertions import Assertions


class TestTeamController:

    __service: MagicMock = MagicMock()

    __controller: TeamController = TeamController(__service)

    @pytest.mark.asyncio
    async def test_should_pass_teams_as_response(self):
        # Given
        self.__service.get_teams.return_value = [
            Team(
                id=UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
                name="Bosnia & Herzegovina",
                imagePath="BIH.png",
                confederation=Confederation.UEFA
            ),
            Team(
                id=UUID("6ee28143-1286-4618-a8b9-ad86d348ead1"),
                name="Botswana",
                imagePath="BOT.png",
                confederation=Confederation.CAF
            ),
            Team(
                id=UUID("e107d069-b277-4902-bdad-7091a494a8b3"),
                name="England",
                imagePath="ENG.png",
                confederation=Confederation.UEFA
            )
        ]

        # When
        teams: list[Team] = await self.__controller.get_teams(None, None)

        # Then
        Assertions.assert_equals(3, len(teams))

        team1: Team = teams[0]
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            team1.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", team1.name)
        Assertions.assert_equals("BIH.png", team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team1.confederation)

        team2: Team = teams[1]
        Assertions.assert_equals(
            UUID("6ee28143-1286-4618-a8b9-ad86d348ead1"),
            team2.id
        )
        Assertions.assert_equals("Botswana", team2.name)
        Assertions.assert_equals("BOT.png", team2.imagePath)
        Assertions.assert_equals(Confederation.CAF, team2.confederation)

        team3: Team = teams[2]
        Assertions.assert_equals(
            UUID("e107d069-b277-4902-bdad-7091a494a8b3"),
            team3.id
        )
        Assertions.assert_equals("England", team3.name)
        Assertions.assert_equals("ENG.png", team3.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team3.confederation)
