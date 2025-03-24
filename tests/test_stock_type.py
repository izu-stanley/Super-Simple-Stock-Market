import pytest
from src.models.stock_type import StockType
import pytest

from src.models.stock_type import StockType


def test_stock_type_values() -> None:
    """Verify that the StockType enum has the correct values."""

    assert StockType.PREFERRED.value == "PREFERRED"
    assert StockType.COMMON.value == "COMMON"

def test_stock_type_membership() -> None:
    """Check that valid values are present in the StockType enum."""

    valid_values = {"PREFERRED", "COMMON"}
    assert valid_values.issubset(set(StockType._value2member_map_.keys()))

def test_stock_type_invalid_value() -> None:
    """Ensure that creating a StockType with an invalid value raises a ValueError."""

    with pytest.raises(ValueError):
        StockType("INVALID")
