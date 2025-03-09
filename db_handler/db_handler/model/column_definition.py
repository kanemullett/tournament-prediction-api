from pydantic import BaseModel

from db_handler.db_handler.model.type.sql_data_type import SqlDataType


class ColumnDefinition(BaseModel):
    """
    Object representing a column definition.

    Attributes:
        name (str): The name of the column.
        dataType (SqlDataType): The data type of the values stored in the
            column.
        primaryKey (bool): True if the column is its table's primary key.
    """
    name: str
    dataType: SqlDataType
    primaryKey: bool = False

    @classmethod
    def of(cls, name: str, data_type: SqlDataType):
        return ColumnDefinition(
            name=name,
            dataType=data_type,
            primaryKey=False
        )
