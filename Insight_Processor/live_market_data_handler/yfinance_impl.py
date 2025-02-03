from .live_market_handler import liveMarketDataHandler
import yfinance as yf
from decimal import Decimal
from datetime import timedelta, datetime
from shared import DATE_FORMAT

class yfinance_impl(liveMarketDataHandler):
    def get_current_stock_price(self, ticker : str, rundate : str):
        try:
            stock = yf.Ticker(f"{ticker}.NS")
            data = stock.history(period="1d", interval = "1m")
            current_price = data["Close"].iloc[-1]

            print(f"{ticker} : {current_price}")

            return Decimal(current_price)
        except Exception as e:
            print(f"Failed to fetch current price for {ticker}: {str(e)}")
            print("Trying to get the latest price available...")

            try:
                return self.get_stock_price(ticker, rundate)
            except Exception as e:
                print(f"Failed to fetch latest price for {ticker}: {str(e)}")
                return 0


    def get_stock_price(self, ticker : str, date : str):
        try:
            stock = yf.Ticker(f"{ticker}.NS")
            start_date = self.__get_working_day(date)
            end_date = datetime.strptime(start_date, DATE_FORMAT) + timedelta(days=1)

            data = stock.history(period = "1d", start = start_date, end = end_date.strftime(DATE_FORMAT))

            #print(data)
            current_price = data["Close"].iloc[0]

            print(f"{ticker} : {current_price}")

            return Decimal(current_price)
        except Exception as e:
            print(f"Failed to fetch price for {ticker}: {str(e)}")
            return 0
        
    def __get_working_day(self, date_str):
        # Convert string to datetime object
        date_obj = datetime.strptime(date_str, DATE_FORMAT)

        # Check if it's a weekend (Saturday=5, Sunday=6)
        if date_obj.weekday() >= 5:
            # Find the last Friday
            days_to_friday = (date_obj.weekday() - 4) % 7
            last_friday = date_obj - timedelta(days=days_to_friday)
            return last_friday.strftime(DATE_FORMAT)
        
        # If it's a weekday, return the same date
        return date_str