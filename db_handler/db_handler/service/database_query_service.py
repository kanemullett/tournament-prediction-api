from psycopg2._psycopg import connection, cursor
from typing import Any
from uuid import uuid4

from db_handler.db_handler.function.query_builder_function import QueryBuilderFunction
from db_handler.db_handler.function.record_builder_function import RecordBuilderFunction
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.sql_query import SqlQuery
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest


class DatabaseQueryService:
    """
    Service for querying the application's database.

    Attributes:
        __connection (connection): The database connection.
        __query_builder (QueryBuilderFunction): The function to build query strings from SqlQuery objects.
        __record_builder (RecordBuilderFunction): The function to build records from database responses.
    """

    def __init__(
            self,
            database_connection: connection,
            query_builder: QueryBuilderFunction,
            record_builder: RecordBuilderFunction) -> None:
        """
        Initialise the DatabaseQueryService.

        Args:
            database_connection (connection): The database connection.
            query_builder (QueryBuilderFunction): The function to build query strings from SqlQuery objects.
            record_builder (RecordBuilderFunction): The function to build records from database responses.
        """
        self.__connection = database_connection
        self.__query_builder = query_builder
        self.__record_builder = record_builder

    def retrieve_records(self, query_request: QueryRequest) -> QueryResponse:
        """
        Retrieve records from the database based on a query request specification.

        Args:
            query_request (QueryRequest): The query request specification.

        Returns:
            list[dict[str, Any]]: The records to return.
        """
        this_cursor: cursor = self.__connection.cursor()

        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=query_request.table,
            columns=query_request.columns,
            tableJoins=query_request.tableJoins,
            conditionGroup=query_request.conditionGroup
        )

        this_cursor.execute(self.__query_builder.apply(sql_query))
        rows: list[tuple[Any, ...]] = this_cursor.fetchall()
        column_headers: list[str] = [desc[0] for desc in this_cursor.description]

        this_cursor.close()

        records: list[dict[str, Any]] = list(map(lambda row: self.__record_builder.apply(column_headers, row), rows))

        return QueryResponse(
            referenceId=uuid4(),
            recordCount=len(rows),
            records=records
        )

    def update_records(self, update_request: UpdateRequest) -> QueryResponse:
        this_cursor: cursor = self.__connection.cursor()

        sql_query: SqlQuery = SqlQuery(
            operator=update_request.operation,
            table=update_request.table,
            conditionGroup=update_request.conditionGroup,
            records=update_request.records
        )

        this_cursor.execute(self.__query_builder.apply(sql_query))
        record_count: int = this_cursor.rowcount

        self.__connection.commit()

        this_cursor.close()

        return QueryResponse(
            referenceId=uuid4(),
            recordCount=record_count
        )
