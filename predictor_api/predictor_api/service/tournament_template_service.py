from uuid import UUID

from db_handler.db_handler.service.database_query_service import DatabaseQueryService
from predictor_api.predictor_api.model.knockout_round import KnockoutRound
from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament_template import TournamentTemplate


class TournamentTemplateService:

    def __init__(self, database_query_service: DatabaseQueryService):
        self.__database_query_service = database_query_service

    def get_tournament_templates(self) -> list[TournamentTemplate]:
        return []

    def create_tournament_templates(self, tournament_templates: list[TournamentTemplate]) -> list[TournamentTemplate]:
        return []

    def get_tournament_template_by_id(self, tournament_template_id: UUID) -> TournamentTemplate:
        return TournamentTemplate(
            name="32-Team Group & Knockout",
            league=LeagueTemplate(
                name="Group Stage",
                groupCount=8,
                teamsPerGroup=4,
                homeAndAway=False
            ),
            knockout=KnockoutTemplate(
                name="Knockout Phase",
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
                        name="Final",
                        teamCount=2,
                        roundOrder=4,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            )
        )

    def delete_tournament_template_by_id(self, tournament_template_id: UUID):
        print("DELETED")
