from enum import Enum


class OrderDirection(Enum):
    """
    Defines SQL order directions.

    Attributes:
        ASC (str): The results should be organised in ascending order.
        DESC (str): The results should be organised in descending order.
    """
    ASC = "ASC"
    DESC = "DESC"
