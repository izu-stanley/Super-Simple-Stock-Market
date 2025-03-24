

import math
from datetime import datetime, timedelta

import pytest
import pytz

from src.models.stock import Stock
from src.models.stock_type import StockType
from src.models.trade import Trade
from src.models.trade_side import TradeSide


class TestStock:
    """Unit tests for Stock class"""

    @pytest.fixture
    def common_stock(self) -> Stock:
        """Create a common stock with nonzero last dividend."""

        return Stock(
            symbol="ABC",
            type=StockType.COMMON,
            last_dividend=8.0,
            fixed_dividend=None,
            par_value=100.0,
        )

    @pytest.fixture
    def preferred_stock(self) -> Stock:
        """Create a preferred stock with fixed dividend."""

        return Stock(
            symbol="XYZ",
            type=StockType.PREFERRED,
            last_dividend=8.0,
            fixed_dividend=0.02,
            par_value=100.0,
        )

    def test_dividend_yield_common(self, common_stock) -> None:
        """
        Test dividend yield from common stock.

        Checks if calculated and expected values are within margin of error. WHere
        margin of error is 1e-4
        """

        price = 80.0
        expected = common_stock.last_dividend / price
        result = common_stock.dividend_yield(price)
        assert math.isclose(result, expected, rel_tol=1e-4)

    def test_dividend_yield_preferred(self, preferred_stock) -> None:
        """
        Test dividend yield from preferred stock.

        Checks if calculated and expected values are within margin of error. Where
        margin of error is 1e-4
        """

        price = 80.0
        expected = (preferred_stock.fixed_dividend * preferred_stock.par_value) / price
        result = preferred_stock.dividend_yield(price)
        assert math.isclose(result, expected, rel_tol=1e-4)

    def test_dividend_yield_invalid_price(self, common_stock) -> None:
        """
        Test dividend yield from invalid price.

        Sets a dividend value of 0, this should raise a ValueError which pytest
        would catch as it is assumed that dividend should always be greater than 0
        """

        with pytest.raises(ValueError):
            common_stock.dividend_yield(0)

    def test_dividend_yield_missing_fixed_for_preferred(self, preferred_stock) -> None:
        """
        Test dividend yield from missing fixed dividend.

        Set fixed_dividend to None to simulate missing fixed dividend for preferred
        stock. Should raise a ValueError which pytest would catch
        """

        preferred_stock.fixed_dividend = None
        with pytest.raises(ValueError):
            preferred_stock.dividend_yield(80.0)

    def test_pe_ratio_common(self, common_stock) -> None:
        """
        Test pe_ratio from common stock.

        Checks if calculated and expected values for PE ratio are within margin of
        error. Where margin of error is 1e-4
        """
        price = 80.0
        # For common stock: dividend = last_dividend / price * price = last_dividend
        expected_ratio = price / common_stock.last_dividend
        result = common_stock.pe_ratio(price)
        assert math.isclose(result, expected_ratio, rel_tol=1e-4)

    def test_pe_ratio_given_zero_last_dividend(self, common_stock) -> None:
        """
        Check that common stock's PE ratio returns 0 when last_dividend is 0.
        """

        common_stock.last_dividend = 0.0
        result = common_stock.pe_ratio(80.0)
        assert result is None

    def test_record_trade(self, common_stock) -> None:
        """
        Test recording a trade for a common stock.

        Verifies trades are empty at the start, adds one trade, verifies trade was
        recorded correctly.
        """

        assert len(common_stock.trades) == 0
        trade = Trade(
            timestamp=datetime.now(pytz.timezone('US/Eastern')),
            quantity=100,
            side=TradeSide.BUY,
            trade_price=80.0,
        )
        common_stock.record_trade(trade)
        assert len(common_stock.trades) == 1
        assert common_stock.trades[0] == trade

    def test_volume_weighted_stock_price_no_trades(self, common_stock) -> None:
        """
        Test volume weighted stock price without trades.

        Should return None when no trades were recorded.
        """

        assert common_stock.volume_weighted_stock_price() is None

    def test_volume_weighted_stock_price_with_trades(self, common_stock) -> None:
        """
        Test volume weighted stock price with trades.

        Create trades with known quantities and prices, record the trades. Verify
        that calculated and expected values are within margin of error, where margin
        of error is 1e-4
        """
        now = datetime.now(pytz.timezone('US/Eastern'))
        # Create trades with known quantities and prices
        trades = [
            Trade(timestamp=now - timedelta(minutes=5), quantity=100, side=TradeSide.BUY, trade_price=80.0),
            Trade(timestamp=now - timedelta(minutes=10), quantity=200, side=TradeSide.SELL, trade_price=82.0),
            # This trade is older than 15 minutes, should not count.
            Trade(timestamp=now - timedelta(minutes=20), quantity=50, side=TradeSide.BUY, trade_price=78.0),
        ]
        for t in trades:
            common_stock.record_trade(t)

        total_trade_value = (80.0 * 100) + (82.0 * 200)
        total_quantity = 100 + 200
        expected_vwsp = total_trade_value / total_quantity
        result = common_stock.volume_weighted_stock_price(now=now)
        assert math.isclose(result, expected_vwsp, rel_tol=1e-4)

