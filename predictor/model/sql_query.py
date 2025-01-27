from pydantic import BaseModel, Field
from typing import Optional

from predictor.model.sql_condition_group import SqlConditionGroup
from predictor.model.type.sql_operator import SqlOperator


class SqlQuery(BaseModel):
    operator: SqlOperator
    schema_: str = Field(alias="schema")
    table: str
    columns: Optional[list[str]] = None
    conditionGroup: SqlConditionGroup = None