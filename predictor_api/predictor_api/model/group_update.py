from db_handler.db_handler.model.database_record import DatabaseRecord


class GroupUpdate(DatabaseRecord):
    """
    Object representing a group update.

    Attributes:
        name (str): The name of the group.
    """
    name: str
