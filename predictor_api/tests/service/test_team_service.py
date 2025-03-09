from unittest.mock import MagicMock
from uuid import UUID

from db_handler.db_handler.model.order_by import OrderBy
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.order_direction import OrderDirection
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.service.team_service import TeamService
from predictor_common.test_resources.assertions import Assertions


class TestTeamService:

    __database_query_service: MagicMock = MagicMock()

    __service: TeamService = TeamService(__database_query_service)

    def test_returns_all_teams_with_no_parameters(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=3,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "name": "Bosnia & Herzegovina",
                        "imagePath": "BIH.png",
                        "confederation": "UEFA"
                    },
                    {
                        "id": "6ee28143-1286-4618-a8b9-ad86d348ead1",
                        "name": "Botswana",
                        "imagePath": "BOT.png",
                        "confederation": "CAF"
                    },
                    {
                        "id": "e107d069-b277-4902-bdad-7091a494a8b3",
                        "name": "England",
                        "imagePath": "ENG.png",
                        "confederation": "UEFA"
                    }
                ]
            )
        )

        # When
        teams: list[Team] = self.__service.get_teams(
            None,
            None
        )

        # Then
        teams_args, teams_kwargs = (
            self.__database_query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, teams_args[0])

        request: QueryRequest = teams_args[0]
        Assertions.assert_none(request.conditionGroup)

        table: Table = request.table
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("teams", table.table)

        order_by: OrderBy = request.orderBy
        Assertions.assert_equals(["name"], order_by.column.parts)
        Assertions.assert_equals(OrderDirection.ASC, order_by.direction)

        Assertions.assert_equals(3, len(teams))

        team1: Team = teams[0]
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            team1.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", team1.name)
        Assertions.assert_equals("BIH.png", team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team1.confederation)

        team2: Team = teams[1]
        Assertions.assert_equals(
            UUID("6ee28143-1286-4618-a8b9-ad86d348ead1"),
            team2.id
        )
        Assertions.assert_equals("Botswana", team2.name)
        Assertions.assert_equals("BOT.png", team2.imagePath)
        Assertions.assert_equals(Confederation.CAF, team2.confederation)

        team3: Team = teams[2]
        Assertions.assert_equals(
            UUID("e107d069-b277-4902-bdad-7091a494a8b3"),
            team3.id
        )
        Assertions.assert_equals("England", team3.name)
        Assertions.assert_equals("ENG.png", team3.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team3.confederation)

    def test_returns_teams_in_confederation(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=2,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "name": "Bosnia & Herzegovina",
                        "imagePath": "BIH.png",
                        "confederation": "UEFA"
                    },
                    {
                        "id": "e107d069-b277-4902-bdad-7091a494a8b3",
                        "name": "England",
                        "imagePath": "ENG.png",
                        "confederation": "UEFA"
                    }
                ]
            )
        )

        # When
        teams: list[Team] = self.__service.get_teams(
            Confederation.UEFA,
            None
        )

        # Then
        teams_args, teams_kwargs = (
            self.__database_query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, teams_args[0])

        request: QueryRequest = teams_args[0]

        table: Table = request.table
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("teams", table.table)

        Assertions.assert_equals(1, len(request.conditionGroup.conditions))

        condition: QueryCondition = request.conditionGroup.conditions[0]
        Assertions.assert_equals(["confederation"], condition.column.parts)
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(Confederation.UEFA, condition.value)

        order_by: OrderBy = request.orderBy
        Assertions.assert_equals(["name"], order_by.column.parts)
        Assertions.assert_equals(OrderDirection.ASC, order_by.direction)

        Assertions.assert_equals(2, len(teams))

        team1: Team = teams[0]
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            team1.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", team1.name)
        Assertions.assert_equals("BIH.png", team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team1.confederation)

        team2: Team = teams[1]
        Assertions.assert_equals(
            UUID("e107d069-b277-4902-bdad-7091a494a8b3"),
            team2.id
        )
        Assertions.assert_equals("England", team2.name)
        Assertions.assert_equals("ENG.png", team2.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team2.confederation)
