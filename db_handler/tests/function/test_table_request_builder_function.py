from db_handler.db_handler.function.table_request_builder_function import (
    TableRequestBuilderFunction
)
from db_handler.db_handler.model.column_definition import ColumnDefinition
from db_handler.db_handler.model.table_definition import TableDefinition
from db_handler.db_handler.model.type.sql_data_type import SqlDataType
from predictor_common.test_resources.assertions import Assertions


class TestTableRequestBuilderFunction:

    __request_builder_function: TableRequestBuilderFunction = (
        TableRequestBuilderFunction()
    )

    def test_should_build_table_request(self):
        # Given
        table_definition: TableDefinition = TableDefinition(
            schema="test-schema",
            table="test-table",
            columns=[
                ColumnDefinition(
                    name="id",
                    dataType=SqlDataType.VARCHAR,
                    primaryKey=True
                ),
                ColumnDefinition.of("name", SqlDataType.VARCHAR),
                ColumnDefinition.of("age", SqlDataType.INTEGER),
                ColumnDefinition.of("hasPets", SqlDataType.BOOLEAN),
                ColumnDefinition.of(
                    "joinDate",
                    SqlDataType.TIMESTAMP_WITH_TIME_ZONE
                )
            ]
        )

        # When
        request_string: str = self.__request_builder_function.apply(
            table_definition
        )

        # Then
        Assertions.assert_equals(
            "CREATE TABLE IF NOT EXISTS "
            "\"test-schema\".\"test-table\" ("
            "\"id\" VARCHAR PRIMARY KEY, "
            "\"name\" VARCHAR, "
            "\"age\" INTEGER, "
            "\"hasPets\" BOOLEAN, "
            "\"joinDate\" TIMESTAMP WITH TIME ZONE"
            ") ;",
            request_string
        )
