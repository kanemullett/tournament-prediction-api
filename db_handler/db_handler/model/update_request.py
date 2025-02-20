from typing import Any, Optional

from pydantic import BaseModel

from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class UpdateRequest(BaseModel):
    operation: SqlOperator
    table: Table
    records: Optional[list[dict[str, Any]]] = None
    conditionGroup: QueryConditionGroup = None
