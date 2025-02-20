from typing import Optional

from pydantic import BaseModel

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin


class QueryRequest(BaseModel):
    """
    Object representing a query to be sent to the database.

    Attributes:
        table (Table): The table to query.
        columns (Optional[list[Column]]): The columns to retrieve.
        tableJoins (Optional[list[TableJoin]]): The tables to join.
        conditionGroup (QueryConditionGroup): The filtering conditions to apply.
    """
    table: Table
    columns: Optional[list[Column]] = None
    tableJoins: Optional[list[TableJoin]] = None
    conditionGroup: QueryConditionGroup = None
