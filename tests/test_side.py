from datetime import datetime

import pytest
import pytz

from src.models.trade import Trade


class TestSide:
    """
    Unit tests for Side Enum class
    """

    def test_valid_side_uppercase(self) -> None:
        """
        Test side provided as uppercase to Trade object.
        """

        trade = Trade(
            timestamp=datetime.now(pytz.timezone('US/Eastern')),
            quantity=100,
            side="BUY",
            trade_price=80.0,
        )
        assert trade.side == "BUY"

    def test_valid_side_lowercase_converted(self) -> None:
        """
        Test side provided as lowercase to Trade object.

        Should raise a ValueError which pytest should catch as lowercase should not
        be accepted
        """

        with pytest.raises(ValueError):
            Trade(
                timestamp=datetime.now(pytz.timezone('US/Eastern')),
                quantity=100,
                side="buy",
                trade_price=80.0,
            )

    def test_invalid_side(self) -> None:
        """
        Test invalid side provided to Trade object.

        Should raise a ValueError which pytest should catch as side should only be
        BUY or SELL.
        """
        with pytest.raises(ValueError):
            Trade(
                timestamp=datetime.now(pytz.timezone('US/Eastern')),
                quantity=100,
                side="HOLD",
                trade_price=80.0,
            )

