from enum import Enum


class ConditionOperator(Enum):
    """
    Defines condition operator types.

    Attributes:
        EQUAL (str): The column value is equal to the value provided in the
            condition.
        LESS_THAN (str): The column value is less than the value provided in
            the condition.
        GREATER_THAN (str): The column value is greater than the value
            provided in the condition.
        IN (str): The column value is one of the values provided in the
            condition.
    """
    EQUAL = "="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    IN = "IN"
