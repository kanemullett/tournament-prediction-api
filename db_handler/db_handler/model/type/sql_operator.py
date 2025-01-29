from enum import Enum


class SqlOperator(Enum):
    """
    Defines SQL operator types.

    Attributes:
        SELECT (str): The query is retrieving records.
        INSERT (str): The query is adding records.
        UPDATE (str): The query is updating existing records.
        DELETE (str): The query is deleting records.
    """
    SELECT = "SELECT"
    INSERT = "INSERT INTO"
    UPDATE = "UPDATE"
    DELETE = "DELETE FROM"
