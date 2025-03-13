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

    async def get_competitions(self) -> list[Competition]:
        return self.__service.get_competitions()

    async def create_competitions(
            self,
            competitions: list[Competition]) -> list[Competition]:
        return self.__service.create_competitions(competitions)
