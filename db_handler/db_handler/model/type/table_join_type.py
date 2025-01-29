from enum import Enum


class TableJoinType(Enum):
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    OUTER = "FULL JOIN"
