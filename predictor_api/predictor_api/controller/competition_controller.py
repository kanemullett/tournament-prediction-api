from uuid import UUID

from fastapi import APIRouter, Response

from predictor_api.predictor_api.model.competition import Competition
from predictor_api.predictor_api.service.competition_service import (
    CompetitionService
)


class CompetitionController:
    """
    Controller containing endpoints to perform competition-related actions.

    Attributes:
        __service (CompetitionService): The competition service containing
            competition-based logic.
    """

    def __init__(self, competition_service: CompetitionService):
        """
        Initialise the CompetitionController.

        Attributes:
            competition_service (CompetitionService): The competition service
                containing competition-based logic.
        """
        self.router: APIRouter = APIRouter(
            tags=["Competitions"]
        )
        self.__service = competition_service

        self.router.add_api_route(
            "/competitions",
            self.get_competitions,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/competitions",
            self.create_competitions,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/competitions",
            self.update_competitions,
            methods=["PUT"]
        )
        self.router.add_api_route(
            "/competitions/{competition_id}",
            self.get_competition_by_id,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No competitions found with a "
                                          "matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/competitions/{competition_id}",
            self.delete_competition_by_id,
            methods=["DELETE"],
            responses={
                204: {
                    "description": "No Content"
                }
            }
        )

    async def get_competitions(self) -> list[Competition]:
        """
        GET /competitions endpoint to retrieve stored competitions.

        Returns:
            list[Competition]: The stored competitions.
        """
        return self.__service.get_competitions()

    async def create_competitions(
            self,
            competitions: list[Competition]) -> list[Competition]:
        """
        POST /competitions endpoint to create new competitions.

        Args:
            competitions (list[Competition]): The new competitions to create.

        Returns:
            list[Competition]: The newly created competitions.
        """
        return self.__service.create_competitions(competitions)

    async def update_competitions(
            self,
            competitions: list[Competition]) -> list[Competition]:
        """
        PUT /competitions endpoint to update existing competitions.

        Args:
            competitions (list[Competition]): The competitions to update.

        Returns:
            list[Competition]: The newly updated competitions.
        """
        return self.__service.update_competitions(competitions)

    async def get_competition_by_id(self, competition_id: UUID) -> Competition:
        """
        GET /competitions/{competition_id} endpoint to retrieve a single
        stored competition by its id.

        Args:
            competition_id (UUID): The id of the competition to retrieve.

        Returns:
            Competition: The retrieved competition.
        """
        return self.__service.get_competition_by_id(competition_id)

    async def delete_competition_by_id(self, competition_id: UUID) -> Response:
        """
        DELETE /competitions/{competition_id} endpoint to delete a single
        stored competition by its id.

        Args:
            competition_id (UUID): The id of the competition to delete.
        """
        self.__service.delete_competition_by_id(competition_id)

        return Response(status_code=204)
