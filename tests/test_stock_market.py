import pytest

from src.models.stock import Stock
from src.models.stock_market import \
    StockMarket  # assuming StockMarket is defined in src/models/stock_market.py
from src.models.stock_type import StockType
from src.models.trade_side import TradeSide


class TestStockMarket:
    """Unit tests for StockMarket."""

    @pytest.fixture
    def market(self) -> StockMarket:
        """Set up a stock market with two stocks."""
        market = StockMarket()
        stock1 = Stock(
            symbol="ABC",
            type=StockType.COMMON,
            last_dividend=8.0,
            fixed_dividend=None,
            par_value=100.0,
        )
        stock2 = Stock(
            symbol="XYZ",
            type=StockType.PREFERRED,
            last_dividend=8.0,
            fixed_dividend=0.02,
            par_value=100.0,
        )
        market.add_stock(stock1)
        market.add_stock(stock2)
        return market

    def test_get_supported_stocks(self, market) -> None:
        """
        Test method to get supported stocks.
        """
        supported = market.get_supported_stocks()
        assert set(supported) == {"ABC", "XYZ"}

    def test_record_trade(self, market) -> None:
        """Test successfully record trade"""

        market.record_trade(symbol="ABC", quantity=100, trade_price=80.0, side=TradeSide.BUY)
        stock = market.stocks["ABC"]
        assert len(stock.trades) == 1
        trade = stock.trades[0]
        assert trade.quantity == 100
        assert trade.trade_price == 80.0
        assert trade.side == TradeSide.BUY

    def test_record_trade_invalid_stock(self, market) -> None:
        """
        Test record trade with invalid stock.

        Should raise a ValueError which pytest would catch
        """
        with pytest.raises(ValueError):
            market.record_trade(symbol="NONEXISTENT", quantity=100, trade_price=80.0,
                                side=TradeSide.BUY)

    def test_all_share_index_no_trades(self, market) -> None:
        """Test all share index without trades."""

        assert market.all_share_index() is None

