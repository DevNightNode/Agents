import os
import requests
import pandas as pd
from typing import Dict, List, Optional

# Alpha Vantage API key from environment
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("ALPHA_VANTAGE_API_KEY environment variable is required")

def get_quote(symbol: str) -> Dict:
    """
    Get the latest stock quote for a given symbol.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dict containing quote data including price, change, volume, etc.
    """
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Global Quote" not in data:
        raise ValueError(f"Could not fetch quote for {symbol}: {data}")
    
    quote = data["Global Quote"]
    return {
        "symbol": quote["01. symbol"],
        "price": float(quote["05. price"]),
        "change": float(quote["09. change"]),
        "change_percent": quote["10. change percent"],
        "volume": int(quote["06. volume"]),
        "latest_trading_day": quote["08. latest trading day"]
    }

def get_news(symbol: str, limit: int = 5) -> Dict:
    """
    Get recent news articles for a given stock symbol.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL', 'MSFT')
        limit (int): Maximum number of articles to return (default: 5)
        
    Returns:
        Dict containing news articles with title, source, url, and published time
    """
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "limit": limit
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "feed" not in data:
        raise ValueError(f"Could not fetch news for {symbol}: {data}")
    
    articles = []
    for article in data["feed"][:limit]:
        articles.append({
            "title": article["title"],
            "source": article["source"],
            "url": article["url"],
            "published_time": article["time_published"],
            "sentiment": article["overall_sentiment_score"]
        })
    
    return {
        "symbol": symbol,
        "articles": articles
    }

def compute_indicators(symbol: str, period: int = 30) -> Dict:
    """
    Compute technical indicators for a given stock symbol over a specified period.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL', 'MSFT')
        period (int): Number of days to look back for indicator calculations (default: 30)
        
    Returns:
        Dict containing computed indicators like RSI, MACD, moving averages, etc.
    """
    # Daily closes from Alpha Vantage ("compact" returns the latest 100 trading days)
    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "apikey": ALPHA_VANTAGE_API_KEY,
        },
    )
    data = response.json()
    series = data.get("Time Series (Daily)")
    if not series:
        raise ValueError(f"Could not fetch daily prices for {symbol}: {data}")

    df = pd.DataFrame(
        [{"date": day, "close": float(values["4. close"])} for day, values in series.items()]
    ).sort_values("date").reset_index(drop=True)
    # Keep enough history for the 50-day average on top of the requested window
    df = df.tail(max(period, 50) + 14).reset_index(drop=True)

    # Compute indicators
    df["MA_20"] = df["close"].rolling(window=20).mean()
    df["MA_50"] = df["close"].rolling(window=50).mean()
    
    # RSI calculation
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    # Simple MACD calculation
    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = exp1 - exp2
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    
    # Get latest values
    latest = df.iloc[-1]
    
    return {
        "symbol": symbol,
        "period": period,
        "as_of": latest["date"],
        "moving_average_20": float(latest["MA_20"]),
        "moving_average_50": float(latest["MA_50"]),
        "rsi": float(latest["RSI"]),
        "macd": float(latest["MACD"]),
        "macd_signal": float(latest["MACD_signal"]),
        "price": float(latest["close"])
    }

def write_brief(symbol: str, indicators: Dict, news: Dict) -> Dict:
    """
    Write a daily market brief for a given stock symbol based on indicators and news.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL', 'MSFT')
        indicators (Dict): Technical indicators computed by compute_indicators
        news (Dict): News articles from get_news
        
    Returns:
        Dict containing the formatted market brief
    """
    # Format the brief
    brief = f"""
Market Brief for {symbol}
========================

Price: ${indicators['price']:.2f}
Moving Averages:
  - 20-day MA: ${indicators['moving_average_20']:.2f}
  - 50-day MA: ${indicators['moving_average_50']:.2f}

Technical Indicators:
  - RSI: {indicators['rsi']:.2f}
  - MACD: {indicators['macd']:.2f}
  - MACD Signal: {indicators['macd_signal']:.2f}

Recent News:
"""
    
    for article in news["articles"]:
        brief += f"""
  - {article['title']}
    Source: {article['source']}
    Sentiment: {article['sentiment']:.3f}
    Published: {article['published_time']}
"""
    
    return {
        "symbol": symbol,
        "brief": brief.strip()
    }
