from pydantic import BaseModel, Field

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup


class QueryRequest(BaseModel):
    schema_: str = Field(alias="schema")
    table: str
    alias: str = None
    columns: list[Column] = None
    conditionGroup: QueryConditionGroup = None
