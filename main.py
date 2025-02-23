from fastapi import FastAPI

from db_handler.db_handler.function.query_builder_function import QueryBuilderFunction
from db_handler.db_handler.function.record_builder_function import RecordBuilderFunction
from db_handler.db_handler.service.database_initializer_service import DatabaseInitializerService
from db_handler.db_handler.service.database_query_service import DatabaseQueryService
from db_handler.db_handler.util.database_utils import DatabaseUtils
from predictor_api.predictor_api.controller.tournament_controller import TournamentController
from predictor_api.predictor_api.service.tournament_service import TournamentService
from predictor_api.predictor_api.util.predictor_constants import PredictorConstants

app = FastAPI()

database_initializer_service: DatabaseInitializerService = DatabaseInitializerService(DatabaseUtils.DATABASE_CONNECTION, PredictorConstants.PREDICTOR_SCHEMA)
database_initializer_service.initialize_tables()

database_query_service: DatabaseQueryService = DatabaseQueryService(DatabaseUtils.DATABASE_CONNECTION, QueryBuilderFunction(), RecordBuilderFunction())

app.include_router(TournamentController(TournamentService(database_query_service)).router)
