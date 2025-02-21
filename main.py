from fastapi import FastAPI

from db_handler.db_handler.function.query_builder_function import QueryBuilderFunction
from db_handler.db_handler.function.record_builder_function import RecordBuilderFunction
from db_handler.db_handler.service.database_query_service import DatabaseQueryService
from db_handler.db_handler.util.database_utils import DatabaseUtils
from predictor_api.predictor_api.controller.tournament_controller import TournamentController


app = FastAPI()

app.include_router(TournamentController(DatabaseQueryService(DatabaseUtils.DATABASE_CONNECTION, QueryBuilderFunction(), RecordBuilderFunction())).router)
