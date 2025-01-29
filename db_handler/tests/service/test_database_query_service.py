from typing import Any
from unittest.mock import MagicMock

from db_handler.db_handler.model.query_request import QueryRequest
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.type.sql_condition_operator import SqlConditionOperator
from db_handler.db_handler.model.type.sql_operator import SqlOperator
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
            schema="test_schema",
            table="test_table",
            columns=["id", "column1", "column2"],
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column="column1",
                        operator=SqlConditionOperator.LESS_THAN,
                        value=23
                    ),
                    QueryCondition(
                        column="column2",
                        operator=SqlConditionOperator.EQUAL,
                        value="hello"
                    )
                ]
            )
        )

        cursor: MagicMock = MagicMock()
        cursor.fetchall.return_value: list[tuple[Any, ...]] = [
            ("id1", 11, "hello")
        ]
        cursor.description = [("id",), ("column1",), ("column2",)]

        self.__connection.cursor.return_value = cursor

        query: str = "SELECT id, column1, column2 FROM test_schema.test_table WHERE column1 < 23 AND column2 = 'hello'"
        self.__query_builder.apply.return_value = query

        self.__record_builder.apply.return_value = {
                "id": "id1",
                "column1": 11,
                "column2": "hello"
            }

        # When
        records: list[dict[str, Any]] = self.__database_query_service.retrieve_records(query_request)

        # Then
        Assertions.assert_true(len(records) == 1)

        built_record: dict[str, Any] = records[0]
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
