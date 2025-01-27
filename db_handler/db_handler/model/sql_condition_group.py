from pydantic import BaseModel

from db_handler.db_handler.model.sql_condition import SqlCondition
from db_handler.db_handler.model.type.sql_join import SqlJoin


class SqlConditionGroup(BaseModel):
    conditions: list[SqlCondition]
    join: SqlJoin
