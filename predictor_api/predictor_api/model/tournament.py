from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.type.competition import Competition


class Tournament(DatabaseRecord):
    year: int
    competition: Competition
