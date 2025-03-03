from typing import Any
from uuid import UUID

from fastapi import HTTPException

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.util.store_constants import StoreConstants
from predictor_api.predictor_api.model.knockout_template import (
    KnockoutTemplate
)
from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.model.tournament import Tournament
from predictor_api.predictor_api.model.tournament_template import (
    TournamentTemplate
)
from predictor_api.predictor_api.model.tournament_template_request import (
    TournamentTemplateRequest
)
from predictor_api.predictor_api.service.knockout_template_service import (
    KnockoutTemplateService
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class TournamentTemplateService:
    """
    Service for performing tournament template-related actions.

    Attributes:
        __query_service (DatabaseQueryService): The database query service.
    """

    def __init__(
            self,
            database_query_service: DatabaseQueryService,
            knockout_template_service: KnockoutTemplateService):
        """
        Initialise the TournamentTemplateService.

        Args:
            database_query_service (DatabaseQueryService): The database query
                service.
        """
        self.__query_service = database_query_service
        self.__knockout_template_service = knockout_template_service

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
                Column.of("tourn", "knockoutTemplateId"),
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
                Column.of("league", "homeAndAway")
            ],
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                TournamentTemplate.TARGET_TABLE,
                "tourn"
            ),
            tableJoins=[
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        LeagueTemplate.TARGET_TABLE,
                        "league"
                    ),
                    QueryCondition.of(
                        Column.of("tourn", "leagueTemplateId"),
                        Column.of("league", StoreConstants.ID)
                    ),
                    TableJoinType.LEFT
                )
            ]
        )

        query_response: QueryResponse = (
            self.__query_service.retrieve_records(query_request)
        )

        return list(
            map(
                lambda record:
                self.__build_tournament_template(record),
                query_response.records
            )
        )

    def create_tournament_templates(
            self,
            tournament_templates: list[TournamentTemplateRequest]
    ) -> list[TournamentTemplate]:
        """
        Create new tournament templates.

        Args:
            tournament_templates (list[TournamentTemplateRequest]): The new
                tournament templates to create.

        Returns:
            list[TournamentTemplate]: The newly created tournament templates.
        """
        records: list[dict[str, Any]] = list(
            map(
                lambda tournament_template:
                tournament_template.model_dump(),
                tournament_templates
            )
        )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.INSERT,
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                TournamentTemplate.TARGET_TABLE
            ),
            records=records
        )

        self.__query_service.update_records(update_request)

        included_tournaments: list[UUID] = list(
            map(
                lambda tournament_template:
                tournament_template.id,
                tournament_templates
            )
        )

        query_request: QueryRequest = QueryRequest(
            columns=[
                Column.of("tourn", StoreConstants.ID),
                Column(
                    parts=["tourn", "name"],
                    alias="tournamentName"
                ),
                Column.of("tourn", "knockoutTemplateId"),
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
                Column.of("league", "homeAndAway")
            ],
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                TournamentTemplate.TARGET_TABLE,
                "tourn"
            ),
            tableJoins=[
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        LeagueTemplate.TARGET_TABLE,
                        "league"
                    ),
                    QueryCondition.of(
                        Column.of("tourn", "leagueTemplateId"),
                        Column.of("league", StoreConstants.ID)
                    ),
                    TableJoinType.LEFT
                )
            ],
            conditionGroup=QueryConditionGroup.of(
                QueryCondition(
                    column=Column.of("tourn", StoreConstants.ID),
                    operator=ConditionOperator.IN,
                    value=included_tournaments
                )
            )
        )

        query_response: QueryResponse = (
            self.__query_service.retrieve_records(query_request)
        )

        return list(
            map(
                lambda record:
                self.__build_tournament_template(record),
                query_response.records
            )
        )

    def get_tournament_template_by_id(
            self,
            tournament_template_id: UUID) -> TournamentTemplate:
        """
        Retrieve a single stored tournament template by its id.

        Args:
            tournament_template_id (UUID): The id of the tournament template
                to retrieve.

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
                Column.of("tourn", "knockoutTemplateId"),
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
                Column.of("league", "homeAndAway")
            ],
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                TournamentTemplate.TARGET_TABLE,
                "tourn"
            ),
            tableJoins=[
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        LeagueTemplate.TARGET_TABLE,
                        "league"
                    ),
                    QueryCondition.of(
                        Column.of("tourn", "leagueTemplateId"),
                        Column.of("league", StoreConstants.ID)
                    ),
                    TableJoinType.LEFT
                )
            ],
            conditionGroup=QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("tourn", StoreConstants.ID),
                    tournament_template_id
                )
            )
        )

        query_response: QueryResponse = (
            self.__query_service.retrieve_records(query_request)
        )

        if len(query_response.records) == 0:
            raise HTTPException(
                status_code=404,
                detail="No tournament templates found with a matching id."
            )

        return list(
            map(
                lambda record:
                self.__build_tournament_template(record),
                query_response.records
            )
        )[0]

    def delete_tournament_template_by_id(self, tournament_template_id: UUID):
        """
        Delete a single stored tournament template by its id.

        Args:
            tournament_template_id (UUID): The id of the tournament template
                to delete.
        """
        query_request: QueryRequest = QueryRequest(
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Tournament.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("templateId"),
                    tournament_template_id
                )
            )
        )

        query_response: QueryResponse = (
            self.__query_service.retrieve_records(query_request)
        )

        if query_response.recordCount > 0:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete tournament template as it is part of an "
                       "existing tournament."
            )

        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.DELETE,
            table=Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                TournamentTemplate.TARGET_TABLE
            ),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(StoreConstants.ID),
                    tournament_template_id
                )
            )
        )

        self.__query_service.update_records(update_request)

    def __build_tournament_template(
            self,
            record: dict[str, Any]) -> TournamentTemplate:
        """
        Build a TournamentTemplate object with child LeagueTemplate and
        KnockoutTemplate objects from a database record.

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

        if ("knockoutTemplateId" in record and
                record["knockoutTemplateId"] is not None):
            knock_template: KnockoutTemplate = (
                self.__knockout_template_service.get_knockout_template_by_id(
                    record["knockoutTemplateId"]
                )
            )

            template = template.model_copy(update={
                "knockout": knock_template
            })

        return template
