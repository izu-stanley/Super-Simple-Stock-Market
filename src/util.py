import logging
import time

from src.models.stock import Stock
from src.models.stock_market import StockMarket
from src.models.stock_type import StockType

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def set_up_stock_market() -> StockMarket:
    """
    Sets up a stock market with predefined stocks.

    Returns:
        StockMarket: A StockMarket object with initialized stocks.
    """

    market = StockMarket()
    market.add_stock(Stock(symbol="TEA", type=StockType.COMMON, last_dividend=0,
                           par_value=100))
    market.add_stock(Stock(symbol="POP", type=StockType.COMMON, last_dividend=8,
                           par_value=100))
    market.add_stock(Stock(symbol="ALE", type=StockType.COMMON, last_dividend=23,
                           par_value=60))
    market.add_stock(Stock(symbol="JOE", type=StockType.COMMON, last_dividend=13,
                           par_value=250))
    market.add_stock(Stock(symbol="GIN", type=StockType.PREFERRED, last_dividend=8,
                           fixed_dividend=0.02, par_value=100))

    log.info("Stock market initialized")
    log.info(f"Supported stocks: {','.join(market.get_supported_stocks())}")

    # Adding delay for logs to show up in order as it is a CLI
    time.sleep(0.5)

    return market


