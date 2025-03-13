from enum import Enum


class Confederation(Enum):
    """
    Defines an international football confederation.

    Attributes:
        AFC (str): Asian Football Confederation (Asia)
        CAF (str): Confederation of African Football (Africa)
        CONCACAF (str): Confederation of North, Central American and
            Caribbean Association Football (North America, Central America,
            The Caribbean)
        CONMEBOL (str): Confederación Sudamericana de Fútbol (South America)
        OFC (str): Oceania Football Confederation (Oceania)
        UEFA (str): Union of European Football Associations (Europe)
    """
    AFC = "AFC"
    CAF = "CAF"
    CONCACAF = "CONCACAF"
    CONMEBOL = "CONMEBOL"
    OFC = "OFC"
    UEFA = "UEFA"
