from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.service.team_service import TeamService


class TeamController:

    def __init__(self, team_service: TeamService):
        self.router: APIRouter = APIRouter(
            tags=["Teams"]
        )
        self.__service = team_service

        self.router.add_api_route(
            "/teams",
            self.get_teams,
            methods=["GET"]
        )

    def get_teams(
            self,
            confederation: Confederation = None,
            tournament_id: UUID = None) -> list[Team]:

        return self.__service.get_teams(confederation, tournament_id)
