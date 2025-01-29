from enum import Enum


class ConditionJoin(Enum):
    """
    Defines condition operator types.

    Attributes:
        AND (str): Both conditions must be satisfied.
        OR (str): Either condition must be satisfied.
    """
    AND = "AND"
    OR = "OR"
