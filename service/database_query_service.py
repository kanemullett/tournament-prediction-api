import os
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from typing import Any

from model.query_request import QueryRequest


class DatabaseQueryService:

    def __init__(self) -> None:
        self.__connection = self.__get_connection()

    @staticmethod
    def __get_connection() -> connection:
        try:
            return connect(
                host=os.environ.get("POSTGRES_HOST"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                port=os.environ.get("POSTGRES_PORT")
            )

        except Exception as e:
            print("Error connecting to the database:", e)

    def retrieve_records(self, query_request: QueryRequest) -> list[tuple[Any, ...]]:
        this_cursor: cursor = self.__connection.cursor()

        this_cursor.execute(f"SELECT * FROM {query_request.schema_}.{query_request.table};")
        rows: list[tuple[Any, ...]] = this_cursor.fetchall()

        this_cursor.close()
        return rows
