
from .llm_interfacer import LLM_Interfacer
from shared import ANALYSE_CUSTOM_MARKET_DATA_PROMPT, ANALYSE_DAILY_MARKET_DATA_PROMPT, LLM_MODEL, LLM_MAX_TOKENS, LLM_TEMPERATURE, OPENAI_API_KEY, Recommendation,DailyAnalysisResponse
import openai
import json

# Here We can Interact with Open ai models to summarise / analyse the market data


class OpenAI_Impl(LLM_Interfacer):

    def summarise_scraped_data(self, market_data : str, additionalPrompt : str) -> str:
        return market_data;
    
    def analyse_daily_market_data(self, market_data : str) -> str:
        response = self.__llm(ANALYSE_DAILY_MARKET_DATA_PROMPT, market_data)

        return self.__verify_response(response, ANALYSE_DAILY_MARKET_DATA_PROMPT, market_data)
    
    def generate_insights(self, market_data : str):
        response = self.__llm(ANALYSE_CUSTOM_MARKET_DATA_PROMPT, market_data)
            
        return self.__verify_response(response, ANALYSE_CUSTOM_MARKET_DATA_PROMPT, market_data)
    
    def __llm(self,prompt : str,content : str):

        openai.api_key = OPENAI_API_KEY
        response = openai.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content},
            ],
            max_tokens=LLM_MAX_TOKENS
        )

        cleaned_response = response.choices[0].message.content.strip("```json").strip("```")
        print("Response from LLM : ", cleaned_response)
        return cleaned_response

    def __verify_response(self,response : str,prompt : str, content:str):
        parsed_response = None
        try:
            parsed_response = json.loads(response)
        except json.JSONDecodeError:
            print("JSON Encoding error, Retrying the output from LLM model...")
            response = self.__llm(prompt, content)
            try:
                parsed_response = json.loads(response)
            except json.JSONDecodeError:
                print("Failed to parse response from LLM")
                return ""
        
        return parsed_response