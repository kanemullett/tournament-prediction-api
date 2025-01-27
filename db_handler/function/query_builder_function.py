from typing import Any

from db_handler.model.sql_condition import SqlCondition
from db_handler.model.sql_condition_group import SqlConditionGroup
from db_handler.model.sql_query import SqlQuery
from db_handler.model.type.sql_operator import SqlOperator


class QueryBuilderFunction:

    def apply(self, sql_query: SqlQuery) -> str:
        string_parts: list[str] = [sql_query.operator.value]

        if sql_query.operator == SqlOperator.SELECT:
            string_parts = self.__build_select_statement(sql_query, string_parts)

        string_parts.append(";")

        return " ".join(string_parts)

    def __build_select_statement(self, sql_query: SqlQuery, string_parts: list[str]) -> list[str]:
        string_parts.append("*" if sql_query.columns is None else ", ".join(sql_query.columns))
        string_parts.append("FROM")
        string_parts.append(f"{sql_query.schema_}.{sql_query.table}")

        if sql_query.conditionGroup is not None and len(sql_query.conditionGroup.conditions) > 0:
            string_parts.append("WHERE")
            string_parts.append(self.__build_conditions(sql_query.conditionGroup))

        return string_parts

    def __build_conditions(self, sql_condition_group: SqlConditionGroup) -> str:
        condition_strings: list[str] = list(map(lambda condition: self.__build_condition(condition), sql_condition_group.conditions))

        return f" {sql_condition_group.join.value} ".join(condition_strings)

    def __build_condition(self, sql_condition: SqlCondition) -> str:

        condition_parts: list[str] = [sql_condition.column, sql_condition.operator.value]

        if sql_condition.value is not None:
            condition_parts.append(self.__build_value(sql_condition.value))

        return " ".join(condition_parts)

    @staticmethod
    def __build_value(value: Any) -> str:

        if isinstance(value, str):
            return f"'{value}'"

        return str(value)
