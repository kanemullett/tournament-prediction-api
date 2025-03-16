from enum import Enum


class SqlDataType(Enum):
    """
    Defines SQL data types.

    Attributes:
        VARCHAR (str): The column contains varchar values.
        INTEGER (str): The column contains integer values.
        TIMESTAMP_WITHOUT_TIME_ZONE (str): The column contains timestamp values
            stored without a time zone.
        BOOLEAN (str): The column contains boolean values.
    """
    VARCHAR = "VARCHAR"
    INTEGER = "INTEGER"
    TIMESTAMP_WITHOUT_TIME_ZONE = "TIMESTAMP WITHOUT TIME ZONE"
    BOOLEAN = "BOOLEAN"
