from db_handler.db_handler.service.database_query_service import DatabaseQueryService


class TournamentTemplateService:

    def __init__(self, database_query_service: DatabaseQueryService):
        self.__database_query_service = database_query_service
