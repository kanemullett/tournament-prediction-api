from psycopg2._psycopg import connection, cursor
from typing import Any

from db_handler.db_handler.function.query_builder_function import QueryBuilderFunction
from db_handler.db_handler.function.record_builder_function import RecordBuilderFunction
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.sql_query import SqlQuery
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class DatabaseQueryService:

    def __init__(
            self,
            database_connection: connection,
            query_builder: QueryBuilderFunction,
            record_builder: RecordBuilderFunction) -> None:
        self.__connection = database_connection
        self.__query_builder = query_builder
        self.__record_builder = record_builder

    def retrieve_records(self, query_request: QueryRequest) -> list[dict[str, Any]]:
        this_cursor: cursor = self.__connection.cursor()

        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            schema=query_request.schema_,
            table=query_request.table,
            columns=query_request.columns,
            conditionGroup=query_request.conditionGroup
        )

        this_cursor.execute(self.__query_builder.apply(sql_query))
        rows: list[tuple[Any, ...]] = this_cursor.fetchall()
        column_headers: list[str] = [desc[0] for desc in this_cursor.description]

        this_cursor.close()

        return list(map(lambda row: self.__record_builder.apply(column_headers, row), rows))