from typing import Any
from fastapi import APIRouter

from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.service.database_query_service import DatabaseQueryService


class TournamentController:

    def __init__(self, database_query_service: DatabaseQueryService) -> None:
        self.router: APIRouter = APIRouter(prefix="/tournaments", tags=["Tournaments"])
        self.__database_query_service = database_query_service

        self.router.add_api_route("/", self.get_tournaments, methods=["GET"])

    async def get_tournaments(self) -> QueryResponse:
        return self.__database_query_service.retrieve_records(
            QueryRequest(
                table=Table(
                    schema="predictor",
                    table="test2"
                )
            )
        )
