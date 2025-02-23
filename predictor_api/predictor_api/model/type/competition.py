from enum import Enum


class Competition(Enum):
    """
    Defines competition types.

    Attributes:
        EUROS (str): The UEFA European Championships.
        WORLD_CUP (str): The FIFA World Cup.
    """
    EUROS = "EUROS"
    WORLD_CUP = "WORLD_CUP"
