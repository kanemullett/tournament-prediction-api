from typing import Optional

from pydantic import BaseModel

from db_handler.db_handler.model.join import Join
from db_handler.db_handler.model.sql_query import SqlQuery


class QueryJoin(Join):
    query: SqlQuery
    alias: Optional[str] = None
