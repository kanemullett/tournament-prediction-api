from pydantic import BaseModel

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.type.condition_join import ConditionJoin


class QueryConditionGroup(BaseModel):
    """
    Object representing a group of query conditions.

    Attributes:
        conditions (list[QueryCondition]): The conditions to validate the
            returning data by.
        join (ConditionJoin): The join to apply to the conditions.
    """
    conditions: list[QueryCondition]
    join: ConditionJoin = ConditionJoin.AND

    @classmethod
    def of(cls, *conditions: QueryCondition):
        return QueryConditionGroup(
            conditions=list(conditions),
            join=ConditionJoin.AND
        )
