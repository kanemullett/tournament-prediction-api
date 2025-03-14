from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.round_template import RoundTemplate


class Round(DatabaseRecord, RoundTemplate):
    pass
