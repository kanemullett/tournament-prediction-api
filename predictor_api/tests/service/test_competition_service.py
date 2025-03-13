from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from predictor_api.predictor_api.model.competition import Competition
from predictor_api.predictor_api.service.competition_service import (
    CompetitionService
)
from predictor_common.test_resources.assertions import Assertions


class TestCompetitionService:

    __query_service: MagicMock = MagicMock()

    __service: CompetitionService = CompetitionService(
        __query_service
    )

    def test_should_return_competitions(self):
        # Given
        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId=UUID("90a6637a-e534-46bd-8715-33c6f2afdd7a"),
            recordCount=2,
            records=[
                {
                    "id": "71d14fb4-ba29-47f7-a235-d2675028d700",
                    "name": "The Boys",
                    "tournamentId": "72ed614f-06a3-41b4-9d50-52e1f8fd9e58"
                },
                {
                    "id": "4cb9e47c-722d-4de0-b63a-ee5f9b9f2900",
                    "name": "Meine Familie",
                    "tournamentId": "72ed614f-06a3-41b4-9d50-52e1f8fd9e58"
                }
            ]
        )

        # When
        competitions: list[Competition] = self.__service.get_competitions()

        # Then
        competitions_args, competitions_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, competitions_args[0])

        request: QueryRequest = competitions_args[0]
        request_table: Table = request.table
        Assertions.assert_equals("predictor", request_table.schema_)
        Assertions.assert_equals("competitions", request_table.table)

        Assertions.assert_equals(2, len(competitions))

        competition1: Competition = competitions[0]
        Assertions.assert_equals(
            UUID("71d14fb4-ba29-47f7-a235-d2675028d700"),
            competition1.id
        )
        Assertions.assert_equals("The Boys", competition1.name)
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            competition1.tournamentId
        )

        competition2: Competition = competitions[1]
        Assertions.assert_equals(
            UUID("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900"),
            competition2.id
        )
        Assertions.assert_equals("Meine Familie", competition2.name)
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            competition2.tournamentId
        )

    def test_should_create_competitions(self):
        # Given
        competitions: list[Competition] = [
            Competition(
                name="The Boys",
                tournamentId=UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
            ),
            Competition(
                name="Meine Familie",
                tournamentId=UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
            )
        ]

        # When
        created: list[Competition] = self.__service.create_competitions(
            competitions
        )

        # Then
        competitions_args, competitions_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, competitions_args[0])

        request: UpdateRequest = competitions_args[0]
        Assertions.assert_equals(SqlOperator.INSERT, request.operation)

        request_table: Table = request.table
        Assertions.assert_equals("predictor", request_table.schema_)
        Assertions.assert_equals("competitions", request_table.table)

        Assertions.assert_equals(2, len(request.records))

        record1: dict[str, Any] = request.records[0]
        Assertions.assert_type(UUID, record1["id"])
        Assertions.assert_equals("The Boys", record1["name"])
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            record1["tournamentId"]
        )

        record2: dict[str, Any] = request.records[1]
        Assertions.assert_type(UUID, record2["id"])
        Assertions.assert_equals("Meine Familie", record2["name"])
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            record2["tournamentId"]
        )

        Assertions.assert_equals(2, len(created))

        competition1: Competition = created[0]
        Assertions.assert_type(UUID, competition1.id)
        Assertions.assert_equals("The Boys", competition1.name)
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            competition1.tournamentId
        )

        competition2: Competition = created[1]
        Assertions.assert_type(UUID, competition2.id)
        Assertions.assert_equals("Meine Familie", competition2.name)
        Assertions.assert_equals(
            UUID("72ed614f-06a3-41b4-9d50-52e1f8fd9e58"),
            competition2.tournamentId
        )
