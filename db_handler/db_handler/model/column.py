from pydantic import BaseModel


class Column(BaseModel):
    parts: list[str]
    alias: str = None
