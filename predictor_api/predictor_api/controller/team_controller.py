from uuid import UUID

from fastapi import APIRouter, Response

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
        self.router.add_api_route(
            "/teams",
            self.create_teams,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/teams",
            self.update_teams,
            methods=["PUT"]
        )
        self.router.add_api_route(
            "/teams/{team_id}",
            self.get_team_by_id,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found - No teams found with a "
                                   "matching id.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No teams found with a matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/teams/{team_id}",
            self.delete_team_by_id,
            methods=["DELETE"],
            responses={
                204: {
                    "description": "No Content - The team was successfully "
                                   "deleted."
                }
            }
        )

    async def get_teams(
            self,
            confederation: Confederation = None,
            tournament_id: UUID = None) -> list[Team]:
        return self.__service.get_teams(confederation, tournament_id)

    async def create_teams(self, teams: list[Team]) -> list[Team]:
        return self.__service.create_teams(teams)

    async def update_teams(self, teams: list[Team]) -> list[Team]:
        return self.__service.update_teams(teams)

    async def get_team_by_id(self, team_id: UUID) -> Team:
        return self.__service.get_team_by_id(team_id)

    async def delete_team_by_id(self, team_id: UUID) -> Response:
        self.__service.delete_team_by_id(team_id)

        return Response(status_code=204)
