from db_handler.db_handler.model.join import Join
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.type.join_type import JoinType


class TableJoin(Join):
    """
    Object representing a join between two database tables.

    Attributes:
        table (Table): The table to join to the base table.
    """
    table: Table

    @classmethod
    def of(
            cls,
            table: Table,
            join_condition: QueryCondition,
            join_type: JoinType):
        return TableJoin(
            table=table,
            joinCondition=join_condition,
            joinType=join_type
        )
