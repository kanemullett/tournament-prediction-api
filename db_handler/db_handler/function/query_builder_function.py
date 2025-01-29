from typing import Any

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.sql_query import SqlQuery
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class QueryBuilderFunction:

    def apply(self, sql_query: SqlQuery) -> str:
        string_parts: list[str] = [sql_query.operator.value]

        if sql_query.operator == SqlOperator.SELECT:
            string_parts = self.__build_select_statement(sql_query, string_parts)

        string_parts.append(";")

        return " ".join(string_parts)

    def __build_select_statement(self, sql_query: SqlQuery, string_parts: list[str]) -> list[str]:
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
        if table.alias is None:
            return f"{table.schema_}.{table.table}"

        return f"{table.schema_}.{table.table} AS {table.alias}"

    def __build_table_joins(self, table_joins: list[TableJoin]) -> str:
        join_strings: list[str] = list(map(lambda join: self.__build_table_join(join), table_joins))

        return " ".join(join_strings)

    def __build_table_join(self, table_join: TableJoin) -> str:

        return f"{table_join.joinType.value} {self.__build_table(table_join.table)} ON {self.__build_condition(table_join.joinCondition)}"

    def __build_conditions(self, sql_condition_group: QueryConditionGroup) -> str:
        condition_strings: list[str] = list(map(lambda condition: self.__build_condition(condition), sql_condition_group.conditions))

        return f" {sql_condition_group.join.value} ".join(condition_strings)

    def __build_condition(self, sql_condition: QueryCondition) -> str:

        condition_parts: list[str] = [self.__build_column(sql_condition.column, True), sql_condition.operator.value]

        if sql_condition.value is not None:
            condition_parts.append(self.__build_value(sql_condition.value))

        return " ".join(condition_parts)

    def __build_value(self, value: Any) -> str:

        if isinstance(value, str):
            return f"'{value}'"

        if isinstance(value, Column):
            return self.__build_column(value, True)

        return str(value)

    @staticmethod
    def __build_column(column: Column, is_condition: bool) -> str:

        if column.alias is not None and not is_condition:
            return f"{".".join(column.parts)} AS {column.alias}"

        return ".".join(column.parts)
