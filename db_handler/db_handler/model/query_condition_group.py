from pydantic import BaseModel

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.type.sql_join import SqlJoin


class QueryConditionGroup(BaseModel):
    conditions: list[QueryCondition]
    join: SqlJoin = SqlJoin.AND
