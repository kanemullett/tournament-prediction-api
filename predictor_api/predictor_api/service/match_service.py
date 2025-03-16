from typing import Any
from uuid import UUID

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.order_by import OrderBy
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_join import ConditionJoin
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.group import Group
from predictor_api.predictor_api.model.match import Match
from predictor_api.predictor_api.model.round import Round
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_api.predictor_api.service.group_service import GroupService
from predictor_api.predictor_api.service.round_service import RoundService
from predictor_api.predictor_api.service.tournament_service import (
    TournamentService
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class MatchService:

    def __init__(
            self,
            database_query_service: DatabaseQueryService,
            tournament_service: TournamentService,
            group_service: GroupService,
            round_service: RoundService) -> None:
        self.__query_service = database_query_service
        self.__tournament_service = tournament_service
        self.__group_service = group_service
        self.__round_service = round_service

    def get_matches(
            self,
            tournament_id: UUID,
            group_id: UUID = None,
            group_match_day: int = None,
            round_id: UUID = None) -> list[Match]:
        self.__tournament_service.get_tournament_by_id(tournament_id)

        table_joins: list[TableJoin] = [
            TableJoin.of(
                Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Team.TARGET_TABLE,
                    "home"
                ),
                QueryCondition.of(
                    Column.of("match", "homeTeamId"),
                    Column.of("home", StoreConstants.ID)
                ),
                TableJoinType.LEFT
            ),
            TableJoin.of(
                Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Team.TARGET_TABLE,
                    "away"
                ),
                QueryCondition.of(
                    Column.of("match", "awayTeamId"),
                    Column.of("away", StoreConstants.ID)
                ),
                TableJoinType.LEFT
            )
        ]

        order_by: list[OrderBy] = [
            OrderBy.of(
                Column.of("match", "kickoff")
            ),
            OrderBy.of(
                Column.of("match", "groupMatchDay")
            )
        ]

        if self.__group_service.tournament_has_group_stage(tournament_id):
            table_joins.append(
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Group.get_target_table(tournament_id),
                        "group"
                    ),
                    QueryCondition.of(
                        Column.of("match", "groupId"),
                        Column.of("group", StoreConstants.ID)
                    ),
                    TableJoinType.LEFT
                )
            )

            order_by.insert(
                1,
                OrderBy.of(
                    Column.of("group", "name")
                )
            )

        if self.__round_service.tournament_has_knockout_stage(tournament_id):
            table_joins.append(
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Round.get_target_table(tournament_id),
                        "round"
                    ),
                    QueryCondition.of(
                        Column.of("match", "roundId"),
                        Column.of("round", StoreConstants.ID)
                    ),
                    TableJoinType.LEFT
                )
            )

            order_by.append(
                OrderBy.of(
                    Column.of("round", "roundOrder")
                )
            )

        conditions: list[QueryCondition] = []

        if group_id is not None:
            conditions.append(
                QueryCondition.of(
                    Column.of("match", "groupId"),
                    group_id
                )
            )

        if group_match_day is not None:
            conditions.append(
                QueryCondition.of(
                    Column.of("match", "groupMatchDay"),
                    group_match_day
                )
            )

        if round_id is not None:
            conditions.append(
                QueryCondition.of(
                    Column.of("match", "roundId"),
                    round_id
                )
            )

        condition_group: QueryConditionGroup | None = None

        if len(conditions) > 0:
            condition_group = QueryConditionGroup(
                conditions=conditions,
                join=ConditionJoin.AND
            )

        response: QueryResponse = self.__query_service.retrieve_records(
            QueryRequest(
                columns=[
                    Column(
                        parts=["match", StoreConstants.ID],
                        alias="matchId"
                    ),
                    Column(
                        parts=["home", StoreConstants.ID],
                        alias="homeId"
                    ),
                    Column(
                        parts=["home", "name"],
                        alias="homeName"
                    ),
                    Column(
                        parts=["home", "imagePath"],
                        alias="homeImagePath"
                    ),
                    Column(
                        parts=["home", "confederation"],
                        alias="homeConfederation"
                    ),
                    Column(
                        parts=["away", StoreConstants.ID],
                        alias="awayId"
                    ),
                    Column(
                        parts=["away", "name"],
                        alias="awayName"
                    ),
                    Column(
                        parts=["away", "imagePath"],
                        alias="awayImagePath"
                    ),
                    Column(
                        parts=["away", "confederation"],
                        alias="awayConfederation"
                    ),
                    Column.of("match", "kickoff"),
                    Column.of("match", "groupMatchDay"),
                    Column.of("match", "groupId"),
                    Column.of("match", "roundId")
                ],
                table=Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    Match.get_target_table(tournament_id),
                    "match"
                ),
                tableJoins=table_joins,
                conditionGroup=condition_group,
                orderBy=order_by
            )
        )

        return list(
            map(
                lambda record:
                self.__build_match(record),
                response.records
            )
        )

    @staticmethod
    def __build_match(record: dict[str, Any]) -> Match:
        home: Team | None = None
        if record["homeId"] is not None:
            home = Team(
                id=UUID(record["homeId"]),
                name=record["homeName"],
                imagePath=record["homeImagePath"],
                confederation=Confederation(record["homeConfederation"])
            )

        away: Team | None = None
        if record["awayId"] is not None:
            away = Team(
                id=UUID(record["awayId"]),
                name=record["awayName"],
                imagePath=record["awayImagePath"],
                confederation=Confederation(record["awayConfederation"])
            )

        return Match(
            id=record["matchId"],
            homeTeam=home,
            awayTeam=away,
            kickoff=record.get("kickoff"),
            groupMatchDay=record.get("groupMatchDay"),
            groupId=record.get("groupId"),
            roundId=record.get("roundId")
        )
