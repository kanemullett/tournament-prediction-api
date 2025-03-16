from datetime import datetime
from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from fastapi import HTTPException
from pytest import raises

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.order_by import OrderBy
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.order_direction import OrderDirection
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from db_handler.db_handler.model.update_request import UpdateRequest
from predictor_api.predictor_api.model.match import Match
from predictor_api.predictor_api.model.match_request import MatchRequest
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.service.match_service import MatchService
from predictor_common.test_resources.assertions import Assertions


class TestMatchService:

    __query_service: MagicMock = MagicMock()
    __tournament_service: MagicMock = MagicMock()
    __group_service: MagicMock = MagicMock()
    __round_service: MagicMock = MagicMock()

    __service: MatchService = MatchService(
        __query_service,
        __tournament_service,
        __group_service,
        __round_service
    )

    def setup_method(self):
        self.__tournament_service.get_tournament_by_id.reset_mock()
        self.__tournament_service.get_tournament_by_id.return_value = None
        self.__tournament_service.get_tournament_by_id.side_effect = None

    def test_should_return_matches(self):
        # Given
        self.__group_service.tournament_has_group_stage.return_value = True
        self.__round_service.tournament_has_knockout_stage.return_value = True
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=2,
                records=[
                    {
                        "matchId": "8efaf853-980e-4607-9b45-d854460ec5e0",
                        "homeId": "bbec1707-7ea3-49cb-9791-7a1358a2b894",
                        "homeName": "Bosnia & Herzegovina",
                        "homeImagePath": "BIH.png",
                        "homeConfederation": "UEFA",
                        "awayId": "463de8d9-8520-4fa4-b30c-5aac0f3b363c",
                        "awayName": "Nigeria",
                        "awayImagePath": "NGA.png",
                        "awayConfederation": "CAF",
                        "kickoff": "2025-06-01T14:00:00",
                        "groupMatchDay": 1,
                        "groupId": "4c2c8046-0007-48db-a76a-865f9048d9de",
                        "roundId": None
                    },
                    {
                        "matchId": "d8b3685b-3749-438d-9d85-da29c97ebaef",
                        "homeId": "977f3f69-0149-43fd-adb0-7c524aea37aa",
                        "homeName": "Argentina",
                        "homeImagePath": "ARG.png",
                        "homeConfederation": "CONMEBOL",
                        "awayId": "58adea3b-bdda-496a-be74-64501e34622b",
                        "awayName": "Iran",
                        "awayImagePath": "IRI.png",
                        "awayConfederation": "AFC",
                        "kickoff": "2025-06-01T17:30:00",
                        "groupMatchDay": None,
                        "groupId": None,
                        "roundId": "322ab9d0-ae46-49ac-89b3-c789a0d9d889"
                    }
                ]
            )
        )

        # When
        matches: list[Match] = self.__service.get_matches(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            None,
            None,
            None
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        group_args, group_kwargs = (
            self.__group_service.tournament_has_group_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            group_args[0]
        )

        round_args, round_kwargs = (
            self.__round_service.tournament_has_knockout_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            round_args[0]
        )

        match_args, match_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, match_args[0])

        request: QueryRequest = match_args[0]
        Assertions.assert_equals(13, len(request.columns))

        column1: Column = request.columns[0]
        Assertions.assert_equals(["match", "id"], column1.parts)
        Assertions.assert_equals("matchId", column1.alias)

        column2: Column = request.columns[1]
        Assertions.assert_equals(["home", "id"], column2.parts)
        Assertions.assert_equals("homeId", column2.alias)

        column3: Column = request.columns[2]
        Assertions.assert_equals(["home", "name"], column3.parts)
        Assertions.assert_equals("homeName", column3.alias)

        column4: Column = request.columns[3]
        Assertions.assert_equals(["home", "imagePath"], column4.parts)
        Assertions.assert_equals("homeImagePath", column4.alias)

        column5: Column = request.columns[4]
        Assertions.assert_equals(["home", "confederation"], column5.parts)
        Assertions.assert_equals("homeConfederation", column5.alias)

        column6: Column = request.columns[5]
        Assertions.assert_equals(["away", "id"], column6.parts)
        Assertions.assert_equals("awayId", column6.alias)

        column7: Column = request.columns[6]
        Assertions.assert_equals(["away", "name"], column7.parts)
        Assertions.assert_equals("awayName", column7.alias)

        column8: Column = request.columns[7]
        Assertions.assert_equals(["away", "imagePath"], column8.parts)
        Assertions.assert_equals("awayImagePath", column8.alias)

        column9: Column = request.columns[8]
        Assertions.assert_equals(["away", "confederation"], column9.parts)
        Assertions.assert_equals("awayConfederation", column9.alias)

        column10: Column = request.columns[9]
        Assertions.assert_equals(["match", "kickoff"], column10.parts)

        column11: Column = request.columns[10]
        Assertions.assert_equals(["match", "groupMatchDay"], column11.parts)

        column12: Column = request.columns[11]
        Assertions.assert_equals(["match", "groupId"], column12.parts)

        column13: Column = request.columns[12]
        Assertions.assert_equals(["match", "roundId"], column13.parts)

        match_table: Table = request.table
        Assertions.assert_equals("predictor", match_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_table.table
        )
        Assertions.assert_equals("match", match_table.alias)

        Assertions.assert_equals(4, len(request.tableJoins))

        match_join1: TableJoin = request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.LEFT, match_join1.joinType)

        match_join1_table: Table = match_join1.table
        Assertions.assert_equals("predictor", match_join1_table.schema_)
        Assertions.assert_equals("teams", match_join1_table.table)
        Assertions.assert_equals("home", match_join1_table.alias)

        match_join1_condition: QueryCondition = match_join1.joinCondition
        Assertions.assert_equals(
            ["match", "homeTeamId"],
            match_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join1_condition.operator
        )
        Assertions.assert_equals(
            ["home", "id"],
            match_join1_condition.value.parts
        )

        match_join2: TableJoin = request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.LEFT, match_join2.joinType)

        match_join2_table: Table = match_join2.table
        Assertions.assert_equals("predictor", match_join2_table.schema_)
        Assertions.assert_equals("teams", match_join2_table.table)
        Assertions.assert_equals("away", match_join2_table.alias)

        match_join2_condition: QueryCondition = match_join2.joinCondition
        Assertions.assert_equals(
            ["match", "awayTeamId"],
            match_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join2_condition.operator
        )
        Assertions.assert_equals(
            ["away", "id"],
            match_join2_condition.value.parts
        )

        match_join3: TableJoin = request.tableJoins[2]
        Assertions.assert_equals(TableJoinType.LEFT, match_join3.joinType)

        match_join3_table: Table = match_join3.table
        Assertions.assert_equals("predictor", match_join3_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join3_table.table
        )
        Assertions.assert_equals("group", match_join3_table.alias)

        match_join3_condition: QueryCondition = match_join3.joinCondition
        Assertions.assert_equals(
            ["match", "groupId"],
            match_join3_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join3_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            match_join3_condition.value.parts
        )

        match_join4: TableJoin = request.tableJoins[3]
        Assertions.assert_equals(TableJoinType.LEFT, match_join4.joinType)

        match_join4_table: Table = match_join4.table
        Assertions.assert_equals("predictor", match_join4_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join4_table.table
        )
        Assertions.assert_equals("round", match_join4_table.alias)

        match_join4_condition: QueryCondition = match_join4.joinCondition
        Assertions.assert_equals(
            ["match", "roundId"],
            match_join4_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join4_condition.operator
        )
        Assertions.assert_equals(
            ["round", "id"],
            match_join4_condition.value.parts
        )

        Assertions.assert_none(request.conditionGroup)
        Assertions.assert_equals(4, len(request.orderBy))

        match_order_by1: OrderBy = request.orderBy[0]
        Assertions.assert_equals(
            ["match", "kickoff"],
            match_order_by1.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by1.direction)

        match_order_by2: OrderBy = request.orderBy[1]
        Assertions.assert_equals(
            ["group", "name"],
            match_order_by2.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by2.direction)

        match_order_by3: OrderBy = request.orderBy[2]
        Assertions.assert_equals(
            ["match", "groupMatchDay"],
            match_order_by3.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by3.direction)

        match_order_by4: OrderBy = request.orderBy[3]
        Assertions.assert_equals(
            ["round", "roundOrder"],
            match_order_by4.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by4.direction)

        Assertions.assert_equals(2, len(matches))

        match1: Match = matches[0]
        Assertions.assert_equals(
            UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
            match1.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 14, 0, 0),
            match1.kickoff
        )
        Assertions.assert_equals(1, match1.groupMatchDay)
        Assertions.assert_equals(
            UUID("4c2c8046-0007-48db-a76a-865f9048d9de"),
            match1.groupId
        )
        Assertions.assert_none(match1.roundId)

        match1_home: Team = match1.homeTeam
        Assertions.assert_equals(
            UUID("bbec1707-7ea3-49cb-9791-7a1358a2b894"),
            match1_home.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", match1_home.name)
        Assertions.assert_equals("BIH.png", match1_home.imagePath)
        Assertions.assert_equals(Confederation.UEFA, match1_home.confederation)

        match1_away: Team = match1.awayTeam
        Assertions.assert_equals(
            UUID("463de8d9-8520-4fa4-b30c-5aac0f3b363c"),
            match1_away.id
        )
        Assertions.assert_equals("Nigeria", match1_away.name)
        Assertions.assert_equals("NGA.png", match1_away.imagePath)
        Assertions.assert_equals(Confederation.CAF, match1_away.confederation)

        match2: Match = matches[1]
        Assertions.assert_equals(
            UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
            match2.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 17, 30, 0),
            match2.kickoff
        )
        Assertions.assert_none(match2.groupMatchDay)
        Assertions.assert_none(match2.groupId)
        Assertions.assert_equals(
            UUID("322ab9d0-ae46-49ac-89b3-c789a0d9d889"),
            match2.roundId
        )

        match2_home: Team = match2.homeTeam
        Assertions.assert_equals(
            UUID("977f3f69-0149-43fd-adb0-7c524aea37aa"),
            match2_home.id
        )
        Assertions.assert_equals("Argentina", match2_home.name)
        Assertions.assert_equals("ARG.png", match2_home.imagePath)
        Assertions.assert_equals(
            Confederation.CONMEBOL,
            match2_home.confederation
        )

        match2_away: Team = match2.awayTeam
        Assertions.assert_equals(
            UUID("58adea3b-bdda-496a-be74-64501e34622b"),
            match2_away.id
        )
        Assertions.assert_equals("Iran", match2_away.name)
        Assertions.assert_equals("IRI.png", match2_away.imagePath)
        Assertions.assert_equals(Confederation.AFC, match2_away.confederation)

    def test_should_return_group_match_day_matches(self):
        # Given
        self.__group_service.tournament_has_group_stage.return_value = True
        self.__round_service.tournament_has_knockout_stage.return_value = True
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "matchId": "8efaf853-980e-4607-9b45-d854460ec5e0",
                        "homeId": "bbec1707-7ea3-49cb-9791-7a1358a2b894",
                        "homeName": "Bosnia & Herzegovina",
                        "homeImagePath": "BIH.png",
                        "homeConfederation": "UEFA",
                        "awayId": "463de8d9-8520-4fa4-b30c-5aac0f3b363c",
                        "awayName": "Nigeria",
                        "awayImagePath": "NGA.png",
                        "awayConfederation": "CAF",
                        "kickoff": "2025-06-01T14:00:00",
                        "groupMatchDay": 1,
                        "groupId": "4c2c8046-0007-48db-a76a-865f9048d9de",
                        "roundId": None
                    }
                ]
            )
        )

        # When
        matches: list[Match] = self.__service.get_matches(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            UUID("4c2c8046-0007-48db-a76a-865f9048d9de"),
            1,
            None
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        group_args, group_kwargs = (
            self.__group_service.tournament_has_group_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            group_args[0]
        )

        round_args, round_kwargs = (
            self.__round_service.tournament_has_knockout_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            round_args[0]
        )

        match_args, match_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, match_args[0])

        request: QueryRequest = match_args[0]
        Assertions.assert_equals(13, len(request.columns))

        column1: Column = request.columns[0]
        Assertions.assert_equals(["match", "id"], column1.parts)
        Assertions.assert_equals("matchId", column1.alias)

        column2: Column = request.columns[1]
        Assertions.assert_equals(["home", "id"], column2.parts)
        Assertions.assert_equals("homeId", column2.alias)

        column3: Column = request.columns[2]
        Assertions.assert_equals(["home", "name"], column3.parts)
        Assertions.assert_equals("homeName", column3.alias)

        column4: Column = request.columns[3]
        Assertions.assert_equals(["home", "imagePath"], column4.parts)
        Assertions.assert_equals("homeImagePath", column4.alias)

        column5: Column = request.columns[4]
        Assertions.assert_equals(["home", "confederation"], column5.parts)
        Assertions.assert_equals("homeConfederation", column5.alias)

        column6: Column = request.columns[5]
        Assertions.assert_equals(["away", "id"], column6.parts)
        Assertions.assert_equals("awayId", column6.alias)

        column7: Column = request.columns[6]
        Assertions.assert_equals(["away", "name"], column7.parts)
        Assertions.assert_equals("awayName", column7.alias)

        column8: Column = request.columns[7]
        Assertions.assert_equals(["away", "imagePath"], column8.parts)
        Assertions.assert_equals("awayImagePath", column8.alias)

        column9: Column = request.columns[8]
        Assertions.assert_equals(["away", "confederation"], column9.parts)
        Assertions.assert_equals("awayConfederation", column9.alias)

        column10: Column = request.columns[9]
        Assertions.assert_equals(["match", "kickoff"], column10.parts)

        column11: Column = request.columns[10]
        Assertions.assert_equals(["match", "groupMatchDay"], column11.parts)

        column12: Column = request.columns[11]
        Assertions.assert_equals(["match", "groupId"], column12.parts)

        column13: Column = request.columns[12]
        Assertions.assert_equals(["match", "roundId"], column13.parts)

        match_table: Table = request.table
        Assertions.assert_equals("predictor", match_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_table.table
        )
        Assertions.assert_equals("match", match_table.alias)

        Assertions.assert_equals(4, len(request.tableJoins))

        match_join1: TableJoin = request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.LEFT, match_join1.joinType)

        match_join1_table: Table = match_join1.table
        Assertions.assert_equals("predictor", match_join1_table.schema_)
        Assertions.assert_equals("teams", match_join1_table.table)
        Assertions.assert_equals("home", match_join1_table.alias)

        match_join1_condition: QueryCondition = match_join1.joinCondition
        Assertions.assert_equals(
            ["match", "homeTeamId"],
            match_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join1_condition.operator
        )
        Assertions.assert_equals(
            ["home", "id"],
            match_join1_condition.value.parts
        )

        match_join2: TableJoin = request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.LEFT, match_join2.joinType)

        match_join2_table: Table = match_join2.table
        Assertions.assert_equals("predictor", match_join2_table.schema_)
        Assertions.assert_equals("teams", match_join2_table.table)
        Assertions.assert_equals("away", match_join2_table.alias)

        match_join2_condition: QueryCondition = match_join2.joinCondition
        Assertions.assert_equals(
            ["match", "awayTeamId"],
            match_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join2_condition.operator
        )
        Assertions.assert_equals(
            ["away", "id"],
            match_join2_condition.value.parts
        )

        match_join3: TableJoin = request.tableJoins[2]
        Assertions.assert_equals(TableJoinType.LEFT, match_join3.joinType)

        match_join3_table: Table = match_join3.table
        Assertions.assert_equals("predictor", match_join3_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join3_table.table
        )
        Assertions.assert_equals("group", match_join3_table.alias)

        match_join3_condition: QueryCondition = match_join3.joinCondition
        Assertions.assert_equals(
            ["match", "groupId"],
            match_join3_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join3_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            match_join3_condition.value.parts
        )

        match_join4: TableJoin = request.tableJoins[3]
        Assertions.assert_equals(TableJoinType.LEFT, match_join4.joinType)

        match_join4_table: Table = match_join4.table
        Assertions.assert_equals("predictor", match_join4_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join4_table.table
        )
        Assertions.assert_equals("round", match_join4_table.alias)

        match_join4_condition: QueryCondition = match_join4.joinCondition
        Assertions.assert_equals(
            ["match", "roundId"],
            match_join4_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join4_condition.operator
        )
        Assertions.assert_equals(
            ["round", "id"],
            match_join4_condition.value.parts
        )

        Assertions.assert_equals(2, len(request.conditionGroup.conditions))

        match_condition1: QueryCondition = request.conditionGroup.conditions[0]
        Assertions.assert_equals(
            ["match", "groupId"],
            match_condition1.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_condition1.operator
        )
        Assertions.assert_equals(
            UUID("4c2c8046-0007-48db-a76a-865f9048d9de"),
            match_condition1.value
        )

        match_condition2: QueryCondition = request.conditionGroup.conditions[1]
        Assertions.assert_equals(
            ["match", "groupMatchDay"],
            match_condition2.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_condition2.operator
        )
        Assertions.assert_equals(1, match_condition2.value)

        Assertions.assert_equals(4, len(request.orderBy))

        match_order_by1: OrderBy = request.orderBy[0]
        Assertions.assert_equals(
            ["match", "kickoff"],
            match_order_by1.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by1.direction)

        match_order_by2: OrderBy = request.orderBy[1]
        Assertions.assert_equals(
            ["group", "name"],
            match_order_by2.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by2.direction)

        match_order_by3: OrderBy = request.orderBy[2]
        Assertions.assert_equals(
            ["match", "groupMatchDay"],
            match_order_by3.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by3.direction)

        match_order_by4: OrderBy = request.orderBy[3]
        Assertions.assert_equals(
            ["round", "roundOrder"],
            match_order_by4.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by4.direction)

        Assertions.assert_equals(1, len(matches))

        match: Match = matches[0]
        Assertions.assert_equals(
            UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
            match.id
        )
        Assertions.assert_equals(datetime(2025, 6, 1, 14, 0, 0), match.kickoff)
        Assertions.assert_equals(1, match.groupMatchDay)
        Assertions.assert_equals(
            UUID("4c2c8046-0007-48db-a76a-865f9048d9de"),
            match.groupId
        )
        Assertions.assert_none(match.roundId)

        home: Team = match.homeTeam
        Assertions.assert_equals(
            UUID("bbec1707-7ea3-49cb-9791-7a1358a2b894"),
            home.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", home.name)
        Assertions.assert_equals("BIH.png", home.imagePath)
        Assertions.assert_equals(Confederation.UEFA, home.confederation)

        away: Team = match.awayTeam
        Assertions.assert_equals(
            UUID("463de8d9-8520-4fa4-b30c-5aac0f3b363c"),
            away.id
        )
        Assertions.assert_equals("Nigeria", away.name)
        Assertions.assert_equals("NGA.png", away.imagePath)
        Assertions.assert_equals(Confederation.CAF, away.confederation)

    def test_should_return_round_matches(self):
        # Given
        self.__group_service.tournament_has_group_stage.return_value = True
        self.__round_service.tournament_has_knockout_stage.return_value = True
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "matchId": "d8b3685b-3749-438d-9d85-da29c97ebaef",
                        "homeId": "977f3f69-0149-43fd-adb0-7c524aea37aa",
                        "homeName": "Argentina",
                        "homeImagePath": "ARG.png",
                        "homeConfederation": "CONMEBOL",
                        "awayId": "58adea3b-bdda-496a-be74-64501e34622b",
                        "awayName": "Iran",
                        "awayImagePath": "IRI.png",
                        "awayConfederation": "AFC",
                        "kickoff": "2025-06-01T17:30:00",
                        "groupMatchDay": None,
                        "groupId": None,
                        "roundId": "322ab9d0-ae46-49ac-89b3-c789a0d9d889"
                    }
                ]
            )
        )

        # When
        matches: list[Match] = self.__service.get_matches(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            None,
            None,
            UUID("322ab9d0-ae46-49ac-89b3-c789a0d9d889")
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        group_args, group_kwargs = (
            self.__group_service.tournament_has_group_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            group_args[0]
        )

        round_args, round_kwargs = (
            self.__round_service.tournament_has_knockout_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            round_args[0]
        )

        match_args, match_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, match_args[0])

        request: QueryRequest = match_args[0]
        Assertions.assert_equals(13, len(request.columns))

        column1: Column = request.columns[0]
        Assertions.assert_equals(["match", "id"], column1.parts)
        Assertions.assert_equals("matchId", column1.alias)

        column2: Column = request.columns[1]
        Assertions.assert_equals(["home", "id"], column2.parts)
        Assertions.assert_equals("homeId", column2.alias)

        column3: Column = request.columns[2]
        Assertions.assert_equals(["home", "name"], column3.parts)
        Assertions.assert_equals("homeName", column3.alias)

        column4: Column = request.columns[3]
        Assertions.assert_equals(["home", "imagePath"], column4.parts)
        Assertions.assert_equals("homeImagePath", column4.alias)

        column5: Column = request.columns[4]
        Assertions.assert_equals(["home", "confederation"], column5.parts)
        Assertions.assert_equals("homeConfederation", column5.alias)

        column6: Column = request.columns[5]
        Assertions.assert_equals(["away", "id"], column6.parts)
        Assertions.assert_equals("awayId", column6.alias)

        column7: Column = request.columns[6]
        Assertions.assert_equals(["away", "name"], column7.parts)
        Assertions.assert_equals("awayName", column7.alias)

        column8: Column = request.columns[7]
        Assertions.assert_equals(["away", "imagePath"], column8.parts)
        Assertions.assert_equals("awayImagePath", column8.alias)

        column9: Column = request.columns[8]
        Assertions.assert_equals(["away", "confederation"], column9.parts)
        Assertions.assert_equals("awayConfederation", column9.alias)

        column10: Column = request.columns[9]
        Assertions.assert_equals(["match", "kickoff"], column10.parts)

        column11: Column = request.columns[10]
        Assertions.assert_equals(["match", "groupMatchDay"], column11.parts)

        column12: Column = request.columns[11]
        Assertions.assert_equals(["match", "groupId"], column12.parts)

        column13: Column = request.columns[12]
        Assertions.assert_equals(["match", "roundId"], column13.parts)

        match_table: Table = request.table
        Assertions.assert_equals("predictor", match_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_table.table
        )
        Assertions.assert_equals("match", match_table.alias)

        Assertions.assert_equals(4, len(request.tableJoins))

        match_join1: TableJoin = request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.LEFT, match_join1.joinType)

        match_join1_table: Table = match_join1.table
        Assertions.assert_equals("predictor", match_join1_table.schema_)
        Assertions.assert_equals("teams", match_join1_table.table)
        Assertions.assert_equals("home", match_join1_table.alias)

        match_join1_condition: QueryCondition = match_join1.joinCondition
        Assertions.assert_equals(
            ["match", "homeTeamId"],
            match_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join1_condition.operator
        )
        Assertions.assert_equals(
            ["home", "id"],
            match_join1_condition.value.parts
        )

        match_join2: TableJoin = request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.LEFT, match_join2.joinType)

        match_join2_table: Table = match_join2.table
        Assertions.assert_equals("predictor", match_join2_table.schema_)
        Assertions.assert_equals("teams", match_join2_table.table)
        Assertions.assert_equals("away", match_join2_table.alias)

        match_join2_condition: QueryCondition = match_join2.joinCondition
        Assertions.assert_equals(
            ["match", "awayTeamId"],
            match_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join2_condition.operator
        )
        Assertions.assert_equals(
            ["away", "id"],
            match_join2_condition.value.parts
        )

        match_join3: TableJoin = request.tableJoins[2]
        Assertions.assert_equals(TableJoinType.LEFT, match_join3.joinType)

        match_join3_table: Table = match_join3.table
        Assertions.assert_equals("predictor", match_join3_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join3_table.table
        )
        Assertions.assert_equals("group", match_join3_table.alias)

        match_join3_condition: QueryCondition = match_join3.joinCondition
        Assertions.assert_equals(
            ["match", "groupId"],
            match_join3_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join3_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            match_join3_condition.value.parts
        )

        match_join4: TableJoin = request.tableJoins[3]
        Assertions.assert_equals(TableJoinType.LEFT, match_join4.joinType)

        match_join4_table: Table = match_join4.table
        Assertions.assert_equals("predictor", match_join4_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join4_table.table
        )
        Assertions.assert_equals("round", match_join4_table.alias)

        match_join4_condition: QueryCondition = match_join4.joinCondition
        Assertions.assert_equals(
            ["match", "roundId"],
            match_join4_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join4_condition.operator
        )
        Assertions.assert_equals(
            ["round", "id"],
            match_join4_condition.value.parts
        )

        Assertions.assert_equals(1, len(request.conditionGroup.conditions))

        match_condition: QueryCondition = request.conditionGroup.conditions[0]
        Assertions.assert_equals(
            ["match", "roundId"],
            match_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_condition.operator
        )
        Assertions.assert_equals(
            UUID("322ab9d0-ae46-49ac-89b3-c789a0d9d889"),
            match_condition.value
        )

        Assertions.assert_equals(4, len(request.orderBy))

        match_order_by1: OrderBy = request.orderBy[0]
        Assertions.assert_equals(
            ["match", "kickoff"],
            match_order_by1.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by1.direction)

        match_order_by2: OrderBy = request.orderBy[1]
        Assertions.assert_equals(
            ["group", "name"],
            match_order_by2.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by2.direction)

        match_order_by3: OrderBy = request.orderBy[2]
        Assertions.assert_equals(
            ["match", "groupMatchDay"],
            match_order_by3.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by3.direction)

        match_order_by4: OrderBy = request.orderBy[3]
        Assertions.assert_equals(
            ["round", "roundOrder"],
            match_order_by4.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by4.direction)

        Assertions.assert_equals(1, len(matches))

        match: Match = matches[0]
        Assertions.assert_equals(
            UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
            match.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 17, 30, 0),
            match.kickoff
        )
        Assertions.assert_none(match.groupMatchDay)
        Assertions.assert_none(match.groupId)
        Assertions.assert_equals(
            UUID("322ab9d0-ae46-49ac-89b3-c789a0d9d889"),
            match.roundId
        )

        home: Team = match.homeTeam
        Assertions.assert_equals(
            UUID("977f3f69-0149-43fd-adb0-7c524aea37aa"),
            home.id
        )
        Assertions.assert_equals("Argentina", home.name)
        Assertions.assert_equals("ARG.png", home.imagePath)
        Assertions.assert_equals(Confederation.CONMEBOL, home.confederation)

        away: Team = match.awayTeam
        Assertions.assert_equals(
            UUID("58adea3b-bdda-496a-be74-64501e34622b"),
            away.id
        )
        Assertions.assert_equals("Iran", away.name)
        Assertions.assert_equals("IRI.png", away.imagePath)
        Assertions.assert_equals(Confederation.AFC, away.confederation)

    def test_should_return_matches_no_group_stage(self):
        # Given
        self.__group_service.tournament_has_group_stage.return_value = False
        self.__round_service.tournament_has_knockout_stage.return_value = True
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "matchId": "d8b3685b-3749-438d-9d85-da29c97ebaef",
                        "homeId": "977f3f69-0149-43fd-adb0-7c524aea37aa",
                        "homeName": "Argentina",
                        "homeImagePath": "ARG.png",
                        "homeConfederation": "CONMEBOL",
                        "awayId": "58adea3b-bdda-496a-be74-64501e34622b",
                        "awayName": "Iran",
                        "awayImagePath": "IRI.png",
                        "awayConfederation": "AFC",
                        "kickoff": "2025-06-01T17:30:00",
                        "groupMatchDay": None,
                        "groupId": None,
                        "roundId": "322ab9d0-ae46-49ac-89b3-c789a0d9d889"
                    }
                ]
            )
        )

        # When
        matches: list[Match] = self.__service.get_matches(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            None,
            None,
            None
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        group_args, group_kwargs = (
            self.__group_service.tournament_has_group_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            group_args[0]
        )

        round_args, round_kwargs = (
            self.__round_service.tournament_has_knockout_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            round_args[0]
        )

        match_args, match_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, match_args[0])

        request: QueryRequest = match_args[0]
        Assertions.assert_equals(13, len(request.columns))

        column1: Column = request.columns[0]
        Assertions.assert_equals(["match", "id"], column1.parts)
        Assertions.assert_equals("matchId", column1.alias)

        column2: Column = request.columns[1]
        Assertions.assert_equals(["home", "id"], column2.parts)
        Assertions.assert_equals("homeId", column2.alias)

        column3: Column = request.columns[2]
        Assertions.assert_equals(["home", "name"], column3.parts)
        Assertions.assert_equals("homeName", column3.alias)

        column4: Column = request.columns[3]
        Assertions.assert_equals(["home", "imagePath"], column4.parts)
        Assertions.assert_equals("homeImagePath", column4.alias)

        column5: Column = request.columns[4]
        Assertions.assert_equals(["home", "confederation"], column5.parts)
        Assertions.assert_equals("homeConfederation", column5.alias)

        column6: Column = request.columns[5]
        Assertions.assert_equals(["away", "id"], column6.parts)
        Assertions.assert_equals("awayId", column6.alias)

        column7: Column = request.columns[6]
        Assertions.assert_equals(["away", "name"], column7.parts)
        Assertions.assert_equals("awayName", column7.alias)

        column8: Column = request.columns[7]
        Assertions.assert_equals(["away", "imagePath"], column8.parts)
        Assertions.assert_equals("awayImagePath", column8.alias)

        column9: Column = request.columns[8]
        Assertions.assert_equals(["away", "confederation"], column9.parts)
        Assertions.assert_equals("awayConfederation", column9.alias)

        column10: Column = request.columns[9]
        Assertions.assert_equals(["match", "kickoff"], column10.parts)

        column11: Column = request.columns[10]
        Assertions.assert_equals(["match", "groupMatchDay"], column11.parts)

        column12: Column = request.columns[11]
        Assertions.assert_equals(["match", "groupId"], column12.parts)

        column13: Column = request.columns[12]
        Assertions.assert_equals(["match", "roundId"], column13.parts)

        match_table: Table = request.table
        Assertions.assert_equals("predictor", match_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_table.table
        )
        Assertions.assert_equals("match", match_table.alias)

        Assertions.assert_equals(3, len(request.tableJoins))

        match_join1: TableJoin = request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.LEFT, match_join1.joinType)

        match_join1_table: Table = match_join1.table
        Assertions.assert_equals("predictor", match_join1_table.schema_)
        Assertions.assert_equals("teams", match_join1_table.table)
        Assertions.assert_equals("home", match_join1_table.alias)

        match_join1_condition: QueryCondition = match_join1.joinCondition
        Assertions.assert_equals(
            ["match", "homeTeamId"],
            match_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join1_condition.operator
        )
        Assertions.assert_equals(
            ["home", "id"],
            match_join1_condition.value.parts
        )

        match_join2: TableJoin = request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.LEFT, match_join2.joinType)

        match_join2_table: Table = match_join2.table
        Assertions.assert_equals("predictor", match_join2_table.schema_)
        Assertions.assert_equals("teams", match_join2_table.table)
        Assertions.assert_equals("away", match_join2_table.alias)

        match_join2_condition: QueryCondition = match_join2.joinCondition
        Assertions.assert_equals(
            ["match", "awayTeamId"],
            match_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join2_condition.operator
        )
        Assertions.assert_equals(
            ["away", "id"],
            match_join2_condition.value.parts
        )

        match_join3: TableJoin = request.tableJoins[2]
        Assertions.assert_equals(TableJoinType.LEFT, match_join3.joinType)

        match_join3_table: Table = match_join3.table
        Assertions.assert_equals("predictor", match_join3_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join3_table.table
        )
        Assertions.assert_equals("round", match_join3_table.alias)

        match_join3_condition: QueryCondition = match_join3.joinCondition
        Assertions.assert_equals(
            ["match", "roundId"],
            match_join3_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join3_condition.operator
        )
        Assertions.assert_equals(
            ["round", "id"],
            match_join3_condition.value.parts
        )

        Assertions.assert_none(request.conditionGroup)
        Assertions.assert_equals(3, len(request.orderBy))

        match_order_by1: OrderBy = request.orderBy[0]
        Assertions.assert_equals(
            ["match", "kickoff"],
            match_order_by1.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by1.direction)

        match_order_by2: OrderBy = request.orderBy[1]
        Assertions.assert_equals(
            ["match", "groupMatchDay"],
            match_order_by2.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by2.direction)

        match_order_by3: OrderBy = request.orderBy[2]
        Assertions.assert_equals(
            ["round", "roundOrder"],
            match_order_by3.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by3.direction)

        Assertions.assert_equals(1, len(matches))

        match: Match = matches[0]
        Assertions.assert_equals(
            UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
            match.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 17, 30, 0),
            match.kickoff
        )
        Assertions.assert_none(match.groupMatchDay)
        Assertions.assert_none(match.groupId)
        Assertions.assert_equals(
            UUID("322ab9d0-ae46-49ac-89b3-c789a0d9d889"),
            match.roundId
        )

        home: Team = match.homeTeam
        Assertions.assert_equals(
            UUID("977f3f69-0149-43fd-adb0-7c524aea37aa"),
            home.id
        )
        Assertions.assert_equals("Argentina", home.name)
        Assertions.assert_equals("ARG.png", home.imagePath)
        Assertions.assert_equals(Confederation.CONMEBOL, home.confederation)

        away: Team = match.awayTeam
        Assertions.assert_equals(
            UUID("58adea3b-bdda-496a-be74-64501e34622b"),
            away.id
        )
        Assertions.assert_equals("Iran", away.name)
        Assertions.assert_equals("IRI.png", away.imagePath)
        Assertions.assert_equals(Confederation.AFC, away.confederation)

    def test_should_return_matches_no_knockout_stage(self):
        # Given
        self.__group_service.tournament_has_group_stage.return_value = True
        self.__round_service.tournament_has_knockout_stage.return_value = False
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "matchId": "8efaf853-980e-4607-9b45-d854460ec5e0",
                        "homeId": "bbec1707-7ea3-49cb-9791-7a1358a2b894",
                        "homeName": "Bosnia & Herzegovina",
                        "homeImagePath": "BIH.png",
                        "homeConfederation": "UEFA",
                        "awayId": "463de8d9-8520-4fa4-b30c-5aac0f3b363c",
                        "awayName": "Nigeria",
                        "awayImagePath": "NGA.png",
                        "awayConfederation": "CAF",
                        "kickoff": "2025-06-01T14:00:00",
                        "groupMatchDay": 1,
                        "groupId": "4c2c8046-0007-48db-a76a-865f9048d9de",
                        "roundId": None
                    }
                ]
            )
        )

        # When
        matches: list[Match] = self.__service.get_matches(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            None,
            None,
            None
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        group_args, group_kwargs = (
            self.__group_service.tournament_has_group_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            group_args[0]
        )

        round_args, round_kwargs = (
            self.__round_service.tournament_has_knockout_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            round_args[0]
        )

        match_args, match_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, match_args[0])

        request: QueryRequest = match_args[0]
        Assertions.assert_equals(13, len(request.columns))

        column1: Column = request.columns[0]
        Assertions.assert_equals(["match", "id"], column1.parts)
        Assertions.assert_equals("matchId", column1.alias)

        column2: Column = request.columns[1]
        Assertions.assert_equals(["home", "id"], column2.parts)
        Assertions.assert_equals("homeId", column2.alias)

        column3: Column = request.columns[2]
        Assertions.assert_equals(["home", "name"], column3.parts)
        Assertions.assert_equals("homeName", column3.alias)

        column4: Column = request.columns[3]
        Assertions.assert_equals(["home", "imagePath"], column4.parts)
        Assertions.assert_equals("homeImagePath", column4.alias)

        column5: Column = request.columns[4]
        Assertions.assert_equals(["home", "confederation"], column5.parts)
        Assertions.assert_equals("homeConfederation", column5.alias)

        column6: Column = request.columns[5]
        Assertions.assert_equals(["away", "id"], column6.parts)
        Assertions.assert_equals("awayId", column6.alias)

        column7: Column = request.columns[6]
        Assertions.assert_equals(["away", "name"], column7.parts)
        Assertions.assert_equals("awayName", column7.alias)

        column8: Column = request.columns[7]
        Assertions.assert_equals(["away", "imagePath"], column8.parts)
        Assertions.assert_equals("awayImagePath", column8.alias)

        column9: Column = request.columns[8]
        Assertions.assert_equals(["away", "confederation"], column9.parts)
        Assertions.assert_equals("awayConfederation", column9.alias)

        column10: Column = request.columns[9]
        Assertions.assert_equals(["match", "kickoff"], column10.parts)

        column11: Column = request.columns[10]
        Assertions.assert_equals(["match", "groupMatchDay"], column11.parts)

        column12: Column = request.columns[11]
        Assertions.assert_equals(["match", "groupId"], column12.parts)

        column13: Column = request.columns[12]
        Assertions.assert_equals(["match", "roundId"], column13.parts)

        match_table: Table = request.table
        Assertions.assert_equals("predictor", match_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_table.table
        )
        Assertions.assert_equals("match", match_table.alias)

        Assertions.assert_equals(3, len(request.tableJoins))

        match_join1: TableJoin = request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.LEFT, match_join1.joinType)

        match_join1_table: Table = match_join1.table
        Assertions.assert_equals("predictor", match_join1_table.schema_)
        Assertions.assert_equals("teams", match_join1_table.table)
        Assertions.assert_equals("home", match_join1_table.alias)

        match_join1_condition: QueryCondition = match_join1.joinCondition
        Assertions.assert_equals(
            ["match", "homeTeamId"],
            match_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join1_condition.operator
        )
        Assertions.assert_equals(
            ["home", "id"],
            match_join1_condition.value.parts
        )

        match_join2: TableJoin = request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.LEFT, match_join2.joinType)

        match_join2_table: Table = match_join2.table
        Assertions.assert_equals("predictor", match_join2_table.schema_)
        Assertions.assert_equals("teams", match_join2_table.table)
        Assertions.assert_equals("away", match_join2_table.alias)

        match_join2_condition: QueryCondition = match_join2.joinCondition
        Assertions.assert_equals(
            ["match", "awayTeamId"],
            match_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join2_condition.operator
        )
        Assertions.assert_equals(
            ["away", "id"],
            match_join2_condition.value.parts
        )

        match_join3: TableJoin = request.tableJoins[2]
        Assertions.assert_equals(TableJoinType.LEFT, match_join3.joinType)

        match_join3_table: Table = match_join3.table
        Assertions.assert_equals("predictor", match_join3_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join3_table.table
        )
        Assertions.assert_equals("group", match_join3_table.alias)

        match_join3_condition: QueryCondition = match_join3.joinCondition
        Assertions.assert_equals(
            ["match", "groupId"],
            match_join3_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join3_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            match_join3_condition.value.parts
        )

        Assertions.assert_none(request.conditionGroup)
        Assertions.assert_equals(3, len(request.orderBy))

        match_order_by1: OrderBy = request.orderBy[0]
        Assertions.assert_equals(
            ["match", "kickoff"],
            match_order_by1.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by1.direction)

        match_order_by2: OrderBy = request.orderBy[1]
        Assertions.assert_equals(
            ["group", "name"],
            match_order_by2.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by2.direction)

        match_order_by3: OrderBy = request.orderBy[2]
        Assertions.assert_equals(
            ["match", "groupMatchDay"],
            match_order_by3.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by3.direction)

        Assertions.assert_equals(1, len(matches))

        match: Match = matches[0]
        Assertions.assert_equals(
            UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
            match.id
        )
        Assertions.assert_equals(datetime(2025, 6, 1, 14, 0, 0), match.kickoff)
        Assertions.assert_equals(1, match.groupMatchDay)
        Assertions.assert_equals(
            UUID("4c2c8046-0007-48db-a76a-865f9048d9de"),
            match.groupId
        )
        Assertions.assert_none(match.roundId)

        home: Team = match.homeTeam
        Assertions.assert_equals(
            UUID("bbec1707-7ea3-49cb-9791-7a1358a2b894"),
            home.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", home.name)
        Assertions.assert_equals("BIH.png", home.imagePath)
        Assertions.assert_equals(Confederation.UEFA, home.confederation)

        away: Team = match.awayTeam
        Assertions.assert_equals(
            UUID("463de8d9-8520-4fa4-b30c-5aac0f3b363c"),
            away.id
        )
        Assertions.assert_equals("Nigeria", away.name)
        Assertions.assert_equals("NGA.png", away.imagePath)
        Assertions.assert_equals(Confederation.CAF, away.confederation)

    def test_should_error_tournament_not_exists_get_matches(self):
        # Given
        self.__tournament_service.get_tournament_by_id.side_effect = (
            HTTPException(
                status_code=404,
                detail="No tournaments found with a matching id."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_matches(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                None,
                None,
                None
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )

    def test_should_update_matches(self):
        # Given
        matches: list[MatchRequest] = [
            MatchRequest(
                id=UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
                kickoff=datetime(2025, 6, 1, 14, 0, 0)
            ),
            MatchRequest(
                id=UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
                kickoff=datetime(2025, 6, 1, 17, 30, 0)
            )
        ]

        self.__group_service.tournament_has_group_stage.return_value = True
        self.__round_service.tournament_has_knockout_stage.return_value = True
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=2,
                records=[
                    {
                        "matchId": "8efaf853-980e-4607-9b45-d854460ec5e0",
                        "homeId": "bbec1707-7ea3-49cb-9791-7a1358a2b894",
                        "homeName": "Bosnia & Herzegovina",
                        "homeImagePath": "BIH.png",
                        "homeConfederation": "UEFA",
                        "awayId": "463de8d9-8520-4fa4-b30c-5aac0f3b363c",
                        "awayName": "Nigeria",
                        "awayImagePath": "NGA.png",
                        "awayConfederation": "CAF",
                        "kickoff": "2025-06-01T14:00:00",
                        "groupMatchDay": 1,
                        "groupId": "4c2c8046-0007-48db-a76a-865f9048d9de",
                        "roundId": None
                    },
                    {
                        "matchId": "d8b3685b-3749-438d-9d85-da29c97ebaef",
                        "homeId": "977f3f69-0149-43fd-adb0-7c524aea37aa",
                        "homeName": "Argentina",
                        "homeImagePath": "ARG.png",
                        "homeConfederation": "CONMEBOL",
                        "awayId": "58adea3b-bdda-496a-be74-64501e34622b",
                        "awayName": "Iran",
                        "awayImagePath": "IRI.png",
                        "awayConfederation": "AFC",
                        "kickoff": "2025-06-01T17:30:00",
                        "groupMatchDay": None,
                        "groupId": None,
                        "roundId": "322ab9d0-ae46-49ac-89b3-c789a0d9d889"
                    }
                ]
            )
        )

        # When
        matches: list[Match] = self.__service.update_matches(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            matches
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        update_args, update_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, update_args[0])

        update: UpdateRequest = update_args[0]
        Assertions.assert_equals(SqlOperator.UPDATE, update.operation)

        update_table: Table = update.table
        Assertions.assert_equals("predictor", update_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            update_table.table
        )

        Assertions.assert_equals(2, len(update.records))

        record1: dict[str, Any] = update.records[0]
        Assertions.assert_equals(
            UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
            record1["id"]
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 14, 0, 0),
            record1["kickoff"]
        )

        record2: dict[str, Any] = update.records[1]
        Assertions.assert_equals(
            UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
            record2["id"]
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 17, 30, 0),
            record2["kickoff"]
        )

        group_args, group_kwargs = (
            self.__group_service.tournament_has_group_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            group_args[0]
        )

        round_args, round_kwargs = (
            self.__round_service.tournament_has_knockout_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            round_args[0]
        )

        match_args, match_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, match_args[0])

        request: QueryRequest = match_args[0]
        Assertions.assert_equals(13, len(request.columns))

        column1: Column = request.columns[0]
        Assertions.assert_equals(["match", "id"], column1.parts)
        Assertions.assert_equals("matchId", column1.alias)

        column2: Column = request.columns[1]
        Assertions.assert_equals(["home", "id"], column2.parts)
        Assertions.assert_equals("homeId", column2.alias)

        column3: Column = request.columns[2]
        Assertions.assert_equals(["home", "name"], column3.parts)
        Assertions.assert_equals("homeName", column3.alias)

        column4: Column = request.columns[3]
        Assertions.assert_equals(["home", "imagePath"], column4.parts)
        Assertions.assert_equals("homeImagePath", column4.alias)

        column5: Column = request.columns[4]
        Assertions.assert_equals(["home", "confederation"], column5.parts)
        Assertions.assert_equals("homeConfederation", column5.alias)

        column6: Column = request.columns[5]
        Assertions.assert_equals(["away", "id"], column6.parts)
        Assertions.assert_equals("awayId", column6.alias)

        column7: Column = request.columns[6]
        Assertions.assert_equals(["away", "name"], column7.parts)
        Assertions.assert_equals("awayName", column7.alias)

        column8: Column = request.columns[7]
        Assertions.assert_equals(["away", "imagePath"], column8.parts)
        Assertions.assert_equals("awayImagePath", column8.alias)

        column9: Column = request.columns[8]
        Assertions.assert_equals(["away", "confederation"], column9.parts)
        Assertions.assert_equals("awayConfederation", column9.alias)

        column10: Column = request.columns[9]
        Assertions.assert_equals(["match", "kickoff"], column10.parts)

        column11: Column = request.columns[10]
        Assertions.assert_equals(["match", "groupMatchDay"], column11.parts)

        column12: Column = request.columns[11]
        Assertions.assert_equals(["match", "groupId"], column12.parts)

        column13: Column = request.columns[12]
        Assertions.assert_equals(["match", "roundId"], column13.parts)

        match_table: Table = request.table
        Assertions.assert_equals("predictor", match_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_table.table
        )
        Assertions.assert_equals("match", match_table.alias)

        Assertions.assert_equals(4, len(request.tableJoins))

        match_join1: TableJoin = request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.LEFT, match_join1.joinType)

        match_join1_table: Table = match_join1.table
        Assertions.assert_equals("predictor", match_join1_table.schema_)
        Assertions.assert_equals("teams", match_join1_table.table)
        Assertions.assert_equals("home", match_join1_table.alias)

        match_join1_condition: QueryCondition = match_join1.joinCondition
        Assertions.assert_equals(
            ["match", "homeTeamId"],
            match_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join1_condition.operator
        )
        Assertions.assert_equals(
            ["home", "id"],
            match_join1_condition.value.parts
        )

        match_join2: TableJoin = request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.LEFT, match_join2.joinType)

        match_join2_table: Table = match_join2.table
        Assertions.assert_equals("predictor", match_join2_table.schema_)
        Assertions.assert_equals("teams", match_join2_table.table)
        Assertions.assert_equals("away", match_join2_table.alias)

        match_join2_condition: QueryCondition = match_join2.joinCondition
        Assertions.assert_equals(
            ["match", "awayTeamId"],
            match_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join2_condition.operator
        )
        Assertions.assert_equals(
            ["away", "id"],
            match_join2_condition.value.parts
        )

        match_join3: TableJoin = request.tableJoins[2]
        Assertions.assert_equals(TableJoinType.LEFT, match_join3.joinType)

        match_join3_table: Table = match_join3.table
        Assertions.assert_equals("predictor", match_join3_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join3_table.table
        )
        Assertions.assert_equals("group", match_join3_table.alias)

        match_join3_condition: QueryCondition = match_join3.joinCondition
        Assertions.assert_equals(
            ["match", "groupId"],
            match_join3_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join3_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            match_join3_condition.value.parts
        )

        match_join4: TableJoin = request.tableJoins[3]
        Assertions.assert_equals(TableJoinType.LEFT, match_join4.joinType)

        match_join4_table: Table = match_join4.table
        Assertions.assert_equals("predictor", match_join4_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join4_table.table
        )
        Assertions.assert_equals("round", match_join4_table.alias)

        match_join4_condition: QueryCondition = match_join4.joinCondition
        Assertions.assert_equals(
            ["match", "roundId"],
            match_join4_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join4_condition.operator
        )
        Assertions.assert_equals(
            ["round", "id"],
            match_join4_condition.value.parts
        )

        Assertions.assert_equals(1, len(request.conditionGroup.conditions))

        match_condition: QueryCondition = request.conditionGroup.conditions[0]
        Assertions.assert_equals(["match", "id"], match_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.IN,
            match_condition.operator
        )
        Assertions.assert_equals(
            [
                UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
                UUID("d8b3685b-3749-438d-9d85-da29c97ebaef")
            ],
            match_condition.value
        )

        Assertions.assert_equals(4, len(request.orderBy))

        match_order_by1: OrderBy = request.orderBy[0]
        Assertions.assert_equals(
            ["match", "kickoff"],
            match_order_by1.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by1.direction)

        match_order_by2: OrderBy = request.orderBy[1]
        Assertions.assert_equals(
            ["group", "name"],
            match_order_by2.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by2.direction)

        match_order_by3: OrderBy = request.orderBy[2]
        Assertions.assert_equals(
            ["match", "groupMatchDay"],
            match_order_by3.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by3.direction)

        match_order_by4: OrderBy = request.orderBy[3]
        Assertions.assert_equals(
            ["round", "roundOrder"],
            match_order_by4.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by4.direction)

        Assertions.assert_equals(2, len(matches))

        match1: Match = matches[0]
        Assertions.assert_equals(
            UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
            match1.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 14, 0, 0),
            match1.kickoff
        )
        Assertions.assert_equals(1, match1.groupMatchDay)
        Assertions.assert_equals(
            UUID("4c2c8046-0007-48db-a76a-865f9048d9de"),
            match1.groupId
        )
        Assertions.assert_none(match1.roundId)

        match1_home: Team = match1.homeTeam
        Assertions.assert_equals(
            UUID("bbec1707-7ea3-49cb-9791-7a1358a2b894"),
            match1_home.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", match1_home.name)
        Assertions.assert_equals("BIH.png", match1_home.imagePath)
        Assertions.assert_equals(Confederation.UEFA, match1_home.confederation)

        match1_away: Team = match1.awayTeam
        Assertions.assert_equals(
            UUID("463de8d9-8520-4fa4-b30c-5aac0f3b363c"),
            match1_away.id
        )
        Assertions.assert_equals("Nigeria", match1_away.name)
        Assertions.assert_equals("NGA.png", match1_away.imagePath)
        Assertions.assert_equals(Confederation.CAF, match1_away.confederation)

        match2: Match = matches[1]
        Assertions.assert_equals(
            UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
            match2.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 17, 30, 0),
            match2.kickoff
        )
        Assertions.assert_none(match2.groupMatchDay)
        Assertions.assert_none(match2.groupId)
        Assertions.assert_equals(
            UUID("322ab9d0-ae46-49ac-89b3-c789a0d9d889"),
            match2.roundId
        )

        match2_home: Team = match2.homeTeam
        Assertions.assert_equals(
            UUID("977f3f69-0149-43fd-adb0-7c524aea37aa"),
            match2_home.id
        )
        Assertions.assert_equals("Argentina", match2_home.name)
        Assertions.assert_equals("ARG.png", match2_home.imagePath)
        Assertions.assert_equals(
            Confederation.CONMEBOL,
            match2_home.confederation
        )

        match2_away: Team = match2.awayTeam
        Assertions.assert_equals(
            UUID("58adea3b-bdda-496a-be74-64501e34622b"),
            match2_away.id
        )
        Assertions.assert_equals("Iran", match2_away.name)
        Assertions.assert_equals("IRI.png", match2_away.imagePath)
        Assertions.assert_equals(Confederation.AFC, match2_away.confederation)

    def test_should_error_tournament_not_exists_update_matches(self):
        # Given
        matches: list[MatchRequest] = [
            MatchRequest(
                id=UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
                kickoff=datetime(2025, 6, 1, 14, 0, 0)
            ),
            MatchRequest(
                id=UUID("d8b3685b-3749-438d-9d85-da29c97ebaef"),
                kickoff=datetime(2025, 6, 1, 17, 30, 0)
            )
        ]

        self.__tournament_service.get_tournament_by_id.side_effect = (
            HTTPException(
                status_code=404,
                detail="No tournaments found with a matching id."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.update_matches(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                matches
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )

    def test_should_return_match(self):
        # Given
        self.__group_service.tournament_has_group_stage.return_value = True
        self.__round_service.tournament_has_knockout_stage.return_value = True
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "matchId": "8efaf853-980e-4607-9b45-d854460ec5e0",
                        "homeId": "bbec1707-7ea3-49cb-9791-7a1358a2b894",
                        "homeName": "Bosnia & Herzegovina",
                        "homeImagePath": "BIH.png",
                        "homeConfederation": "UEFA",
                        "awayId": "463de8d9-8520-4fa4-b30c-5aac0f3b363c",
                        "awayName": "Nigeria",
                        "awayImagePath": "NGA.png",
                        "awayConfederation": "CAF",
                        "kickoff": "2025-06-01T14:00:00",
                        "groupMatchDay": 1,
                        "groupId": "4c2c8046-0007-48db-a76a-865f9048d9de",
                        "roundId": None
                    }
                ]
            )
        )

        # When
        match: Match = self.__service.get_match_by_id(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            UUID("8efaf853-980e-4607-9b45-d854460ec5e0")
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        group_args, group_kwargs = (
            self.__group_service.tournament_has_group_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            group_args[0]
        )

        round_args, round_kwargs = (
            self.__round_service.tournament_has_knockout_stage.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            round_args[0]
        )

        match_args, match_kwargs = (
            self.__query_service.retrieve_records.call_args
        )
        Assertions.assert_type(QueryRequest, match_args[0])

        request: QueryRequest = match_args[0]
        Assertions.assert_equals(13, len(request.columns))

        column1: Column = request.columns[0]
        Assertions.assert_equals(["match", "id"], column1.parts)
        Assertions.assert_equals("matchId", column1.alias)

        column2: Column = request.columns[1]
        Assertions.assert_equals(["home", "id"], column2.parts)
        Assertions.assert_equals("homeId", column2.alias)

        column3: Column = request.columns[2]
        Assertions.assert_equals(["home", "name"], column3.parts)
        Assertions.assert_equals("homeName", column3.alias)

        column4: Column = request.columns[3]
        Assertions.assert_equals(["home", "imagePath"], column4.parts)
        Assertions.assert_equals("homeImagePath", column4.alias)

        column5: Column = request.columns[4]
        Assertions.assert_equals(["home", "confederation"], column5.parts)
        Assertions.assert_equals("homeConfederation", column5.alias)

        column6: Column = request.columns[5]
        Assertions.assert_equals(["away", "id"], column6.parts)
        Assertions.assert_equals("awayId", column6.alias)

        column7: Column = request.columns[6]
        Assertions.assert_equals(["away", "name"], column7.parts)
        Assertions.assert_equals("awayName", column7.alias)

        column8: Column = request.columns[7]
        Assertions.assert_equals(["away", "imagePath"], column8.parts)
        Assertions.assert_equals("awayImagePath", column8.alias)

        column9: Column = request.columns[8]
        Assertions.assert_equals(["away", "confederation"], column9.parts)
        Assertions.assert_equals("awayConfederation", column9.alias)

        column10: Column = request.columns[9]
        Assertions.assert_equals(["match", "kickoff"], column10.parts)

        column11: Column = request.columns[10]
        Assertions.assert_equals(["match", "groupMatchDay"], column11.parts)

        column12: Column = request.columns[11]
        Assertions.assert_equals(["match", "groupId"], column12.parts)

        column13: Column = request.columns[12]
        Assertions.assert_equals(["match", "roundId"], column13.parts)

        match_table: Table = request.table
        Assertions.assert_equals("predictor", match_table.schema_)
        Assertions.assert_equals(
            "matches_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_table.table
        )
        Assertions.assert_equals("match", match_table.alias)

        Assertions.assert_equals(4, len(request.tableJoins))

        match_join1: TableJoin = request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.LEFT, match_join1.joinType)

        match_join1_table: Table = match_join1.table
        Assertions.assert_equals("predictor", match_join1_table.schema_)
        Assertions.assert_equals("teams", match_join1_table.table)
        Assertions.assert_equals("home", match_join1_table.alias)

        match_join1_condition: QueryCondition = match_join1.joinCondition
        Assertions.assert_equals(
            ["match", "homeTeamId"],
            match_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join1_condition.operator
        )
        Assertions.assert_equals(
            ["home", "id"],
            match_join1_condition.value.parts
        )

        match_join2: TableJoin = request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.LEFT, match_join2.joinType)

        match_join2_table: Table = match_join2.table
        Assertions.assert_equals("predictor", match_join2_table.schema_)
        Assertions.assert_equals("teams", match_join2_table.table)
        Assertions.assert_equals("away", match_join2_table.alias)

        match_join2_condition: QueryCondition = match_join2.joinCondition
        Assertions.assert_equals(
            ["match", "awayTeamId"],
            match_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join2_condition.operator
        )
        Assertions.assert_equals(
            ["away", "id"],
            match_join2_condition.value.parts
        )

        match_join3: TableJoin = request.tableJoins[2]
        Assertions.assert_equals(TableJoinType.LEFT, match_join3.joinType)

        match_join3_table: Table = match_join3.table
        Assertions.assert_equals("predictor", match_join3_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join3_table.table
        )
        Assertions.assert_equals("group", match_join3_table.alias)

        match_join3_condition: QueryCondition = match_join3.joinCondition
        Assertions.assert_equals(
            ["match", "groupId"],
            match_join3_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join3_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            match_join3_condition.value.parts
        )

        match_join4: TableJoin = request.tableJoins[3]
        Assertions.assert_equals(TableJoinType.LEFT, match_join4.joinType)

        match_join4_table: Table = match_join4.table
        Assertions.assert_equals("predictor", match_join4_table.schema_)
        Assertions.assert_equals(
            "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87",
            match_join4_table.table
        )
        Assertions.assert_equals("round", match_join4_table.alias)

        match_join4_condition: QueryCondition = match_join4.joinCondition
        Assertions.assert_equals(
            ["match", "roundId"],
            match_join4_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            match_join4_condition.operator
        )
        Assertions.assert_equals(
            ["round", "id"],
            match_join4_condition.value.parts
        )

        Assertions.assert_equals(1, len(request.conditionGroup.conditions))

        match_condition: QueryCondition = request.conditionGroup.conditions[0]
        Assertions.assert_equals(["match", "id"], match_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.IN,
            match_condition.operator
        )
        Assertions.assert_equals(
            [UUID("8efaf853-980e-4607-9b45-d854460ec5e0")],
            match_condition.value
        )

        Assertions.assert_equals(4, len(request.orderBy))

        match_order_by1: OrderBy = request.orderBy[0]
        Assertions.assert_equals(
            ["match", "kickoff"],
            match_order_by1.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by1.direction)

        match_order_by2: OrderBy = request.orderBy[1]
        Assertions.assert_equals(
            ["group", "name"],
            match_order_by2.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by2.direction)

        match_order_by3: OrderBy = request.orderBy[2]
        Assertions.assert_equals(
            ["match", "groupMatchDay"],
            match_order_by3.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by3.direction)

        match_order_by4: OrderBy = request.orderBy[3]
        Assertions.assert_equals(
            ["round", "roundOrder"],
            match_order_by4.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, match_order_by4.direction)

        Assertions.assert_equals(
            UUID("8efaf853-980e-4607-9b45-d854460ec5e0"),
            match.id
        )
        Assertions.assert_equals(
            datetime(2025, 6, 1, 14, 0, 0),
            match.kickoff
        )
        Assertions.assert_equals(1, match.groupMatchDay)
        Assertions.assert_equals(
            UUID("4c2c8046-0007-48db-a76a-865f9048d9de"),
            match.groupId
        )
        Assertions.assert_none(match.roundId)

        match1_home: Team = match.homeTeam
        Assertions.assert_equals(
            UUID("bbec1707-7ea3-49cb-9791-7a1358a2b894"),
            match1_home.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", match1_home.name)
        Assertions.assert_equals("BIH.png", match1_home.imagePath)
        Assertions.assert_equals(Confederation.UEFA, match1_home.confederation)

        match1_away: Team = match.awayTeam
        Assertions.assert_equals(
            UUID("463de8d9-8520-4fa4-b30c-5aac0f3b363c"),
            match1_away.id
        )
        Assertions.assert_equals("Nigeria", match1_away.name)
        Assertions.assert_equals("NGA.png", match1_away.imagePath)
        Assertions.assert_equals(Confederation.CAF, match1_away.confederation)

    def test_should_error_tournament_not_exists_get_match_by_id(self):
        # Given
        self.__tournament_service.get_tournament_by_id.side_effect = (
            HTTPException(
                status_code=404,
                detail="No tournaments found with a matching id."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_match_by_id(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                UUID("8efaf853-980e-4607-9b45-d854460ec5e0")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No tournaments found with a matching id.",
            httpe.value.detail
        )

    def test_should_error_match_not_exists_get_match_by_id(self):
        # Given
        self.__group_service.tournament_has_group_stage.return_value = True
        self.__round_service.tournament_has_knockout_stage.return_value = True
        self.__query_service.retrieve_records.return_value = (
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=0,
                records=[]
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_match_by_id(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                UUID("8efaf853-980e-4607-9b45-d854460ec5e0")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No matches found with a matching id.",
            httpe.value.detail
        )
