from typing import Optional

from pydantic import BaseModel, Field


class Table(BaseModel):
    """
    Object representing a database table.

    Attributes:
        schema_ (str): The schema to which the table belongs.
        table (str): The name of the table.
        alias (str): The alias to assign to the table.
    """
    schema_: str = Field(alias="schema")
    table: str
    alias: Optional[str] = None

    @classmethod
    def of(cls, schema: str, table: str, alias: str = None):
        return Table(
            schema=schema,
            table=table,
            alias=alias
        )
