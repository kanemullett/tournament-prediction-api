from pydantic import BaseModel

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.type.order_direction import OrderDirection


class OrderBy(BaseModel):
    column: Column
    direction: OrderDirection = OrderDirection.ASC

    @classmethod
    def of(cls, column: Column):
        return OrderBy(
            column=column,
            direction=OrderDirection.ASC
        )
