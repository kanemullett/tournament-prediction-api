from psycopg2._psycopg import connection, cursor

from db_handler.db_handler.function.table_request_builder_function import (
    TableRequestBuilderFunction
)
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_definition import TableDefinition


class DatabaseTableService:
    """
    Service for managing tables in the database.

    Attributes:
        __connection (connection): The database connection.
        __request_builder (TableRequestBuilderFunction): The function to
            build table creation requests from TableDefinition objects.
    """

    def __init__(
            self,
            database_connection: connection,
            request_builder: TableRequestBuilderFunction) -> None:
        """
        Initialise the DatabaseTableService.

        Args:
            database_connection (connection): The database connection.
            request_builder (TableRequestBuilderFunction): The function to
                build table creation requests from TableDefinition objects.
        """
        self.__connection = database_connection
        self.__request_builder: request_builder = request_builder

    def create_table(self, table_definition: TableDefinition) -> None:
        """
        Create a database table from a TableDefinition object.

        Args:
            table_definition (TableDefinition): The table definition.
        """
        this_cursor: cursor = self.__connection.cursor()

        this_cursor.execute(self.__request_builder.apply(table_definition))
        self.__connection.commit()

        this_cursor.close()

    def delete_table(self, table: Table) -> None:
        """
        Delete a database table.

        Args:
            table (Table): The table to be deleted.
        """
        this_cursor: cursor = self.__connection.cursor()

        this_cursor.execute(
            f'DROP TABLE IF EXISTS \"{table.schema_}\".\"{table.table}\";'
        )
        self.__connection.commit()

        this_cursor.close()
