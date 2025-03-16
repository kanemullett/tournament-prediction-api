from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.match import Match
from predictor_api.predictor_api.model.match_request import MatchUpdate
from predictor_api.predictor_api.service.match_service import MatchService


class MatchController:
    """
    Controller containing endpoints to perform match-related actions.

    Attributes:
        __service (MatchService): The match service containing match-based
            logic.
    """

    def __init__(self, match_service: MatchService):
        """
        Initialise the MatchController.

        Attributes:
            match_service (MatchService): The match service containing
                match-based logic.
        """
        self.router: APIRouter = APIRouter(
            tags=["Matches"]
        )
        self.__service = match_service

        self.router.add_api_route(
            "/tournaments/{tournament_id}/matches",
            self.get_matches,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No tournaments found with a "
                                          "matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/matches",
            self.update_matches,
            methods=["PUT"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No tournaments found with a "
                                          "matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/matches/{match_id}",
            self.get_match_by_id,
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
                                "matchNotFound": {
                                    "summary": "Match not found",
                                    "value": {
                                        "detail": "No matches found with a "
                                                  "matching id."
                                    }
                                },
                            }
                        }
                    }
                }
            }
        )

    async def get_matches(
            self,
            tournament_id: UUID,
            group_id: UUID = None,
            group_match_day: int = None,
            round_id: UUID = None) -> list[Match]:
        """
        GET /tournaments/{tournament_id}/matches endpoint to retrieve stored
        matches.

        Args:
            tournament_id (UUID): The id of the tournament whose matches are
                to be retrieved.
            group_id (UUID): The id of the group whose matches are to be
                retrieved.
            group_match_day (int): The match day whose matches are to be
                retrieved.
            round_id (UUID): The id of the round whose matches are to be
                retrieved.

        Returns:
            list[Match]: The stored matches.
        """
        return self.__service.get_matches(
            tournament_id,
            group_id,
            group_match_day,
            round_id
        )

    async def update_matches(
            self,
            tournament_id: UUID,
            matches: list[MatchUpdate]) -> list[Match]:
        """
        PUT /tournaments/{tournament_id}/matches endpoint to update existing
        matches.

        Args:
            tournament_id (UUID): The id of the tournament whose matches are
                to be updated.
            matches (list[MatchUpdate]): The matches to update.

        Returns:
            list[Match]: The newly updated matches.
        """
        return self.__service.update_matches(tournament_id, matches)

    async def get_match_by_id(

            self,
            tournament_id: UUID,
            match_id: UUID) -> Match:
        """
        GET /tournaments/{tournament_id}/matches/{match_id} endpoint to
        retrieve a single stored match by its id.

        Args:
            tournament_id (UUID): The id of the tournament the match belongs
                to.
            match_id (UUID): The id of the match to retrieve.

        Returns:
            Round: The retrieved match.
        """
        return self.__service.get_match_by_id(tournament_id, match_id)
