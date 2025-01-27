from model.type.sql_condition_operator import SqlConditionOperator
from pydantic import BaseModel
from typing import Any


class SqlCondition(BaseModel):
    column: str
    operator: SqlConditionOperator
    value: Any = None
