from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.query_response import QueryResponse
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.condition_operator import ConditionOperator
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.update_request import UpdateRequest
from db_handler.db_handler.service.database_query_service import DatabaseQueryService
from predictor_common.test_resources.assertions import Assertions


class TestDatabaseQueryService:

    __connection: MagicMock = MagicMock()
    __query_builder: MagicMock = MagicMock()
    __record_builder: MagicMock = MagicMock()

    __database_query_service: DatabaseQueryService = DatabaseQueryService(__connection, __query_builder, __record_builder)

    def test_should_build_and_send_select_query(self):
        # Given
        query_request: QueryRequest = QueryRequest(
            table=Table.of("test_schema", "test_table"),
            columns=[
                Column.of("id"),
                Column.of("column1"),
                Column.of("column2")
            ],
            conditionGroup=QueryConditionGroup.of(
                QueryCondition(
                    column=Column.of("column1"),
                    operator=ConditionOperator.LESS_THAN,
                    value=23
                ),
                QueryCondition.of(Column.of("column2"), "hello")
            )
        )

        cursor: MagicMock = MagicMock()
        cursor.fetchall.return_value: list[tuple[Any, ...]] = [
            ("id1", 11, "hello")
        ]
        cursor.description = [("id",), ("column1",), ("column2",)]

        self.__connection.cursor.return_value = cursor

        query: str = "SELECT id, column1, column2 FROM test_schema.test_table WHERE column1 < 23 AND column2 = 'hello' ;"
        self.__query_builder.apply.return_value = query

        self.__record_builder.apply.return_value = {
                "id": "id1",
                "column1": 11,
                "column2": "hello"
            }

        # When
        query_response: QueryResponse = self.__database_query_service.retrieve_records(query_request)

        # Then
        Assertions.assert_equals(1, query_response.recordCount)
        Assertions.assert_equals(1, len(query_response.records))

        built_record: dict[str, Any] = query_response.records[0]
        Assertions.assert_equals("id1", built_record["id"])
        Assertions.assert_equals(11, built_record["column1"])
        Assertions.assert_equals("hello", built_record["column2"])

        captured_args_query, captured_kwargs = cursor.execute.call_args
        Assertions.assert_equals(query, captured_args_query[0])

        captured_args_query_build, captured_kwargs = self.__query_builder.apply.call_args
        Assertions.assert_equals(SqlOperator.SELECT, captured_args_query_build[0].operator)

        captured_args_record, captured_kwargs = self.__record_builder.apply.call_args
        Assertions.assert_equals(["id", "column1", "column2"], captured_args_record[0])
        Assertions.assert_equals(("id1", 11, "hello"), captured_args_record[1])

    def test_should_build_and_send_insert_query(self):
        # Given
        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.INSERT,
            table=Table.of("test_schema", "test_table"),
            records=[
                {
                    "column1": "value1",
                    "column2": 2,
                    "column3": "value3"
                },
                {
                    "column3": "value3",
                    "column4": 4,
                    "column5": "value5"
                }
            ]
        )

        cursor: MagicMock = MagicMock()
        cursor.rowcount = 2

        self.__connection.cursor.return_value = cursor

        query: str = ("INSERT INTO test_schema.test_table (column1, column2, column3, column4, column5) VALUES "
                      "('value1', 2, 'value3', NULL, NULL), (NULL, NULL, 'value3', 4, 'value5') ;")
        self.__query_builder.apply.return_value = query

        # When
        query_response: QueryResponse = self.__database_query_service.update_records(update_request)

        # Then
        Assertions.assert_type(UUID, query_response.referenceId)
        Assertions.assert_equals(2, query_response.recordCount)
        Assertions.assert_none(query_response.records)

        captured_args_query, captured_kwargs = cursor.execute.call_args
        Assertions.assert_equals(query, captured_args_query[0])

        captured_args_query_build, captured_kwargs = self.__query_builder.apply.call_args
        Assertions.assert_equals(SqlOperator.INSERT, captured_args_query_build[0].operator)
        Assertions.assert_equals(update_request.table, captured_args_query_build[0].table)
        Assertions.assert_equals(update_request.records, captured_args_query_build[0].records)

    def test_should_build_and_send_update_query(self):
        # Given
        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.UPDATE,
            table=Table.of("test_schema", "test_table"),
            records=[
                {
                    "id": "id1",
                    "column1": "value1"
                }
            ]
        )

        cursor: MagicMock = MagicMock()
        cursor.rowcount = 1

        self.__connection.cursor.return_value = cursor

        query: str = ("UPDATE test_schema.test_table SET column1 = CASE WHEN id = 'id1' THEN 'value1' ELSE column1 END "
                      "WHERE id IN ('id1') ;")
        self.__query_builder.apply.return_value = query

        # When
        query_response: QueryResponse = self.__database_query_service.update_records(update_request)

        # Then
        Assertions.assert_type(UUID, query_response.referenceId)
        Assertions.assert_equals(1, query_response.recordCount)
        Assertions.assert_none(query_response.records)

        captured_args_query, captured_kwargs = cursor.execute.call_args
        Assertions.assert_equals(query, captured_args_query[0])

        captured_args_query_build, captured_kwargs = self.__query_builder.apply.call_args
        Assertions.assert_equals(SqlOperator.UPDATE, captured_args_query_build[0].operator)
        Assertions.assert_equals(update_request.table, captured_args_query_build[0].table)
        Assertions.assert_equals(update_request.records, captured_args_query_build[0].records)

    def test_should_build_and_send_delete_query(self):
        # Given
        update_request: UpdateRequest = UpdateRequest(
            operation=SqlOperator.DELETE,
            table=Table.of("test_schema", "test_table"),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition(
                    column=Column.of("column1"),
                    operator=ConditionOperator.LESS_THAN,
                    value=23
                ),
                QueryCondition.of(Column.of("column2"), "hello")
            )
        )

        cursor: MagicMock = MagicMock()
        cursor.rowcount = 1

        self.__connection.cursor.return_value = cursor

        query: str = "DELETE FROM test_schema.test_table WHERE column1 < 23 AND column2 = 'hello';"
        self.__query_builder.apply.return_value = query

        # When
        query_response: QueryResponse = self.__database_query_service.update_records(update_request)

        # Then
        Assertions.assert_type(UUID, query_response.referenceId)
        Assertions.assert_equals(1, query_response.recordCount)
        Assertions.assert_none(query_response.records)

        captured_args_query, captured_kwargs = cursor.execute.call_args
        Assertions.assert_equals(query, captured_args_query[0])

        captured_args_query_build, captured_kwargs = self.__query_builder.apply.call_args
        Assertions.assert_equals(SqlOperator.DELETE, captured_args_query_build[0].operator)
        Assertions.assert_equals(update_request.table, captured_args_query_build[0].table)
        Assertions.assert_equals(update_request.records, captured_args_query_build[0].records)
