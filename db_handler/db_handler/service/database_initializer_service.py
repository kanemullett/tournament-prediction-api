from psycopg2._psycopg import connection, cursor

from predictor_api.predictor_api.util.predictor_constants import PredictorConstants


class DatabaseInitializerService:

    __tables: list[str] = ["tournaments"]

    def __init__(self, database_connection: connection) -> None:
        self.__database_connection = database_connection

    def initialize_tables(self) -> None:
        self.__initialize_schema()

        with open("sql/tables/tournaments.sql", "r") as file:
            sql_string = file.read()

        self.__execute_database_action(sql_string)

    def __initialize_schema(self) -> None:
        self.__execute_database_action(f"CREATE SCHEMA IF NOT EXISTS {PredictorConstants.PREDICTOR_SCHEMA};")

    def __execute_database_action(self, sql_string: str) -> None:
        this_cursor: cursor = self.__database_connection.cursor()
        this_cursor.execute(sql_string)
        self.__database_connection.commit()
        this_cursor.close()
