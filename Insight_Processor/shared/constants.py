import os
from dataclasses import dataclass

# Date Format
DATE_FORMAT = "%Y-%m-%d"


# AWS Configurations
S3_BUCKET_NAME = "market-pulse-ai"
DYNAMODB_TABLE_NAME = "marketpulseai-recommendations"
SCRAPED_DATA_DIRECTORY = "scraped_data/"
DAILY_SUMMARY_DATA_DIRECTORY = "summary_data/Daily/"
WEEKLY_SUMMARY_DATA_DIRECTORY = "summary_data/Weekly/"
MONTHLY_SUMMARY_DATA_DIRECTORY = "summary_data/Monthly/"
YEARLY_SUMMARY_DATA_DIRECTORY = "summary_data/Yearly/"
AWS_REGION = "us-east-1" ##TODO : should change to ap-south-1

#API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#LLM model configurations
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS = 15000

# LLM model response models
@dataclass
class Recommendation:
    name: str
    ticker : str
    recommendation: str
    reason: str
    source: str

@dataclass
class DailyAnalysisResponse:
    marketnews: str
    recommendations: list[Recommendation]


#LLM model Prompts
GENERATE_SUMMARY_PROMPT = "Summarise the market data provided to you & do not forget to mention the source of content provider."

##TODO: "- Be exhaustive and consider all input data for its analysis." add this to get bigger result.
ANALYSE_DAILY_MARKET_DATA_PROMPT = '''
You are an expert financial analyst. Your task is to process stock market-related news sourced from various news website blogs and generate a comprehensive report, ensuring **no relavant information is missed**. You must output the results in JSON format with two components: 

1. **MarketHighlights**(String): A structured and detailed explanation of the market news for the day, understand all the blogs and generate a report 
using different headings and sub headings(if required) which should cover almost all the market news for the day and do not miss any news details that might help in analysing a stock, sector or market trends later.
Try to add more detailed explanation for various market events provided.
   
2. **Recommendations**(List): A list of at most best 5 stock recommendations (if any). Each recommendation must include:
   - The stock name.
   - The recommendation (e.g., "Buy" or "Sell").
   - A reason for the recommendation that is detailed, elaborative, and provides a comprehensive explanation
   - The source website from where the recommendation was found.

If there are no recommendations, set Recommendations as an empty list.

### Input Format:
Data sourced from <News Website 1> on <Date>: 
[
 {Headline: <Headline>
 Description: <Description>
 Content: <Full content>
 Author: <Author>},
 ...
]

Data sourced from <News Website 2> on <Date>:
...continues

### Output Format:
{
    "marketnews": "<MarketHighlights as mentioned above>",
    "recommendations": [
        {
            "name": "<Stock name>" or "<IPO name>" or "<Commodity name>" or "Crypto currency name" etc,
            "ticker": "<NSE Ticker of that Stock>",
            "recommendation": "<Buy/Sell>",
            "reason": "<Reason for the recommendation>",
            "source": "<News Website>"
        },
    ]
}
'''

ANALYSE_CUSTOM_MARKET_DATA_PROMPT = '''
You are an expert financial analyst. I have market data summarized over multiple time periods, each in the following format:

### Input Format:
<Time Period 1> ((@StartDate-@EndDate) or @RunDate):  
json{
  "marketnews": "<Analysis / Summary of the market data during that period>",
  "recommendations": [    {      "name": "<Stock Name>"  , "recommendation": "<Buy/Sell/Accumulate>",      "reason": "<Reason for the recommendation>",      "source": "<Source of the recommendation>"    }    ...  ]
}

<Time Period 2>:  
json{
  "marketnews": "<Analysis / Summary of the market data during that period>",
  "recommendations": [...]
}
...

Task - You must output the results in JSON format with two components:
1. Detailed Analysis:
Combine the market data from all provided time periods to create a comprehensive and detailed explanatory report. This report should:

Provide insights into how markets or specific sectors have behaved over the given periods.
Highlight major market events occurred.
Highlight major trends, patterns, or significant market movements.
Explain how different factors (global events, sector performance, government policies, etc.) have influenced the market during this time.
Provide an outlook for the upcoming days based on observed trends and market sentiment.
Use headings, subheadings, and structured content for clarity.
Be as detailed as possible without worrying about conciseness.

2. **Recommendations**(List): Based on the analysis, provide a list of top 8 investment recommendations considering their future perspective, strength, and consistency across the periods. Each recommendation must include:
   - The stock name.
   - The recommendation (e.g., "Buy" or "Sell").
   - A reason for the recommendation that is detailed, elaborative, and provides a comprehensive explanation
   - The source website from where the recommendation was found.

If there are no recommendations, set Recommendations as an empty list.

### Output Json Format:
{
    "analysis": "<Detailed Analysis as mentioned above>",
    "recommendations": [
        {
            "name": "<Stock name>" or "<IPO name>" or "<Commodity name>" or "Crypto currency name" etc,
            "ticker": "<NSE Ticker of that Stock>",
            "recommendation": "<Buy/Sell>",
            "reason": "<Reason for the recommendation>",
            "source": "<News Website>"
        },
    ]
}
'''

