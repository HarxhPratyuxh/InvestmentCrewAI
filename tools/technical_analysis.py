import json
import yfinance as yf
import pandas as pd
from crewai.tools import tool
from services.rate_limiter import rate_limited

@tool("Get Technical Indicators")
@rate_limited("yfinance")
def get_technical_indicators(symbol: str):
    """
    Calculates RSI, MACD, and Moving Averages (50/200) for a stock.
    """
    try:
        ticker = yf.Ticker(symbol)
        # Get enough history for 200 SMA
        hist = ticker.history(period="1y")
        
        if hist.empty:
            return f"No historical data for {symbol}"

        # 1. Moving Averages
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        hist['SMA_200'] = hist['Close'].rolling(window=200).mean()

        # 2. RSI (14)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))

        # 3. MACD (12, 26, 9)
        exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
        exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
        hist['MACD'] = exp1 - exp2
        hist['Signal_Line'] = hist['MACD'].ewm(span=9, adjust=False).mean()

        latest = hist.iloc[-1]
        
        return json.dumps({
            "current_price": round(latest['Close'], 2),
            "sma_50": round(latest['SMA_50'], 2),
            "sma_200": round(latest['SMA_200'], 2),
            "rsi": round(latest['RSI'], 2),
            "macd": round(latest['MACD'], 2),
            "macd_signal": round(latest['Signal_Line'], 2),
            "trend": "Bullish" if latest['SMA_50'] > latest['SMA_200'] else "Bearish"
        }, indent=2)
    except Exception as e:
        return f"Error calculating technicals: {str(e)}"