from psycopg2._psycopg import connection, cursor

from db_handler.db_handler.function.table_request_builder_function import (
    TableRequestBuilderFunction
)
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_definition import TableDefinition


class DatabaseTableService:

    def __init__(
            self,
            database_connection: connection,
            request_builder: TableRequestBuilderFunction) -> None:
        self.__connection = database_connection
        self.__request_builder: request_builder = request_builder

    def create_table(self, table_definition: TableDefinition) -> None:
        this_cursor: cursor = self.__connection.cursor()

        this_cursor.execute(self.__request_builder.apply(table_definition))
        self.__connection.commit()

        this_cursor.close()

    def delete_table(self, table: Table) -> None:
        this_cursor: cursor = self.__connection.cursor()

        this_cursor.execute(
            f'DROP TABLE \"{table.schema_}\".\"{table.table}\";'
        )
        self.__connection.commit()

        this_cursor.close()
