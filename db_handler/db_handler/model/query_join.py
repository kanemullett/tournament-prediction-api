from typing import Optional

from db_handler.db_handler.model.join import Join
from db_handler.db_handler.model.sql_query import SqlQuery


class QueryJoin(Join):
    """
    Object representing a join between two queries.

    Attributes:
        query (SqlQuery): The query to join.
        alias (Optional[str]): The alias of the join.
    """
    query: SqlQuery
    alias: Optional[str] = None
