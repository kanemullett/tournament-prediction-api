from db_handler.db_handler.model.database_record import DatabaseRecord


class TournamentTemplateBase(DatabaseRecord):
    """
    Base object representing a tournament template to be inherited by TournamentTemplate and TournamentTemplateRequest
    objects.

    Attributes:
        name (str): The name of the tournament template.
    """
    name: str
