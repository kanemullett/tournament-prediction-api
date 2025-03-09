from pydantic import BaseModel, Field

from db_handler.db_handler.model.column_definition import ColumnDefinition


class TableDefinition(BaseModel):
    """
    Object representing a table definition to created in the database.

    Attributes:
        schema_ (str): The database schema within which the table should be
            created.
        table (str): The name of the table to create.
        columns (list[ColumnDefinition]): The columns that will be created
            within the table.

    """
    schema_: str = Field(alias="schema")
    table: str
    columns: list[ColumnDefinition]
