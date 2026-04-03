import json
import yfinance as yf
from crewai.tools import tool
from services.rate_limiter import rate_limited, with_retry

@tool("Get Company Fundamentals")
@with_retry(max_retries=3)
@rate_limited("yfinance")
def get_company_fundamentals(symbol: str):
    """
    Fetches key fundamental data (P/E, Market Cap, Margins) for a stock symbol.
    Args:
        symbol (str): Stock ticker (e.g., AAPL, RELIANCE.NS)
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Filter for most relevant data to save context window
        relevant_keys = [
            "marketCap", "trailingPE", "forwardPE", "trailingEps", 
            "revenueGrowth", "profitMargins", "totalDebt", "totalCash",
            "returnOnEquity", "sector", "industry", "currentPrice"
        ]
        
        data = {k: info.get(k, "N/A") for k in relevant_keys}
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching fundamentals for {symbol}: {str(e)}"

@tool("Get Income Statement")
@with_retry(max_retries=3)
@rate_limited("yfinance")
def get_income_statement(symbol: str):
    """
    Fetches the last 3 years of income statements.
    """
    try:
        ticker = yf.Ticker(symbol)
        financials = ticker.financials
        if financials.empty:
            return "No financial data available."
        
        # Return only the first 3 columns (last 3 years) to save tokens
        return financials.iloc[:, :3].to_json()
    except Exception as e:
        return f"Error fetching financials for {symbol}: {str(e)}"

@tool("Get Current Price")
@rate_limited("yfinance")
def get_current_price(symbol: str):
    """Get real-time price."""
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.info.get("regularMarketPrice", ticker.info.get("currentPrice"))
        if not price:
            # Fallback to history
            price = ticker.history(period="1d")["Close"].iloc[-1]
        return str(price)
    except Exception:
        return "Price unavailable"