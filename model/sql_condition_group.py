from pydantic import BaseModel

from model.sql_condition import SqlCondition
from model.type.sql_join import SqlJoin


class SqlConditionGroup(BaseModel):
    conditions: list[SqlCondition]
    join: SqlJoin
