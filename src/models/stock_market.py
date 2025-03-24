import logging
import math
from datetime import datetime
from typing import Optional, Dict, List

import pytz
from pydantic import BaseModel, Field

from src.models.trade_side import TradeSide
from src.models.stock import Stock
from src.models.trade import Trade

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class StockMarket(BaseModel):
    """
    Class representing the model stock market and related functionality
    """

    stocks: Optional[Dict[str, Stock]] = Field(default_factory=dict)


    def add_stock(self, stock: Stock) -> None:
        """Add a stock to the market."""
        if self.stocks is None:
            self.stocks = {}
        self.stocks[stock.symbol] = stock
        log.info(f"Added stock {stock.symbol} to market. Stock details: {stock}")


    def get_supported_stocks(self) -> List[str]:
        """
        Return a list of supported stock symbols.
        """

        return list(self.stocks.keys())

    def record_trade(self, symbol: str, quantity: int, trade_price: float, side: TradeSide) \
            -> None:
        """Record a trade for the given stock symbol."""
        if symbol not in self.stocks:
            raise ValueError("Stock symbol not found")

        trade = Trade(timestamp=datetime.now(pytz.timezone('US/Eastern')), quantity=quantity,
                      side=side, trade_price=trade_price)
        self.stocks[symbol].record_trade(trade)
        log.info(f"Recorded trade for {symbol}: {trade}")


    def all_share_index(self) -> Optional[float]:
        """Calculate the GBCE All Share Index as the geometric mean of the VWSP for all stocks.

        Only stocks with a valid VWSP (i.e. with recent trades) are considered.
        Returns None if no stock has a recent trade.
        """
        prices = []
        log.info("Calculating GBCE All Share Index")
        for stock in self.stocks.values():
            price = stock.volume_weighted_stock_price()
            if price is not None:
                prices.append(price)
        if not prices:
            return None
        product = math.prod(prices)
        index_value = product ** (1/len(prices))
        log.info(f"Number of prices used in calculation: {len(prices)}")
        log.info(f"GBCE All Share Index Calculated Value: {index_value}")

StockMarket.model_rebuild()