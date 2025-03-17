from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.type.join_type import JoinType
from db_handler.db_handler.model.update_request import UpdateRequest
from predictor_api.predictor_api.model.round_template import RoundTemplate
from predictor_api.predictor_api.model.knockout_template import (
    KnockoutTemplate
)
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament_template import (
    TournamentTemplate
)
from predictor_api.predictor_api.model.tournament_template_request import (
    TournamentTemplateRequest
)
from predictor_api.predictor_api.service.tournament_template_service import (
    TournamentTemplateService
)
from predictor_common.test_resources.assertions import Assertions


class TestTournamentTemplateService:
    __query_service: MagicMock = MagicMock()
    __knock_temp_service: MagicMock = MagicMock()

    __service: TournamentTemplateService = (
        TournamentTemplateService(__query_service, __knock_temp_service)
    )

    def setup_method(self):
        self.__query_service.retrieve_records.reset_mock()
        self.__query_service.retrieve_records.return_value = None
        self.__query_service.retrieve_records.side_effect = None

        self.__knock_temp_service.get_knockout_template_by_id.reset_mock()
        self.__knock_temp_service.get_knockout_template_by_id.return_value = \
            None
        self.__knock_temp_service.get_knockout_template_by_id.side_effect = \
            None

    def test_should_return_tournament_templates_with_child_templates(self):
        # Given
        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=3,
            records=[
                {
                    "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                    "tournamentName": "tournament1",
                    "leagueId": None,
                    "leagueName": None,
                    "groupCount": None,
                    "teamsPerGroup": None,
                    "homeAndAway": None,
                    "knockoutTemplateId": "80e9c164-637d-400f-a3cf-"
                                          "bf922073bc9b"
                },
                {
                    "id": "6ee28143-1286-4618-a8b9-ad86d348ead1",
                    "tournamentName": "tournament2",
                    "leagueId": "0ca3adf1-f5a5-43e9-9c82-5619340739be",
                    "leagueName": "league1",
                    "groupCount": 8,
                    "teamsPerGroup": 4,
                    "homeAndAway": True,
                    "knockoutTemplateId": None
                },
                {
                    "id": "d15956ef-d199-40b1-b7d7-850a9add97e7",
                    "tournamentName": "tournament3",
                    "leagueId": "508c8b55-2e0c-415b-8078-2dcb2065c7ca",
                    "leagueName": "league2",
                    "groupCount": 6,
                    "teamsPerGroup": 4,
                    "homeAndAway": False,
                    "knockoutTemplateId": "1a4d1cc8-f035-439a-b274-"
                                          "fe739b8fcfa5"
                }
            ]
        )

        self.__knock_temp_service.get_knockout_template_by_id.side_effect = [
            KnockoutTemplate(
                id=UUID("80e9c164-637d-400f-a3cf-bf922073bc9b"),
                name="knockout1",
                rounds=[
                    RoundTemplate(
                        name="round1",
                        teamCount=4,
                        roundOrder=1,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    RoundTemplate(
                        name="round2",
                        teamCount=2,
                        roundOrder=2,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            ),
            KnockoutTemplate(
                id=UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"),
                name="knockout2",
                rounds=[
                    RoundTemplate(
                        name="round3",
                        teamCount=4,
                        roundOrder=1,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    RoundTemplate(
                        name="round4",
                        teamCount=2,
                        roundOrder=2,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            )
        ]

        # When
        tournament_templates: list[TournamentTemplate] = (
            self.__service.get_tournament_templates()
        )

        # Then
        captured_args_retrieve_records, captured_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]

        columns: list[Column] = query_request.columns
        Assertions.assert_equals(8, len(columns))

        column1: Column = columns[0]
        Assertions.assert_equals(["tourn", "id"], column1.parts)

        column2: Column = columns[1]
        Assertions.assert_equals(["tourn", "name"], column2.parts)
        Assertions.assert_equals("tournamentName", column2.alias)

        column3: Column = columns[2]
        Assertions.assert_equals(
            ["tourn", "knockoutTemplateId"],
            column3.parts
        )

        column4: Column = columns[3]
        Assertions.assert_equals(["league", "id"], column4.parts)
        Assertions.assert_equals("leagueId", column4.alias)

        column5: Column = columns[4]
        Assertions.assert_equals(["league", "name"], column5.parts)
        Assertions.assert_equals("leagueName", column5.alias)

        column6: Column = columns[5]
        Assertions.assert_equals(["league", "groupCount"], column6.parts)

        column7: Column = columns[6]
        Assertions.assert_equals(["league", "teamsPerGroup"], column7.parts)

        column8: Column = columns[7]
        Assertions.assert_equals(["league", "homeAndAway"], column8.parts)

        table: Table = query_request.table
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("tournament-templates", table.table)
        Assertions.assert_equals("tourn", table.alias)

        table_joins: list[TableJoin] = query_request.joins
        Assertions.assert_equals(1, len(table_joins))

        join1: TableJoin = table_joins[0]
        Assertions.assert_equals(JoinType.LEFT, join1.joinType)

        join1_table: Table = join1.table
        Assertions.assert_equals("predictor", join1_table.schema_)
        Assertions.assert_equals("league-templates", join1_table.table)
        Assertions.assert_equals("league", join1_table.alias)

        join1_condition: QueryCondition = join1.joinCondition
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            join1_condition.operator
        )

        join1_column: Column = join1_condition.column
        Assertions.assert_equals(
            ["tourn", "leagueTemplateId"],
            join1_column.parts
        )

        join1_value: Column = join1_condition.value
        Assertions.assert_equals(["league", "id"], join1_value.parts)

        Assertions.assert_equals(3, len(tournament_templates))

        tournament1: TournamentTemplate = tournament_templates[0]
        Assertions.assert_type(TournamentTemplate, tournament1)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            tournament1.id
        )
        Assertions.assert_equals("tournament1", tournament1.name)
        Assertions.assert_none(tournament1.league)

        knockout1: KnockoutTemplate = tournament1.knockout
        Assertions.assert_type(KnockoutTemplate, knockout1)
        Assertions.assert_equals(
            UUID("80e9c164-637d-400f-a3cf-bf922073bc9b"),
            knockout1.id
        )
        Assertions.assert_equals("knockout1", knockout1.name)
        Assertions.assert_equals(2, len(knockout1.rounds))

        knockout1_round1: RoundTemplate = knockout1.rounds[0]
        Assertions.assert_equals("round1", knockout1_round1.name)
        Assertions.assert_equals(4, knockout1_round1.teamCount)
        Assertions.assert_equals(1, knockout1_round1.roundOrder)
        Assertions.assert_true(knockout1_round1.twoLegs)
        Assertions.assert_true(knockout1_round1.extraTime)
        Assertions.assert_true(knockout1_round1.awayGoals)

        knockout1_round2: RoundTemplate = knockout1.rounds[1]
        Assertions.assert_equals("round2", knockout1_round2.name)
        Assertions.assert_equals(2, knockout1_round2.teamCount)
        Assertions.assert_equals(2, knockout1_round2.roundOrder)
        Assertions.assert_false(knockout1_round2.twoLegs)
        Assertions.assert_true(knockout1_round2.extraTime)
        Assertions.assert_false(knockout1_round2.awayGoals)

        tournament2: TournamentTemplate = tournament_templates[1]
        Assertions.assert_type(TournamentTemplate, tournament2)
        Assertions.assert_equals(
            UUID("6ee28143-1286-4618-a8b9-ad86d348ead1"),
            tournament2.id
        )
        Assertions.assert_equals("tournament2", tournament2.name)
        Assertions.assert_none(tournament2.knockout)

        league1: LeagueTemplate = tournament2.league
        Assertions.assert_equals(
            UUID("0ca3adf1-f5a5-43e9-9c82-5619340739be"),
            league1.id
        )
        Assertions.assert_equals("league1", league1.name)
        Assertions.assert_equals(8, league1.groupCount)
        Assertions.assert_equals(4, league1.teamsPerGroup)
        Assertions.assert_true(league1.homeAndAway)

        tournament3: TournamentTemplate = tournament_templates[2]
        Assertions.assert_type(TournamentTemplate, tournament3)
        Assertions.assert_equals(
            UUID("d15956ef-d199-40b1-b7d7-850a9add97e7"),
            tournament3.id
        )
        Assertions.assert_equals("tournament3", tournament3.name)

        league2: LeagueTemplate = tournament3.league
        Assertions.assert_equals(
            UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"),
            league2.id
        )
        Assertions.assert_equals("league2", league2.name)
        Assertions.assert_equals(6, league2.groupCount)
        Assertions.assert_equals(4, league2.teamsPerGroup)
        Assertions.assert_false(league2.homeAndAway)

        knockout2: KnockoutTemplate = tournament3.knockout
        Assertions.assert_type(KnockoutTemplate, knockout2)
        Assertions.assert_equals(
            UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"),
            knockout2.id
        )
        Assertions.assert_equals("knockout2", knockout2.name)
        Assertions.assert_equals(2, len(knockout2.rounds))

        knockout2_round1: RoundTemplate = knockout2.rounds[0]
        Assertions.assert_equals("round3", knockout2_round1.name)
        Assertions.assert_equals(4, knockout2_round1.teamCount)
        Assertions.assert_equals(1, knockout2_round1.roundOrder)
        Assertions.assert_true(knockout2_round1.twoLegs)
        Assertions.assert_true(knockout2_round1.extraTime)
        Assertions.assert_true(knockout2_round1.awayGoals)

        knockout2_round2: RoundTemplate = knockout2.rounds[1]
        Assertions.assert_equals("round4", knockout2_round2.name)
        Assertions.assert_equals(2, knockout2_round2.teamCount)
        Assertions.assert_equals(2, knockout2_round2.roundOrder)
        Assertions.assert_false(knockout2_round2.twoLegs)
        Assertions.assert_true(knockout2_round2.extraTime)
        Assertions.assert_false(knockout2_round2.awayGoals)

    def test_should_create_tournament_templates(self):
        # Given
        templates: list[TournamentTemplateRequest] = [
            TournamentTemplateRequest(
                name="tournament1",
                knockoutTemplateId=UUID("80e9c164-637d-400f-a3cf-bf922073bc9b")
            ),
            TournamentTemplateRequest(
                name="tournament2",
                leagueTemplateId=UUID("0ca3adf1-f5a5-43e9-9c82-5619340739be")
            ),
            TournamentTemplateRequest(
                name="tournament3",
                leagueTemplateId=UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"),
                knockoutTemplateId=UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5")
            )
        ]

        self.__knock_temp_service.get_knockout_template_by_id.side_effect = [
            KnockoutTemplate(
                id=UUID("80e9c164-637d-400f-a3cf-bf922073bc9b"),
                name="knockout1",
                rounds=[
                    RoundTemplate(
                        name="round1",
                        teamCount=4,
                        roundOrder=1,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    RoundTemplate(
                        name="round2",
                        teamCount=2,
                        roundOrder=2,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            ),
            KnockoutTemplate(
                id=UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"),
                name="knockout2",
                rounds=[
                    RoundTemplate(
                        name="round3",
                        teamCount=4,
                        roundOrder=1,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    RoundTemplate(
                        name="round4",
                        teamCount=2,
                        roundOrder=2,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            )
        ]

        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=3,
            records=[
                {
                    "id": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                    "tournamentName": "tournament1",
                    "leagueId": None,
                    "leagueName": None,
                    "groupCount": None,
                    "teamsPerGroup": None,
                    "homeAndAway": None,
                    "knockoutTemplateId": "80e9c164-637d-400f-a3cf-"
                                          "bf922073bc9b"
                },
                {
                    "id": "6ee28143-1286-4618-a8b9-ad86d348ead1",
                    "tournamentName": "tournament2",
                    "leagueId": "0ca3adf1-f5a5-43e9-9c82-5619340739be",
                    "leagueName": "league1",
                    "groupCount": 8,
                    "teamsPerGroup": 4,
                    "homeAndAway": True,
                    "knockoutTemplateId": None
                },
                {
                    "id": "d15956ef-d199-40b1-b7d7-850a9add97e7",
                    "tournamentName": "tournament3",
                    "leagueId": "508c8b55-2e0c-415b-8078-2dcb2065c7ca",
                    "leagueName": "league2",
                    "groupCount": 6,
                    "teamsPerGroup": 4,
                    "homeAndAway": False,
                    "knockoutTemplateId": "1a4d1cc8-f035-439a-b274-"
                                          "fe739b8fcfa5"
                }
            ]
        )

        # When
        created: list[TournamentTemplate] = (
            self.__service.create_tournament_templates(templates)
        )

        # Then
        captured_args_retrieve_records, captured_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(
            UpdateRequest,
            captured_args_retrieve_records[0]
        )

        update_request: UpdateRequest = captured_args_retrieve_records[0]
        Assertions.assert_equals(SqlOperator.INSERT, update_request.operation)

        table: Table = update_request.table
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("tournament-templates", table.table)

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_type(UUID, record1["id"])
        Assertions.assert_equals("tournament1", record1["name"])
        Assertions.assert_equals(
            UUID("80e9c164-637d-400f-a3cf-bf922073bc9b"),
            record1["knockoutTemplateId"]
        )

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_type(UUID, record2["id"])
        Assertions.assert_equals("tournament2", record2["name"])
        Assertions.assert_equals(
            UUID("0ca3adf1-f5a5-43e9-9c82-5619340739be"),
            record2["leagueTemplateId"]
        )

        record3: dict[str, Any] = update_request.records[2]
        Assertions.assert_type(UUID, record3["id"])
        Assertions.assert_equals("tournament3", record3["name"])
        Assertions.assert_equals(
            UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"),
            record3["leagueTemplateId"]
        )
        Assertions.assert_equals(
            UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"),
            record3["knockoutTemplateId"]
        )

        Assertions.assert_equals(3, len(created))

        tournament1: TournamentTemplate = created[0]
        Assertions.assert_type(TournamentTemplate, tournament1)
        Assertions.assert_type(UUID, tournament1.id)
        Assertions.assert_equals("tournament1", tournament1.name)
        Assertions.assert_none(tournament1.league)

        knockout1: KnockoutTemplate = tournament1.knockout
        Assertions.assert_type(KnockoutTemplate, knockout1)
        Assertions.assert_equals(
            UUID("80e9c164-637d-400f-a3cf-bf922073bc9b"),
            knockout1.id
        )
        Assertions.assert_equals("knockout1", knockout1.name)
        Assertions.assert_equals(2, len(knockout1.rounds))

        knockout1_round1: RoundTemplate = knockout1.rounds[0]
        Assertions.assert_equals("round1", knockout1_round1.name)
        Assertions.assert_equals(4, knockout1_round1.teamCount)
        Assertions.assert_equals(1, knockout1_round1.roundOrder)
        Assertions.assert_true(knockout1_round1.twoLegs)
        Assertions.assert_true(knockout1_round1.extraTime)
        Assertions.assert_true(knockout1_round1.awayGoals)

        knockout1_round2: RoundTemplate = knockout1.rounds[1]
        Assertions.assert_equals("round2", knockout1_round2.name)
        Assertions.assert_equals(2, knockout1_round2.teamCount)
        Assertions.assert_equals(2, knockout1_round2.roundOrder)
        Assertions.assert_false(knockout1_round2.twoLegs)
        Assertions.assert_true(knockout1_round2.extraTime)
        Assertions.assert_false(knockout1_round2.awayGoals)

        tournament2: TournamentTemplate = created[1]
        Assertions.assert_type(TournamentTemplate, tournament2)
        Assertions.assert_type(UUID, tournament2.id)
        Assertions.assert_equals("tournament2", tournament2.name)
        Assertions.assert_none(tournament2.knockout)

        league1: LeagueTemplate = tournament2.league
        Assertions.assert_equals(
            UUID("0ca3adf1-f5a5-43e9-9c82-5619340739be"),
            league1.id
        )
        Assertions.assert_equals("league1", league1.name)
        Assertions.assert_equals(8, league1.groupCount)
        Assertions.assert_equals(4, league1.teamsPerGroup)
        Assertions.assert_true(league1.homeAndAway)

        tournament3: TournamentTemplate = created[2]
        Assertions.assert_type(TournamentTemplate, tournament3)
        Assertions.assert_type(UUID, tournament3.id)
        Assertions.assert_equals("tournament3", tournament3.name)

        league2: LeagueTemplate = tournament3.league
        Assertions.assert_equals(
            UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"),
            league2.id
        )
        Assertions.assert_equals("league2", league2.name)
        Assertions.assert_equals(6, league2.groupCount)
        Assertions.assert_equals(4, league2.teamsPerGroup)
        Assertions.assert_false(league2.homeAndAway)

        knockout2: KnockoutTemplate = tournament3.knockout
        Assertions.assert_type(KnockoutTemplate, knockout2)
        Assertions.assert_equals(
            UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"),
            knockout2.id
        )
        Assertions.assert_equals("knockout2", knockout2.name)
        Assertions.assert_equals(2, len(knockout2.rounds))

        knockout2_round1: RoundTemplate = knockout2.rounds[0]
        Assertions.assert_equals("round3", knockout2_round1.name)
        Assertions.assert_equals(4, knockout2_round1.teamCount)
        Assertions.assert_equals(1, knockout2_round1.roundOrder)
        Assertions.assert_true(knockout2_round1.twoLegs)
        Assertions.assert_true(knockout2_round1.extraTime)
        Assertions.assert_true(knockout2_round1.awayGoals)

        knockout2_round2: RoundTemplate = knockout2.rounds[1]
        Assertions.assert_equals("round4", knockout2_round2.name)
        Assertions.assert_equals(2, knockout2_round2.teamCount)
        Assertions.assert_equals(2, knockout2_round2.roundOrder)
        Assertions.assert_false(knockout2_round2.twoLegs)
        Assertions.assert_true(knockout2_round2.extraTime)
        Assertions.assert_false(knockout2_round2.awayGoals)

    def test_should_return_tournament_template_by_id(self):
        # Given
        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=1,
            records=[
                {
                    "id": "d15956ef-d199-40b1-b7d7-850a9add97e7",
                    "tournamentName": "tournament3",
                    "leagueId": "508c8b55-2e0c-415b-8078-2dcb2065c7ca",
                    "leagueName": "league2",
                    "groupCount": 6,
                    "teamsPerGroup": 4,
                    "homeAndAway": False,
                    "knockoutTemplateId": "1a4d1cc8-f035-439a-b274-"
                                          "fe739b8fcfa5"
                }
            ]
        )

        self.__knock_temp_service.get_knockout_template_by_id.return_value = (
            KnockoutTemplate(
                id=UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"),
                name="knockout2",
                rounds=[
                    RoundTemplate(
                        name="round3",
                        teamCount=4,
                        roundOrder=1,
                        twoLegs=True,
                        extraTime=True,
                        awayGoals=True
                    ),
                    RoundTemplate(
                        name="round4",
                        teamCount=2,
                        roundOrder=2,
                        twoLegs=False,
                        extraTime=True,
                        awayGoals=False
                    )
                ]
            )
        )

        # When
        tournament_template: TournamentTemplate = (
            self.__service.get_tournament_template_by_id(
                UUID("d15956ef-d199-40b1-b7d7-850a9add97e7")
            )
        )

        # Then
        captured_args_retrieve_records, captured_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, captured_args_retrieve_records[0])

        query_request: QueryRequest = captured_args_retrieve_records[0]

        columns: list[Column] = query_request.columns
        Assertions.assert_equals(8, len(columns))

        column1: Column = columns[0]
        Assertions.assert_equals(["tourn", "id"], column1.parts)

        column2: Column = columns[1]
        Assertions.assert_equals(["tourn", "name"], column2.parts)
        Assertions.assert_equals("tournamentName", column2.alias)

        column3: Column = columns[2]
        Assertions.assert_equals(
            ["tourn", "knockoutTemplateId"],
            column3.parts
        )

        column4: Column = columns[3]
        Assertions.assert_equals(["league", "id"], column4.parts)
        Assertions.assert_equals("leagueId", column4.alias)

        column5: Column = columns[4]
        Assertions.assert_equals(["league", "name"], column5.parts)
        Assertions.assert_equals("leagueName", column5.alias)

        column6: Column = columns[5]
        Assertions.assert_equals(["league", "groupCount"], column6.parts)

        column7: Column = columns[6]
        Assertions.assert_equals(["league", "teamsPerGroup"], column7.parts)

        column8: Column = columns[7]
        Assertions.assert_equals(["league", "homeAndAway"], column8.parts)

        table: Table = query_request.table
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("tournament-templates", table.table)
        Assertions.assert_equals("tourn", table.alias)

        table_joins: list[TableJoin] = query_request.joins
        Assertions.assert_equals(1, len(table_joins))

        join1: TableJoin = table_joins[0]
        Assertions.assert_equals(JoinType.LEFT, join1.joinType)

        join1_table: Table = join1.table
        Assertions.assert_equals("predictor", join1_table.schema_)
        Assertions.assert_equals("league-templates", join1_table.table)
        Assertions.assert_equals("league", join1_table.alias)

        join1_condition: QueryCondition = join1.joinCondition
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            join1_condition.operator
        )

        join1_column: Column = join1_condition.column
        Assertions.assert_equals(
            ["tourn", "leagueTemplateId"],
            join1_column.parts
        )

        join1_value: Column = join1_condition.value
        Assertions.assert_equals(["league", "id"], join1_value.parts)

        condition: QueryCondition = query_request.conditionGroup.conditions[0]
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(
            UUID("d15956ef-d199-40b1-b7d7-850a9add97e7"),
            condition.value
        )

        condition_column: Column = condition.column
        Assertions.assert_equals(["tourn", "id"], condition_column.parts)

        Assertions.assert_type(TournamentTemplate, tournament_template)
        Assertions.assert_equals(
            UUID("d15956ef-d199-40b1-b7d7-850a9add97e7"),
            tournament_template.id
        )
        Assertions.assert_equals("tournament3", tournament_template.name)

        league2: LeagueTemplate = tournament_template.league
        Assertions.assert_equals(
            UUID("508c8b55-2e0c-415b-8078-2dcb2065c7ca"),
            league2.id
        )
        Assertions.assert_equals("league2", league2.name)
        Assertions.assert_equals(6, league2.groupCount)
        Assertions.assert_equals(4, league2.teamsPerGroup)
        Assertions.assert_false(league2.homeAndAway)

        knockout2: KnockoutTemplate = tournament_template.knockout
        Assertions.assert_type(KnockoutTemplate, knockout2)
        Assertions.assert_equals(
            UUID("1a4d1cc8-f035-439a-b274-fe739b8fcfa5"),
            knockout2.id
        )
        Assertions.assert_equals("knockout2", knockout2.name)
        Assertions.assert_equals(2, len(knockout2.rounds))

        knockout2_round1: RoundTemplate = knockout2.rounds[0]
        Assertions.assert_equals("round3", knockout2_round1.name)
        Assertions.assert_equals(4, knockout2_round1.teamCount)
        Assertions.assert_equals(1, knockout2_round1.roundOrder)
        Assertions.assert_true(knockout2_round1.twoLegs)
        Assertions.assert_true(knockout2_round1.extraTime)
        Assertions.assert_true(knockout2_round1.awayGoals)

        knockout2_round2: RoundTemplate = knockout2.rounds[1]
        Assertions.assert_equals("round4", knockout2_round2.name)
        Assertions.assert_equals(2, knockout2_round2.teamCount)
        Assertions.assert_equals(2, knockout2_round2.roundOrder)
        Assertions.assert_false(knockout2_round2.twoLegs)
        Assertions.assert_true(knockout2_round2.extraTime)
        Assertions.assert_false(knockout2_round2.awayGoals)

    def test_should_raise_exception_if_tournament_template_not_found(self):
        # Given
        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=0,
            records=[]
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_tournament_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournament templates found with a matching id.",
            httpe.value.detail
        )

    def test_should_delete_tournament_template_by_id(self):
        # Given
        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=0,
            records=[]
        )

        # When
        self.__service.delete_tournament_template_by_id(
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
        Assertions.assert_equals("predictor", table.schema_)
        Assertions.assert_equals("tournament-templates", table.table)

        condition: QueryCondition = update_request.conditionGroup.conditions[0]
        Assertions.assert_equals("id", condition.column.parts[0])
        Assertions.assert_equals(ConditionOperator.EQUAL, condition.operator)
        Assertions.assert_equals(
            UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"),
            condition.value
        )

    def test_no_tournament_template_delete_if_used_by_tournament(self):
        # Given
        self.__query_service.retrieve_records.return_value = QueryResponse(
            referenceId="90a6637a-e534-46bd-8715-33c6f2afdd7a",
            recordCount=1,
            records=[
                {
                    "templateId": "c08fd796-7fea-40d9-9a0a-cb3a49cce2e4",
                }
            ]
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.delete_tournament_template_by_id(
                UUID("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
            )

        # Then
        Assertions.assert_equals(409, httpe.value.status_code)
        Assertions.assert_equals(
            "Cannot delete tournament template as it is part of an existing "
            "tournament.",
            httpe.value.detail
        )
