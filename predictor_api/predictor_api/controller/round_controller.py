from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.round import Round
from predictor_api.predictor_api.service.round_service import RoundService


class RoundController:

    def __init__(self, round_service: RoundService) -> None:
        self.router: APIRouter = APIRouter(
            tags=["Rounds"]
        )
        self.__service = round_service

        self.router.add_api_route(
            "/tournaments/{tournament_id}/rounds",
            self.get_rounds,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "examples": {
                                "tournamentNotFound": {
                                    "summary": "Tournament not found",
                                    "value": {
                                        "detail": "No tournaments found with "
                                                  "a matching id."
                                    }
                                },
                                "noKnockoutStage": {
                                    "summary": "Tournament has no knockout "
                                               "stage",
                                    "value": {
                                        "detail": "The tournament with the "
                                                  "supplied id does not have "
                                                  "a knockout stage."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )

    async def get_rounds(self, tournament_id: UUID) -> list[Round]:
        """
        GET /tournaments/{tournament_id}/rounds endpoint to retrieve stored
        rounds.

        Args:
            tournament_id (UUID): The id of the tournament whose rounds are
                to be retrieved.

        Returns:
            list[Round]: The stored rounds.
        """
        return self.__service.get_rounds(tournament_id)
