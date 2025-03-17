from typing import Optional

from pydantic import BaseModel

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.group_by import GroupBy
from db_handler.db_handler.model.join import Join
from db_handler.db_handler.model.order_by import OrderBy
from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.table import Table


class QueryRequest(BaseModel):
    """
    Object representing a query to be sent to the database.

    Attributes:
        table (Table): The table to query.
        columns (Optional[list[Column]]): The columns to retrieve.
        joins (Optional[list[Join]]): The tables to join.
        conditionGroup (QueryConditionGroup): The filtering conditions to
            apply.
    """
    distinct: bool = False
    table: Table
    columns: Optional[list[Column]] = None
    joins: Optional[list[Join]] = None
    conditionGroup: Optional[QueryConditionGroup] = None
    groupBy: Optional[GroupBy] = None
    orderBy: Optional[list[OrderBy]] = None
