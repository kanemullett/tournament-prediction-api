from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.match import Match
from predictor_api.predictor_api.model.match_request import MatchRequest
from predictor_api.predictor_api.service.match_service import MatchService


class MatchController:

    def __init__(self, match_service: MatchService):
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

    async def get_matches(
            self,
            tournament_id: UUID,
            group_id: UUID = None,
            group_match_day: int = None,
            round_id: UUID = None) -> list[Match]:
        return self.__service.get_matches(
            tournament_id,
            group_id,
            group_match_day,
            round_id
        )

    async def update_matches(
            self,
            tournament_id: UUID,
            matches: list[MatchRequest]) -> list[Match]:
        return self.__service.update_matches(tournament_id, matches)
