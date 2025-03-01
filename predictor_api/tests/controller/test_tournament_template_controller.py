import pytest

from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from predictor_api.predictor_api.controller.tournament_template_controller import TournamentTemplateController
from predictor_api.predictor_api.model.knockout_round import KnockoutRound
from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament_template import TournamentTemplate
from predictor_api.predictor_api.model.tournament_template_request import TournamentTemplateRequest
from predictor_common.test_resources.assertions import Assertions


class TestTournamentTemplateController:

    __tournament_template_service: MagicMock = MagicMock()

    __tournament_template_controller: TournamentTemplateController = TournamentTemplateController(
        __tournament_template_service
    )

    @pytest.mark.asyncio
    async def test_should_pass_tournament_templates_as_response(self):
        # Given
        self.__tournament_template_service.get_tournament_templates.return_value = [
            TournamentTemplate(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                name="tournament1",
                knockout=KnockoutTemplate(
                    id="80e9c164-637d-400f-a3cf-bf922073bc9b",
                    name="knockout1",
                    rounds=[
                        KnockoutRound(
                            name="round1",
                            teamCount=4,
                            roundOrder=1,
                            twoLegs=True,
                            extraTime=True,
                            awayGoals=True
                        ),
                        KnockoutRound(
                            name="round2",
                            teamCount=2,
                            roundOrder=2,
                            twoLegs=False,
                            extraTime=True,
                            awayGoals=False
                        )
                    ]
                )
            ),
            TournamentTemplate(
                id="6ee28143-1286-4618-a8b9-ad86d348ead1",
                name="tournament2",
                league=LeagueTemplate(
                    id="0ca3adf1-f5a5-43e9-9c82-5619340739be",
                    name="league1",
                    groupCount=8,
                    teamsPerGroup=4,
                    homeAndAway=True
                )
            ),
            TournamentTemplate(
                id="d15956ef-d199-40b1-b7d7-850a9add97e7",
                name="tournament3",
                league=LeagueTemplate(
                    id="508c8b55-2e0c-415b-8078-2dcb2065c7ca",
                    name="league2",
                    groupCount=6,
                    teamsPerGroup=4,
                    homeAndAway=False
                ),
                knockout=KnockoutTemplate(
                    id="1a4d1cc8-f035-439a-b274-fe739b8fcfa5",
                    name="knockout2",
                    rounds=[
                        KnockoutRound(
                            name="round3",
                            teamCount=4,
                            roundOrder=1,
                            twoLegs=True,
                            extraTime=True,
                            awayGoals=True
                        ),
                        KnockoutRound(
                            name="round4",
                            teamCount=2,
                            roundOrder=2,
                            twoLegs=False,
                            extraTime=True,
                            awayGoals=False
                        )
                    ]
                )
            )
        ]

        # When
        tournament_templates: list[KnockoutTemplate] = \
            await self.__tournament_template_controller.get_tournament_templates()

        # Then
        Assertions.assert_equals(3, len(tournament_templates))

        tournament1: TournamentTemplate = tournament_templates[0]
        Assertions.assert_type(TournamentTemplate, tournament1)
        Assertions.assert_equals(UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"), tournament1.id)
        Assertions.assert_equals("tournament1", tournament1.name)
        Assertions.assert_none(tournament1.league)

        knockout1: KnockoutTemplate = tournament1.knockout
        Assertions.assert_type(KnockoutTemplate, knockout1)
        Assertions.assert_equals(UUID("80e9c164-637d-400f-a3cf-bf922073bc9b"), knockout1.id)
        Assertions.assert_equals("knockout1", knockout1.name)
        Assertions.assert_equals(2, len(knockout1.rounds))

        knockout1_round1: KnockoutRound = knockout1.rounds[0]
        Assertions.assert_equals("round1", knockout1_round1.name)
        Assertions.assert_equals(4, knockout1_round1.teamCount)
        Assertions.assert_equals(1, knockout1_round1.roundOrder)
        Assertions.assert_true(knockout1_round1.twoLegs)
        Assertions.assert_true(knockout1_round1.extraTime)
        Assertions.assert_true(knockout1_round1.awayGoals)

        knockout1_round2: KnockoutRound = knockout1.rounds[1]
        Assertions.assert_equals("round2", knockout1_round2.name)
        Assertions.assert_equals(2, knockout1_round2.teamCount)
        Assertions.assert_equals(2, knockout1_round2.roundOrder)
        Assertions.assert_false(knockout1_round2.twoLegs)
        Assertions.assert_true(knockout1_round2.extraTime)
        Assertions.assert_false(knockout1_round2.awayGoals)

        tournament2: TournamentTemplate = tournament_templates[1]
        Assertions.assert_type(TournamentTemplate, tournament2)
        Assertions.assert_equals(UUID("6ee28143-1286-4618-a8b9-ad86d348ead1"), tournament2.id)
        Assertions.assert_equals("tournament2", tournament2.name)
        Assertions.assert_none(tournament2.knockout)

        league1: LeagueTemplate = tournament2.league
        Assertions.assert_equals(UUID("0ca3adf1-f5a5-43e9-9c82-5619340739be"), league1.id)
        Assertions.assert_equals("league1", league1.name)
        Assertions.assert_equals(8, league1.groupCount)
        Assertions.assert_equals(4, league1.teamsPerGroup)
        Assertions.assert_true(league1.homeAndAway)

        tournament3: TournamentTemplate = tournament_templates[2]
        Assertions.assert_type(TournamentTemplate, tournament3)
        Assertions.assert_equals(UUID("d15956ef-d199-40b1-b7d7-850a9add97e7"), tournament3.id)
        Assertions.assert_equals("tournament3", tournament3.name)

        league2: LeagueTemplate = tournament3.league
        Assertions.assert_equals(UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"), league2.id)
        Assertions.assert_equals("league2", league2.name)
        Assertions.assert_equals(6, league2.groupCount)
        Assertions.assert_equals(4, league2.teamsPerGroup)
        Assertions.assert_false(league2.homeAndAway)

        knockout2: KnockoutTemplate = tournament3.knockout
        Assertions.assert_type(KnockoutTemplate, knockout2)
        Assertions.assert_equals(UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"), knockout2.id)
        Assertions.assert_equals("knockout2", knockout2.name)
        Assertions.assert_equals(2, len(knockout2.rounds))

        knockout2_round1: KnockoutRound = knockout2.rounds[0]
        Assertions.assert_equals("round3", knockout2_round1.name)
        Assertions.assert_equals(4, knockout2_round1.teamCount)
        Assertions.assert_equals(1, knockout2_round1.roundOrder)
        Assertions.assert_true(knockout2_round1.twoLegs)
        Assertions.assert_true(knockout2_round1.extraTime)
        Assertions.assert_true(knockout2_round1.awayGoals)

        knockout2_round2: KnockoutRound = knockout2.rounds[1]
        Assertions.assert_equals("round4", knockout2_round2.name)
        Assertions.assert_equals(2, knockout2_round2.teamCount)
        Assertions.assert_equals(2, knockout2_round2.roundOrder)
        Assertions.assert_false(knockout2_round2.twoLegs)
        Assertions.assert_true(knockout2_round2.extraTime)
        Assertions.assert_false(knockout2_round2.awayGoals)

    @pytest.mark.asyncio
    async def test_should_pass_created_tournament_templates_as_response(self):
        # Given
        tournament_templates: list[TournamentTemplateRequest] = [
            TournamentTemplateRequest(
                name="tournament1",
                knockoutTemplateId=UUID("80e9c164-637d-400f-a3cf-bf922073bc9b")
            ),
            TournamentTemplateRequest(
                name="tournament2",
                leagueTemplateId=UUID("0ca3adf1-f5a5-43e9-9c82-5619340739be")
            ),
            TournamentTemplateRequest(
                name="tournament3",
                leagueTemplateId=UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"),
                knockoutTemplateId=UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5")
            )
        ]

        self.__tournament_template_service.create_tournament_templates.return_value = [
            TournamentTemplate(
                id="c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                name="tournament1",
                knockout=KnockoutTemplate(
                    id="80e9c164-637d-400f-a3cf-bf922073bc9b",
                    name="knockout1",
                    rounds=[
                        KnockoutRound(
                            name="round1",
                            teamCount=4,
                            roundOrder=1,
                            twoLegs=True,
                            extraTime=True,
                            awayGoals=True
                        ),
                        KnockoutRound(
                            name="round2",
                            teamCount=2,
                            roundOrder=2,
                            twoLegs=False,
                            extraTime=True,
                            awayGoals=False
                        )
                    ]
                )
            ),
            TournamentTemplate(
                id="6ee28143-1286-4618-a8b9-ad86d348ead1",
                name="tournament2",
                league=LeagueTemplate(
                    id="0ca3adf1-f5a5-43e9-9c82-5619340739be",
                    name="league1",
                    groupCount=8,
                    teamsPerGroup=4,
                    homeAndAway=True
                )
            ),
            TournamentTemplate(
                id="d15956ef-d199-40b1-b7d7-850a9add97e7",
                name="tournament3",
                league=LeagueTemplate(
                    id="508c8b55-2e0c-415b-8078-2dcb2065c7ca",
                    name="league2",
                    groupCount=6,
                    teamsPerGroup=4,
                    homeAndAway=False
                ),
                knockout=KnockoutTemplate(
                    id="1a4d1cc8-f035-439a-b274-fe739b8fcfa5",
                    name="knockout2",
                    rounds=[
                        KnockoutRound(
                            name="round3",
                            teamCount=4,
                            roundOrder=1,
                            twoLegs=True,
                            extraTime=True,
                            awayGoals=True
                        ),
                        KnockoutRound(
                            name="round4",
                            teamCount=2,
                            roundOrder=2,
                            twoLegs=False,
                            extraTime=True,
                            awayGoals=False
                        )
                    ]
                )
            )
        ]

        # When
        created: list[TournamentTemplate] = await self.__tournament_template_controller.create_tournament_templates(
            tournament_templates
        )

        # Then
        Assertions.assert_equals(3, len(created))

        tournament1: TournamentTemplate = created[0]
        Assertions.assert_type(TournamentTemplate, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals("tournament1", tournament1.name)
        Assertions.assert_none(tournament1.league)

        knockout1: KnockoutTemplate = tournament1.knockout
        Assertions.assert_type(KnockoutTemplate, knockout1)
        Assertions.assert_equals(UUID("80e9c164-637d-400f-a3cf-bf922073bc9b"), knockout1.id)
        Assertions.assert_equals("knockout1", knockout1.name)
        Assertions.assert_equals(2, len(knockout1.rounds))

        knockout1_round1: KnockoutRound = knockout1.rounds[0]
        Assertions.assert_equals("round1", knockout1_round1.name)
        Assertions.assert_equals(4, knockout1_round1.teamCount)
        Assertions.assert_equals(1, knockout1_round1.roundOrder)
        Assertions.assert_true(knockout1_round1.twoLegs)
        Assertions.assert_true(knockout1_round1.extraTime)
        Assertions.assert_true(knockout1_round1.awayGoals)

        knockout1_round2: KnockoutRound = knockout1.rounds[1]
        Assertions.assert_equals("round2", knockout1_round2.name)
        Assertions.assert_equals(2, knockout1_round2.teamCount)
        Assertions.assert_equals(2, knockout1_round2.roundOrder)
        Assertions.assert_false(knockout1_round2.twoLegs)
        Assertions.assert_true(knockout1_round2.extraTime)
        Assertions.assert_false(knockout1_round2.awayGoals)

        tournament2: TournamentTemplate = created[1]
        Assertions.assert_type(TournamentTemplate, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals("tournament2", tournament2.name)
        Assertions.assert_none(tournament2.knockout)

        league1: LeagueTemplate = tournament2.league
        Assertions.assert_equals(UUID("0ca3adf1-f5a5-43e9-9c82-5619340739be"), league1.id)
        Assertions.assert_equals("league1", league1.name)
        Assertions.assert_equals(8, league1.groupCount)
        Assertions.assert_equals(4, league1.teamsPerGroup)
        Assertions.assert_true(league1.homeAndAway)

        tournament3: TournamentTemplate = created[2]
        Assertions.assert_type(TournamentTemplate, tournament3)
        Assertions.assert_type(UUID, tournament3.id)
        Assertions.assert_equals("tournament3", tournament3.name)

        league2: LeagueTemplate = tournament3.league
        Assertions.assert_equals(UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"), league2.id)
        Assertions.assert_equals("league2", league2.name)
        Assertions.assert_equals(6, league2.groupCount)
        Assertions.assert_equals(4, league2.teamsPerGroup)
        Assertions.assert_false(league2.homeAndAway)

        knockout2: KnockoutTemplate = tournament3.knockout
        Assertions.assert_type(KnockoutTemplate, knockout2)
        Assertions.assert_equals(UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"), knockout2.id)
        Assertions.assert_equals("knockout2", knockout2.name)
        Assertions.assert_equals(2, len(knockout2.rounds))

        knockout2_round1: KnockoutRound = knockout2.rounds[0]
        Assertions.assert_equals("round3", knockout2_round1.name)
        Assertions.assert_equals(4, knockout2_round1.teamCount)
        Assertions.assert_equals(1, knockout2_round1.roundOrder)
        Assertions.assert_true(knockout2_round1.twoLegs)
        Assertions.assert_true(knockout2_round1.extraTime)
        Assertions.assert_true(knockout2_round1.awayGoals)

        knockout2_round2: KnockoutRound = knockout2.rounds[1]
        Assertions.assert_equals("round4", knockout2_round2.name)
        Assertions.assert_equals(2, knockout2_round2.teamCount)
        Assertions.assert_equals(2, knockout2_round2.roundOrder)
        Assertions.assert_false(knockout2_round2.twoLegs)
        Assertions.assert_true(knockout2_round2.extraTime)
        Assertions.assert_false(knockout2_round2.awayGoals)

    @pytest.mark.asyncio
    async def test_should_pass_found_tournament_template_as_response(self):
        # Given
        self.__tournament_template_service.get_tournament_template_by_id.return_value = TournamentTemplate(
            id="d15956ef-d199-40b1-b7d7-850a9add97e7",
            name="tournament3",
            league=LeagueTemplate(
                id="508c8b55-2e0c-415b-8078-2dcb2065c7ca",
                name="league2",
                groupCount=6,
                teamsPerGroup=4,
                homeAndAway=False
            ),
            knockout=KnockoutTemplate(
                id="1a4d1cc8-f035-439a-b274-fe739b8fcfa5",
                name="knockout2",
                rounds=[
                    KnockoutRound(
                        name="round3",
                        teamCount=4,
                        roundOrder=1,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    KnockoutRound(
                        name="round4",
                        teamCount=2,
                        roundOrder=2,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            )
        )

        # When
        tournament_template: TournamentTemplate = \
            await self.__tournament_template_controller.get_tournament_template_by_id(
                UUID("d15956ef-d199-40b1-b7d7-850a9add97e7")
            )

        # Then
        Assertions.assert_type(TournamentTemplate, tournament_template)
        Assertions.assert_equals(UUID("d15956ef-d199-40b1-b7d7-850a9add97e7"), tournament_template.id)
        Assertions.assert_equals("tournament3", tournament_template.name)

        league2: LeagueTemplate = tournament_template.league
        Assertions.assert_equals(UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"), league2.id)
        Assertions.assert_equals("league2", league2.name)
        Assertions.assert_equals(6, league2.groupCount)
        Assertions.assert_equals(4, league2.teamsPerGroup)
        Assertions.assert_false(league2.homeAndAway)

        knockout2: KnockoutTemplate = tournament_template.knockout
        Assertions.assert_type(KnockoutTemplate, knockout2)
        Assertions.assert_equals(UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"), knockout2.id)
        Assertions.assert_equals("knockout2", knockout2.name)
        Assertions.assert_equals(2, len(knockout2.rounds))

        knockout2_round1: KnockoutRound = knockout2.rounds[0]
        Assertions.assert_equals("round3", knockout2_round1.name)
        Assertions.assert_equals(4, knockout2_round1.teamCount)
        Assertions.assert_equals(1, knockout2_round1.roundOrder)
        Assertions.assert_true(knockout2_round1.twoLegs)
        Assertions.assert_true(knockout2_round1.extraTime)
        Assertions.assert_true(knockout2_round1.awayGoals)

        knockout2_round2: KnockoutRound = knockout2.rounds[1]
        Assertions.assert_equals("round4", knockout2_round2.name)
        Assertions.assert_equals(2, knockout2_round2.teamCount)
        Assertions.assert_equals(2, knockout2_round2.roundOrder)
        Assertions.assert_false(knockout2_round2.twoLegs)
        Assertions.assert_true(knockout2_round2.extraTime)
        Assertions.assert_false(knockout2_round2.awayGoals)

    @pytest.mark.asyncio
    async def test_should_pass_error_if_tournament_template_not_found(self):
        # Given
        self.__tournament_template_service.get_tournament_template_by_id.side_effect = HTTPException(
            status_code=404,
            detail="No tournament templates found with a matching id."
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__tournament_template_controller.get_tournament_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("No tournament templates found with a matching id.", httpe.value.detail)

    @pytest.mark.asyncio
    async def test_should_pass_error_if_tournament_template_is_being_used(self):
        # Given
        self.__tournament_template_service.delete_tournament_template_by_id.side_effect = HTTPException(
            status_code=409,
            detail="Cannot delete tournament template as it is part of an existing tournament."
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__tournament_template_controller.delete_tournament_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"))

        # Then
        Assertions.assert_equals(409, httpe.value.status_code)
        Assertions.assert_equals(
            "Cannot delete tournament template as it is part of an existing tournament.",
            httpe.value.detail
        )
