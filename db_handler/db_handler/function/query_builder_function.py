from typing import Any

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.sql_query import SqlQuery
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class QueryBuilderFunction:
    """
    Function for building SQL query strings from SqlQuery objects.
    """

    def apply(self, sql_query: SqlQuery) -> str:
        """
        Convert a SqlQuery object into a SQL query string.

        Args:
            sql_query (SqlQuery): The SqlQuery object to be converted.

        Returns:
            str: The SQL query string.
        """
        string_parts: list[str] = [sql_query.operator.value]

        if sql_query.operator == SqlOperator.SELECT:
            string_parts = self.__build_select_statement(sql_query, string_parts)

        string_parts.append(";")

        return " ".join(string_parts)

    def __build_select_statement(self, sql_query: SqlQuery, string_parts: list[str]) -> list[str]:
        """
        Convert a SqlQuery object representing a SELECT query into a SQL query string.

        Args:
            sql_query (SqlQuery): The SqlQuery object to be converted.
            string_parts (list[str]): The component parts of the SQL query string.

        Returns:
            str: The SQL SELECT query string.

        Examples:
            - SELECT * FROM example_schema.example_table ;
        """
        string_parts.append("*" if sql_query.columns is None else ", ".join(list(map(lambda column: self.__build_column(column, False), sql_query.columns))))
        string_parts.append("FROM")
        string_parts.append(self.__build_table(sql_query.table))

        if sql_query.tableJoins is not None and len(sql_query.tableJoins) > 0:
            string_parts.append(self.__build_table_joins(sql_query.tableJoins))

        if sql_query.conditionGroup is not None and len(sql_query.conditionGroup.conditions) > 0:
            string_parts.append("WHERE")
            string_parts.append(self.__build_conditions(sql_query.conditionGroup))

        return string_parts

    @staticmethod
    def __build_table(table: Table) -> str:
        """
        Convert a Table object into a SQL string.

        Args:
            table (Table): The Table object to be converted.

        Returns:
            str: The SQL table string.

        Examples:
            - example_schema.example_table
            - example_schema.example_table as example
        """
        if table.alias is None:
            return f"{table.schema_}.{table.table}"

        return f"{table.schema_}.{table.table} AS {table.alias}"

    def __build_table_joins(self, table_joins: list[TableJoin]) -> str:
        """
        Convert a list of TableJoin objects into a SQL string.

        Args:
            table_joins (list[TableJoin]): The list of TableJoin objects to be converted.

        Returns:
            str: The SQL table joins string.
        """
        join_strings: list[str] = list(map(lambda join: self.__build_table_join(join), table_joins))

        return " ".join(join_strings)

    def __build_table_join(self, table_join: TableJoin) -> str:
        """
        Convert a TableJoin object into a SQL string.

        Args:
            table_join (TableJoin): The TableJoin object to be converted.

        Returns:
            str: The SQL table join string.

        Examples:
            - INNER JOIN example_schema.join_table AS joiner ON example.id = joiner.id
        """
        return f"{table_join.joinType.value} {self.__build_table(table_join.table)} ON {self.__build_condition(table_join.joinCondition)}"

    def __build_conditions(self, query_condition_group: QueryConditionGroup) -> str:
        """
        Convert a QueryConditionGroup object into a SQL string.

        Args:
            query_condition_group (QueryConditionGroup): The QueryConditionGroup object to be converted.

        Returns:
            str: The SQL condition group string.

        Examples:
            - example.column1 = 'example' AND joiner.column2 < 23
        """
        condition_strings: list[str] = list(map(lambda condition: self.__build_condition(condition), query_condition_group.conditions))

        return f" {query_condition_group.join.value} ".join(condition_strings)

    def __build_condition(self, query_condition: QueryCondition) -> str:
        """
        Convert a QueryCondition object into a SQL string.

        Args:
            query_condition (QueryCondition): The QueryCondition object to be converted.

        Returns:
            str: The SQL condition string.

        Examples:
            - example.column1 = 'example'
            - joiner.column2 < 23
        """
        condition_parts: list[str] = [self.__build_column(query_condition.column, True), query_condition.operator.value]

        if query_condition.value is not None:
            condition_parts.append(self.__build_value(query_condition.value))

        return " ".join(condition_parts)

    def __build_value(self, value: Any) -> str:
        """
        Convert the value of a condition into a SQL string.

        Args:
            value (Any): The value to be converted.

        Returns:
            str: The SQL value string.

        Examples:
            - 'example'
            - 23
            - example_schema.example_table
        """
        if isinstance(value, str):
            return f"'{value}'"

        if isinstance(value, Column):
            return self.__build_column(value, True)

        return str(value)

    @staticmethod
    def __build_column(column: Column, is_condition: bool) -> str:
        """
        Convert a Column object into a SQL string.

        Args:
            column (Column): The Column object to be converted.
            is_condition (bool): True if the column belongs to a condition object.

        Returns:
            str: The SQL column string.

        Examples:
            - example_table.example_column
            - example_table.example_column AS example
        """
        if column.alias is not None and not is_condition:
            return f"{".".join(column.parts)} AS {column.alias}"

        return ".".join(column.parts)
