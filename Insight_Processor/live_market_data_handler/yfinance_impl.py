
from .live_market_handler import liveMarketDataHandler
import yfinance
from decimal import Decimal
class yfinance_impl(liveMarketDataHandler):
    def get_current_stock_price(self, ticker : str):
        try:
            stock = yfinance.Ticker(f"{ticker}.NS")
            data = stock.history(period="1d", interval = "1m")
            current_price = data["Close"].iloc[-1]

            print(f"{ticker} : {current_price}")

            return Decimal(current_price)
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {str(e)}")
            return 0