from pydantic import BaseModel

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.type.order_direction import OrderDirection


class OrderBy(BaseModel):
    """
    Object representing an order by clause.

    Attributes:
        column (Column): The column to order by.
        direction (OrderDirection): The direction in which to order.
    """
    column: Column
    direction: OrderDirection = OrderDirection.ASC

    @classmethod
    def of(cls, column: Column):
        return OrderBy(
            column=column,
            direction=OrderDirection.ASC
        )
