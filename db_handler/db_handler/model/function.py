from typing import Any

from db_handler.db_handler.model.column import Column


class Function(Column):
    args: list[Any]
