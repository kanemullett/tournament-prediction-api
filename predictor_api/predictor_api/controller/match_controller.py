from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.match import Match
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
                            "examples": {
                                "tournamentNotFound": {
                                    "summary": "Tournament not found",
                                    "value": {
                                        "detail": "No tournaments found with "
                                                  "a matching id."
                                    }
                                },
                                "noGroupStage": {
                                    "summary": "Tournament has no group stage",
                                    "value": {
                                        "detail": "The tournament with the "
                                                  "supplied id does not have "
                                                  "a group stage."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )

    def get_matches(
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
