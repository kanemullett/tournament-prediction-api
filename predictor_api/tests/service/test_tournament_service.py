from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from db_handler.db_handler.model.column_definition import ColumnDefinition
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_definition import TableDefinition
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.sql_data_type import SqlDataType
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.service.tournament_service import (
    TournamentService
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)
from predictor_common.test_resources.assertions import Assertions


class TestTournamentService:

    __query_service: MagicMock = MagicMock()
    __table_service: MagicMock = MagicMock()

    __service: TournamentService = TournamentService(
        __query_service,
        __table_service
    )

    def setup_method(self):
        self.__query_service.retrieve_records.reset_mock()
        self.__query_service.retrieve_records.return_value = None
        self.__query_service.retrieve_records.side_effect = None

        self.__query_service.update_records.reset_mock()
        self.__query_service.update_records.return_value = None
        self.__query_service.update_records.side_effect = None

        self.__table_service.create_table.reset_mock()
        self.__table_service.create_table.return_value = None
        self.__table_service.create_table.side_effect = None

        self.__table_service.delete_table.reset_mock()
        self.__table_service.delete_table.return_value = None
        self.__table_service.delete_table.side_effect = None

    def test_should_return_tournaments(self):
        # Given
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=2,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "year": 2024,
                        "confederation": "UEFA"
                    },
                    {
                        "id": "6ee28143-1286-4618-a8b9-ad86d348ead1",
                        "year": 2026,
                        "confederation": None
                    }
                ]
            )
        )

        # When
        tournaments: list[Tournament] = self.__service.get_tournaments()

        # Then
        captured_args_retrieve_records, captured_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]
        table: Table = query_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            table.schema_
        )
        Assertions.assert_equals("tournaments", table.table)

        Assertions.assert_equals(2, len(tournaments))

        tournament1 = tournaments[0]
        Assertions.assert_type(Tournament, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals(2024, tournament1.year)
        Assertions.assert_equals(Confederation.UEFA, tournament1.confederation)

        tournament2 = tournaments[1]
        Assertions.assert_type(Tournament, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals(2026, tournament2.year)
        Assertions.assert_none(tournament2.confederation)

    def test_should_create_tournaments(self):
        # Given
        tournaments: list[Tournament] = [
            Tournament(
                id=UUID("34e1fae2-f630-4a7b-a813-8e692d443871"),
                year=2024,
                confederation=Confederation.UEFA
            ),
            Tournament(
                id=UUID("690d998a-14a5-4058-a6ab-25d1ddd86df5"),
                year=2022
            )
        ]

        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=2,
                records=[
                    {
                        "id": "34e1fae2-f630-4a7b-a813-8e692d443871",
                        "leagueTemplateId": None,
                        "knockoutTemplateId": None
                    },
                    {
                        "id": "690d998a-14a5-4058-a6ab-25d1ddd86df5",
                        "leagueTemplateId": None,
                        "knockoutTemplateId": None
                    }
                ]
            ),
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "groupCount": 8,
                    }
                ]
            ),
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "groupCount": 4,
                    }
                ]
            )
        ]

        # When
        created: list[Tournament] = (
            self.__service.create_tournaments(tournaments)
        )

        # Then
        captured_args_retrieve_records, captured_kwargs = (
            self.__query_service.update_records.call_args_list
        )[0]
        Assertions.assert_type(
            UpdateRequest,
            captured_args_retrieve_records[0]
        )

        update_request: UpdateRequest = captured_args_retrieve_records[0]
        Assertions.assert_equals(SqlOperator.INSERT, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            table.schema_
        )
        Assertions.assert_equals("tournaments", table.table)

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_type(UUID, record1["id"])
        Assertions.assert_equals(2024, record1["year"])
        Assertions.assert_equals(Confederation.UEFA, record1["confederation"])

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_type(UUID, record2["id"])
        Assertions.assert_equals(2022, record2["year"])
        Assertions.assert_none(record2["confederation"])

        Assertions.assert_equals(2, len(created))

        tournament1 = created[0]
        Assertions.assert_type(Tournament, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals(2024, tournament1.year)
        Assertions.assert_equals(Confederation.UEFA, tournament1.confederation)

        tournament2 = created[1]
        Assertions.assert_type(Tournament, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals(2022, tournament2.year)
        Assertions.assert_none(tournament2.confederation)

    def test_should_update_tournaments(self):
        # Given
        tournaments: list[Tournament] = [
            Tournament(
                id=UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
                confederation=Confederation.UEFA
            ),
            Tournament(
                id=UUID("023b3aa0-7f61-4331-8206-d75232f49ebc"),
                year=2022
            )
        ]

        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=2,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "year": 2024,
                        "confederation": "UEFA"
                    },
                    {
                        "id": "023b3aa0-7f61-4331-8206-d75232f49ebc",
                        "year": 2022,
                        "confederation": None
                    }
                ]
            )
        )

        # When
        updated: list[Tournament] = (
            self.__service.update_tournaments(tournaments)
        )

        # Then
        captured_args_update_records, captured_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, captured_args_update_records[0])

        update_request: UpdateRequest = captured_args_update_records[0]
        Assertions.assert_equals(SqlOperator.UPDATE, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            table.schema_
        )
        Assertions.assert_equals("tournaments", table.table)

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            record1["id"]
        )
        Assertions.assert_equals(Confederation.UEFA, record1["confederation"])

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_equals(
            UUID("023b3aa0-7f61-4331-8206-d75232f49ebc"),
            record2["id"]
        )
        Assertions.assert_equals(2022, record2["year"])

        captured_args_retrieve_records, captured_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]

        table: Table = query_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            table.schema_
        )
        Assertions.assert_equals("tournaments", table.table)

        condition: QueryCondition = query_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.IN, condition.operator)
        Assertions.assert_equals(
            [
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
                UUID("023b3aa0-7f61-4331-8206-d75232f49ebc")
            ],
            condition.value
        )

        Assertions.assert_equals(2, len(updated))

        tournament1 = updated[0]
        Assertions.assert_type(Tournament, tournament1)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            tournament1.id
        )
        Assertions.assert_equals(2024, tournament1.year)
        Assertions.assert_equals(Confederation.UEFA, tournament1.confederation)

        tournament2 = updated[1]
        Assertions.assert_type(Tournament, tournament2)
        Assertions.assert_equals(
            UUID("023b3aa0-7f61-4331-8206-d75232f49ebc"),
            tournament2.id
        )
        Assertions.assert_equals(2022, tournament2.year)
        Assertions.assert_none(tournament2.confederation)

    def test_should_return_tournament_by_id(self):
        # Given
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "year": 2024,
                        "confederation": "UEFA"
                    }
                ]
            )
        )

        # When
        tournament: Tournament = self.__service.get_tournament_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        )

        # Then
        captured_args_retrieve_records, captured_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]
        table: Table = query_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            table.schema_
        )
        Assertions.assert_equals("tournaments", table.table)

        condition: QueryCondition = query_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            condition.value
        )

        Assertions.assert_type(Tournament, tournament)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            tournament.id
        )
        Assertions.assert_equals(2024, tournament.year)
        Assertions.assert_equals(Confederation.UEFA, tournament.confederation)

    def test_should_raise_exception_if_tournament_not_found(self):
        # Given
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=0,
                records=[]
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_tournament_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )

    def test_should_delete_tournament_by_id(self):
        # When
        self.__service.delete_tournament_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        )

        # Then
        captured_args_update_records, captured_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, captured_args_update_records[0])

        update_request: UpdateRequest = captured_args_update_records[0]
        Assertions.assert_equals(SqlOperator.DELETE, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals(
            PredictorConstants.PREDICTOR_SCHEMA,
            table.schema_
        )
        Assertions.assert_equals("tournaments", table.table)

        condition: QueryCondition = update_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            condition.value
        )

    def test_should_create_tournament_tables_and_groups(self):
        # Given
        tournament: Tournament = Tournament(
            id=UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            name="Club World Cup",
            year=2025,
            templateId=UUID("e6689ab3-f234-4278-9718-713b4232034b")
        )

        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                        "leagueTemplateId": "69b7ef49-5c3a-4419-9dbb-"
                                            "b5beae71c6c8",
                        "knockoutTemplateId": "d930ce6a-eaed-47eb-9cf3-"
                                              "c6134b344714"
                    }
                ]
            ),
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "groupCount": 4,
                        "teamsPerGroup": 4,
                        "homeAndAway": False
                    }
                ]
            ),
            QueryResponse(
                referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
                recordCount=1,
                records=[
                    {
                        "rounds": [
                            {
                                "name": "Round of 16",
                                "teamCount": 16,
                                "roundOrder": 1,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Quarter-Finals",
                                "teamCount": 8,
                                "roundOrder": 2,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Semi-Finals",
                                "teamCount": 4,
                                "roundOrder": 3,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Third-Place Play-Off",
                                "teamCount": 2,
                                "roundOrder": 4,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            },
                            {
                                "name": "Final",
                                "teamCount": 2,
                                "roundOrder": 5,
                                "twoLegs": False,
                                "extraTime": True,
                                "awayGoals": False
                            }
                        ]
                    }
                ]
            )
        ]

        # When
        self.__service.create_tournaments([tournament])

        # Then
        matches_table_args, matches_table_kwargs = (
            self.__table_service.create_table.call_args_list
        )[0]
        Assertions.assert_type(TableDefinition, matches_table_args[0])

        matches_table_definition: TableDefinition = matches_table_args[0]
        Assertions.assert_equals("predictor", matches_table_definition.schema_)
        Assertions.assert_equals(
            "matches_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            matches_table_definition.table
        )

        Assertions.assert_equals(7, len(matches_table_definition.columns))

        matches_table_column1: ColumnDefinition = (
            matches_table_definition.columns
        )[0]
        Assertions.assert_equals("id", matches_table_column1.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            matches_table_column1.dataType
        )
        Assertions.assert_true(matches_table_column1.primaryKey)

        matches_table_column2: ColumnDefinition = (
            matches_table_definition.columns
        )[1]
        Assertions.assert_equals("homeTeamId", matches_table_column2.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            matches_table_column2.dataType
        )
        Assertions.assert_false(matches_table_column2.primaryKey)

        matches_table_column3: ColumnDefinition = (
            matches_table_definition.columns
        )[2]
        Assertions.assert_equals("awayTeamId", matches_table_column3.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            matches_table_column3.dataType
        )
        Assertions.assert_false(matches_table_column3.primaryKey)

        matches_table_column4: ColumnDefinition = (
            matches_table_definition.columns
        )[3]
        Assertions.assert_equals("kickoff", matches_table_column4.name)
        Assertions.assert_equals(
            SqlDataType.TIMESTAMP_WITHOUT_TIME_ZONE,
            matches_table_column4.dataType
        )
        Assertions.assert_false(matches_table_column4.primaryKey)

        matches_table_column5: ColumnDefinition = (
            matches_table_definition.columns
        )[4]
        Assertions.assert_equals("groupMatchDay", matches_table_column5.name)
        Assertions.assert_equals(
            SqlDataType.INTEGER,
            matches_table_column5.dataType
        )
        Assertions.assert_false(matches_table_column5.primaryKey)

        matches_table_column6: ColumnDefinition = (
            matches_table_definition.columns
        )[5]
        Assertions.assert_equals("groupId", matches_table_column6.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            matches_table_column6.dataType
        )
        Assertions.assert_false(matches_table_column6.primaryKey)

        matches_table_column7: ColumnDefinition = (
            matches_table_definition.columns
        )[6]
        Assertions.assert_equals("roundId", matches_table_column7.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            matches_table_column7.dataType
        )
        Assertions.assert_false(matches_table_column7.primaryKey)

        groups_table_args, groups_table_kwargs = (
            self.__table_service.create_table.call_args_list
        )[1]
        Assertions.assert_type(TableDefinition, groups_table_args[0])

        groups_table_definition: TableDefinition = groups_table_args[0]
        Assertions.assert_equals("predictor", groups_table_definition.schema_)
        Assertions.assert_equals(
            "groups_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            groups_table_definition.table
        )

        Assertions.assert_equals(2, len(groups_table_definition.columns))

        groups_table_column1: ColumnDefinition = (
            groups_table_definition.columns
        )[0]
        Assertions.assert_equals("id", groups_table_column1.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            groups_table_column1.dataType
        )
        Assertions.assert_true(groups_table_column1.primaryKey)

        groups_table_column2: ColumnDefinition = (
            groups_table_definition.columns
        )[1]
        Assertions.assert_equals("name", groups_table_column2.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            groups_table_column2.dataType
        )
        Assertions.assert_false(groups_table_column2.primaryKey)

        rounds_table_args, groups_update_kwargs = (
            self.__table_service.create_table.call_args_list
        )[2]
        Assertions.assert_type(TableDefinition, rounds_table_args[0])

        group_teams_table_definition: TableDefinition = (
            rounds_table_args
        )[0]
        Assertions.assert_equals(
            "predictor",
            group_teams_table_definition.schema_
        )
        Assertions.assert_equals(
            "group-teams_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            group_teams_table_definition.table
        )

        Assertions.assert_equals(2, len(group_teams_table_definition.columns))

        group_teams_table_column1: ColumnDefinition = (
            group_teams_table_definition.columns
        )[0]
        Assertions.assert_equals("groupId", group_teams_table_column1.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            group_teams_table_column1.dataType
        )
        Assertions.assert_false(group_teams_table_column1.primaryKey)

        group_teams_table_column2: ColumnDefinition = (
            group_teams_table_definition.columns
        )[1]
        Assertions.assert_equals("teamId", group_teams_table_column2.name)
        Assertions.assert_equals(
            SqlDataType.VARCHAR,
            group_teams_table_column2.dataType
        )
        Assertions.assert_false(group_teams_table_column2.primaryKey)

        rounds_table_args, groups_update_kwargs = (
            self.__query_service.update_records.call_args_list
        )[1]
        Assertions.assert_type(UpdateRequest, rounds_table_args[0])

        groups_update_request: UpdateRequest = rounds_table_args[0]
        Assertions.assert_equals(
            SqlOperator.INSERT,
            groups_update_request.operation
        )

        groups_update_table: Table = groups_update_request.table
        Assertions.assert_equals("predictor", groups_update_table.schema_)
        Assertions.assert_equals(
            "groups_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            groups_update_table.table
        )
        Assertions.assert_equals(4, len(groups_update_request.records))

        record1: dict[str, Any] = groups_update_request.records[0]
        Assertions.assert_type(UUID, record1["id"])
        Assertions.assert_equals("Group A", record1["name"])

        record2: dict[str, Any] = groups_update_request.records[1]
        Assertions.assert_type(UUID, record2["id"])
        Assertions.assert_equals("Group B", record2["name"])

        record3: dict[str, Any] = groups_update_request.records[2]
        Assertions.assert_type(UUID, record3["id"])
        Assertions.assert_equals("Group C", record3["name"])

        record4: dict[str, Any] = groups_update_request.records[3]
        Assertions.assert_type(UUID, record4["id"])
        Assertions.assert_equals("Group D", record4["name"])

        rounds_table_args, rounds_table_kwargs = (
            self.__table_service.create_table.call_args_list
        )[3]
        Assertions.assert_type(TableDefinition, rounds_table_args[0])

        rounds_definition: TableDefinition = rounds_table_args[0]
        Assertions.assert_equals("predictor", rounds_definition.schema_)
        Assertions.assert_equals(
            "rounds_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            rounds_definition.table
        )
        Assertions.assert_equals(7, len(rounds_definition.columns))

        column1: ColumnDefinition = rounds_definition.columns[0]
        Assertions.assert_equals("id", column1.name)
        Assertions.assert_equals(SqlDataType.VARCHAR, column1.dataType)
        Assertions.assert_true(column1.primaryKey)

        column2: ColumnDefinition = rounds_definition.columns[1]
        Assertions.assert_equals("name", column2.name)
        Assertions.assert_equals(SqlDataType.VARCHAR, column2.dataType)
        Assertions.assert_false(column2.primaryKey)

        column3: ColumnDefinition = rounds_definition.columns[2]
        Assertions.assert_equals("teamCount", column3.name)
        Assertions.assert_equals(SqlDataType.INTEGER, column3.dataType)
        Assertions.assert_false(column3.primaryKey)

        column4: ColumnDefinition = rounds_definition.columns[3]
        Assertions.assert_equals("roundOrder", column4.name)
        Assertions.assert_equals(SqlDataType.INTEGER, column4.dataType)
        Assertions.assert_false(column4.primaryKey)

        column5: ColumnDefinition = rounds_definition.columns[4]
        Assertions.assert_equals("twoLegs", column5.name)
        Assertions.assert_equals(SqlDataType.BOOLEAN, column5.dataType)
        Assertions.assert_false(column5.primaryKey)

        column6: ColumnDefinition = rounds_definition.columns[5]
        Assertions.assert_equals("extraTime", column6.name)
        Assertions.assert_equals(SqlDataType.BOOLEAN, column6.dataType)
        Assertions.assert_false(column6.primaryKey)

        column7: ColumnDefinition = rounds_definition.columns[6]
        Assertions.assert_equals("awayGoals", column7.name)
        Assertions.assert_equals(SqlDataType.BOOLEAN, column7.dataType)
        Assertions.assert_false(column7.primaryKey)

    def test_should_delete_tournament_tables(self):
        # When
        self.__service.delete_tournament_by_id(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        )

        # Then
        delete_matches_table_args, delete_matches_table_kwargs = (
            self.__table_service.delete_table.call_args_list
        )[0]
        Assertions.assert_type(Table, delete_matches_table_args[0])

        matches_table: Table = delete_matches_table_args[0]
        Assertions.assert_equals("predictor", matches_table.schema_)
        Assertions.assert_equals(
            "matches_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            matches_table.table
        )

        delete_groups_table_args, delete_groups_table_kwargs = (
            self.__table_service.delete_table.call_args_list
        )[1]
        Assertions.assert_type(Table, delete_groups_table_args[0])

        groups_table: Table = delete_groups_table_args[0]
        Assertions.assert_equals("predictor", groups_table.schema_)
        Assertions.assert_equals(
            "groups_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            groups_table.table
        )

        delete_group_teams_table_args, delete_group_teams_table_kwargs = (
            self.__table_service.delete_table.call_args_list
        )[2]
        Assertions.assert_type(Table, delete_group_teams_table_args[0])

        group_teams_table: Table = delete_group_teams_table_args[0]
        Assertions.assert_equals("predictor", group_teams_table.schema_)
        Assertions.assert_equals(
            "group-teams_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            group_teams_table.table
        )

        delete_rounds_table_args, delete_rounds_table_kwargs = (
            self.__table_service.delete_table.call_args_list
        )[3]
        Assertions.assert_type(Table, delete_rounds_table_args[0])

        rounds_table: Table = delete_rounds_table_args[0]
        Assertions.assert_equals("predictor", rounds_table.schema_)
        Assertions.assert_equals(
            "rounds_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
            rounds_table.table
        )
