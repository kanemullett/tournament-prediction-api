from pydantic import BaseModel

from predictor.model.sql_condition import SqlCondition
from predictor.model.type.sql_join import SqlJoin


class SqlConditionGroup(BaseModel):
    conditions: list[SqlCondition]
    join: SqlJoin
