from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.competition import Competition
from predictor_api.predictor_api.service.competition_service import (
    CompetitionService
)


class CompetitionController:

    def __init__(self, competition_service: CompetitionService):
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

    async def get_competitions(self) -> list[Competition]:
        return self.__service.get_competitions()

    async def create_competitions(
            self,
            competitions: list[Competition]) -> list[Competition]:
        return self.__service.create_competitions(competitions)

    async def update_competitions(
            self,
            competitions: list[Competition]) -> list[Competition]:
        return self.__service.update_competitions(competitions)

    async def get_competition_by_id(self, competition_id: UUID) -> Competition:
        return self.__service.get_competition_by_id(competition_id)
