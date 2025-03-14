from typing import ClassVar

from db_handler.db_handler.model.database_record import DatabaseRecord


class LeagueTemplate(DatabaseRecord):
    """
    Object representing a league template.

    League templates are an optional component of tournament templates and
    define the structure of a tournament's league phase.

    This template is used to generate groups and matches within those groups
    upon creation of a tournament that uses it.

    Attributes:
        name (str): The name of the league template.
        groupCount (int): The number of groups that make up the league phase.
        teamsPerGroup (int): The number of teams competing in each group.
        homeAndAway (bool): True if each team should play against each of
            their fellow league-phase teams both home and away.
    """
    name: str
    groupCount: int
    teamsPerGroup: int
    homeAndAway: bool

    TARGET_TABLE: ClassVar[str] = "league-templates"
