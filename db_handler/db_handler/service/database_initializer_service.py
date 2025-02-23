from pathlib import Path

from psycopg2._psycopg import connection, cursor


class DatabaseInitializerService:
    """
    Service for initializing the database tables that are required on start-up.

    Attributes:
        __database_connection (connection): The database connection.
        __application_schema (str): The schema of the application.
    """
    __sql_folder: str = f"sql/"

    def __init__(self, database_connection: connection, application_schema: str) -> None:
        """
        Initialise the DatabaseInitializerService.

        Args:
            database_connection (connection): The database connection.
            application_schema (str): The schema of the application.
        """
        self.__database_connection = database_connection
        self.__application_schema = application_schema

    def initialize_tables(self) -> None:
        """
        Initialize the tables the application requires upon start-up.
        """
        self.__create_application_schema()

        for table in self.__get_tables_to_create():
            self.__create_table(table)

    def __create_application_schema(self) -> None:
        """
        Create the database schema for the application.
        """
        self.__execute_database_action(f"CREATE SCHEMA IF NOT EXISTS {self.__application_schema};")

    def __get_tables_to_create(self) -> list[str]:
        """
        Retrieve the names of the template files to create database tables from.

        Returns:
            list[str]: List of table template filenames.
        """
        folder_path = Path(f"{self.__sql_folder}{self.__application_schema}/tables/")

        return [file.name for file in folder_path.iterdir() if file.is_file()]

    def __create_table(self, table: str) -> None:
        """
        Create a database table from its template file.

        Args:
            table (str): The filename of the table's template.
        """
        with open(f"{self.__sql_folder}{self.__application_schema}/tables/{table}", "r") as file:
            sql_string = file.read()

        self.__execute_database_action(sql_string)

    def __execute_database_action(self, sql_string: str) -> None:
        """
        Execute an action within the database.

        Args:
            sql_string (str): The SQL query action to perform.
        """
        this_cursor: cursor = self.__database_connection.cursor()
        this_cursor.execute(sql_string)
        self.__database_connection.commit()
        this_cursor.close()
