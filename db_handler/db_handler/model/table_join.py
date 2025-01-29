from pydantic import BaseModel

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.table_join_type import TableJoinType


class TableJoin(BaseModel):
    table: Table
    joinCondition: QueryCondition
    joinType: TableJoinType
