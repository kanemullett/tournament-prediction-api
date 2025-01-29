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
    alias: str = None
