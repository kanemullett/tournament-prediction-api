from typing import ClassVar

from db_handler.db_handler.model.database_record import DatabaseRecord


class LeagueTemplate(DatabaseRecord):
    """
    Object representing a league template.

    Attributes:
        name (str): The name of the league template.
        groupCount (int): The number of groups that make up the league phase.
        teamsPerGroup (int): The number of teams competing in each group.
        homeAndAway (bool): True if each team should play against each of their fellow league-phase teams both home and
            away.
    """
    name: str
    groupCount: int
    teamsPerGroup: int
    homeAndAway: bool

    TARGET_TABLE: ClassVar[str] = "league-templates"
