from pydantic import BaseModel
from typing import Any

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.type.condition_operator import ConditionOperator


class QueryCondition(BaseModel):
    column: Column
    operator: ConditionOperator
    value: Any = None
