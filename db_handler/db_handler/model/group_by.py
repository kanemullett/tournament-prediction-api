from pydantic import BaseModel

from db_handler.db_handler.model.column import Column


class GroupBy(BaseModel):
    columns: list[Column]

    @classmethod
    def of(cls, *parts: Column):
        return GroupBy(
            columns=list(parts)
        )
