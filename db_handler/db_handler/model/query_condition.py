from pydantic import BaseModel
from typing import Any

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.type.condition_operator import ConditionOperator


class QueryCondition(BaseModel):
    """
    Object representing a query condition.

    Attributes:
        column (Column): The column whose value is subject to the condition.
        operator (ConditionOperator): The condition operator.
        value (Any): The value to compare the column value with.
    """
    column: Column
    operator: ConditionOperator
    value: Any = None
