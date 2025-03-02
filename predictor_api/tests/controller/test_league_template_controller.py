import pytest

from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from predictor_api.predictor_api.controller.league_template_controller import (
    LeagueTemplateController
)
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_common.test_resources.assertions import Assertions


class TestLeagueTemplateController:

    __service: MagicMock = MagicMock()

    __controller: LeagueTemplateController = (
        LeagueTemplateController(__service)
    )

    @pytest.mark.asyncio
    async def test_should_pass_league_templates_as_response(self):
        # Given
        self.__service.get_league_templates.return_value = [
            LeagueTemplate(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                name="8x4 Group-Stage Single-Game",
                groupCount=8,
                teamsPerGroup=4,
                homeAndAway=False
            ),
            LeagueTemplate(
                id="6ee28143-1286-4618-a8b9-ad86d348ead1",
                name="6x4 Group-Stage Single-Game",
                groupCount=6,
                teamsPerGroup=4,
                homeAndAway=False
            )
        ]

        # When
        league_templates: list[LeagueTemplate] = await (
            self.__controller.get_league_templates()
        )

        # Then
        Assertions.assert_equals(2, len(league_templates))

        template1 = league_templates[0]
        Assertions.assert_type(LeagueTemplate, template1)
        Assertions.assert_type(UUID, template1.id)
        Assertions.assert_equals("8x4 Group-Stage Single-Game", template1.name)
        Assertions.assert_equals(8, template1.groupCount)
        Assertions.assert_equals(4, template1.teamsPerGroup)
        Assertions.assert_false(template1.homeAndAway)

        template2 = league_templates[1]
        Assertions.assert_type(LeagueTemplate, template2)
        Assertions.assert_type(UUID, template2.id)
        Assertions.assert_equals("6x4 Group-Stage Single-Game", template2.name)
        Assertions.assert_equals(6, template2.groupCount)
        Assertions.assert_equals(4, template2.teamsPerGroup)
        Assertions.assert_false(template2.homeAndAway)

    @pytest.mark.asyncio
    async def test_should_pass_created_league_templates_as_response(self):
        # Given
        league_templates: list[LeagueTemplate] = [
            LeagueTemplate(
                name="8x4 Group-Stage Single-Game",
                groupCount=8,
                teamsPerGroup=4,
                homeAndAway=False
            ),
            LeagueTemplate(
                name="6x4 Group-Stage Single-Game",
                groupCount=6,
                teamsPerGroup=4,
                homeAndAway=False
            )
        ]

        self.__service.create_league_templates.return_value = [
            LeagueTemplate(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                name="8x4 Group-Stage Single-Game",
                groupCount=8,
                teamsPerGroup=4,
                homeAndAway=False
            ),
            LeagueTemplate(
                id="6ee28143-1286-4618-a8b9-ad86d348ead1",
                name="6x4 Group-Stage Single-Game",
                groupCount=6,
                teamsPerGroup=4,
                homeAndAway=False
            )
        ]

        # When
        created: list[LeagueTemplate] = await (
            self.__controller.create_league_templates(
                league_templates
            )
        )

        # Then
        Assertions.assert_equals(2, len(created))

        template1 = created[0]
        Assertions.assert_type(LeagueTemplate, template1)
        Assertions.assert_type(UUID, template1.id)
        Assertions.assert_equals("8x4 Group-Stage Single-Game", template1.name)
        Assertions.assert_equals(8, template1.groupCount)
        Assertions.assert_equals(4, template1.teamsPerGroup)
        Assertions.assert_false(template1.homeAndAway)

        template2 = created[1]
        Assertions.assert_type(LeagueTemplate, template2)
        Assertions.assert_type(UUID, template2.id)
        Assertions.assert_equals("6x4 Group-Stage Single-Game", template2.name)
        Assertions.assert_equals(6, template2.groupCount)
        Assertions.assert_equals(4, template2.teamsPerGroup)
        Assertions.assert_false(template2.homeAndAway)

    @pytest.mark.asyncio
    async def test_should_pass_found_league_template_as_response(self):
        # Given
        self.__service.get_league_template_by_id.return_value = LeagueTemplate(
            id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            name="8x4 Group-Stage Single-Game",
            groupCount=8,
            teamsPerGroup=4,
            homeAndAway=False
        )

        # When
        league_template: LeagueTemplate = await (
            self.__controller.get_league_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )
        )

        # Then
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            league_template.id
        )
        Assertions.assert_equals(
            "8x4 Group-Stage Single-Game",
            league_template.name
        )
        Assertions.assert_equals(8, league_template.groupCount)
        Assertions.assert_equals(4, league_template.teamsPerGroup)
        Assertions.assert_false(league_template.homeAndAway)

    @pytest.mark.asyncio
    async def test_should_pass_error_if_league_template_not_found(self):
        # Given
        self.__service.get_league_template_by_id.side_effect = HTTPException(
            status_code=404,
            detail="No league templates found with a matching id."
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.get_league_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No league templates found with a matching id.",
            httpe.value.detail
        )

    @pytest.mark.asyncio
    async def test_should_pass_error_if_league_template_is_being_used(self):
        # Given
        self.__service.delete_league_template_by_id.side_effect = (
            HTTPException(
                status_code=409,
                detail="Cannot delete league template as it is part of an "
                       "existing tournament template."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.delete_league_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"))

        # Then
        Assertions.assert_equals(409, httpe.value.status_code)
        Assertions.assert_equals(
            "Cannot delete league template as it is part of an existing "
            "tournament template.",
            httpe.value.detail
        )
