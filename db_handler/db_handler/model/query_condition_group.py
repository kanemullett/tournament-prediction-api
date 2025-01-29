from pydantic import BaseModel

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.type.join import Join


class QueryConditionGroup(BaseModel):
    conditions: list[QueryCondition]
    join: Join = Join.AND
