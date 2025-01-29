from typing import Optional

from pydantic import BaseModel, Field

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.sql_operator import SqlOperator


class SqlQuery(BaseModel):
    operator: SqlOperator
    table: Table
    columns: Optional[list[Column]] = None
    tableJoins: Optional[list[TableJoin]] = None
    conditionGroup: QueryConditionGroup = None