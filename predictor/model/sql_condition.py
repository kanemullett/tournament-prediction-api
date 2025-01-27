from pydantic import BaseModel
from typing import Any

from predictor.model.type.sql_condition_operator import SqlConditionOperator


class SqlCondition(BaseModel):
    column: str
    operator: SqlConditionOperator
    value: Any = None
