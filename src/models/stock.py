import logging
from datetime import datetime, timedelta
from typing import List, Optional

import pytz
from pydantic import BaseModel, Field

from src.models.stock_type import StockType
from src.models.trade import Trade

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Amount of time to take into consideration when filtering trades for stock price calc
STOCK_DEFAULT_TIME_LAG = 15

class Stock(BaseModel):
    """
    Stock class holding stock data and related information.
    """

    symbol: str = Field(min_length=1, max_length=5, description="Stock symbol")
    type: StockType = Field(description="Stock type, should be PREFERRED or COMMON")
    last_dividend: float = Field(ge=0, description="Last dividend value, "
                                                   "should always be >= 0")
    fixed_dividend: Optional[float] = Field(gt=0, default=None,
                                            description="Fixed dividend value. If "
                                                         "provided, should be >= 0")
    par_value: float = Field(gt=0, description="Par value value")
    trades: Optional[List[Trade]] = Field(default_factory=list, description="List of trades")


    def dividend_yield(self, price: float) -> float:
        """Calculate dividend yield given a price.

        For Common stocks: last_dividend / price.
        For Preferred stocks: (fixed_dividend * par_value) / price.
        """
        if price <= 0:
            raise ValueError("Price must be positive")

        log.info(f"Calculating dividend yield for stock with Symbol: {self.symbol} ")
        match self.type:
            case StockType.COMMON:
                dividend = self.last_dividend / price
            case StockType.PREFERRED:
                if self.fixed_dividend is None:
                    raise ValueError("Fixed dividend is not set for preferred stock")
                dividend = (self.fixed_dividend * self.par_value) / price
            case _:
                raise ValueError("Unknown stock type")

        log.info(f"Calculated dividend yield for stock with Symbol: {self.symbol} = {dividend}")
        return dividend

    def pe_ratio(self, price: float) -> Optional[float]:
        """Calculate the P/E Ratio given a price.

        P/E Ratio = Price / Dividend.
        If the dividend is zero then P/E Ratio is undefined (None).
        """

        log.info(f"Calculating P/E Ratio for stock with Symbol: {self.symbol} ")
        dividend = self.dividend_yield(price) * price
        if dividend == 0:
            return None
        ratio = price / dividend
        log.info(f"Calculated P/E Ratio for stock with Symbol: {self.symbol} = {ratio:.2f} ")
        return ratio

    def record_trade(self, trade: Trade) -> None:
        """Records a trade for given stock."""

        self.trades.append(trade)
        log.info(f"Recorded trade for stock with Symbol: {self.symbol}")

    def volume_weighted_stock_price(self, now: Optional[datetime] = None) -> Optional[float]:
        """Calculate the volume weighted stock price (VWSP) using trades in the past 15 minutes.

        VWSP = (Sum(trade_price * quantity)) / (Sum(quantity))
        Returns None if there are no trades in the 15 mins time window.
        """
        if now is None:
            now = datetime.now(pytz.timezone('US/Eastern'))
        time_threshold = now - timedelta(minutes=STOCK_DEFAULT_TIME_LAG)

        relevant_trades = [t for t in self.trades if t.timestamp >= time_threshold]
        log.info(f"Determined {len(relevant_trades)} relevant trades for stock "
                 f"with Symbol: {self.symbol}")
        if not relevant_trades:
            return None

        total_trade_value = sum(t.trade_price * t.quantity for t in relevant_trades)
        total_quantity = sum(t.quantity for t in relevant_trades)
        log.info(f"Stock Symbol: {self.symbol}, Total trade value: {total_trade_value}, "
                 f"Total quantity: {total_quantity}")
        if total_quantity == 0:
            return None
        price: float = total_trade_value / total_quantity
        log.info(f"Calculated volume weighted stock price for stock with Symbol: "
                 f"{self.symbol}: {price:.2f}")
        return price

