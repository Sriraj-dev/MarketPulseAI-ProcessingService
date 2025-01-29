from fuzzywuzzy import process
import pandas as pd

def get_all_stock_codes():
    df = pd.read_csv('https://archives.nseindia.com/content/equities/EQUITY_L.csv')  # Fetch all stock symbols and company names
    eq_list_pd =  dict(zip(df['SYMBOL'], df['NAME OF COMPANY']))
    return eq_list_pd

def get_verified_ticker(recommendations):
    print("Ticker Verifier called")
    all_stock_codes = get_all_stock_codes()  # Returns a dictionary of stock codes and their full names

    for recommendation in recommendations:
        name = recommendation.get("name")
        ticker = recommendation.get("ticker")

        # Check if the provided ticker is valid
        if ticker in all_stock_codes:
            continue
        else:
            print("invalid ticker",ticker, recommendation)
            # Perform fuzzy matching to find the closest stock name
            closest_match, confidence = process.extractOne(name, all_stock_codes.values())
            
            # Find the stock code corresponding to the closest match
            corrected_ticker = [
                code for code, stock_name in all_stock_codes.items()
                if stock_name == closest_match
            ]
            
            # If a match is found, update the recommendation with the corrected ticker
            if corrected_ticker:
                recommendation["ticker"] = corrected_ticker[0]
                print(
                    f"Corrected ticker for '{name}' is '{corrected_ticker[0]}' "
                    f"(Confidence: {confidence}%)"
                )
            else:
                print(f"Could not find a matching ticker for '{name}'")

    return recommendations