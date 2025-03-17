from typing import Optional

from pydantic import BaseModel

from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.type.join_type import JoinType


class Join(BaseModel):
    joinCondition: Optional[QueryCondition] = None
    joinType: JoinType
