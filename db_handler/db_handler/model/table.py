from pydantic import BaseModel, Field


class Table(BaseModel):
    schema_: str = Field(alias="schema")
    table: str
    alias: str = None
