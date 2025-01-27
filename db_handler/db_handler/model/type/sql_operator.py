from enum import Enum


class SqlOperator(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT INTO"
    UPDATE = "UPDATE"
    DELETE = "DELETE FROM"
