import abc
from abc import ABC, abstractmethod

class liveMarketDataHandler(ABC):

    @abstractmethod
    def get_current_stock_price(self,ticker : str) :
        pass
