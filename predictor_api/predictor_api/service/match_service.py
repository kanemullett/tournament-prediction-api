from uuid import UUID

from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from predictor_api.predictor_api.model.match import Match
from predictor_api.predictor_api.service.tournament_service import (
    TournamentService
)


class MatchService:

    def __init__(
            self,
            database_query_service: DatabaseQueryService,
            tournament_service: TournamentService) -> None:
        self.__query_service = database_query_service
        self.__tournament_service = tournament_service

    def get_matches(
            self,
            tournament_id: UUID,
            group_id: UUID = None,
            group_match_day: int = None,
            round_id: UUID = None) -> list[Match]:
        self.__tournament_service.get_tournament_by_id(tournament_id)

        return []
