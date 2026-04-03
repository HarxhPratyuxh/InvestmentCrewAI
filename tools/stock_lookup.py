import requests
from crewai.tools import tool
from services.rate_limiter import rate_limited

@tool("Stock Symbol Lookup")
@rate_limited("yfinance")
def lookup_stock_symbol(company_name: str):
    """
    Finds the stock ticker symbol for a company name using Yahoo Finance Search.
    Example: 'Reliance' -> 'RELIANCE.NS', 'Apple' -> 'AAPL'.
    """
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company_name}&quotesCount=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        quotes = data.get("quotes", [])
        
        if quotes and len(quotes) > 0:
            best_match = quotes[0]
            symbol = best_match.get("symbol")
            exchange = best_match.get("exchange", "Unknown")
            name = best_match.get("shortname", best_match.get("longname", "Unknown"))
            
            return f"Found Symbol: {symbol} (Company: {name}, Exchange: {exchange})"
            
        return f"Could not find any ticker symbol matching the company '{company_name}'."
    except Exception as e:
        return f"Search failed for '{company_name}': {str(e)}. Please provide the exact ticker instead."