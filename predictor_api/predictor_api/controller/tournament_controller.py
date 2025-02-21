from fastapi import APIRouter

from db_handler.db_handler.model.query_response import QueryResponse
from predictor_api.predictor_api.service.tournament_service import TournamentService


class TournamentController:

    def __init__(self, tournament_service: TournamentService) -> None:
        self.router: APIRouter = APIRouter(prefix="/tournaments", tags=["Tournaments"])
        self.__tournament_service = tournament_service

        self.router.add_api_route("/", self.get_tournaments, methods=["GET"])

    async def get_tournaments(self) -> QueryResponse:
        return self.__tournament_service.get_tournaments()
