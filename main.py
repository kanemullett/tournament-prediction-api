from typing import Any

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from db_handler.db_handler.function.query_builder_function import (
    QueryBuilderFunction
)
from db_handler.db_handler.function.record_builder_function import (
    RecordBuilderFunction
)
from db_handler.db_handler.function.table_request_builder_function import (
    TableRequestBuilderFunction
)
from db_handler.db_handler.service.database_initializer_service import (
    DatabaseInitializerService
)
from db_handler.db_handler.service.database_query_service import (
    DatabaseQueryService
)
from db_handler.db_handler.service.database_table_service import (
    DatabaseTableService
)
from db_handler.db_handler.util.database_utils import DatabaseUtils
from predictor_api.predictor_api.controller.knockout_template_controller import (  # noqa: E501
    KnockoutTemplateController
)
from predictor_api.predictor_api.controller.league_template_controller import (
    LeagueTemplateController
)
from predictor_api.predictor_api.controller.team_controller import (
    TeamController
)
from predictor_api.predictor_api.controller.tournament_controller import (
    TournamentController
)
from predictor_api.predictor_api.controller.tournament_template_controller import (  # noqa: E501
    TournamentTemplateController
)
from predictor_api.predictor_api.service.knockout_template_service import (
    KnockoutTemplateService
)
from predictor_api.predictor_api.service.league_template_service import (
    LeagueTemplateService
)
from predictor_api.predictor_api.service.team_service import TeamService
from predictor_api.predictor_api.service.tournament_service import (
    TournamentService
)
from predictor_api.predictor_api.service.tournament_template_service import (
    TournamentTemplateService
)
from predictor_api.predictor_api.util.predictor_constants import (
    PredictorConstants
)


class ExcludeNoneJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        # Automatically exclude None values from all responses
        return super().render(jsonable_encoder(content, exclude_none=True))


app = FastAPI(default_response_class=ExcludeNoneJSONResponse)

database_initializer_service: DatabaseInitializerService = (
    DatabaseInitializerService(
        DatabaseUtils.DATABASE_CONNECTION,
        PredictorConstants.PREDICTOR_SCHEMA
    )
)
database_initializer_service.initialize_tables()

database_query_service: DatabaseQueryService = DatabaseQueryService(
    DatabaseUtils.DATABASE_CONNECTION,
    QueryBuilderFunction(),
    RecordBuilderFunction()
)
database_table_service: DatabaseTableService = DatabaseTableService(
    DatabaseUtils.DATABASE_CONNECTION,
    TableRequestBuilderFunction()
)
knockout_template_service: KnockoutTemplateService = KnockoutTemplateService(
    database_query_service
)

app.include_router(
    TournamentController(
        TournamentService(database_query_service, database_table_service)
    ).router
)
app.include_router(
    TournamentTemplateController(
        TournamentTemplateService(
            database_query_service,
            knockout_template_service
        )
    ).router
)
app.include_router(
    LeagueTemplateController(
        LeagueTemplateService(database_query_service)
    ).router
)
app.include_router(
    KnockoutTemplateController(
        knockout_template_service
    ).router
)
app.include_router(
    TeamController(
        TeamService(
            database_query_service
        )
    ).router
)
