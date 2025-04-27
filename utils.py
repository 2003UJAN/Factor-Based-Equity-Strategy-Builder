import requests
import os

# Function to fetch real-time fundamental data from Alpha Vantage
def fetch_fundamental_data(ticker):
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')  # Get your Alpha Vantage API key from environment variable
    
    # URL for the Alpha Vantage fundamental data API
    url = f"https://www.alphavantage.co/query"
    
    # Parameters for fundamental data (Company Overview)
    params = {
        'function': 'OVERVIEW',
        'symbol': ticker,
        'apikey': api_key
    }
    
    # Send request to Alpha Vantage API
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract fundamental data
        pe_ratio = float(data.get("PERatio", 0))
        ev_to_ebitda = float(data.get("EVToEBITDA", 0))
        price_to_book = float(data.get("PriceToBookRatio", 0))
        
        return {
            "PERatio": pe_ratio,
            "EVtoEBITDA": ev_to_ebitda,
            "PriceToBook": price_to_book
        }
    else:
        return {
            "PERatio": 0,
            "EVtoEBITDA": 0,
            "PriceToBook": 0
        }
