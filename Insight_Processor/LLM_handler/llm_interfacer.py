
from abc import ABC, abstractmethod

class LLM_Interfacer(ABC): 

    @abstractmethod
    def summarise_scraped_data(self, market_data : str, additionalPrompt : str) -> str:
        pass


    @abstractmethod
    def analyse_daily_market_data(self, market_data : str) -> str:
        pass

    @abstractmethod
    def generate_insights(self, market_data : str):
        pass



