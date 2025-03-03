from enum import Enum


class TableJoinType(Enum):
    """
    Defines SQL table join types.

    Attributes:
        INNER (str): Only records that have matching values in both tables
            should be returned.
        LEFT (str): All records from the left table and matching records from
            the right table should be returned.
        RIGHT (str): All records from the right table and matching records
            from the left table should be returned.
        OUTER (str): All records from either table that have a match should
            be returned.
    """
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    OUTER = "FULL JOIN"
