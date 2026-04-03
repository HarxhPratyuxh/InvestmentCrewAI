import os
from crewai_tools import EXASearchTool
from crewai.tools import tool
from services.rate_limiter import rate_limited

# Initialize the base tool
try:
    _exa_tool = EXASearchTool()
except Exception:
    _exa_tool = None

@tool("Search Stock News")
@rate_limited("exa")
def search_stock_news(query: str):
    """
    Searches for the latest news, analyst ratings, and market sentiment for a stock.
    """
    if not _exa_tool:
        return "Exa Search Tool is not configured. Please check API keys."
    
    try:
        # We wrap the run method to apply our rate limiter
        return _exa_tool.run(query)
    except Exception as e:
        return f"Error searching news: {str(e)}"