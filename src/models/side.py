from enum import Enum

class Side(str, Enum):
    """
    Enum class containing all possible side types.
    """

    BUY = "BUY"
    SELL = "SELL"
