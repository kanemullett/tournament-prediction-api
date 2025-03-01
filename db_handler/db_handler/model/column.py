from pydantic import BaseModel


class Column(BaseModel):
    """
    Object representing a database table column.

    Attributes:
        parts (list[str]): The component parts of the column's name.
        alias (str): The name the column should be displayed as.
    """
    parts: list[str]
    alias: str = None

    @classmethod
    def of(cls, *parts: str):
        return Column(
            parts=list(parts)
        )
