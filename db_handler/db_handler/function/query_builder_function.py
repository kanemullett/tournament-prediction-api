from typing import Any

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.sql_query import SqlQuery
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
        string_parts.append(self.__build_table(sql_query.schema_, sql_query.table, sql_query.alias))

        if sql_query.conditionGroup is not None and len(sql_query.conditionGroup.conditions) > 0:
            string_parts.append("WHERE")
            string_parts.append(self.__build_conditions(sql_query.conditionGroup))

        return string_parts

    @staticmethod
    def __build_table(schema: str, table: str, alias: str) -> str:
        if alias is None:
            return f"{schema}.{table}"

        return f"{schema}.{table} AS {alias}"

    def __build_conditions(self, sql_condition_group: QueryConditionGroup) -> str:
        condition_strings: list[str] = list(map(lambda condition: self.__build_condition(condition), sql_condition_group.conditions))

        return f" {sql_condition_group.join.value} ".join(condition_strings)

    def __build_condition(self, sql_condition: QueryCondition) -> str:

        condition_parts: list[str] = [self.__build_column(sql_condition.column, True), sql_condition.operator.value]

        if sql_condition.value is not None:
            condition_parts.append(self.__build_value(sql_condition.value))

        return " ".join(condition_parts)

    @staticmethod
    def __build_value(value: Any) -> str:

        if isinstance(value, str):
            return f"'{value}'"

        return str(value)

    @staticmethod
    def __build_column(column: Column, is_condition: bool) -> str:

        if column.alias is not None and not is_condition:
            return f"{".".join(column.parts)} AS {column.alias}"

        return ".".join(column.parts)
