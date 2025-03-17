from typing import Optional, Any

from pydantic import BaseModel

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.group_by import GroupBy
from db_handler.db_handler.model.join import Join
from db_handler.db_handler.model.order_by import OrderBy
from db_handler.db_handler.model.query_condition_group import (
    QueryConditionGroup
)
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class SqlQuery(BaseModel):
    """
    Object representing a SQL query.

    Attributes:
        operator (SqlOperator): The sql query operator.
        table (Table): The table to query.
        columns (Optional[list[Column]]): The columns to retrieve.
        joins (Optional[list[Join]]): The tables to join.
        conditionGroup (QueryConditionGroup): The filtering conditions to
            apply.
        records (Optional[list[dict[str, Any]]]): The records to create/update.
    """

    operator: SqlOperator = SqlOperator.SELECT
    distinct: bool = False
    table: Table
    columns: Optional[list[Column]] = None
    joins: Optional[list[Join]] = None
    conditionGroup: Optional[QueryConditionGroup] = None
    records: Optional[list[dict[str, Any]]] = None
    groupBy: Optional[GroupBy] = None
    orderBy: Optional[list[OrderBy]] = None
