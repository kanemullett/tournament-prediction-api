from pydantic import BaseModel, Field

from db_handler.db_handler.model.sql_condition_group import SqlConditionGroup


class QueryRequest(BaseModel):
    schema_: str = Field(alias="schema")
    table: str
    columns: list[str] = None
    conditionGroup: SqlConditionGroup = None
