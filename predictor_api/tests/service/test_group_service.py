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
from predictor_api.predictor_api.model.group import Group
from predictor_api.predictor_api.model.group_update import GroupUpdate
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.service.group_service import GroupService
from predictor_common.test_resources.assertions import Assertions


class TestGroupService:

    __query_service: MagicMock = MagicMock()
    __tournament_service: MagicMock = MagicMock()

    __service: GroupService = GroupService(
        __query_service,
        __tournament_service
    )

    def setup_method(self):
        self.__query_service.retrieve_records.reset_mock()
        self.__query_service.retrieve_records.return_value = None
        self.__query_service.retrieve_records.side_effect = None

        self.__query_service.update_records.reset_mock()
        self.__query_service.update_records.return_value = None
        self.__query_service.update_records.side_effect = None

        self.__tournament_service.get_tournament_by_id.reset_mock()
        self.__tournament_service.get_tournament_by_id.return_value = None
        self.__tournament_service.get_tournament_by_id.side_effect = None

    def test_should_return_groups(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "leagueTemplateId": "72119bfa-212b-443c-b992-"
                                            "7dc6983c6a1a"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=2,
                records=[
                    {
                        "id": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "name": "Group A"
                    },
                    {
                        "id": "e0ee5d0e-9d57-4c74-b938-0aa306a2313e",
                        "name": "Group B"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=4,
                records=[
                    {
                        "groupId": "e0ee5d0e-9d57-4c74-b938-0aa306a2313e",
                        "id": "6c1496f5-b819-4ed3-b4c3-17bdaa6f252d",
                        "name": "Bosnia & Herzegovina",
                        "imagePath": "BIH.png",
                        "confederation": "UEFA"
                    },
                    {
                        "groupId": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "id": "525bf855-a5b1-45cf-a1de-c017e67c0ce7",
                        "name": "Croatia",
                        "imagePath": "HRV.png",
                        "confederation": "UEFA"
                    },
                    {
                        "groupId": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "id": "bc339fee-cfda-4dbd-b1de-337a270bc414",
                        "name": "Serbia",
                        "imagePath": "SRB.png",
                        "confederation": "UEFA"
                    },
                    {
                        "groupId": "e0ee5d0e-9d57-4c74-b938-0aa306a2313e",
                        "id": "1708fce1-2862-4604-b863-5fb4f00b68d2",
                        "name": "Slovenia",
                        "imagePath": "SLO.png",
                        "confederation": "UEFA"
                    }
                ]
            )
        ]

        # When
        groups: list[Group] = self.__service.get_groups(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87")
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        template_args, template_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[0]
        Assertions.assert_type(QueryRequest, template_args[0])

        template_request: QueryRequest = template_args[0]
        Assertions.assert_equals(1, len(template_request.columns))

        template_column: Column = template_request.columns[0]
        Assertions.assert_equals(
            ["temp", "leagueTemplateId"],
            template_column.parts
        )

        template_table: Table = template_request.table
        Assertions.assert_equals("predictor", template_table.schema_)
        Assertions.assert_equals("tournaments", template_table.table)
        Assertions.assert_equals("tourn", template_table.alias)

        Assertions.assert_equals(1, len(template_request.tableJoins))

        template_join: TableJoin = template_request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.INNER, template_join.joinType)

        template_join_table: Table = template_join.table
        Assertions.assert_equals("predictor", template_join_table.schema_)
        Assertions.assert_equals(
            "tournament-templates",
            template_join_table.table
        )
        Assertions.assert_equals("temp", template_join_table.alias)

        template_join_condition: QueryCondition = template_join.joinCondition
        Assertions.assert_equals(
            ["tourn", "templateId"],
            template_join_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_join_condition.operator
        )
        Assertions.assert_equals(
            ["temp", "id"],
            template_join_condition.value.parts
        )

        Assertions.assert_equals(
            1,
            len(template_request.conditionGroup.conditions)
        )

        template_condition: QueryCondition = (
            template_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(
            ["tourn", "id"],
            template_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_condition.operator
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            template_condition.value
        )

        group_args, group_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[1]
        Assertions.assert_type(QueryRequest, group_args[0])

        group_request: QueryRequest = group_args[0]

        group_table: Table = group_request.table
        Assertions.assert_equals("predictor", group_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            group_table.table
        )
        Assertions.assert_equals("group", group_table.alias)

        Assertions.assert_none(group_request.conditionGroup)

        group_order_by: OrderBy = group_request.orderBy
        Assertions.assert_equals(
            ["group", "name"],
            group_order_by.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, group_order_by.direction)

        team_args, team_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[2]
        Assertions.assert_type(QueryRequest, team_args[0])

        team_request: QueryRequest = team_args[0]
        Assertions.assert_equals(5, len(team_request.columns))
        Assertions.assert_equals(
            ["gt", "groupId"],
            team_request.columns[0].parts
        )
        Assertions.assert_equals(["team", "id"], team_request.columns[1].parts)
        Assertions.assert_equals(
            ["team", "name"],
            team_request.columns[2].parts
        )
        Assertions.assert_equals(
            ["team", "imagePath"],
            team_request.columns[3].parts
        )
        Assertions.assert_equals(
            ["team", "confederation"],
            team_request.columns[4].parts
        )

        team_table: Table = team_request.table
        Assertions.assert_equals("predictor", team_table.schema_)
        Assertions.assert_equals(
            "group-teams_5341cff8-df9f-4068-8a42-4b4288ecba87",
            team_table.table
        )
        Assertions.assert_equals("gt", team_table.alias)

        Assertions.assert_equals(2, len(team_request.tableJoins))

        team_join1: TableJoin = team_request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.INNER, team_join1.joinType)

        team_join1_table: Table = team_join1.table
        Assertions.assert_equals("predictor", team_join1_table.schema_)
        Assertions.assert_equals("teams", team_join1_table.table)
        Assertions.assert_equals("team", team_join1_table.alias)

        team_join1_condition: QueryCondition = team_join1.joinCondition
        Assertions.assert_equals(
            ["gt", "teamId"],
            team_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            team_join1_condition.operator
        )
        Assertions.assert_equals(
            ["team", "id"],
            team_join1_condition.value.parts
        )

        team_join2: TableJoin = team_request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.INNER, team_join2.joinType)

        team_join2_table: Table = team_join2.table
        Assertions.assert_equals("predictor", team_join2_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            team_join2_table.table
        )
        Assertions.assert_equals("group", team_join2_table.alias)

        team_join2_condition: QueryCondition = team_join2.joinCondition
        Assertions.assert_equals(
            ["gt", "groupId"],
            team_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            team_join2_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            team_join2_condition.value.parts
        )

        Assertions.assert_none(team_request.conditionGroup)

        team_order_by: OrderBy = team_request.orderBy
        Assertions.assert_equals(["team", "name"], team_order_by.column.parts)
        Assertions.assert_equals(OrderDirection.ASC, team_order_by.direction)

        Assertions.assert_equals(2, len(groups))

        group1: Group = groups[0]
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            group1.id
        )
        Assertions.assert_equals("Group A", group1.name)
        Assertions.assert_equals(2, len(group1.teams))

        group1_team1: Team = group1.teams[0]
        Assertions.assert_equals(
            UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
            group1_team1.id
        )
        Assertions.assert_equals("Croatia", group1_team1.name)
        Assertions.assert_equals("HRV.png", group1_team1.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group1_team1.confederation
        )

        group1_team2: Team = group1.teams[1]
        Assertions.assert_equals(
            UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"),
            group1_team2.id
        )
        Assertions.assert_equals("Serbia", group1_team2.name)
        Assertions.assert_equals("SRB.png", group1_team2.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group1_team2.confederation
        )

        group2: Group = groups[1]
        Assertions.assert_equals(
            UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
            group2.id
        )
        Assertions.assert_equals("Group B", group2.name)
        Assertions.assert_equals(2, len(group2.teams))

        group2_team1: Team = group2.teams[0]
        Assertions.assert_equals(
            UUID("6c1496f5-b819-4ed3-b4c3-17bdaa6f252d"),
            group2_team1.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", group2_team1.name)
        Assertions.assert_equals("BIH.png", group2_team1.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group2_team1.confederation
        )

        group2_team2: Team = group2.teams[1]
        Assertions.assert_equals(
            UUID("1708fce1-2862-4604-b863-5fb4f00b68d2"),
            group2_team2.id
        )
        Assertions.assert_equals("Slovenia", group2_team2.name)
        Assertions.assert_equals("SLO.png", group2_team2.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group2_team2.confederation
        )

    def test_should_error_tournament_not_exists_get_groups(self):
        # Given
        self.__tournament_service.get_tournament_by_id.side_effect = (
            HTTPException(
                status_code=404,
                detail="No teams found with a matching id."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_groups(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No teams found with a matching id.",
            httpe.value.detail
        )

    def test_should_error_tournament_no_group_stage_get_groups(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "leagueTemplateId": None
                    }
                ]
            )
        ]

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_groups(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "The tournament with the supplied id does not have a group stage.",
            httpe.value.detail
        )

    def test_should_update_groups(self):
        # Given
        group_updates: list[GroupUpdate] = [
            GroupUpdate(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A"
            ),
            GroupUpdate(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B"
            )
        ]

        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "leagueTemplateId": "72119bfa-212b-443c-b992-"
                                            "7dc6983c6a1a"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=2,
                records=[
                    {
                        "id": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "name": "Group A"
                    },
                    {
                        "id": "e0ee5d0e-9d57-4c74-b938-0aa306a2313e",
                        "name": "Group B"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=4,
                records=[
                    {
                        "groupId": "e0ee5d0e-9d57-4c74-b938-0aa306a2313e",
                        "id": "6c1496f5-b819-4ed3-b4c3-17bdaa6f252d",
                        "name": "Bosnia & Herzegovina",
                        "imagePath": "BIH.png",
                        "confederation": "UEFA"
                    },
                    {
                        "groupId": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "id": "525bf855-a5b1-45cf-a1de-c017e67c0ce7",
                        "name": "Croatia",
                        "imagePath": "HRV.png",
                        "confederation": "UEFA"
                    },
                    {
                        "groupId": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "id": "bc339fee-cfda-4dbd-b1de-337a270bc414",
                        "name": "Serbia",
                        "imagePath": "SRB.png",
                        "confederation": "UEFA"
                    },
                    {
                        "groupId": "e0ee5d0e-9d57-4c74-b938-0aa306a2313e",
                        "id": "1708fce1-2862-4604-b863-5fb4f00b68d2",
                        "name": "Slovenia",
                        "imagePath": "SLO.png",
                        "confederation": "UEFA"
                    }
                ]
            )
        ]

        # When
        updated: list[Group] = self.__service.update_groups(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            group_updates
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        template_args, template_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[0]
        Assertions.assert_type(QueryRequest, template_args[0])

        template_request: QueryRequest = template_args[0]
        Assertions.assert_equals(1, len(template_request.columns))

        template_column: Column = template_request.columns[0]
        Assertions.assert_equals(
            ["temp", "leagueTemplateId"],
            template_column.parts
        )

        template_table: Table = template_request.table
        Assertions.assert_equals("predictor", template_table.schema_)
        Assertions.assert_equals("tournaments", template_table.table)
        Assertions.assert_equals("tourn", template_table.alias)

        Assertions.assert_equals(1, len(template_request.tableJoins))

        template_join: TableJoin = template_request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.INNER, template_join.joinType)

        template_join_table: Table = template_join.table
        Assertions.assert_equals("predictor", template_join_table.schema_)
        Assertions.assert_equals(
            "tournament-templates",
            template_join_table.table
        )
        Assertions.assert_equals("temp", template_join_table.alias)

        template_join_condition: QueryCondition = template_join.joinCondition
        Assertions.assert_equals(
            ["tourn", "templateId"],
            template_join_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_join_condition.operator
        )
        Assertions.assert_equals(
            ["temp", "id"],
            template_join_condition.value.parts
        )

        Assertions.assert_equals(
            1,
            len(template_request.conditionGroup.conditions)
        )

        template_condition: QueryCondition = (
            template_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(
            ["tourn", "id"],
            template_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_condition.operator
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            template_condition.value
        )

        update_args, update_kwargs = (
            self.__query_service.update_records.call_args
        )
        Assertions.assert_type(UpdateRequest, update_args[0])

        update_request: UpdateRequest = update_args[0]
        Assertions.assert_equals(SqlOperator.UPDATE, update_request.operation)

        update_table: Table = update_request.table
        Assertions.assert_equals("predictor", update_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            update_table.table
        )

        Assertions.assert_equals(2, len(update_request.records))

        record1: dict[str, Any] = update_request.records[0]
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            record1["id"]
        )
        Assertions.assert_equals("Group A", record1["name"])

        record2: dict[str, Any] = update_request.records[1]
        Assertions.assert_equals(
            UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
            record2["id"]
        )
        Assertions.assert_equals("Group B", record2["name"])

        group_args, group_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[1]
        Assertions.assert_type(QueryRequest, group_args[0])

        group_request: QueryRequest = group_args[0]

        group_table: Table = group_request.table
        Assertions.assert_equals("predictor", group_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            group_table.table
        )
        Assertions.assert_equals("group", group_table.alias)

        Assertions.assert_equals(
            1,
            len(group_request.conditionGroup.conditions)
        )

        group_condition: QueryCondition = (
            group_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["group", "id"], group_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.IN,
            group_condition.operator
        )
        Assertions.assert_equals(
            [
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e")
            ],
            group_condition.value
        )

        group_order_by: OrderBy = group_request.orderBy
        Assertions.assert_equals(
            ["group", "name"],
            group_order_by.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, group_order_by.direction)

        team_args, team_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[2]
        Assertions.assert_type(QueryRequest, team_args[0])

        team_request: QueryRequest = team_args[0]
        Assertions.assert_equals(5, len(team_request.columns))
        Assertions.assert_equals(
            ["gt", "groupId"],
            team_request.columns[0].parts
        )
        Assertions.assert_equals(["team", "id"], team_request.columns[1].parts)
        Assertions.assert_equals(
            ["team", "name"],
            team_request.columns[2].parts
        )
        Assertions.assert_equals(
            ["team", "imagePath"],
            team_request.columns[3].parts
        )
        Assertions.assert_equals(
            ["team", "confederation"],
            team_request.columns[4].parts
        )

        team_table: Table = team_request.table
        Assertions.assert_equals("predictor", team_table.schema_)
        Assertions.assert_equals(
            "group-teams_5341cff8-df9f-4068-8a42-4b4288ecba87",
            team_table.table
        )
        Assertions.assert_equals("gt", team_table.alias)

        Assertions.assert_equals(2, len(team_request.tableJoins))

        team_join1: TableJoin = team_request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.INNER, team_join1.joinType)

        team_join1_table: Table = team_join1.table
        Assertions.assert_equals("predictor", team_join1_table.schema_)
        Assertions.assert_equals("teams", team_join1_table.table)
        Assertions.assert_equals("team", team_join1_table.alias)

        team_join1_condition: QueryCondition = team_join1.joinCondition
        Assertions.assert_equals(
            ["gt", "teamId"],
            team_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            team_join1_condition.operator
        )
        Assertions.assert_equals(
            ["team", "id"],
            team_join1_condition.value.parts
        )

        team_join2: TableJoin = team_request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.INNER, team_join2.joinType)

        team_join2_table: Table = team_join2.table
        Assertions.assert_equals("predictor", team_join2_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            team_join2_table.table
        )
        Assertions.assert_equals("group", team_join2_table.alias)

        team_join2_condition: QueryCondition = team_join2.joinCondition
        Assertions.assert_equals(
            ["gt", "groupId"],
            team_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            team_join2_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            team_join2_condition.value.parts
        )

        Assertions.assert_equals(
            1,
            len(team_request.conditionGroup.conditions)
        )

        team_condition: QueryCondition = (
            team_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["group", "id"], team_condition.column.parts)
        Assertions.assert_equals(ConditionOperator.IN, team_condition.operator)
        Assertions.assert_equals(
            [
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e")
            ],
            team_condition.value
        )

        team_order_by: OrderBy = team_request.orderBy
        Assertions.assert_equals(["team", "name"], team_order_by.column.parts)
        Assertions.assert_equals(OrderDirection.ASC, team_order_by.direction)

        Assertions.assert_equals(2, len(updated))

        group1: Group = updated[0]
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            group1.id
        )
        Assertions.assert_equals("Group A", group1.name)
        Assertions.assert_equals(2, len(group1.teams))

        group1_team1: Team = group1.teams[0]
        Assertions.assert_equals(
            UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
            group1_team1.id
        )
        Assertions.assert_equals("Croatia", group1_team1.name)
        Assertions.assert_equals("HRV.png", group1_team1.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group1_team1.confederation
        )

        group1_team2: Team = group1.teams[1]
        Assertions.assert_equals(
            UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"),
            group1_team2.id
        )
        Assertions.assert_equals("Serbia", group1_team2.name)
        Assertions.assert_equals("SRB.png", group1_team2.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group1_team2.confederation
        )

        group2: Group = updated[1]
        Assertions.assert_equals(
            UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
            group2.id
        )
        Assertions.assert_equals("Group B", group2.name)
        Assertions.assert_equals(2, len(group2.teams))

        group2_team1: Team = group2.teams[0]
        Assertions.assert_equals(
            UUID("6c1496f5-b819-4ed3-b4c3-17bdaa6f252d"),
            group2_team1.id
        )
        Assertions.assert_equals("Bosnia & Herzegovina", group2_team1.name)
        Assertions.assert_equals("BIH.png", group2_team1.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group2_team1.confederation
        )

        group2_team2: Team = group2.teams[1]
        Assertions.assert_equals(
            UUID("1708fce1-2862-4604-b863-5fb4f00b68d2"),
            group2_team2.id
        )
        Assertions.assert_equals("Slovenia", group2_team2.name)
        Assertions.assert_equals("SLO.png", group2_team2.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group2_team2.confederation
        )

    def test_should_error_tournament_not_exists_update_groups(self):
        # Given
        group_updates: list[GroupUpdate] = [
            GroupUpdate(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A"
            ),
            GroupUpdate(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B"
            )
        ]

        self.__tournament_service.get_tournament_by_id.side_effect = (
            HTTPException(
                status_code=404,
                detail="No teams found with a matching id."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.update_groups(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                group_updates
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No teams found with a matching id.",
            httpe.value.detail
        )

    def test_should_error_tournament_no_group_stage_update_groups(self):
        # Given
        group_updates: list[GroupUpdate] = [
            GroupUpdate(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A"
            ),
            GroupUpdate(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B"
            )
        ]

        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "leagueTemplateId": None
                    }
                ]
            )
        ]

        # When
        with raises(HTTPException) as httpe:
            self.__service.update_groups(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                group_updates
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "The tournament with the supplied id does not have a group stage.",
            httpe.value.detail
        )

    def test_should_return_group_by_id(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "leagueTemplateId": "72119bfa-212b-443c-b992-"
                                            "7dc6983c6a1a"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "id": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "name": "Group A"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "id": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "name": "Group A"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=2,
                records=[
                    {
                        "groupId": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "id": "525bf855-a5b1-45cf-a1de-c017e67c0ce7",
                        "name": "Croatia",
                        "imagePath": "HRV.png",
                        "confederation": "UEFA"
                    },
                    {
                        "groupId": "96074478-23c4-4b6f-a8a4-1abe9fac2659",
                        "id": "bc339fee-cfda-4dbd-b1de-337a270bc414",
                        "name": "Serbia",
                        "imagePath": "SRB.png",
                        "confederation": "UEFA"
                    }
                ]
            )
        ]

        # When
        group: Group = self.__service.get_group_by_id(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659")
        )

        # Then
        tournament_args, tournament_kwargs = (
            self.__tournament_service.get_tournament_by_id.call_args
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            tournament_args[0]
        )

        template_args, template_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[0]
        Assertions.assert_type(QueryRequest, template_args[0])

        template_request: QueryRequest = template_args[0]
        Assertions.assert_equals(1, len(template_request.columns))

        template_column: Column = template_request.columns[0]
        Assertions.assert_equals(
            ["temp", "leagueTemplateId"],
            template_column.parts
        )

        template_table: Table = template_request.table
        Assertions.assert_equals("predictor", template_table.schema_)
        Assertions.assert_equals("tournaments", template_table.table)
        Assertions.assert_equals("tourn", template_table.alias)

        Assertions.assert_equals(1, len(template_request.tableJoins))

        template_join: TableJoin = template_request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.INNER, template_join.joinType)

        template_join_table: Table = template_join.table
        Assertions.assert_equals("predictor", template_join_table.schema_)
        Assertions.assert_equals(
            "tournament-templates",
            template_join_table.table
        )
        Assertions.assert_equals("temp", template_join_table.alias)

        template_join_condition: QueryCondition = template_join.joinCondition
        Assertions.assert_equals(
            ["tourn", "templateId"],
            template_join_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_join_condition.operator
        )
        Assertions.assert_equals(
            ["temp", "id"],
            template_join_condition.value.parts
        )

        Assertions.assert_equals(
            1,
            len(template_request.conditionGroup.conditions)
        )

        template_condition: QueryCondition = (
            template_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(
            ["tourn", "id"],
            template_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            template_condition.operator
        )
        Assertions.assert_equals(
            UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
            template_condition.value
        )

        group_check_args, group_check_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[1]
        Assertions.assert_type(QueryRequest, group_check_args[0])

        group_check_request: QueryRequest = group_check_args[0]

        group_check_table: Table = group_check_request.table
        Assertions.assert_equals("predictor", group_check_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            group_check_table.table
        )

        Assertions.assert_equals(
            1,
            len(group_check_request.conditionGroup.conditions)
        )

        group_check_condition: QueryCondition = (
            group_check_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["id"], group_check_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            group_check_condition.operator
        )
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            group_check_condition.value
        )

        group_args, group_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[2]
        Assertions.assert_type(QueryRequest, group_args[0])

        group_request: QueryRequest = group_args[0]

        group_table: Table = group_request.table
        Assertions.assert_equals("predictor", group_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            group_table.table
        )
        Assertions.assert_equals("group", group_table.alias)

        Assertions.assert_equals(
            1,
            len(group_request.conditionGroup.conditions)
        )

        group_condition: QueryCondition = (
            group_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["group", "id"], group_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            group_condition.operator
        )
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            group_condition.value
        )

        group_order_by: OrderBy = group_request.orderBy
        Assertions.assert_equals(
            ["group", "name"],
            group_order_by.column.parts
        )
        Assertions.assert_equals(OrderDirection.ASC, group_order_by.direction)

        team_args, team_kwargs = (
            self.__query_service.retrieve_records.call_args_list
        )[3]
        Assertions.assert_type(QueryRequest, team_args[0])

        team_request: QueryRequest = team_args[0]
        Assertions.assert_equals(5, len(team_request.columns))
        Assertions.assert_equals(
            ["gt", "groupId"],
            team_request.columns[0].parts
        )
        Assertions.assert_equals(["team", "id"], team_request.columns[1].parts)
        Assertions.assert_equals(
            ["team", "name"],
            team_request.columns[2].parts
        )
        Assertions.assert_equals(
            ["team", "imagePath"],
            team_request.columns[3].parts
        )
        Assertions.assert_equals(
            ["team", "confederation"],
            team_request.columns[4].parts
        )

        team_table: Table = team_request.table
        Assertions.assert_equals("predictor", team_table.schema_)
        Assertions.assert_equals(
            "group-teams_5341cff8-df9f-4068-8a42-4b4288ecba87",
            team_table.table
        )
        Assertions.assert_equals("gt", team_table.alias)

        Assertions.assert_equals(2, len(team_request.tableJoins))

        team_join1: TableJoin = team_request.tableJoins[0]
        Assertions.assert_equals(TableJoinType.INNER, team_join1.joinType)

        team_join1_table: Table = team_join1.table
        Assertions.assert_equals("predictor", team_join1_table.schema_)
        Assertions.assert_equals("teams", team_join1_table.table)
        Assertions.assert_equals("team", team_join1_table.alias)

        team_join1_condition: QueryCondition = team_join1.joinCondition
        Assertions.assert_equals(
            ["gt", "teamId"],
            team_join1_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            team_join1_condition.operator
        )
        Assertions.assert_equals(
            ["team", "id"],
            team_join1_condition.value.parts
        )

        team_join2: TableJoin = team_request.tableJoins[1]
        Assertions.assert_equals(TableJoinType.INNER, team_join2.joinType)

        team_join2_table: Table = team_join2.table
        Assertions.assert_equals("predictor", team_join2_table.schema_)
        Assertions.assert_equals(
            "groups_5341cff8-df9f-4068-8a42-4b4288ecba87",
            team_join2_table.table
        )
        Assertions.assert_equals("group", team_join2_table.alias)

        team_join2_condition: QueryCondition = team_join2.joinCondition
        Assertions.assert_equals(
            ["gt", "groupId"],
            team_join2_condition.column.parts
        )
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            team_join2_condition.operator
        )
        Assertions.assert_equals(
            ["group", "id"],
            team_join2_condition.value.parts
        )

        team_condition: QueryCondition = (
            team_request.conditionGroup.conditions
        )[0]
        Assertions.assert_equals(["group", "id"], team_condition.column.parts)
        Assertions.assert_equals(
            ConditionOperator.EQUAL,
            team_condition.operator
        )
        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            team_condition.value
        )

        team_order_by: OrderBy = team_request.orderBy
        Assertions.assert_equals(["team", "name"], team_order_by.column.parts)
        Assertions.assert_equals(OrderDirection.ASC, team_order_by.direction)

        Assertions.assert_equals(
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            group.id
        )
        Assertions.assert_equals("Group A", group.name)
        Assertions.assert_equals(2, len(group.teams))

        group1_team1: Team = group.teams[0]
        Assertions.assert_equals(
            UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
            group1_team1.id
        )
        Assertions.assert_equals("Croatia", group1_team1.name)
        Assertions.assert_equals("HRV.png", group1_team1.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group1_team1.confederation
        )

        group1_team2: Team = group.teams[1]
        Assertions.assert_equals(
            UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"),
            group1_team2.id
        )
        Assertions.assert_equals("Serbia", group1_team2.name)
        Assertions.assert_equals("SRB.png", group1_team2.imagePath)
        Assertions.assert_equals(
            Confederation.UEFA,
            group1_team2.confederation
        )

    def test_should_error_tournament_not_exists_get_group_by_id(self):
        # Given
        self.__tournament_service.get_tournament_by_id.side_effect = (
            HTTPException(
                status_code=404,
                detail="No teams found with a matching id."
            )
        )

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_group_by_id(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No teams found with a matching id.",
            httpe.value.detail
        )

    def test_should_error_tournament_no_group_stage_get_group_by_id(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "leagueTemplateId": None
                    }
                ]
            )
        ]

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_group_by_id(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "The tournament with the supplied id does not have a group stage.",
            httpe.value.detail
        )

    def test_should_error_group_not_exists_get_group_by_id(self):
        # Given
        self.__query_service.retrieve_records.side_effect = [
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=1,
                records=[
                    {
                        "leagueTemplateId": "72119bfa-212b-443c-b992-"
                                            "7dc6983c6a1a"
                    }
                ]
            ),
            QueryResponse(
                referenceId=UUID("ac97eb18-d9b7-40b8-b406-14f90455121a"),
                recordCount=0,
                records=[]
            )
        ]

        # When
        with raises(HTTPException) as httpe:
            self.__service.get_group_by_id(
                UUID("5341cff8-df9f-4068-8a42-4b4288ecba87"),
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals(
            "No groups found with a matching id.",
            httpe.value.detail
        )
