from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.model.type.competition import Competition
from predictor_api.predictor_api.service.tournament_service import TournamentService
from predictor_api.predictor_api.util.predictor_constants import PredictorConstants
from predictor_common.test_resources.assertions import Assertions


class TestTournamentService:

    __database_query_service: MagicMock = MagicMock()

    __tournament_service: TournamentService = TournamentService(__database_query_service)

    def test_should_return_tournaments(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=2,
            records=[
                {
                    "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                    "year": 2024,
                    "competition": "EUROS"
                },
                {
                    "id": "6ee28143-1286-4618-a8b9-ad86d348ead1",
                    "year": 2026,
                    "competition": "WORLD_CUP"
                }
            ]
        )

        # When
        tournaments: list[Tournament] = self.__tournament_service.get_tournaments()

        # Then
        captured_args_retrieve_records, captured_kwargs = self.__database_query_service.retrieve_records.call_args
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]
        table: Table = query_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("tournaments", table.table)

        Assertions.assert_equals(2, len(tournaments))

        tournament1 = tournaments[0]
        Assertions.assert_type(Tournament, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals(2024, tournament1.year)
        Assertions.assert_equals(Competition.EUROS, tournament1.competition)

        tournament2 = tournaments[1]
        Assertions.assert_type(Tournament, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals(2026, tournament2.year)
        Assertions.assert_equals(Competition.WORLD_CUP, tournament2.competition)

    def test_should_create_tournaments(self):
        # Given
        tournaments: list[Tournament] = [
            Tournament(
                year=2024,
                competition=Competition.EUROS
            ),
            Tournament(
                year=2022,
                competition=Competition.WORLD_CUP
            )
        ]

        # When
        created: list[Tournament] = self.__tournament_service.create_tournaments(tournaments)

        # Then
        captured_args_retrieve_records, captured_kwargs = self.__database_query_service.update_records.call_args
        Assertions.assert_type(UpdateRequest, captured_args_retrieve_records[0])

        update_request: UpdateRequest = captured_args_retrieve_records[0]
        Assertions.assert_equals(SqlOperator.INSERT, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals(PredictorConstants.PREDICTOR_SCHEMA, table.schema_)
        Assertions.assert_equals("tournaments", table.table)

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_type(UUID, record1["id"])
        Assertions.assert_equals(2024, record1["year"])
        Assertions.assert_equals(Competition.EUROS, record1["competition"])

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_type(UUID, record2["id"])
        Assertions.assert_equals(2022, record2["year"])
        Assertions.assert_equals(Competition.WORLD_CUP, record2["competition"])

        Assertions.assert_equals(2, len(created))

        tournament1 = created[0]
        Assertions.assert_type(Tournament, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals(2024, tournament1.year)
        Assertions.assert_equals(Competition.EUROS, tournament1.competition)

        tournament2 = created[1]
        Assertions.assert_type(Tournament, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals(2022, tournament2.year)
        Assertions.assert_equals(Competition.WORLD_CUP, tournament2.competition)
