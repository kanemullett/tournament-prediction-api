from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.service.tournament_service import TournamentService


class TournamentController:

    def __init__(self, tournament_service: TournamentService) -> None:
        self.router: APIRouter = APIRouter(prefix="/tournaments", tags=["Tournaments"])
        self.__tournament_service = tournament_service

        self.router.add_api_route("/", self.get_tournaments, methods=["GET"])
        self.router.add_api_route("/", self.create_tournaments, methods=["POST"])
        self.router.add_api_route("/{tournament_id}", self.get_tournament_by_id, methods=["GET"])

    async def get_tournaments(self) -> list[Tournament]:
        return self.__tournament_service.get_tournaments()

    async def create_tournaments(self, tournaments: list[Tournament]) -> list[Tournament]:
        return self.__tournament_service.create_tournaments(tournaments)

    async def get_tournament_by_id(self, tournament_id: UUID) -> Tournament:
        return self.__tournament_service.get_tournament_by_id(tournament_id)
