from typing import Any, Optional

from pydantic import BaseModel

from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class UpdateRequest(BaseModel):
    """
    Object representing the response an update request.

    Attributes:
        operation (SqlOperator): The type of update action to perform.
        table (Table): The table within which the records to be updated exist.
        records (Optional[list[dict[str, Any]]]): The records returned from
            the query.
        conditionGroup (QueryConditionGroup): The conditions upon which to
            apply the update.
    """
    operation: SqlOperator
    table: Table
    records: Optional[list[dict[str, Any]]] = None
    conditionGroup: QueryConditionGroup = None
