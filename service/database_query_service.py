import os
from psycopg2 import connect
from psycopg2._psycopg import cursor
from typing import Any

from model.query_request import QueryRequest


class DatabaseQueryService:

    def __init__(self) -> None:
        self.__cursor = self.__get_cursor()

    @staticmethod
    def __get_cursor() -> cursor:
        try:
            connection = connect(
                host=os.environ.get("POSTGRES_HOST"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                port=os.environ.get("POSTGRES_PORT")
            )

            return connection.cursor()

        except Exception as e:
            print("Error connecting to the database:", e)

    def test_connection(self):
        self.__cursor.execute("SELECT * FROM predictor.test;")
        rows = self.__cursor.fetchall()
        for row in rows:
            print(row)

    def retrieve_records(self, query_request: QueryRequest) -> list[tuple[Any, ...]]:
        self.__cursor.execute(f"SELECT * FROM {query_request.schema_}.{query_request.table};")
        return self.__cursor.fetchall()
