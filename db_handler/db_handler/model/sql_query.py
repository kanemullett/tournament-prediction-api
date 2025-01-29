from pydantic import BaseModel, Field

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class SqlQuery(BaseModel):
    operator: SqlOperator
    schema_: str = Field(alias="schema")
    table: str
    alias: str = None
    columns: list[Column] = None
    conditionGroup: QueryConditionGroup = None