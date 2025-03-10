from db_handler.db_handler.function.query_builder_function import (
    QueryBuilderFunction
)
from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.sql_query import SqlQuery
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.condition_operator import (
    ConditionOperator
)
from db_handler.db_handler.model.type.condition_join import ConditionJoin
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.model.type.table_join_type import TableJoinType
from predictor_common.test_resources.assertions import Assertions

from fastapi import HTTPException
from pytest import raises


class TestQueryBuilderFunction:

    __query_builder: QueryBuilderFunction = QueryBuilderFunction()

    def test_should_build_select_statement_with_schema_and_table(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=Table.of("test_schema", "test_table")
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "SELECT * FROM \"test_schema\".\"test_table\" ;",
            query_string
        )

    def test_should_build_select_statement_with_single_column(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=Table.of("test_schema", "test_table"),
            columns=[
                Column.of("column1")
            ]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "SELECT \"column1\" FROM \"test_schema\".\"test_table\" ;",
            query_string
        )

    def test_should_build_select_statement_with_multiple_columns(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=Table.of("test_schema", "test_table"),
            columns=[
                Column.of("column1"),
                Column.of("column2"),
                Column.of("column3")
            ]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "SELECT \"column1\", \"column2\", \"column3\" FROM "
            "\"test_schema\".\"test_table\" ;",
            query_string
        )

    def test_should_build_select_statement_with_single_condition(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=Table.of("test_schema", "test_table"),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition.of(Column.of("column1"), "test_value")
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "SELECT * FROM \"test_schema\".\"test_table\" WHERE \"column1\" "
            "= 'test_value' ;",
            query_string
        )

    def test_should_build_select_statement_with_multiple_conditions(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=Table.of("test_schema", "test_table"),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition.of(Column.of("column1"), "test_value"),
                    QueryCondition.of(Column.of("column2"), 23)
                ],
                join=ConditionJoin.OR
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "SELECT * FROM \"test_schema\".\"test_table\" "
            "WHERE \"column1\" = 'test_value' OR \"column2\" = 23 ;",
            query_string
        )

    def test_select_statement_with_multiple_conditions_and_alias(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=Table.of("test_schema", "test_table", "my_table"),
            columns=[
                Column(
                    parts=["my_table", "name"],
                    alias="user_name"
                )
            ],
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition.of(
                        Column(
                            parts=["my_table", "column1"],
                            alias="should_ignore"
                        ),
                        "test_value"
                    ),
                    QueryCondition.of(
                        Column(
                            parts=["my_table", "column2"],
                            alias="should_ignore"
                        ),
                        23
                    )
                ],
                join=ConditionJoin.OR
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "SELECT \"my_table\".\"name\" AS \"user_name\" FROM "
            "\"test_schema\".\"test_table\" AS \"my_table\" WHERE "
            "\"my_table\".\"column1\" = 'test_value' OR "
            "\"my_table\".\"column2\" = 23 ;",
            query_string
        )

    def test_select_statement_with_multiple_conditions_and_table_joins(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=Table.of("test_schema", "test_table", "my_table"),
            columns=[
                Column(
                    parts=["my_table", "name"],
                    alias="user_name"
                )
            ],
            tableJoins=[
                TableJoin.of(
                    Table.of("test_schema", "join_table_one", "first_joiner"),
                    QueryCondition.of(
                        Column.of("my_table", "id"),
                        Column.of("first_joiner", "baseId")
                    ),
                    TableJoinType.INNER
                ),
                TableJoin.of(
                    Table.of("test_schema", "join_table_two", "second_joiner"),
                    QueryCondition.of(
                        Column.of("my_table", "id"),
                        Column.of("second_joiner", "baseId")
                    ),
                    TableJoinType.LEFT
                )
            ],
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition.of(
                        Column(
                            parts=["my_table", "column1"],
                            alias="should_ignore"
                        ),
                        "test_value"
                    ),
                    QueryCondition.of(
                        Column(
                            parts=["my_table", "column2"],
                            alias="should_ignore"
                        ),
                        23
                    )
                ],
                join=ConditionJoin.OR
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "SELECT \"my_table\".\"name\" AS \"user_name\" FROM "
            "\"test_schema\".\"test_table\" AS \"my_table\" INNER JOIN "
            "\"test_schema\".\"join_table_one\" AS \"first_joiner\" ON "
            "\"my_table\".\"id\" = \"first_joiner\".\"baseId\" LEFT JOIN "
            "\"test_schema\".\"join_table_two\" AS \"second_joiner\" ON "
            "\"my_table\".\"id\" = \"second_joiner\".\"baseId\" WHERE "
            "\"my_table\".\"column1\" = 'test_value' OR "
            "\"my_table\".\"column2\" = 23 ;",
            query_string
        )

    def test_should_build_insert_statement_with_single_record(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.INSERT,
            table=Table.of("test_schema", "test_table"),
            records=[
                {
                    "col1": "val1",
                    "col2": 2
                }
            ]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "INSERT INTO \"test_schema\".\"test_table\" (\"col1\", \"col2\") "
            "VALUES ('val1', 2) ;",
            query_string
        )

    def test_should_build_insert_statement_with_multiple_records(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.INSERT,
            table=Table.of("test_schema", "test_table"),
            records=[
                {
                    "col1": "val1",
                    "col2": 2
                },
                {
                    "col1": 3,
                    "col2": "val4"
                }
            ]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "INSERT INTO \"test_schema\".\"test_table\" (\"col1\", \"col2\") "
            "VALUES ('val1', 2), (3, 'val4') ;",
            query_string
        )

    def test_insert_statement_with_multiple_records_and_missing_columns(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.INSERT,
            table=Table.of("test_schema", "test_table"),
            records=[
                {
                    "col2": 2
                },
                {
                    "col1": "val3"
                }
            ]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "INSERT INTO \"test_schema\".\"test_table\" (\"col1\", \"col2\") "
            "VALUES (NULL, 2), ('val3', NULL) ;",
            query_string
        )

    def test_should_build_update_statement_with_single_record(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.UPDATE,
            table=Table.of("test_schema", "test_table"),
            records=[
                {
                    "id": "id1",
                    "col1": "val1",
                    "col2": 2
                }
            ]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)
        expected: str = ("UPDATE \"test_schema\".\"test_table\" SET \"col1\" "
                         "= CASE WHEN \"id\" = 'id1' THEN 'val1' ELSE "
                         "\"col1\" END, \"col2\" = CASE WHEN \"id\" = 'id1' "
                         "THEN 2 ELSE \"col2\" END WHERE \"id\" IN ('id1') ;")

        # Then
        Assertions.assert_equals(expected, query_string)

    def test_should_build_update_statement_with_multiple_records(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.UPDATE,
            table=Table.of("test_schema", "test_table"),
            records=[
                {
                    "id": "id1",
                    "col1": "val1",
                    "col2": 2
                },
                {
                    "id": "id2",
                    "col2": 5,
                    "col3": "val3"
                }
            ]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)
        expected: str = ("UPDATE \"test_schema\".\"test_table\" SET \"col1\" "
                         "= CASE WHEN \"id\" = 'id1' THEN 'val1' ELSE "
                         "\"col1\" END, \"col2\" = CASE WHEN \"id\" = 'id1' "
                         "THEN 2 WHEN \"id\" = 'id2' THEN 5 ELSE \"col2\" "
                         "END, \"col3\" = CASE WHEN \"id\" = 'id2' THEN "
                         "'val3' ELSE \"col3\" END WHERE \"id\" IN ('id1', "
                         "'id2') ;")

        # Then
        Assertions.assert_equals(expected, query_string)

    def test_should_throw_exception_if_missing_id(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.UPDATE,
            table=Table.of("test_schema", "test_table"),
            records=[
                {
                    "id": "id1",
                    "col1": "val1",
                    "col2": 2
                },
                {
                    "col2": 5,
                    "col3": "val3"
                }
            ]
        )

        # When
        with raises(HTTPException) as httpe:
            self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(400, httpe.value.status_code)
        Assertions.assert_equals(
            "All records in update requests should contain id field.",
            httpe.value.detail
        )

    def test_should_build_delete_statement_with_single_condition(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.DELETE,
            table=Table.of("test_schema", "test_table"),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition.of(Column.of("column1"), "test_value")
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "DELETE FROM \"test_schema\".\"test_table\" WHERE \"column1\" = "
            "'test_value' ;",
            query_string
        )

    def test_should_build_delete_statement_with_multiple_conditions(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.DELETE,
            table=Table.of("test_schema", "test_table"),
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition.of(Column.of("column1"), "test_value"),
                    QueryCondition.of(Column.of("column2"), 23)
                ],
                join=ConditionJoin.OR
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "DELETE FROM \"test_schema\".\"test_table\" WHERE \"column1\" = "
            "'test_value' OR \"column2\" = 23 ;",
            query_string
        )

    def test_should_build_statement_with_in_condition(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            table=Table.of("test_schema", "test_table"),
            conditionGroup=QueryConditionGroup.of(
                QueryCondition(
                    column=Column.of("column1"),
                    operator=ConditionOperator.IN,
                    value=["val", 23]
                )
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals(
            "SELECT * FROM \"test_schema\".\"test_table\" WHERE \"column1\" "
            "IN ('val', 23) ;",
            query_string
        )
