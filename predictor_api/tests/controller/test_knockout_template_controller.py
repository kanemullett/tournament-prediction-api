import pytest

from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from predictor_api.predictor_api.controller.knockout_template_controller import (  # noqa: E501
    KnockoutTemplateController
)
from predictor_api.predictor_api.model.knockout_round import KnockoutRound
from predictor_api.predictor_api.model.knockout_template import (
    KnockoutTemplate
)
from predictor_common.test_resources.assertions import Assertions


class TestKnockoutTemplateController:

    __service: MagicMock = MagicMock()

    __controller: KnockoutTemplateController = (
        KnockoutTemplateController(__service)
    )

    @pytest.mark.asyncio
    async def test_should_pass_knockout_templates_as_response(self):
        # Given
        self.__service.get_knockout_templates.return_value = [
            KnockoutTemplate(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
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
                id="6ee28143-1286-4618-a8b9-ad86d348ead1",
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
        knockout_templates: list[KnockoutTemplate] = await (
            self.__controller.get_knockout_templates()
        )

        # Then
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
        Assertions.assert_equals(
            "8-Team Double-Leg Away Goals",
            template2.name
        )
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

    @pytest.mark.asyncio
    async def test_should_pass_created_knockout_templates_as_response(self):
        # Given
        knockout_templates: list[KnockoutTemplate] = [
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

        self.__service.create_knockout_templates.return_value = [
            KnockoutTemplate(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
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
                id="6ee28143-1286-4618-a8b9-ad86d348ead1",
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
        created: list[KnockoutTemplate] = await (
            self.__controller.create_knockout_templates(
                knockout_templates
            )
        )

        # Then
        Assertions.assert_equals(2, len(created))

        template1 = created[0]
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

        template2 = created[1]
        Assertions.assert_type(KnockoutTemplate, template2)
        Assertions.assert_type(UUID, template2.id)
        Assertions.assert_equals(
            "8-Team Double-Leg Away Goals",
            template2.name
        )
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

    @pytest.mark.asyncio
    async def test_should_pass_found_knockout_template_as_response(self):
        # Given
        self.__service.get_knockout_template_by_id.return_value = (
            KnockoutTemplate(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
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
        )

        # When
        knockout_template: KnockoutTemplate = await (
            self.__controller.get_knockout_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )
        )

        # Then
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            knockout_template.id
        )
        Assertions.assert_equals(
            "8-Team Double-Leg Away Goals",
            knockout_template.name
        )
        Assertions.assert_equals(3, len(knockout_template.rounds))

        template2_round1 = knockout_template.rounds[0]
        Assertions.assert_type(KnockoutRound, template2_round1)
        Assertions.assert_equals("Quarter-Finals", template2_round1.name)
        Assertions.assert_equals(8, template2_round1.teamCount)
        Assertions.assert_equals(1, template2_round1.roundOrder)
        Assertions.assert_true(template2_round1.twoLegs)
        Assertions.assert_true(template2_round1.extraTime)
        Assertions.assert_true(template2_round1.awayGoals)

        template2_round2 = knockout_template.rounds[1]
        Assertions.assert_type(KnockoutRound, template2_round2)
        Assertions.assert_equals("Semi-Finals", template2_round2.name)
        Assertions.assert_equals(4, template2_round2.teamCount)
        Assertions.assert_equals(2, template2_round2.roundOrder)
        Assertions.assert_true(template2_round2.twoLegs)
        Assertions.assert_true(template2_round2.extraTime)
        Assertions.assert_true(template2_round2.awayGoals)

        template2_round3 = knockout_template.rounds[2]
        Assertions.assert_type(KnockoutRound, template2_round3)
        Assertions.assert_equals("Final", template2_round3.name)
        Assertions.assert_equals(2, template2_round3.teamCount)
        Assertions.assert_equals(3, template2_round3.roundOrder)
        Assertions.assert_false(template2_round3.twoLegs)
        Assertions.assert_true(template2_round3.extraTime)
        Assertions.assert_false(template2_round3.awayGoals)

    @pytest.mark.asyncio
    async def test_should_pass_error_if_knockout_template_not_found(self):
        # Given
        self.__service.get_knockout_template_by_id.side_effect = HTTPException(
            status_code=404,
            detail="No knockout templates found with a matching id."
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.get_knockout_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No knockout templates found with a matching id.",
            httpe.value.detail
        )

    @pytest.mark.asyncio
    async def test_should_pass_error_if_knockout_template_is_being_used(self):
        # Given
        self.__service.delete_knockout_template_by_id.side_effect = (
            HTTPException(
                status_code=409,
                detail="Cannot delete knockout template as it is part of an "
                       "existing tournament template."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.delete_knockout_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(409, httpe.value.status_code)
        Assertions.assert_equals(
            "Cannot delete knockout template as it is part of an existing "
            "tournament template.",
            httpe.value.detail
        )
