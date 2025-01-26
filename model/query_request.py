from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    schema_: str = Field(alias="schema")
    table: str
