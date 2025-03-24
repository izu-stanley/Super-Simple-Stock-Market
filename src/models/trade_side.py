from enum import Enum

class TradeSide(str, Enum):
    """
    Enum class containing all possible side types.
    """

    BUY = "BUY"
    SELL = "SELL"
