from pydantic import BaseModel, Field

from db_handler.db_handler.model.column_definition import ColumnDefinition


class TableDefinition(BaseModel):
    schema_: str = Field(alias="schema")
    table: str
    columns: list[ColumnDefinition]
