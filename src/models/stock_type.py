from enum import Enum

class StockType(str, Enum):
    """
    Enum class for the different types of stocks
    """

    PREFERRED = "PREFERRED"
    COMMON = "COMMON"
