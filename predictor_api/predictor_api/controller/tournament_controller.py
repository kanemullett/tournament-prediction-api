from uuid import UUID

from fastapi import APIRouter, Response

from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.service.tournament_service import TournamentService


class TournamentController:
    """
    Controller containing endpoints to perform tournament-related actions.

    Attributes:
        __tournament_service (TournamentService): The tournament service containing tournament-based logic.
    """

    def __init__(self, tournament_service: TournamentService) -> None:
        """
        Initialise the TournamentController.

        Attributes:
            tournament_service (TournamentService): The tournament service containing tournament-based logic.
        """
        self.router: APIRouter = APIRouter(prefix="/tournaments", tags=["Tournaments"])
        self.__tournament_service = tournament_service

        self.router.add_api_route(
            "/",
            self.get_tournaments,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/",
            self.create_tournaments,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/",
            self.update_tournaments,
            methods=["PUT"]
        )
        self.router.add_api_route(
            "/{tournament_id}",
            self.get_tournament_by_id,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found - No tournaments found with a matching id.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No tournaments found with a matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/{tournament_id}",
            self.delete_tournament_by_id,
            methods=["DELETE"],
            responses={
                204: {
                    "description": "No Content - The league template was successfully deleted."
                }
            }
        )

    async def get_tournaments(self) -> list[Tournament]:
        """
        GET /tournaments endpoint to retrieve stored tournaments.

        Returns:
            list[Tournament]: The stored tournaments.
        """
        return self.__tournament_service.get_tournaments()

    async def create_tournaments(self, tournaments: list[Tournament]) -> list[Tournament]:
        """
        POST /tournaments endpoint to create new tournaments.

        Args:
            tournaments (list[Tournament]): The new tournaments to create.

        Returns:
            list[Tournament]: The newly created tournaments.
        """
        return self.__tournament_service.create_tournaments(tournaments)

    async def update_tournaments(self, tournaments: list[Tournament]) -> list[Tournament]:
        """
        PUT /tournaments endpoint to update existing tournaments.

        Args:
            tournaments (list[Tournament]): The tournaments to update.

        Returns:
            list[Tournament]: The newly updated tournaments.
        """
        return self.__tournament_service.update_tournaments(tournaments)

    async def get_tournament_by_id(self, tournament_id: UUID) -> Tournament:
        """
        GET /tournaments/{tournament_id} endpoint to retrieve a single stored tournament by its id.

        Args:
            tournament_id (UUID): The id of the tournament to retrieve.

        Returns:
            Tournament: The retrieved tournament.
        """
        return self.__tournament_service.get_tournament_by_id(tournament_id)

    async def delete_tournament_by_id(self, tournament_id: UUID) -> Response:
        """
        DELETE /tournaments/{tournament_id} endpoint to delete a single stored tournament by its id.

        Args:
            tournament_id (UUID): The id of the tournament to delete.
        """
        self.__tournament_service.delete_tournament_by_id(tournament_id)

        return Response(status_code=204)
