from pydantic import BaseModel, Field
from typing import Optional

from db_handler.model.sql_condition_group import SqlConditionGroup


class QueryRequest(BaseModel):
    schema_: str = Field(alias="schema")
    table: str
    columns: Optional[list[str]] = None
    conditionGroup: SqlConditionGroup = None
