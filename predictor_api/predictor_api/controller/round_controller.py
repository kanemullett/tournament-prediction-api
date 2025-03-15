from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.round import Round
from predictor_api.predictor_api.model.round_update import RoundUpdate
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
        self.router.add_api_route(
            "/tournaments/{tournament_id}/rounds",
            self.update_rounds,
            methods=["PUT"],
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

    async def update_rounds(
            self,
            tournament_id: UUID,
            rounds: list[RoundUpdate]) -> list[Round]:
        """
        PUT /tournaments/{tournament_id}/rounds endpoint to update existing
        rounds.

        Args:
            tournament_id (UUID): The id of the tournament whose rounds are
                to be updated.
            rounds (list[RoundUpdate]): The rounds to update.

        Returns:
            list[Round]: The newly updated rounds.
        """
        return self.__service.update_rounds(tournament_id, rounds)
