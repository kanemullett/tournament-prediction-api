from typing import Optional

from pydantic import BaseModel

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.type.join_type import JoinType


class Join(BaseModel):
    """
    Object representing a SQL join.

    Attributes:
        joinCondition (Optional[QueryCondition]): The condition upon which to
            join.
        joinType (JoinType): The type of join.
    """
    joinCondition: Optional[QueryCondition] = None
    joinType: JoinType
