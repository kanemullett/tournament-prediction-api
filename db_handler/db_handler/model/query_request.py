from pydantic import BaseModel, Field

from db_handler.db_handler.model.query_condition_group import QueryConditionGroup


class QueryRequest(BaseModel):
    schema_: str = Field(alias="schema")
    table: str
    columns: list[str] = None
    conditionGroup: QueryConditionGroup = None
