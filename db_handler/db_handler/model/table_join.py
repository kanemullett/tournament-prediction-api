from pydantic import BaseModel

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.table_join_type import TableJoinType


class TableJoin(BaseModel):
    """
    Object representing a join between two database tables.

    Attributes:
        table (Table): The table to join to the base table.
        joinCondition (QueryCondition): The condition upon which to join the tables.
        joinType (TableJoinType): The way in which to join the tables.
    """
    table: Table
    joinCondition: QueryCondition
    joinType: TableJoinType
