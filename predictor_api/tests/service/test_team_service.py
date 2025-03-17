from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.order_by import OrderBy
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_join import QueryJoin
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.sql_query import SqlQuery
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.join_type import JoinType
from db_handler.db_handler.model.type.order_direction import OrderDirection
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
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

        order_by: OrderBy = request.orderBy[0]
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

        order_by: OrderBy = request.orderBy[0]
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

    def test_returns_teams_in_tournament(self):
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
            None,
            UUID("7a5d1149-7be0-4cdd-a651-e54ee8cd4051")
        )

        # Then
        teams_args, teams_kwargs = (
            self.__database_query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, teams_args[0])

        request: QueryRequest = teams_args[0]
        Assertions.assert_true(request.distinct)
        Assertions.assert_equals(4, len(request.columns))

        column1: Column = request.columns[0]
        Assertions.assert_equals(["team", "id"], column1.parts)

        column2: Column = request.columns[1]
        Assertions.assert_equals(["team", "name"], column2.parts)

        column3: Column = request.columns[2]
        Assertions.assert_equals(["team", "imagePath"], column3.parts)

        column4: Column = request.columns[3]
        Assertions.assert_equals(["team", "confederation"], column4.parts)

        table: Table = request.table
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("teams", table.table)
        Assertions.assert_equals("team", table.alias)

        Assertions.assert_equals(1, len(request.joins))
        Assertions.assert_type(QueryJoin, request.joins[0])

        query_join: QueryJoin = request.joins[0]
        Assertions.assert_equals("teamIds", query_join.alias)
        Assertions.assert_equals(JoinType.INNER, query_join.joinType)

        join_query: SqlQuery = query_join.query
        Assertions.assert_true(join_query.distinct)
        Assertions.assert_equals(1, len(join_query.columns))

        join_query_column: Column = join_query.columns[0]
        Assertions.assert_equals(["teamId"], join_query_column.parts)

        join_query_table: Table = join_query.table
        Assertions.assert_equals("predictor", join_query_table.schema_)
        Assertions.assert_equals(
            "group-teams_7a5d1149-7be0-4cdd-a651-e54ee8cd4051",
            join_query_table.table
        )

        Assertions.assert_equals(2, len(join_query.joins))
        Assertions.assert_type(QueryJoin, join_query.joins[0])

        join_query_join1: QueryJoin = join_query.joins[0]
        Assertions.assert_equals(JoinType.UNION, join_query_join1.joinType)

        join_query_join1_query: SqlQuery = join_query_join1.query
        Assertions.assert_true(join_query_join1_query.distinct)
        Assertions.assert_equals(1, len(join_query_join1_query.columns))

        join_query_join1_query_column: Column = (
            join_query_join1_query.columns
        )[0]
        Assertions.assert_equals(
            ["homeTeamId"],
            join_query_join1_query_column.parts
        )

        join_query_join1_query_table: Table = join_query_join1_query.table
        Assertions.assert_equals(
            "predictor",
            join_query_join1_query_table.schema_
        )
        Assertions.assert_equals(
            "matches_7a5d1149-7be0-4cdd-a651-e54ee8cd4051",
            join_query_join1_query_table.table
        )

        Assertions.assert_type(QueryJoin, join_query.joins[1])

        join_query_join1: QueryJoin = join_query.joins[1]
        Assertions.assert_equals(JoinType.UNION, join_query_join1.joinType)

        join_query_join1_query: SqlQuery = join_query_join1.query
        Assertions.assert_true(join_query_join1_query.distinct)
        Assertions.assert_equals(1, len(join_query_join1_query.columns))

        join_query_join1_query_column: Column = (
            join_query_join1_query.columns
        )[0]
        Assertions.assert_equals(
            ["awayTeamId"],
            join_query_join1_query_column.parts
        )

        join_query_join1_query_table: Table = join_query_join1_query.table
        Assertions.assert_equals(
            "predictor",
            join_query_join1_query_table.schema_
        )
        Assertions.assert_equals(
            "matches_7a5d1149-7be0-4cdd-a651-e54ee8cd4051",
            join_query_join1_query_table.table
        )

        query_join_condition: QueryCondition = query_join.joinCondition
        Assertions.assert_equals(
            ["team", "id"],
            query_join_condition.column.parts
        )
        Assertions.assert_equals(
            ["teamIds", "teamId"],
            query_join_condition.value.parts
        )

        Assertions.assert_none(request.conditionGroup)
        Assertions.assert_equals(1, len(request.orderBy))

        order_by: OrderBy = request.orderBy[0]
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

    def test_creates_new_teams(self):
        # Given
        teams: list[Team] = [
            Team(
                name="Bosnia & Herzegovina",
                imagePath="BIH.png",
                confederation=Confederation.UEFA
            ),
            Team(
                name="Botswana",
                imagePath="BOT.png",
                confederation=Confederation.CAF
            )
        ]

        # When
        created: list[Team] = self.__service.create_teams(teams)

        # Then
        teams_args, teams_kwargs = (
            self.__database_query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, teams_args[0])

        request: UpdateRequest = teams_args[0]
        Assertions.assert_equals(SqlOperator.INSERT, request.operation)

        table: Table = request.table
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("teams", table.table)

        Assertions.assert_equals(2, len(request.records))

        record1: dict[str, Any] = request.records[0]
        Assertions.assert_type(UUID, record1["id"])
        Assertions.assert_equals("Bosnia & Herzegovina", record1["name"])
        Assertions.assert_equals("BIH.png", record1["imagePath"])
        Assertions.assert_equals(Confederation.UEFA, record1["confederation"])

        record2: dict[str, Any] = request.records[1]
        Assertions.assert_type(UUID, record2["id"])
        Assertions.assert_equals("Botswana", record2["name"])
        Assertions.assert_equals("BOT.png", record2["imagePath"])
        Assertions.assert_equals(Confederation.CAF, record2["confederation"])

        Assertions.assert_equals(2, len(created))

        team1: Team = created[0]
        Assertions.assert_type(UUID, team1.id)
        Assertions.assert_equals("Bosnia & Herzegovina", team1.name)
        Assertions.assert_equals("BIH.png", team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team1.confederation)

        team2: Team = created[1]
        Assertions.assert_type(UUID, team2.id)
        Assertions.assert_equals("Botswana", team2.name)
        Assertions.assert_equals("BOT.png", team2.imagePath)
        Assertions.assert_equals(Confederation.CAF, team2.confederation)

    def test_updates_existing_teams(self):
        # Given
        teams: list[Team] = [
            Team(
                id=UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
                confederation=Confederation.UEFA
            ),
            Team(
                id=UUID("6ee28143-1286-4618-a8b9-ad86d348ead1"),
                imagePath="BOT.png"
            )
        ]

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
                        "id": "6ee28143-1286-4618-a8b9-ad86d348ead1",
                        "name": "Botswana",
                        "imagePath": "BOT.png",
                        "confederation": "CAF"
                    }
                ]
            )
        )

        # When
        updated: list[Team] = self.__service.update_teams(teams)

        # Then
        update_teams_args, update_teams_kwargs = (
            self.__database_query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, update_teams_args[0])

        update_request: UpdateRequest = update_teams_args[0]
        Assertions.assert_equals(SqlOperator.UPDATE, update_request.operation)

        update_table: Table = update_request.table
        Assertions.assert_equals("predictor", update_table.schema_)
        Assertions.assert_equals("teams", update_table.table)

        Assertions.assert_equals(2, len(update_request.records))

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            record1["id"]
        )
        Assertions.assert_equals(Confederation.UEFA, record1["confederation"])

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_equals(
            UUID("6ee28143-1286-4618-a8b9-ad86d348ead1"),
            record2["id"]
        )
        Assertions.assert_equals("BOT.png", record2["imagePath"])

        get_teams_args, get_teams_kwargs = (
            self.__database_query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, get_teams_args[0])

        query_request: QueryRequest = get_teams_args[0]

        query_table: Table = query_request.table
        Assertions.assert_equals("predictor", query_table.schema_)
        Assertions.assert_equals("teams", query_table.table)

        Assertions.assert_equals(
            1,
            len(query_request.conditionGroup.conditions)
        )

        query_condition: QueryCondition = (
            query_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["id"], query_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.IN,
            query_condition.operator
        )
        Assertions.assert_equals(
            [
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
                UUID("6ee28143-1286-4618-a8b9-ad86d348ead1")
            ],
            query_condition.value
        )

        query_order_by: OrderBy = query_request.orderBy[0]
        Assertions.assert_equals(["name"], query_order_by.column.parts)
        Assertions.assert_equals(OrderDirection.ASC, query_order_by.direction)

        Assertions.assert_equals(2, len(updated))

        team1: Team = updated[0]
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            team1.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", team1.name)
        Assertions.assert_equals("BIH.png", team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team1.confederation)

        team2: Team = updated[1]
        Assertions.assert_equals(
            UUID("6ee28143-1286-4618-a8b9-ad86d348ead1"),
            team2.id
        )
        Assertions.assert_equals("Botswana", team2.name)
        Assertions.assert_equals("BOT.png", team2.imagePath)
        Assertions.assert_equals(Confederation.CAF, team2.confederation)

    def test_returns_team_by_id(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "name": "Bosnia & Herzegovina",
                        "imagePath": "BIH.png",
                        "confederation": "UEFA"
                    }
                ]
            )
        )

        # When
        team: Team = self.__service.get_team_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
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
        Assertions.assert_equals(["id"], condition.column.parts)
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            condition.value
        )

        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            team.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", team.name)
        Assertions.assert_equals("BIH.png", team.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team.confederation)

    def test_should_raise_exception_if_team_not_found(self):
        # Given
        self.__database_query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=0,
                records=[]
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_team_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No teams found with a matching id.",
            httpe.value.detail
        )

    def test_should_delete_team_by_id(self):
        # When
        self.__service.delete_team_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        )

        # Then
        delete_args, delete_kwargs = (
            self.__database_query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, delete_args[0])

        update_request: UpdateRequest = delete_args[0]
        Assertions.assert_equals(SqlOperator.DELETE, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("teams", table.table)

        condition: QueryCondition = update_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            condition.value
        )
