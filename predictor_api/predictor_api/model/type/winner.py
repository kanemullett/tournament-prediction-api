from enum import Enum


class Winner(Enum):
    """
    Defines the winner of a match.

    Attributes:
        HOME (str): The home team.
        AWAY (str): The away team.
    """
    HOME = "HOME"
    AWAY = "AWAY"
