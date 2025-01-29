from pydantic import BaseModel, Field
from typing import Optional

from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class SqlQuery(BaseModel):
    operator: SqlOperator
    schema_: str = Field(alias="schema")
    table: str
    columns: Optional[list[str]] = None
    conditionGroup: QueryConditionGroup = None