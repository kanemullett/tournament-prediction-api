from pydantic import BaseModel

from db_handler.db_handler.model.type.sql_data_type import SqlDataType


class ColumnDefinition(BaseModel):
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
