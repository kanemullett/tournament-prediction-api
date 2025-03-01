from typing import Any
from uuid import UUID

from fastapi import HTTPException

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_operator import ConditionOperator
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import DatabaseQueryService
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.knockout_round import KnockoutRound
from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.model.tournament_template import TournamentTemplate
from predictor_api.predictor_api.model.tournament_template_request import TournamentTemplateRequest
from predictor_api.predictor_api.util.predictor_constants import PredictorConstants


class TournamentTemplateService:
    """
    Service for performing tournament template-related actions.

    Attributes:
        __database_query_service (DatabaseQueryService): The database query service.
    """

    def __init__(self, database_query_service: DatabaseQueryService):
        """
        Initialise the TournamentTemplateService.

        Args:
            database_query_service (DatabaseQueryService): The database query service.
        """
        self.__database_query_service = database_query_service

    def get_tournament_templates(self) -> list[TournamentTemplate]:
        """
        Retrieve stored tournament templates.

        Returns:
            list[TournamentTemplate]: The stored tournament templates.
        """
        query_request: QueryRequest = QueryRequest(
            columns=[
                Column.of("tourn", StoreConstants.ID),
                Column(
                    parts=["tourn", "name"],
                    alias="tournamentName"
                ),
                Column(
                    parts=["league", StoreConstants.ID],
                    alias="leagueId"
                ),
                Column(
                    parts=["league", "name"],
                    alias="leagueName"
                ),
                Column.of("league", "groupCount"),
                Column.of("league", "teamsPerGroup"),
                Column.of("league", "homeAndAway"),
                Column(
                    parts=["knock", StoreConstants.ID],
                    alias="knockoutId"
                ),
                Column(
                    parts=["knock", "name"],
                    alias="knockoutName"
                ),
                Column.of("knock", "rounds")
            ],
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=TournamentTemplate.TARGET_TABLE,
                alias="tourn"
            ),
            tableJoins=[
                TableJoin(
                    table=Table(
                        schema=PredictorConstants.PREDICTOR_SCHEMA,
                        table=LeagueTemplate.TARGET_TABLE,
                        alias="league"
                    ),
                    joinCondition=QueryCondition(
                        column=Column.of("tourn", "leagueTemplateId"),
                        operator=ConditionOperator.EQUAL,
                        value=Column.of("league", StoreConstants.ID)
                    ),
                    joinType=TableJoinType.LEFT
                ),
                TableJoin(
                    table=Table(
                        schema=PredictorConstants.PREDICTOR_SCHEMA,
                        table=KnockoutTemplate.TARGET_TABLE,
                        alias="knock"
                    ),
                    joinCondition=QueryCondition(
                        column=Column.of("tourn", "knockoutTemplateId"),
                        operator=ConditionOperator.EQUAL,
                        value=Column.of("knock", StoreConstants.ID)
                    ),
                    joinType=TableJoinType.LEFT
                )
            ]
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        return list(map(lambda record: self.__build_tournament_template(record), query_response.records))

    def create_tournament_templates(
            self,
            tournament_templates: list[TournamentTemplateRequest]
    ) -> list[TournamentTemplate]:
        """
        Create new tournament templates.

        Args:
            tournament_templates (list[TournamentTemplateRequest]): The new tournament templates to create.

        Returns:
            list[TournamentTemplate]: The newly created tournament templates.
        """
        records: list[dict[str, Any]] = list(
            map(lambda tournament_template: tournament_template.model_dump(), tournament_templates)
        )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.INSERT,
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=TournamentTemplate.TARGET_TABLE
            ),
            records=records
        )

        self.__database_query_service.update_records(update_request)

        included_tournaments: list[UUID] = list(map(lambda tournament_template: tournament_template.id, tournament_templates))

        query_request: QueryRequest = QueryRequest(
            columns=[
                Column.of("tourn", StoreConstants.ID),
                Column(
                    parts=["tourn", "name"],
                    alias="tournamentName"
                ),
                Column(
                    parts=["league", StoreConstants.ID],
                    alias="leagueId"
                ),
                Column(
                    parts=["league", "name"],
                    alias="leagueName"
                ),
                Column.of("league", "groupCount"),
                Column.of("league", "teamsPerGroup"),
                Column.of("league", "homeAndAway"),
                Column(
                    parts=["knock", StoreConstants.ID],
                    alias="knockoutId"
                ),
                Column(
                    parts=["knock", "name"],
                    alias="knockoutName"
                ),
                Column.of("knock", "rounds")
            ],
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=TournamentTemplate.TARGET_TABLE,
                alias="tourn"
            ),
            tableJoins=[
                TableJoin(
                    table=Table(
                        schema=PredictorConstants.PREDICTOR_SCHEMA,
                        table=LeagueTemplate.TARGET_TABLE,
                        alias="league"
                    ),
                    joinCondition=QueryCondition(
                        column=Column.of("tourn", "leagueTemplateId"),
                        operator=ConditionOperator.EQUAL,
                        value=Column.of("league", StoreConstants.ID)
                    ),
                    joinType=TableJoinType.LEFT
                ),
                TableJoin(
                    table=Table(
                        schema=PredictorConstants.PREDICTOR_SCHEMA,
                        table=KnockoutTemplate.TARGET_TABLE,
                        alias="knock"
                    ),
                    joinCondition=QueryCondition(
                        column=Column.of("tourn", "knockoutTemplateId"),
                        operator=ConditionOperator.EQUAL,
                        value=Column.of("knock", StoreConstants.ID)
                    ),
                    joinType=TableJoinType.LEFT
                )
            ],
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column.of("tourn", StoreConstants.ID),
                        operator=ConditionOperator.IN,
                        value=included_tournaments
                    )
                ]
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        return list(map(lambda record: self.__build_tournament_template(record), query_response.records))

    def get_tournament_template_by_id(self, tournament_template_id: UUID) -> TournamentTemplate:
        """
        Retrieve a single stored tournament template by its id.

        Args:
            tournament_template_id (UUID): The id of the tournament template to retrieve.

        Returns:
            TournamentTemplate: The retrieved tournament template.
        """
        query_request: QueryRequest = QueryRequest(
            columns=[
                Column.of("tourn", StoreConstants.ID),
                Column(
                    parts=["tourn", "name"],
                    alias="tournamentName"
                ),
                Column(
                    parts=["league", StoreConstants.ID],
                    alias="leagueId"
                ),
                Column(
                    parts=["league", "name"],
                    alias="leagueName"
                ),
                Column.of("league", "groupCount"),
                Column.of("league", "teamsPerGroup"),
                Column.of("league", "homeAndAway"),
                Column(
                    parts=["knock", StoreConstants.ID],
                    alias="knockoutId"
                ),
                Column(
                    parts=["knock", "name"],
                    alias="knockoutName"
                ),
                Column.of("knock", "rounds")
            ],
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=TournamentTemplate.TARGET_TABLE,
                alias="tourn"
            ),
            tableJoins=[
                TableJoin(
                    table=Table(
                        schema=PredictorConstants.PREDICTOR_SCHEMA,
                        table=LeagueTemplate.TARGET_TABLE,
                        alias="league"
                    ),
                    joinCondition=QueryCondition(
                        column=Column.of("tourn", "leagueTemplateId"),
                        operator=ConditionOperator.EQUAL,
                        value=Column.of("league", StoreConstants.ID)
                    ),
                    joinType=TableJoinType.LEFT
                ),
                TableJoin(
                    table=Table(
                        schema=PredictorConstants.PREDICTOR_SCHEMA,
                        table=KnockoutTemplate.TARGET_TABLE,
                        alias="knock"
                    ),
                    joinCondition=QueryCondition(
                        column=Column.of("tourn", "knockoutTemplateId"),
                        operator=ConditionOperator.EQUAL,
                        value=Column.of("knock", StoreConstants.ID)
                    ),
                    joinType=TableJoinType.LEFT
                )
            ],
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column.of("tourn", StoreConstants.ID),
                        operator=ConditionOperator.EQUAL,
                        value=tournament_template_id
                    )
                ]
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        if len(query_response.records) == 0:
            raise HTTPException(status_code=404, detail="No tournament templates found with a matching id.")

        return list(map(lambda record: self.__build_tournament_template(record), query_response.records))[0]

    def delete_tournament_template_by_id(self, tournament_template_id: UUID):
        """
        Delete a single stored tournament template by its id.

        Args:
            tournament_template_id (UUID): The id of the tournament template to delete.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=Tournament.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column.of("templateId"),
                        operator=ConditionOperator.EQUAL,
                        value=tournament_template_id
                    )
                ]
            )
        )

        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        if query_response.recordCount > 0:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete tournament template as it is part of an existing tournament."
            )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.DELETE,
            table=Table(
                schema=PredictorConstants.PREDICTOR_SCHEMA,
                table=TournamentTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column=Column.of(StoreConstants.ID),
                        operator=ConditionOperator.EQUAL,
                        value=tournament_template_id
                    )
                ]
            )
        )

        self.__database_query_service.update_records(update_request)

    @staticmethod
    def __build_tournament_template(record: dict[str, Any]) -> TournamentTemplate:
        """
        Build a TournamentTemplate object with child LeagueTemplate and KnockoutTemplate objects from a database record.

        Args:
            record (dict[str, Any]): The database record.

        Returns:
            TournamentTemplate: The newly created TournamentTemplate object.
        """
        template: TournamentTemplate = TournamentTemplate(
            id=record[StoreConstants.ID],
            name=record["tournamentName"]
        )

        if "leagueId" in record and record["leagueId"] is not None:
            template = template.model_copy(update={
                "league": LeagueTemplate(
                    id=record["leagueId"],
                    name=record["leagueName"],
                    groupCount=record["groupCount"],
                    teamsPerGroup=record["teamsPerGroup"],
                    homeAndAway=record["homeAndAway"]
                )
            })

        if "knockoutId" in record and record["knockoutId"] is not None:
            template = template.model_copy(update={
                "knockout": KnockoutTemplate(
                    id=record["knockoutId"],
                    name=record["knockoutName"],
                    rounds=list(map(lambda record_round: KnockoutRound.model_validate(record_round), record["rounds"]))
                )
            })

        return template
