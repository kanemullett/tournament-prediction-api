from uuid import UUID

from fastapi import APIRouter, Response

from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.service.team_service import TeamService


class TeamController:
    """
    Controller containing endpoints to perform team-related actions.

    Attributes:
        __service (TeamService): The team service containing tournament-based
            logic.
    """

    def __init__(self, team_service: TeamService):
        """
        Initialise the TeamController.

        Attributes:
            team_service (TeamService): The team service containing
                team-based logic.
        """
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
        """
        GET /teams endpoint to retrieve stored teams.

        Args:
            confederation (Confederation): The confederation to filter by.
            tournament_id (UUID): The tournament id to filter by.

        Returns:
            list[Team]: The stored teams.
        """
        return self.__service.get_teams(confederation, tournament_id)

    async def create_teams(self, teams: list[Team]) -> list[Team]:
        """
        POST /teams endpoint to create new teams.

        Args:
            teams (list[Team]): The new teams to create.

        Returns:
            list[Team]: The newly created teams.
        """
        return self.__service.create_teams(teams)

    async def update_teams(self, teams: list[Team]) -> list[Team]:
        """
        PUT /teams endpoint to update existing teams.

        Args:
            teams (list[Team]): The teams to update.

        Returns:
            list[Team]: The newly updated teams.
        """
        return self.__service.update_teams(teams)

    async def get_team_by_id(self, team_id: UUID) -> Team:
        """
        GET /teams/{team_id} endpoint to retrieve a single stored team by its
        id.

        Args:
            team_id (UUID): The id of the team to retrieve.

        Returns:
            Team: The retrieved team.
        """
        return self.__service.get_team_by_id(team_id)

    async def delete_team_by_id(self, team_id: UUID) -> Response:
        """
        DELETE /teams/{team_id} endpoint to delete a single stored team by
        its id.

        Args:
            team_id (UUID): The id of the team to delete.
        """
        self.__service.delete_team_by_id(team_id)

        return Response(status_code=204)
