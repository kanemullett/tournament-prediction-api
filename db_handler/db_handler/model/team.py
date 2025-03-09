from db_handler.db_handler.model.database_record import DatabaseRecord
from predictor_api.predictor_api.model.type.confederation import Confederation


class Team(DatabaseRecord):
    name: str
    imagePath: str
    confederation: Confederation
