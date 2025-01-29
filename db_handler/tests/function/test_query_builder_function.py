from db_handler.db_handler.function.query_builder_function import QueryBuilderFunction
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.sql_query import SqlQuery
from db_handler.db_handler.model.type.sql_condition_operator import SqlConditionOperator
from db_handler.db_handler.model.type.sql_join import SqlJoin
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from predictor_common.test_resources.assertions import Assertions


class TestQueryBuilderFunction:

    __query_builder: QueryBuilderFunction = QueryBuilderFunction()

    def test_should_build_select_statement_with_schema_and_table(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            schema="test_schema",
            table="test_table"
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals("SELECT * FROM test_schema.test_table ;", query_string)

    def test_should_build_select_statement_with_single_column(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            schema="test_schema",
            table="test_table",
            columns=["column1"]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals("SELECT column1 FROM test_schema.test_table ;", query_string)

    def test_should_build_select_statement_with_multiple_columns(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            schema="test_schema",
            table="test_table",
            columns=["column1", "column2", "column3"]
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals("SELECT column1, column2, column3 FROM test_schema.test_table ;", query_string)

    def test_should_build_select_statement_with_single_condition(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            schema="test_schema",
            table="test_table",
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column="column1",
                        operator=SqlConditionOperator.EQUAL,
                        value="test_value"
                    )
                ]
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals("SELECT * FROM test_schema.test_table WHERE column1 = 'test_value' ;", query_string)

    def test_should_build_select_statement_with_multiple_condition(self):
        # Given
        sql_query: SqlQuery = SqlQuery(
            operator=SqlOperator.SELECT,
            schema="test_schema",
            table="test_table",
            conditionGroup=QueryConditionGroup(
                conditions=[
                    QueryCondition(
                        column="column1",
                        operator=SqlConditionOperator.EQUAL,
                        value="test_value"
                    ),
                    QueryCondition(
                        column="column2",
                        operator=SqlConditionOperator.EQUAL,
                        value=23
                    )
                ],
                join=SqlJoin.OR
            )
        )

        # When
        query_string: str = self.__query_builder.apply(sql_query)

        # Then
        Assertions.assert_equals("SELECT * FROM test_schema.test_table WHERE column1 = 'test_value' OR column2 = 23 ;", query_string)
