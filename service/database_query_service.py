import os
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from typing import Any

from function.query_builder_function import QueryBuilderFunction
from model.query_request import QueryRequest
from model.sql_query import SqlQuery
from model.type.sql_operator import SqlOperator


class DatabaseQueryService:

    def __init__(self) -> None:
        self.__connection = self.__get_connection()
        self.__query_builder = QueryBuilderFunction()

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

        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            schema=query_request.schema_,
            table=query_request.table,
            columns=query_request.columns,
            conditionGroup=query_request.conditionGroup
        )

        print(self.__query_builder.apply(sql_query))
        this_cursor.execute(self.__query_builder.apply(sql_query))
        rows: list[tuple[Any, ...]] = this_cursor.fetchall()

        this_cursor.close()
        return rows
