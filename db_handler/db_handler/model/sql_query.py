from typing import Optional, Any

from pydantic import BaseModel, Field

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class SqlQuery(BaseModel):
    """
    Object representing a SQL query.

    Attributes:
        operator (SqlOperator): The sql query operator.
        table (Table): The table to query.
        columns (Optional[list[Column]]): The columns to retrieve.
        tableJoins (Optional[list[TableJoin]]): The tables to join.
        conditionGroup (QueryConditionGroup): The filtering conditions to apply.
        records (Optional[list[dict[str, Any]]]): The records to create/update.
    """

    operator: SqlOperator
    table: Table
    columns: Optional[list[Column]] = None
    tableJoins: Optional[list[TableJoin]] = None
    conditionGroup: Optional[QueryConditionGroup] = None
    records: Optional[list[dict[str, Any]]] = None